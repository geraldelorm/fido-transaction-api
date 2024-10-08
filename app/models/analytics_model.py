from datetime import datetime
from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional
from app.models.transaction_model import PyObjectId

class AnalyticsModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    average_transaction_value: float
    highest_transactions_day: datetime
    debit_total: float
    credit_total: float
    last_updated: datetime

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "user_id": "user123",
                "average_transaction_value": 150.75,
                "highest_transactions_day": "2023-10-01T00:00:00Z",
                "debit_total": 5000.00,
                "credit_total": 4500.00,
                "last_updated": "2023-10-01T12:00:00Z"
            }
        }


def ResponseModel(data, message, code):
    return {
        "data": data,
        "code": code,
        "message": message,
    }
