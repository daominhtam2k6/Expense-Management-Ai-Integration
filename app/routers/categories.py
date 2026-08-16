from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.category import Category
from app.models.user import User
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryOut
from app.core.deps import get_current_user
from app.models.transaction import Transaction
import uuid

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("/", response_model=List[CategoryOut])
def list_categories(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Category).filter(Category.user_id == current_user.id).all()

@router.post("/", response_model=CategoryOut)
def create_category(payload: CategoryCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    existing = db.query(Category).filter(
        Category.user_id == current_user.id,
        Category.name == payload.name,
        Category.type == payload.type,
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Danh mục này đã tồn tại")

    category = Category(id=str(uuid.uuid4()), user_id=current_user.id, **payload.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@router.put("/{category_id}", response_model=CategoryOut)
def update_category(category_id: str, payload: CategoryUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    category = db.query(Category).filter(Category.id == category_id, Category.user_id == current_user.id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Không tìm thấy danh mục")

    new_name = payload.name if payload.name is not None else category.name
    new_type = payload.type if payload.type is not None else category.type
    duplicate = db.query(Category).filter(
        Category.user_id == current_user.id,
        Category.name == new_name,
        Category.type == new_type,
        Category.id != category_id,
    ).first()
    if duplicate:
        raise HTTPException(status_code=400, detail="Danh mục này đã tồn tại")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(category, key, value)
    db.commit()
    db.refresh(category)
    return category

@router.delete("/{category_id}")
def delete_category(category_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    category = db.query(Category).filter(Category.id == category_id, Category.user_id == current_user.id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Không tìm thấy danh mục")

    in_use = db.query(Transaction).filter(Transaction.category_id == category_id).first()
    if in_use:
        raise HTTPException(status_code=400, detail="Không thể xóa danh mục đã có giao dịch sử dụng")

    db.delete(category)
    db.commit()
    return {"message": "Đã xóa danh mục"}
