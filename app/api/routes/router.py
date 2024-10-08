from fastapi import APIRouter
from . import transactions, analytics

base_router = APIRouter()

base_router.include_router(
    transactions.router, tags=["transactions"], prefix="/v1/transaction"
)

base_router.include_router(
    analytics.router, tags=["analytics"], prefix="/v1/analytics"
)