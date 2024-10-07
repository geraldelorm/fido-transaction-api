from fastapi import FastAPI
from app.api.v1.routes.transactions import router as transaction_router

app = FastAPI()

app.include_router(transaction_router, tags=["Transaction"], prefix="/transaction")

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to Fido Transactions API"}
