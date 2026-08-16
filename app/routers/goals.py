from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from decimal import Decimal
from datetime import date
from app.database import get_db
from app.models.saving_goal import SavingGoal
from app.models.goal_item import GoalItem
from app.models.goal_transaction import GoalTransaction
from app.models.user import User
from app.schemas.goal import GoalCreate, GoalItemCreate, GoalTxCreate, GoalOut
from app.core.deps import get_current_user
from app.core.finance import compute_available_balance
from pydantic import BaseModel
import uuid

router = APIRouter(prefix="/goals", tags=["goals"])

def compute_current(db: Session, goal_id: str) -> Decimal:
    deposits = db.query(func.sum(GoalTransaction.amount)).filter(GoalTransaction.goal_id == goal_id, GoalTransaction.type == "deposit").scalar() or Decimal(0)
    withdrawals = db.query(func.sum(GoalTransaction.amount)).filter(GoalTransaction.goal_id == goal_id, GoalTransaction.type == "withdraw").scalar() or Decimal(0)
    return deposits - withdrawals

def to_goal_out(db: Session, goal: SavingGoal) -> dict:
    items = db.query(GoalItem).filter(GoalItem.goal_id == goal.id).all()
    return {
        "id": goal.id, "name": goal.name, "target_amount": goal.target_amount,
        "deadline": goal.deadline, "status": goal.status,
        "current_amount": compute_current(db, goal.id), "items": items,
    }

@router.get("/", response_model=List[GoalOut])
def list_goals(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    goals = db.query(SavingGoal).filter(SavingGoal.user_id == current_user.id).all()
    return [to_goal_out(db, g) for g in goals]

@router.post("/", response_model=GoalOut)
def create_goal(payload: GoalCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    goal = SavingGoal(id=str(uuid.uuid4()), user_id=current_user.id, status="active", **payload.model_dump())
    db.add(goal)
    db.commit()
    db.refresh(goal)
    return to_goal_out(db, goal)

@router.delete("/{goal_id}")
def delete_goal(goal_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    goal = db.query(SavingGoal).filter(SavingGoal.id == goal_id, SavingGoal.user_id == current_user.id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Không tìm thấy mục tiêu")
    db.query(GoalItem).filter(GoalItem.goal_id == goal_id).delete()
    db.query(GoalTransaction).filter(GoalTransaction.goal_id == goal_id).delete()
    db.delete(goal)
    db.commit()
    return {"message": "Đã xóa mục tiêu"}

@router.post("/{goal_id}/items", response_model=GoalOut)
def add_item(goal_id: str, payload: GoalItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    goal = db.query(SavingGoal).filter(SavingGoal.id == goal_id, SavingGoal.user_id == current_user.id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Không tìm thấy mục tiêu")
    item = GoalItem(id=str(uuid.uuid4()), goal_id=goal_id, **payload.model_dump())
    db.add(item)
    db.commit()
    return to_goal_out(db, goal)

@router.post("/{goal_id}/deposit", response_model=GoalOut)
def deposit(goal_id: str, payload: GoalTxCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    goal = db.query(SavingGoal).filter(SavingGoal.id == goal_id, SavingGoal.user_id == current_user.id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Không tìm thấy mục tiêu")

    balance = compute_available_balance(db, current_user.id)
    if payload.amount > balance:
        raise HTTPException(status_code=400, detail=f"Không thể nạp quá số dư khả dụng hiện có ({balance})")

    tx = GoalTransaction(id=str(uuid.uuid4()), goal_id=goal_id, amount=payload.amount, type="deposit", txn_date=date.today(), note=payload.note)
    db.add(tx)
    db.commit()
    return to_goal_out(db, goal)

@router.post("/{goal_id}/withdraw", response_model=GoalOut)
def withdraw(goal_id: str, payload: GoalTxCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    goal = db.query(SavingGoal).filter(SavingGoal.id == goal_id, SavingGoal.user_id == current_user.id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Không tìm thấy mục tiêu")
    current = compute_current(db, goal_id)
    if payload.amount > current:
        raise HTTPException(status_code=400, detail=f"Không thể rút quá số đã tiết kiệm ({current})")
    tx = GoalTransaction(id=str(uuid.uuid4()), goal_id=goal_id, amount=payload.amount, type="withdraw", txn_date=date.today(), note=payload.note)
    db.add(tx)
    db.commit()
    return to_goal_out(db, goal)

class GoalItemUpdate(BaseModel):
    name: Optional[str] = None
    cost: Optional[Decimal] = None
    is_purchased: Optional[bool] = None

@router.post("/{goal_id}/complete", response_model=GoalOut)
def complete_goal(goal_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    goal = db.query(SavingGoal).filter(SavingGoal.id == goal_id, SavingGoal.user_id == current_user.id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Không tìm thấy mục tiêu")

    current = compute_current(db, goal_id)
    if current < goal.target_amount:
        raise HTTPException(status_code=400, detail="Chưa đạt mốc mục tiêu, không thể hoàn thành")

    if current > 0:
        tx = GoalTransaction(id=str(uuid.uuid4()), goal_id=goal_id, amount=current, type="withdraw", txn_date=date.today(), note="Hoàn thành mục tiêu — rút toàn bộ")
        db.add(tx)
    goal.status = "completed"
    db.commit()
    db.refresh(goal)
    return to_goal_out(db, goal)

@router.patch("/{goal_id}/items/{item_id}", response_model=GoalOut)
def update_item(goal_id: str, item_id: str, payload: GoalItemUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    goal = db.query(SavingGoal).filter(SavingGoal.id == goal_id, SavingGoal.user_id == current_user.id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Không tìm thấy mục tiêu")
    item = db.query(GoalItem).filter(GoalItem.id == item_id, GoalItem.goal_id == goal_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Không tìm thấy hạng mục")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, key, value)
    db.commit()
    return to_goal_out(db, goal)

@router.delete("/{goal_id}/items/{item_id}", response_model=GoalOut)
def delete_item(goal_id: str, item_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    goal = db.query(SavingGoal).filter(SavingGoal.id == goal_id, SavingGoal.user_id == current_user.id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Không tìm thấy mục tiêu")
    item = db.query(GoalItem).filter(GoalItem.id == item_id, GoalItem.goal_id == goal_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Không tìm thấy hạng mục")
    db.delete(item)
    db.commit()
    return to_goal_out(db, goal)
