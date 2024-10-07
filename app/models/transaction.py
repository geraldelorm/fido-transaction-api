from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.utils.encryption_utils import encrypt_data, decrypt_data

class TransactionType(str, Enum):
    CREDIT = "credit"
    DEBIT = "debit"

class TransactionSchema(BaseModel):
    user_id: str = Field(..., description="Unique identifier for the user")
    full_name: str = Field(..., description="Full name of the user: encrypted in DB")
    transaction_date: datetime = Field(default_factory=datetime.now, description="Date of the transaction")
    transaction_amount: float = Field(..., description="Amount of the transaction")
    transaction_type: TransactionType = Field(..., description="Type of transaction: credit or debit")

    def __init__(self, **data):
        super().__init__(**data)
        # Encrypt full_name when creating a new instance
        if 'full_name' in data:
            self.full_name = encrypt_data(data['full_name'])

    class Config:
        schema_extra = {
            "example": {
                "user_id": "123456789",
                "full_name": "John Doe",
                "transaction_date": "2023-10-06T10:23:58.741Z",
                "transaction_amount": 250.50,
                "transaction_type": "credit"
            }
        }

class UpdateTransactionModel(BaseModel):
    full_name: Optional[str]
    transaction_date: Optional[datetime]
    transaction_amount: Optional[float]
    transaction_type: Optional[TransactionType]

    class Config:
        schema_extra = {
            "example": {
                "transaction_id": "615d8a9b08658c349de0735b",
                "full_name": "John Doe",
                "transaction_amount": 300.75,
                "transaction_type": "debit"
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
