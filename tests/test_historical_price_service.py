import pytest
from unittest.mock import patch
import requests
from src.historical_price_service import HistoricalPriceService, TimeGranularity

@pytest.fixture
def historical_price_service():
    return HistoricalPriceService()

def test_time_granularity_enum():
    """Test that TimeGranularity enum works correctly."""
    assert TimeGranularity.DAILY.value == 'daily'
    assert TimeGranularity.HOURLY.value == 'hourly'

@patch('requests.get')
def test_get_historical_prices_daily(mock_get, historical_price_service):
    """Test retrieving daily historical prices."""
    mock_response = {
        'prices': [
            [1625097600000, 30000.0],
            [1625184000000, 31000.0]
        ]
    }
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.raise_for_status.return_value = None

    prices = historical_price_service.get_historical_prices(
        'bitcoin', 'usd', 7, TimeGranularity.DAILY
    )

    assert len(prices) == 2
    assert prices[0]['timestamp'] == 1625097600
    assert prices[0]['price'] == 30000.0

@patch('requests.get')
def test_get_historical_prices_hourly(mock_get, historical_price_service):
    """Test retrieving hourly historical prices."""
    mock_response = {
        'prices': [
            [1625097600000, 30000.0],
            [1625101200000, 31000.0]
        ]
    }
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.raise_for_status.return_value = None

    prices = historical_price_service.get_historical_prices(
        'bitcoin', 'usd', 1, TimeGranularity.HOURLY
    )

    assert len(prices) == 2
    assert prices[1]['timestamp'] == 1625101200

def test_invalid_input_validation(historical_price_service):
    """Test input validation for historical prices."""
    with pytest.raises(ValueError, match="Coin ID and currency must be provided"):
        historical_price_service.get_historical_prices('', 'usd', 7)
    
    with pytest.raises(ValueError, match="Days must be a positive integer"):
        historical_price_service.get_historical_prices('bitcoin', 'usd', -1)

@patch('requests.get')
def test_api_error_handling(mock_get, historical_price_service):
    """Test error handling for API request failures."""
    mock_get.return_value.raise_for_status.side_effect = requests.RequestException("API Error")

    with pytest.raises(RuntimeError, match="Failed to retrieve historical prices"):
        historical_price_service.get_historical_prices('bitcoin', 'usd', 7)