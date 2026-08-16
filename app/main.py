from fastapi import FastAPI
from app.database import Base, engine
from app import models
from app.routers import auth, transactions, budgets, goals

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Expense Management API")
app.include_router(auth.router)
app.include_router(transactions.router)
app.include_router(budgets.router)
app.include_router(goals.router)

@app.get("/")
def root():
    return {"message": "Expense Management API đang chạy"}
