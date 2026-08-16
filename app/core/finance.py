from sqlalchemy.orm import Session
from sqlalchemy import func
from decimal import Decimal
from app.models.transaction import Transaction
from app.models.saving_goal import SavingGoal
from app.models.goal_transaction import GoalTransaction

def compute_available_balance(db: Session, user_id: str) -> Decimal:
    income = db.query(func.sum(Transaction.amount)).filter(Transaction.user_id == user_id, Transaction.type == "income").scalar() or Decimal(0)
    expense = db.query(func.sum(Transaction.amount)).filter(Transaction.user_id == user_id, Transaction.type == "expense").scalar() or Decimal(0)
    goal_ids = [g.id for g in db.query(SavingGoal.id).filter(SavingGoal.user_id == user_id).all()]
    deposits = Decimal(0)
    withdrawals = Decimal(0)
    if goal_ids:
        deposits = db.query(func.sum(GoalTransaction.amount)).filter(GoalTransaction.goal_id.in_(goal_ids), GoalTransaction.type == "deposit").scalar() or Decimal(0)
        withdrawals = db.query(func.sum(GoalTransaction.amount)).filter(GoalTransaction.goal_id.in_(goal_ids), GoalTransaction.type == "withdraw").scalar() or Decimal(0)
    return income - expense - deposits + withdrawals
