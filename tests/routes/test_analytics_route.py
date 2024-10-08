import json
from datetime import datetime
import pytest
from pytest_mock import MockerFixture
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from app.models.analytics_model import AnalyticsModel
from app.exceptions.exceptions import EntityDoesNotExistError, ServiceError

client = TestClient(app)
PREFIX = "/api/v1/analytics"

@pytest.mark.asyncio
async def test_get_transaction_analytics_success(mocker: MockerFixture):
    user_id = "12345"
    analytics_data = {
        "user_id": user_id,
        "average_transaction_value": 100.0,
        "highest_transactions_day": "2023-10-06",
        "debit_total": 50.0,
        "credit_total": 150.0,
        "last_updated": "2023-10-06T00:00:00"
    }
    mock_retrieve_transaction_analytics = mocker.patch(
        "app.api.routes.analytics.retrieve_transaction_analytics",
        return_value=analytics_data
    )

    response = client.get(f"{PREFIX}/{user_id}")
    
    assert response.status_code == 200
    assert response.json() == {
        "data": analytics_data,
        "message": "Transaction analytics retrieved successfully",
        "code": 200
    }
    mock_retrieve_transaction_analytics.assert_called_once_with(user_id)

@pytest.mark.asyncio
async def test_get_transaction_analytics_not_found(mocker: MockerFixture):
    user_id = "12345"
    mock_retrieve_transaction_analytics = mocker.patch(
        "app.api.routes.analytics.retrieve_transaction_analytics",
        side_effect=EntityDoesNotExistError("Transaction analytics not found for user ID")
    )

    response = client.get(f"{PREFIX}/{user_id}")

    assert response.status_code == 404
    assert response.json() == {
        'message': 'Transaction analytics not found for user ID 12345',
        'name': 'FidoTransactionsAPI'
    }
    mock_retrieve_transaction_analytics.assert_called_once_with(user_id)

@pytest.mark.asyncio
async def test_get_transaction_analytics_service_error(mocker: MockerFixture):
    user_id = "12345"
    mock_retrieve_transaction_analytics = mocker.patch(
        "app.api.routes.analytics.retrieve_transaction_analytics",
        side_effect=Exception("Unexpected error")
    )

    response = client.get(f"{PREFIX}/{user_id}")

    assert response.status_code == 503
    assert response.json() == {
        'message': 'Service is unavailable, please try again later',
        'name': 'FidoTransactionsAPI'
    }
    mock_retrieve_transaction_analytics.assert_called_once_with(user_id)

@pytest.mark.asyncio
async def test_get_range_transaction_analytics_success(mocker: MockerFixture):
    user_id = "12345"
    start_date = "2024-10-08T01:05:37.574299"
    end_date = "2024-11-08T01:05:37.574299"
    analytics_data = {
        "user_id": user_id,
        "average_transaction_value": 100.0,
        "highest_transactions_day": "2023-10-06",
        "debit_total": 50.0,
        "credit_total": 150.0,
        "last_updated": "2023-10-06T00:00:00"
    }
    mock_retrieve_live_transaction_analytics = mocker.patch(
        "app.api.routes.analytics.retrieve_live_transaction_analytics",
        return_value=analytics_data
    )

    response = client.get(f"{PREFIX}/range/{user_id}?start_date={start_date}&end_date={end_date}")
    
    assert response.status_code == 200
    assert response.json() == {
        "code": 200,
        "data": analytics_data,
        "message": "Transaction analytics retrieved successfully"
    }
    mock_retrieve_live_transaction_analytics.assert_called_once_with(user_id, datetime.fromisoformat(start_date), datetime.fromisoformat(end_date))

@pytest.mark.asyncio
async def test_get_range_transaction_analytics_not_found(mocker: MockerFixture):
    user_id = "12345"
    start_date = "2024-10-08T01:05:37.574299"
    end_date = "2024-11-08T01:05:37.574299"

    mock_retrieve_live_transaction_analytics = mocker.patch(
        "app.api.routes.analytics.retrieve_live_transaction_analytics",
        side_effect=EntityDoesNotExistError("Transaction analytics not found for user ID")
    )

    response = client.get(f"{PREFIX}/range/{user_id}?start_date={start_date}&end_date={end_date}")

    assert response.status_code == 404
    assert response.json() ==  {
        'message': 'Transaction analytics not found for user ID 12345',
        'name': 'FidoTransactionsAPI'
    }
    mock_retrieve_live_transaction_analytics.assert_called_once_with(user_id, datetime.fromisoformat(start_date), datetime.fromisoformat(end_date))

@pytest.mark.asyncio
async def test_get_range_transaction_analytics_service_error(mocker: MockerFixture):
    user_id = "12345"
    start_date = "2024-10-08T01:05:37.574299"
    end_date = "2024-11-08T01:05:37.574299"

    mock_retrieve_live_transaction_analytics = mocker.patch(
        "app.api.routes.analytics.retrieve_live_transaction_analytics",
        side_effect=Exception("Unexpected error")
    )

    response = client.get(f"{PREFIX}/range/{user_id}?start_date={start_date}&end_date={end_date}")

    print(response)
    assert response.status_code == 503
    assert response.json() == {
    'message': 'Service is unavailable, please try again later',
    'name': 'FidoTransactionsAPI'
}
    mock_retrieve_live_transaction_analytics.assert_called_once_with(user_id, datetime.fromisoformat(start_date), datetime.fromisoformat(end_date))