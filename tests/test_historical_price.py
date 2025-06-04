from datetime import datetime, timedelta
import pytest
from src.coingecko_api.historical_price import CoinGeckoHistoricalPriceClient

def test_get_historical_prices_valid_input():
    client = CoinGeckoHistoricalPriceClient()
    
    # Note: Replace 'bitcoin' with a valid coin ID
    prices = client.get_historical_prices('bitcoin', days=7)
    
    assert isinstance(prices, list)
    assert len(prices) > 0
    
    for price_data in prices:
        assert 'timestamp' in price_data
        assert 'price' in price_data
        assert isinstance(price_data['timestamp'], (int, float))
        assert isinstance(price_data['price'], (int, float))

def test_get_historical_prices_invalid_days():
    client = CoinGeckoHistoricalPriceClient()
    
    with pytest.raises(ValueError):
        client.get_historical_prices('bitcoin', days=-1)

def test_get_historical_prices_invalid_coin_id():
    client = CoinGeckoHistoricalPriceClient()
    
    with pytest.raises(Exception):
        client.get_historical_prices('', currency='usd')

def test_get_price_on_date():
    client = CoinGeckoHistoricalPriceClient()
    
    # Use a recent date for testing
    test_date = datetime.now() - timedelta(days=7)
    price = client.get_price_on_date('bitcoin', test_date)
    
    assert price is not None
    assert isinstance(price, (int, float))

def test_get_price_on_date_invalid_inputs():
    client = CoinGeckoHistoricalPriceClient()
    
    with pytest.raises(ValueError):
        client.get_price_on_date('', datetime.now())
    
    with pytest.raises(ValueError):
        client.get_price_on_date('bitcoin', None)