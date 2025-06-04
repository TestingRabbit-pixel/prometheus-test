import os
import pytest
from src.coingecko_api.config import CoinGeckoConfig

def test_default_config():
    """Test default configuration settings"""
    config = CoinGeckoConfig()
    assert config.api_base_url == 'https://api.coingecko.com/api/v3'
    assert config.api_key is None
    assert config.request_timeout == 10
    assert config.cache_enabled is True
    assert config.rate_limit_per_minute == 30

def test_env_variable_override():
    """Test overriding configuration via environment variables"""
    os.environ['COINGECKO_API_BASE_URL'] = 'https://test-api.coingecko.com'
    os.environ['COINGECKO_API_KEY'] = 'test_key'
    os.environ['COINGECKO_REQUEST_TIMEOUT'] = '20'
    os.environ['COINGECKO_CACHE_ENABLED'] = 'false'
    os.environ['COINGECKO_RATE_LIMIT_PER_MINUTE'] = '50'

    try:
        config = CoinGeckoConfig()
        assert config.api_base_url == 'https://test-api.coingecko.com'
        assert config.api_key == 'test_key'
        assert config.request_timeout == 20
        assert config.cache_enabled is False
        assert config.rate_limit_per_minute == 50
    finally:
        # Clean up environment variables
        for key in [
            'COINGECKO_API_BASE_URL', 'COINGECKO_API_KEY', 
            'COINGECKO_REQUEST_TIMEOUT', 'COINGECKO_CACHE_ENABLED', 
            'COINGECKO_RATE_LIMIT_PER_MINUTE'
        ]:
            os.environ.pop(key, None)

def test_invalid_timeout():
    """Test invalid timeout configuration"""
    os.environ['COINGECKO_REQUEST_TIMEOUT'] = '-5'
    
    with pytest.raises(ValueError, match="Request timeout must be a positive integer"):
        CoinGeckoConfig()
    
    os.environ.pop('COINGECKO_REQUEST_TIMEOUT', None)

def test_invalid_rate_limit():
    """Test invalid rate limit configuration"""
    os.environ['COINGECKO_RATE_LIMIT_PER_MINUTE'] = '0'
    
    with pytest.raises(ValueError, match="Rate limit must be a positive integer"):
        CoinGeckoConfig()
    
    os.environ.pop('COINGECKO_RATE_LIMIT_PER_MINUTE', None)

def test_config_summary():
    """Test configuration summary method"""
    config = CoinGeckoConfig()
    summary = config.get_config_summary()
    
    assert isinstance(summary, dict)
    assert summary['api_base_url'] == 'https://api.coingecko.com/api/v3'
    assert summary['api_key_set'] is False
    assert summary['request_timeout'] == 10
    assert summary['cache_enabled'] is True
    assert summary['rate_limit_per_minute'] == 30