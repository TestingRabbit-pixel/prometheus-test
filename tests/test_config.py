import os
import pytest
from src.config import CoinGeckoConfig

def test_default_config():
    """Test default configuration settings."""
    config = CoinGeckoConfig()
    
    assert config.api_base_url == "https://api.coingecko.com/api/v3"
    assert config.api_key is None
    assert config.timeout == 10
    assert config.max_requests_per_minute == 30

def test_config_from_env(monkeypatch):
    """Test configuration from environment variables."""
    monkeypatch.setenv('COINGECKO_API_BASE_URL', 'https://custom-api.com')
    monkeypatch.setenv('COINGECKO_API_KEY', 'test_key')
    monkeypatch.setenv('COINGECKO_TIMEOUT', '15')
    monkeypatch.setenv('COINGECKO_MAX_REQUESTS', '50')
    
    config = CoinGeckoConfig.from_env()
    
    assert config.api_base_url == 'https://custom-api.com'
    assert config.api_key == 'test_key'
    assert config.timeout == 15
    assert config.max_requests_per_minute == 50

def test_config_validation():
    """Test configuration validation."""
    config = CoinGeckoConfig()
    config.validate()  # Should not raise any exceptions

def test_invalid_base_url():
    """Test validation with invalid base URL."""
    config = CoinGeckoConfig(api_base_url='')
    with pytest.raises(ValueError, match="Invalid API base URL"):
        config.validate()

def test_invalid_timeout():
    """Test validation with invalid timeout."""
    config = CoinGeckoConfig(timeout=0)
    with pytest.raises(ValueError, match="Timeout must be a positive integer"):
        config.validate()

def test_invalid_max_requests():
    """Test validation with invalid max requests."""
    config = CoinGeckoConfig(max_requests_per_minute=0)
    with pytest.raises(ValueError, match="Max requests per minute must be a positive integer"):
        config.validate()