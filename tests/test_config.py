import os
import pytest
from src.config import CoinGeckoConfig, Environment

def test_default_config():
    config = CoinGeckoConfig()
    assert config.base_url == 'https://api.coingecko.com/api/v3'
    assert config.environment == Environment.DEVELOPMENT
    assert config.request_timeout == 10
    assert config.max_retries == 3
    assert config.rate_limit_per_minute == 30
    assert config.api_key is None

def test_custom_config():
    config = CoinGeckoConfig(
        api_key='test_key',
        base_url='https://custom.api.com',
        environment=Environment.PRODUCTION,
        request_timeout=15,
        max_retries=2,
        rate_limit_per_minute=50
    )
    assert config.api_key == 'test_key'
    assert config.base_url == 'https://custom.api.com'
    assert config.environment == Environment.PRODUCTION
    assert config.request_timeout == 15
    assert config.max_retries == 2
    assert config.rate_limit_per_minute == 50

def test_invalid_base_url():
    with pytest.raises(ValueError, match="Invalid base URL"):
        CoinGeckoConfig(base_url='http://invalid')

def test_invalid_timeout():
    with pytest.raises(ValueError, match="Request timeout must be between 1 and 60"):
        CoinGeckoConfig(request_timeout=0)
    with pytest.raises(ValueError, match="Request timeout must be between 1 and 60"):
        CoinGeckoConfig(request_timeout=61)

def test_invalid_retries():
    with pytest.raises(ValueError, match="Max retries must be between 0 and 5"):
        CoinGeckoConfig(max_retries=6)
    with pytest.raises(ValueError, match="Max retries must be between 0 and 5"):
        CoinGeckoConfig(max_retries=-1)

def test_invalid_rate_limit():
    with pytest.raises(ValueError, match="Rate limit must be between 1 and 100"):
        CoinGeckoConfig(rate_limit_per_minute=0)
    with pytest.raises(ValueError, match="Rate limit must be between 1 and 100"):
        CoinGeckoConfig(rate_limit_per_minute=101)

def test_production_api_key_requirement():
    with pytest.raises(ValueError, match="API key is required for production environment"):
        CoinGeckoConfig(environment=Environment.PRODUCTION)

def test_from_env_config(monkeypatch):
    monkeypatch.setenv('COINGECKO_API_KEY', 'test_env_key')
    monkeypatch.setenv('COINGECKO_BASE_URL', 'https://env.api.com')
    monkeypatch.setenv('COINGECKO_ENV', 'production')
    monkeypatch.setenv('COINGECKO_REQUEST_TIMEOUT', '20')
    monkeypatch.setenv('COINGECKO_MAX_RETRIES', '4')
    monkeypatch.setenv('COINGECKO_RATE_LIMIT', '60')

    config = CoinGeckoConfig.from_env()
    
    assert config.api_key == 'test_env_key'
    assert config.base_url == 'https://env.api.com'
    assert config.environment == Environment.PRODUCTION
    assert config.request_timeout == 20
    assert config.max_retries == 4
    assert config.rate_limit_per_minute == 60