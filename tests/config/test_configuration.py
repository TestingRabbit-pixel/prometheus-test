"""
Unit tests for configuration management.
"""

import os
import pytest
from src.config import Configuration, ConfigurationError

def test_default_configuration():
    """Test default configuration settings."""
    config = Configuration()
    
    assert config.base_url == 'https://api.coingecko.com/api/v3'
    assert config.timeout == 10
    assert config.cache_expiry == 300
    assert config.log_level == 'INFO'
    assert config.api_key is None

def test_configuration_override():
    """Test configuration override with explicit parameters."""
    config = Configuration(
        api_key='test_key',
        base_url='https://custom-api.com',
        timeout=15,
        cache_expiry=600,
        log_level='DEBUG'
    )
    
    assert config.api_key == 'test_key'
    assert config.base_url == 'https://custom-api.com'
    assert config.timeout == 15
    assert config.cache_expiry == 600
    assert config.log_level == 'DEBUG'

def test_invalid_log_level():
    """Test invalid log level raises ConfigurationError."""
    with pytest.raises(ConfigurationError, match="Invalid log level"):
        Configuration(log_level='INVALID')

def test_invalid_timeout():
    """Test invalid timeout raises ConfigurationError."""
    with pytest.raises(ConfigurationError, match="Invalid timeout"):
        Configuration(timeout=-5)

def test_invalid_cache_expiry():
    """Test invalid cache expiry raises ConfigurationError."""
    with pytest.raises(ConfigurationError, match="Invalid cache expiry"):
        Configuration(cache_expiry=-1)

def test_configuration_to_dict():
    """Test configuration to_dict method."""
    config = Configuration(
        api_key='test_key',
        base_url='https://custom-api.com',
        timeout=15,
        cache_expiry=600,
        log_level='DEBUG'
    )
    
    config_dict = config.to_dict()
    
    assert isinstance(config_dict, dict)
    assert config_dict['api_key'] == 'test_key'
    assert config_dict['base_url'] == 'https://custom-api.com'
    assert config_dict['timeout'] == 15
    assert config_dict['cache_expiry'] == 600
    assert config_dict['log_level'] == 'DEBUG'