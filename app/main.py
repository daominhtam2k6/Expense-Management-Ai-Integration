from fastapi import FastAPI

app = FastAPI(title="Expense Management API")

@app.get("/")
def root():
    return {"message": "Expense Management API đang chạy"}
