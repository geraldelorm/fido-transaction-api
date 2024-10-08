import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from app.main import app
from app.models.transaction_model import TransactionModel, ResponseModel
from app.exceptions.exceptions import EntityDoesNotExistError, ServiceError
import json
from datetime import datetime
from pytest_mock import MockerFixture
from app.models.analytics_model import AnalyticsModel
from app.api.routes.transactions import get_transaction_data, get_transaction_history, update_transaction_data, delete_transaction_data
from app.models.transaction_model import ResponseModel, UpdateTransactionModel

client = TestClient(app)
PREFIX = "/api/v1/transaction"

@pytest.mark.asyncio
async def test_get_transaction_data_success(mocker: MockerFixture):
    transaction_id = "67890"
    transaction_data = {
        "id": transaction_id,
        "user_id": "12345",
        "full_name": "Gerald Lol",
        "transaction_amount": 100.0,
        "transaction_type": "credit",
        "timestamp": "2023-10-06T00:00:00"
    }
    mock_retrieve_transaction = mocker.patch(
        "app.api.routes.transactions.retrieve_transaction",
        return_value=transaction_data
    )

    response = client.get(f"{PREFIX}/{transaction_id}")
    
    assert response.status_code == 200
    assert response.json() == {
        "data": transaction_data,
        "message": "Transaction data retrieved successfully",
        "code": 200
    }
    mock_retrieve_transaction.assert_called_once_with(transaction_id)


@pytest.mark.asyncio
async def test_get_transaction_history_success(mocker: MockerFixture):
    user_id = "12345"
    transaction_history = [
        {
            "id": "67890",
            "user_id": user_id,
            "full_name": "Gerald Lol",
            "transaction_amount": 100.0,
            "transaction_type": "credit",
            "timestamp": "2023-10-06T00:00:00"
        }
    ]
    mock_retrieve_transaction_history = mocker.patch(
        "app.api.routes.transactions.retrieve_transaction_history",
        return_value=transaction_history
    )

    response = client.get(f"{PREFIX}/history/{user_id}")
    
    assert response.status_code == 200
    assert response.json() == {
        "data": transaction_history,
        "message": "Transaction history retrieved successfully",
        "code": 200
    }
    mock_retrieve_transaction_history.assert_called_once_with(user_id)

@pytest.mark.asyncio
async def test_get_transaction_history_not_found(mocker: MockerFixture):
    user_id = "12345"
    mock_retrieve_transaction_history = mocker.patch(
        "app.api.routes.transactions.retrieve_transaction_history",
        side_effect=EntityDoesNotExistError("Transaction history not found")
    )

    response = client.get(f"{PREFIX}/history/{user_id}")
    
    assert response.status_code == 404
    print(response)
    assert response.json() == {
        'message': 'Transaction history not found for user ID 12345',
        'name': 'FidoTransactionsAPI'}
    mock_retrieve_transaction_history.assert_called_once_with(user_id)

@pytest.mark.asyncio
async def test_get_transaction_history_service_error(mocker: MockerFixture):
    user_id = "12345"
    mock_retrieve_transaction_history = mocker.patch(
        "app.api.routes.transactions.retrieve_transaction_history",
        side_effect=ServiceError("Service error")
    )

    response = client.get(f"{PREFIX}/history/{user_id}")
    
    assert response.status_code == 503
    assert response.json() ==  {
        'message': 'Service is unavailable, please try again later',
        'name': 'FidoTransactionsAPI'}
    mock_retrieve_transaction_history.assert_called_once_with(user_id)

@pytest.mark.asyncio
async def test_update_transaction_data_success(mocker: MockerFixture):
    transaction_id = "67890"
    update_data = {
        "transaction_amount": 200.0,
        "transaction_type": "debit"
    }
    mock_update_transaction = mocker.patch(
        "app.api.routes.transactions.update_transaction",
        return_value=True
    )

    response = client.put(f"{PREFIX}/{transaction_id}", json=update_data)
    
    assert response.status_code == 200
    assert response.json() == {
        "data": f"Transaction with ID: {transaction_id} update is successful",
        "message": "Transaction updated successfully",
        "code": 200
    }
    mock_update_transaction.assert_called_once_with(transaction_id, update_data)

@pytest.mark.asyncio
async def test_update_transaction_data_not_found(mocker: MockerFixture):
    transaction_id = "67890"
    update_data = {
        "transaction_amount": 200.0
    }
    mock_update_transaction = mocker.patch(
        "app.api.routes.transactions.update_transaction",
        side_effect=EntityDoesNotExistError("Transaction not found")
    )

    response = client.put(f"{PREFIX}/{transaction_id}", json=update_data)
    
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_update_transaction_data_service_error(mocker: MockerFixture):
    transaction_id = "67890"
    update_data = {
        "transaction_amount": 200.0
    }
    mock_update_transaction = mocker.patch(
        "app.api.routes.transactions.update_transaction",
        side_effect=ServiceError("Service error")
    )

    response = client.put(f"{PREFIX}/{transaction_id}", json=update_data)
    
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_delete_transaction_data_success(mocker: MockerFixture):
    transaction_id = "67890"
    mock_delete_transaction = mocker.patch(
        "app.api.routes.transactions.delete_transaction",
        return_value=True
    )

    response = client.delete(f"{PREFIX}/{transaction_id}")
    
    assert response.status_code == 200
    assert response.json() == {
        "data": f"Transaction with ID: {transaction_id} removed",
        "message": "Transaction deleted successfully",
        "code": 200
    }
    mock_delete_transaction.assert_called_once_with(transaction_id)

@pytest.mark.asyncio
async def test_delete_transaction_data_not_found(mocker: MockerFixture):
    transaction_id = "67890"
    mock_delete_transaction = mocker.patch(
        "app.api.routes.transactions.delete_transaction",
        side_effect=EntityDoesNotExistError("Transaction not found")
    )

    response = client.delete(f"{PREFIX}/{transaction_id}")

    assert response.status_code == 404
    assert response.json() == {
        'detail': "('Transaction not found', 'FidoTransactionsAPI')"
        }
    
    mock_delete_transaction.assert_called_once_with(transaction_id)

@pytest.mark.asyncio
async def test_delete_transaction_data_service_error(mocker: MockerFixture):
    transaction_id = "67890"
    mock_delete_transaction = mocker.patch(
        "app.api.routes.transactions.delete_transaction",
        side_effect=ServiceError("Service error")
    )

    response = client.delete(f"{PREFIX}/{transaction_id}")

    assert response.status_code == 503
    assert response.json() ==  {
        'message': 'Service is unavailable, please try again later',
        'name': 'FidoTransactionsAPI'}
    mock_delete_transaction.assert_called_once_with(transaction_id)
