"""
Configuration management for CoinGecko API integration.

This module handles loading and managing configuration settings
from environment variables with sensible defaults.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ConfigurationError(Exception):
    """Raised when there is an issue with configuration."""
    pass

class Configuration:
    """
    Centralized configuration management for CoinGecko API integration.
    
    Attributes:
        api_key (Optional[str]): Optional API key for CoinGecko Pro.
        base_url (str): Base URL for CoinGecko API.
        timeout (int): Request timeout in seconds.
        cache_expiry (int): Cache expiration time in seconds.
        log_level (str): Logging level.
    """
    
    def __init__(
        self, 
        api_key: Optional[str] = None, 
        base_url: Optional[str] = None,
        timeout: Optional[int] = None,
        cache_expiry: Optional[int] = None,
        log_level: Optional[str] = None
    ):
        """
        Initialize configuration with optional override parameters.
        
        Args:
            api_key: Optional API key, overrides environment variable.
            base_url: Optional base URL, overrides environment variable.
            timeout: Optional request timeout, overrides environment variable.
            cache_expiry: Optional cache expiry, overrides environment variable.
            log_level: Optional log level, overrides environment variable.
        """
        # Use provided values or fallback to environment variables
        self.api_key = api_key or os.getenv('COINGECKO_API_KEY')
        
        self.base_url = base_url or os.getenv(
            'COINGECKO_BASE_URL', 
            'https://api.coingecko.com/api/v3'
        )
        
        self.timeout = timeout or int(
            os.getenv('REQUEST_TIMEOUT', 10)
        )
        
        self.cache_expiry = cache_expiry or int(
            os.getenv('CACHE_EXPIRY', 300)
        )
        
        self.log_level = log_level or os.getenv(
            'LOG_LEVEL', 
            'INFO'
        ).upper()
        
        # Validate configuration
        self._validate()
    
    def _validate(self):
        """
        Validate configuration settings.
        
        Raises:
            ConfigurationError: If configuration is invalid.
        """
        valid_log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        
        if self.log_level not in valid_log_levels:
            raise ConfigurationError(
                f"Invalid log level: {self.log_level}. "
                f"Must be one of {valid_log_levels}"
            )
        
        if not isinstance(self.timeout, int) or self.timeout <= 0:
            raise ConfigurationError(
                f"Invalid timeout: {self.timeout}. Must be a positive integer."
            )
        
        if not isinstance(self.cache_expiry, int) or self.cache_expiry < 0:
            raise ConfigurationError(
                f"Invalid cache expiry: {self.cache_expiry}. Must be a non-negative integer."
            )
    
    def to_dict(self) -> dict:
        """
        Convert configuration to a dictionary.
        
        Returns:
            dict: Configuration settings.
        """
        return {
            'api_key': self.api_key,
            'base_url': self.base_url,
            'timeout': self.timeout,
            'cache_expiry': self.cache_expiry,
            'log_level': self.log_level
        }