from fastapi import APIRouter
from . import transactions 

base_router = APIRouter()

base_router.include_router(
    transactions.router, tags=["transactions"], prefix="/v1/transaction"
)  
