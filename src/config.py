import os
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

class ConfigError(Exception):
    """Custom exception for configuration validation errors."""
    pass

class Environment(Enum):
    DEVELOPMENT = 'development'
    PRODUCTION = 'production'
    TESTING = 'testing'

@dataclass
class CoinGeckoConfig:
    """Configuration for CoinGecko API integration."""
    
    api_base_url: str = 'https://api.coingecko.com/api/v3'
    timeout: int = 10
    retries: int = 3
    environment: Environment = Environment.DEVELOPMENT
    cache_enabled: bool = True
    cache_expiry: int = 300  # 5 minutes
    rate_limit_per_second: int = 10

    def __post_init__(self):
        """
        Validate configuration after initialization.
        Raises ConfigError if any configuration is invalid.
        """
        self._validate_api_base_url()
        self._validate_timeout()
        self._validate_retries()
        self._validate_environment()
        self._validate_cache_settings()
        self._validate_rate_limit()

    def _validate_api_base_url(self):
        """Validate the API base URL."""
        if not self.api_base_url or not self.api_base_url.startswith('https://'):
            raise ConfigError("API base URL must be a valid HTTPS URL")

    def _validate_timeout(self):
        """Validate request timeout."""
        if not isinstance(self.timeout, int) or self.timeout <= 0:
            raise ConfigError("Timeout must be a positive integer")

    def _validate_retries(self):
        """Validate retry configuration."""
        if not isinstance(self.retries, int) or self.retries < 0:
            raise ConfigError("Retries must be a non-negative integer")

    def _validate_environment(self):
        """Validate environment setting."""
        if not isinstance(self.environment, Environment):
            raise ConfigError("Invalid environment setting")

    def _validate_cache_settings(self):
        """Validate cache-related settings."""
        if not isinstance(self.cache_enabled, bool):
            raise ConfigError("Cache enabled must be a boolean")
        
        if not isinstance(self.cache_expiry, int) or self.cache_expiry < 0:
            raise ConfigError("Cache expiry must be a non-negative integer")

    def _validate_rate_limit(self):
        """Validate rate limit settings."""
        if not isinstance(self.rate_limit_per_second, int) or self.rate_limit_per_second <= 0:
            raise ConfigError("Rate limit must be a positive integer")

    @classmethod
    def from_env(cls) -> 'CoinGeckoConfig':
        """
        Create a configuration from environment variables.
        
        Environment variables take precedence over default values.
        """
        return cls(
            api_base_url=os.getenv('COINGECKO_API_URL', 'https://api.coingecko.com/api/v3'),
            timeout=int(os.getenv('COINGECKO_TIMEOUT', 10)),
            retries=int(os.getenv('COINGECKO_RETRIES', 3)),
            environment=Environment(os.getenv('COINGECKO_ENV', 'development')),
            cache_enabled=os.getenv('COINGECKO_CACHE_ENABLED', 'true').lower() == 'true',
            cache_expiry=int(os.getenv('COINGECKO_CACHE_EXPIRY', 300)),
            rate_limit_per_second=int(os.getenv('COINGECKO_RATE_LIMIT', 10))
        )