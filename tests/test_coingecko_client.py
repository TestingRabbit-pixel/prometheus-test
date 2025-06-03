import pytest
from unittest.mock import patch, Mock
from src.coingecko_client import CoinGeckoClient, PriceResponse

@pytest.fixture
def coingecko_client():
    return CoinGeckoClient()

def test_coingecko_client_initialization(coingecko_client):
    assert isinstance(coingecko_client, CoinGeckoClient)
    assert coingecko_client.timeout == 10

def test_get_simple_price_empty_ids(coingecko_client):
    with pytest.raises(ValueError, match="At least one cryptocurrency id must be provided"):
        coingecko_client.get_simple_price([])

@patch('requests.get')
def test_get_simple_price_successful(mock_get, coingecko_client):
    mock_response = Mock()
    mock_response.json.return_value = {
        'bitcoin': {'usd': 50000, 'last_updated_at': '2023-01-01T00:00:00Z'}
    }
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    result = coingecko_client.get_simple_price(['bitcoin'])
    assert result == {'bitcoin': {'usd': 50000, 'last_updated_at': '2023-01-01T00:00:00Z'}}

def test_parse_price_response(coingecko_client):
    sample_response = {
        'bitcoin': {'usd': 50000, 'last_updated_at': '2023-01-01T00:00:00Z'},
        'ethereum': {'usd': 3000, 'last_updated_at': '2023-01-01T00:00:00Z'}
    }

    parsed_result = coingecko_client.parse_price_response(sample_response)
    
    assert len(parsed_result) == 2
    assert all(isinstance(pr, PriceResponse) for pr in parsed_result)
    assert {pr.symbol for pr in parsed_result} == {'bitcoin', 'ethereum'}
    assert all(pr.price > 0 for pr in parsed_result)

@patch('requests.get')
def test_get_simple_price_network_error(mock_get, coingecko_client):
    mock_get.side_effect = requests.RequestException("Network error")

    with pytest.raises(RuntimeError, match="Failed to fetch prices"):
        coingecko_client.get_simple_price(['bitcoin'])