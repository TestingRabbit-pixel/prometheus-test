import os
import pytest
from src.config import CoinGeckoConfig

def test_default_configuration():
    config = CoinGeckoConfig()
    assert config.api_base_url == 'https://api.coingecko.com/api/v3'
    assert config.timeout == 10
    assert config.max_retries == 3
    assert config.api_key is None

def test_environment_variable_configuration(monkeypatch):
    monkeypatch.setenv('COINGECKO_API_BASE_URL', 'https://custom-api.com')
    monkeypatch.setenv('COINGECKO_API_KEY', 'test_key')
    monkeypatch.setenv('COINGECKO_API_TIMEOUT', '15')
    monkeypatch.setenv('COINGECKO_MAX_RETRIES', '5')
    
    config = CoinGeckoConfig()
    assert config.api_base_url == 'https://custom-api.com'
    assert config.api_key == 'test_key'
    assert config.timeout == 15
    assert config.max_retries == 5

def test_explicit_parameter_precedence(monkeypatch):
    monkeypatch.setenv('COINGECKO_API_BASE_URL', 'https://env-api.com')
    
    config = CoinGeckoConfig(
        api_base_url='https://explicit-api.com',
        timeout=20,
        max_retries=7
    )
    assert config.api_base_url == 'https://explicit-api.com'
    assert config.timeout == 20
    assert config.max_retries == 7

def test_configuration_validation():
    config = CoinGeckoConfig()
    assert config.validate() is True
    
    # Invalid timeout
    with pytest.raises(Exception):
        CoinGeckoConfig(timeout=-1)
    
    # Invalid max retries
    with pytest.raises(Exception):
        CoinGeckoConfig(max_retries=-1)

def test_config_get_config():
    config = CoinGeckoConfig(api_key='test_key')
    config_dict = config.get_config()
    
    assert config_dict['api_base_url'] == 'https://api.coingecko.com/api/v3'
    assert config_dict['api_key'] == '****'
    assert config_dict['timeout'] == 10
    assert config_dict['max_retries'] == 3