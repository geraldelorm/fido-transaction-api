from datetime import datetime
from enum import Enum
from typing import Annotated, List, Optional

from bson.objectid import ObjectId
from pydantic import BaseModel, BeforeValidator, ConfigDict, Field

from app.utils.encryption_utils import encrypt_data


class TransactionType(str, Enum):
    CREDIT = "credit"
    DEBIT = "debit"


PyObjectId = Annotated[str, BeforeValidator(str)]


class TransactionModel(BaseModel):
    user_id: str = Field(..., description="Unique identifier for the user")
    full_name: str = Field(..., description="Full name of the user: encrypted in DB")
    transaction_date: datetime = Field(
        default_factory=datetime.now, description="Date of the transaction"
    )
    transaction_amount: float = Field(..., description="Amount of the transaction")
    transaction_type: TransactionType = Field(
        ..., description="Type of transaction: credit or debit"
    )

    def __init__(self, **data):
        super().__init__(**data)

        if "full_name" in data:
            self.full_name = encrypt_data(data["full_name"])

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "user_id": "123456789",
                "full_name": "John Doe",
                "transaction_date": "2024-10-08T01:04:08.762475",
                "transaction_amount": 250.50,
                "transaction_type": "credit",
            }
        },
    )


class UpdateTransactionModel(BaseModel):
    """
    A set of optional updates to be made to a document in the database.
    """

    transaction_amount: Optional[float]
    transaction_type: Optional[TransactionType]

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {"transaction_amount": 300.75, "transaction_type": "debit"}
        },
    )


class TrasactionCollection(BaseModel):
    students: List[TransactionModel]


def ResponseModel(data, message, code):
    return {
        "data": data,
        "code": code,
        "message": message,
    }
