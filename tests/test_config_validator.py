import os
import pytest
from src.config_validator import CoinGeckoConfigValidator, ConfigValidationError

def test_valid_config_validation():
    """Test successful configuration validation."""
    valid_config = {
        'API_BASE_URL': 'https://api.coingecko.com/api/v3',
        'API_KEY': 'test_api_key_123456',
        'REQUEST_TIMEOUT': 30,
        'RATE_LIMIT': 50
    }
    
    validated_config = CoinGeckoConfigValidator.validate_config(valid_config)
    assert validated_config == valid_config

def test_missing_required_keys():
    """Test validation fails with missing required keys."""
    invalid_configs = [
        {},
        {'API_BASE_URL': 'https://api.example.com'},
        {'API_KEY': 'test_key'}
    ]
    
    for config in invalid_configs:
        with pytest.raises(ConfigValidationError, match="Missing required configuration key"):
            CoinGeckoConfigValidator.validate_config(config)

def test_invalid_url_format():
    """Test URL validation."""
    invalid_urls = [
        'not_a_url',
        'http://',
        'https://invalid url.com',
        'ftp://example.com'
    ]
    
    for url in invalid_urls:
        with pytest.raises(ConfigValidationError, match="Invalid URL format"):
            CoinGeckoConfigValidator.validate_config({
                'API_BASE_URL': url,
                'API_KEY': 'test_key'
            })

def test_api_key_validation():
    """Test API key validation."""
    invalid_keys = [
        '',
        '   ',
        'short'
    ]
    
    for key in invalid_keys:
        with pytest.raises(ConfigValidationError, match="API key is too short"):
            CoinGeckoConfigValidator.validate_config({
                'API_BASE_URL': 'https://api.coingecko.com/api/v3',
                'API_KEY': key
            })

def test_timeout_validation():
    """Test timeout value validation."""
    invalid_timeouts = [
        -1,
        0,
        '0',
        130,
        'not_a_number'
    ]
    
    for timeout in invalid_timeouts:
        with pytest.raises(ConfigValidationError, match="Invalid timeout value"):
            CoinGeckoConfigValidator.validate_config({
                'API_BASE_URL': 'https://api.coingecko.com/api/v3',
                'API_KEY': 'test_key',
                'REQUEST_TIMEOUT': timeout
            })

def test_rate_limit_validation():
    """Test rate limit validation."""
    invalid_rate_limits = [
        -1,
        0,
        '0',
        150,
        'not_a_number'
    ]
    
    for rate_limit in invalid_rate_limits:
        with pytest.raises(ConfigValidationError, match="Invalid rate limit value"):
            CoinGeckoConfigValidator.validate_config({
                'API_BASE_URL': 'https://api.coingecko.com/api/v3',
                'API_KEY': 'test_key',
                'RATE_LIMIT': rate_limit
            })

def test_env_config_loading(monkeypatch):
    """Test loading configuration from environment variables."""
    monkeypatch.setenv('COINGECKO_API_BASE_URL', 'https://custom-api.coingecko.com')
    monkeypatch.setenv('COINGECKO_API_KEY', 'test_env_key')
    monkeypatch.setenv('COINGECKO_REQUEST_TIMEOUT', '45')
    monkeypatch.setenv('COINGECKO_RATE_LIMIT', '75')
    
    config = CoinGeckoConfigValidator.load_from_env()
    
    assert config['API_BASE_URL'] == 'https://custom-api.coingecko.com'
    assert config['API_KEY'] == 'test_env_key'
    assert config['REQUEST_TIMEOUT'] == 45
    assert config['RATE_LIMIT'] == 75