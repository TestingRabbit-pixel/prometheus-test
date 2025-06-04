import os
import pytest
from config.example_config import CoinGeckoConfig, load_config

def test_default_config():
    """Test default configuration settings."""
    config = CoinGeckoConfig()
    
    assert config.base_url == "https://api.coingecko.com/api/v3"
    assert config.request_timeout == 10
    assert config.log_level == "INFO"
    assert config.api_key is None

def test_config_validation():
    """Test configuration validation."""
    config = CoinGeckoConfig()
    assert config.validate() is True

def test_invalid_config():
    """Test invalid configuration raises appropriate errors."""
    with pytest.raises(ValueError, match="Base URL must be a string"):
        CoinGeckoConfig(base_url=123).validate()
    
    with pytest.raises(ValueError, match="Request timeout must be a positive integer"):
        CoinGeckoConfig(request_timeout=-1).validate()
    
    with pytest.raises(ValueError, match="Invalid log level"):
        CoinGeckoConfig(log_level="INVALID").validate()

def test_load_config_from_env(monkeypatch):
    """Test loading configuration from environment variables."""
    monkeypatch.setenv("COINGECKO_API_KEY", "test_key")
    monkeypatch.setenv("COINGECKO_API_BASE_URL", "https://custom-api.com")
    monkeypatch.setenv("COINGECKO_REQUEST_TIMEOUT", "15")
    monkeypatch.setenv("COINGECKO_LOG_LEVEL", "DEBUG")
    
    config = load_config()
    
    assert config.api_key == "test_key"
    assert config.base_url == "https://custom-api.com"
    assert config.request_timeout == 15
    assert config.log_level == "DEBUG"