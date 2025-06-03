import os
import pytest
from src.config_validator import (
    CoinGeckoConfig, 
    ConfigurationError, 
    Environment, 
    load_config_from_env
)

def test_default_config_validation():
    """Test default configuration is valid."""
    config = CoinGeckoConfig()
    config.validate()  # Should not raise any exception

def test_config_invalid_timeout():
    """Test configuration with invalid timeout."""
    with pytest.raises(ConfigurationError, match="Request timeout must be a positive integer"):
        config = CoinGeckoConfig(request_timeout=-1)
        config.validate()

def test_config_invalid_rate_limit():
    """Test configuration with invalid rate limit."""
    with pytest.raises(ConfigurationError, match="Rate limit must be a positive integer"):
        config = CoinGeckoConfig(rate_limit_calls_per_second=0)
        config.validate()

def test_config_invalid_proxy_url():
    """Test configuration with invalid proxy URL."""
    with pytest.raises(ConfigurationError, match="Invalid proxy URL format"):
        config = CoinGeckoConfig(proxy_url="invalid_url")
        config.validate()

def test_config_valid_proxy_url():
    """Test configuration with valid proxy URL."""
    config = CoinGeckoConfig(proxy_url="http://proxy.example.com")
    config.validate()  # Should not raise an exception

def test_load_config_from_env(monkeypatch):
    """Test loading configuration from environment variables."""
    # Set environment variables
    monkeypatch.setenv('COINGECKO_API_KEY', 'test_key')
    monkeypatch.setenv('COINGECKO_ENV', 'PRODUCTION')
    monkeypatch.setenv('COINGECKO_REQUEST_TIMEOUT', '15')
    monkeypatch.setenv('COINGECKO_RATE_LIMIT', '20')
    monkeypatch.setenv('COINGECKO_PROXY_URL', 'http://test-proxy.com')

    config = load_config_from_env()
    
    assert config.api_key == 'test_key'
    assert config.environment == Environment.PRODUCTION
    assert config.request_timeout == 15
    assert config.rate_limit_calls_per_second == 20
    assert config.proxy_url == 'http://test-proxy.com'