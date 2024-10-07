import pytest
from bson import ObjectId
from app.models.transaction_model import TransactionModel
from app.services.transaction_service import (
    create_transaction,
    read_transaction,
    read_transactions,
    update_transaction,
    delete_transaction,
)
from app.database.database import mongo_db_connection


@pytest.mark.asyncio
async def test_create_transaction():
    transaction_data = TransactionModel(
        user_id="12345",
        full_name="Jane Doe",
        transaction_date="2023-10-06",
        transaction_amount=100.0,
        transaction_type="credit",
    )

    created_transaction = await create_transaction(transaction_data)
    assert created_transaction["user_id"] == transaction_data.user_id
    assert created_transaction["full_name"] == transaction_data.full_name


@pytest.mark.asyncio
async def test_read_transaction():
    # Create a transaction to read
    transaction_data = TransactionModel(
        user_id="12345",
        full_name="Jane Doe",
        transaction_date="2023-10-06",
        transaction_amount=100.0,
        transaction_type="credit",
    )
    created_transaction = await create_transaction(transaction_data)
    transaction_id = created_transaction["id"]

    # Now read the transaction
    transaction = await read_transaction(transaction_id)
    assert transaction is not None
    assert transaction["_id"] == ObjectId(transaction_id)


@pytest.mark.asyncio
async def test_read_transactions():
    # Create a couple of transactions to read
    transaction1 = TransactionModel(
        user_id="12345",
        full_name="Jane Doe",
        transaction_date="2023-10-06",
        transaction_amount=100.0,
        transaction_type="credit",
    )
    transaction2 = TransactionModel(
        user_id="12345",
        full_name="Jane Doe",
        transaction_date="2023-10-07",
        transaction_amount=50.0,
        transaction_type="debit",
    )

    await create_transaction(transaction1)
    await create_transaction(transaction2)

    # Now read all transactions for user_id '12345'
    transactions = await read_transactions("12345")
    assert len(transactions) >= 2  # Check that we have at least 2 transactions


@pytest.mark.asyncio
async def test_update_transaction():
    # Create a transaction to update
    transaction_data = TransactionModel(
        user_id="12345",
        full_name="Jane Doe",
        transaction_date="2023-10-06",
        transaction_amount=100.0,
        transaction_type="credit",
    )
    created_transaction = await create_transaction(transaction_data)
    transaction_id = created_transaction["id"]

    # Prepare updated data
    update_data = {"transaction_amount": 150.0, "transaction_type": "debit"}

    updated_transaction = await update_transaction(transaction_id, update_data)
    assert updated_transaction["transaction_amount"] == 150.0
    assert updated_transaction["transaction_type"] == "debit"


@pytest.mark.asyncio
async def test_delete_transaction():
    # Create a transaction to delete
    transaction_data = TransactionModel(
        user_id="12345",
        full_name="Jane Doe",
        transaction_date="2023-10-06",
        transaction_amount=100.0,
        transaction_type="credit",
    )
    created_transaction = await create_transaction(transaction_data)
    transaction_id = created_transaction["id"]

    # Now delete the transaction
    delete_result = await delete_transaction(transaction_id)
    assert delete_result is True

    # Verify it has been deleted
    deleted_transaction = await read_transaction(transaction_id)
    assert deleted_transaction is None
