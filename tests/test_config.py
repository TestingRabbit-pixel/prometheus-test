import os
import pytest
from src.config import CoinGeckoConfig, ConfigError, Environment

def test_default_config():
    """Test default configuration values."""
    config = CoinGeckoConfig()
    
    assert config.api_base_url == 'https://api.coingecko.com/api/v3'
    assert config.timeout == 10
    assert config.retries == 3
    assert config.environment == Environment.DEVELOPMENT
    assert config.cache_enabled is True
    assert config.cache_expiry == 300
    assert config.rate_limit_per_second == 10

def test_invalid_api_base_url():
    """Test invalid API base URL."""
    with pytest.raises(ConfigError, match="API base URL must be a valid HTTPS URL"):
        CoinGeckoConfig(api_base_url='http://invalid')

def test_invalid_timeout():
    """Test invalid timeout values."""
    with pytest.raises(ConfigError, match="Timeout must be a positive integer"):
        CoinGeckoConfig(timeout=0)
    
    with pytest.raises(ConfigError, match="Timeout must be a positive integer"):
        CoinGeckoConfig(timeout=-1)

def test_invalid_retries():
    """Test invalid retry configurations."""
    with pytest.raises(ConfigError, match="Retries must be a non-negative integer"):
        CoinGeckoConfig(retries=-1)

def test_invalid_environment():
    """Test invalid environment settings."""
    with pytest.raises(ConfigError, match="Invalid environment setting"):
        CoinGeckoConfig(environment="invalid_env")

def test_invalid_cache_settings():
    """Test invalid cache configurations."""
    with pytest.raises(ConfigError, match="Cache enabled must be a boolean"):
        CoinGeckoConfig(cache_enabled=1)  # type: ignore
    
    with pytest.raises(ConfigError, match="Cache expiry must be a non-negative integer"):
        CoinGeckoConfig(cache_expiry=-1)

def test_invalid_rate_limit():
    """Test invalid rate limit configurations."""
    with pytest.raises(ConfigError, match="Rate limit must be a positive integer"):
        CoinGeckoConfig(rate_limit_per_second=0)

def test_config_from_env(monkeypatch):
    """Test configuration loading from environment variables."""
    monkeypatch.setenv('COINGECKO_API_URL', 'https://custom-api.com')
    monkeypatch.setenv('COINGECKO_TIMEOUT', '15')
    monkeypatch.setenv('COINGECKO_RETRIES', '5')
    monkeypatch.setenv('COINGECKO_ENV', 'production')
    monkeypatch.setenv('COINGECKO_CACHE_ENABLED', 'false')
    monkeypatch.setenv('COINGECKO_CACHE_EXPIRY', '600')
    monkeypatch.setenv('COINGECKO_RATE_LIMIT', '20')

    config = CoinGeckoConfig.from_env()
    
    assert config.api_base_url == 'https://custom-api.com'
    assert config.timeout == 15
    assert config.retries == 5
    assert config.environment == Environment.PRODUCTION
    assert config.cache_enabled is False
    assert config.cache_expiry == 600
    assert config.rate_limit_per_second == 20