import os
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

class Environment(Enum):
    DEVELOPMENT = 'development'
    PRODUCTION = 'production'
    STAGING = 'staging'

@dataclass
class CoinGeckoConfig:
    api_key: Optional[str] = None
    base_url: str = 'https://api.coingecko.com/api/v3'
    environment: Environment = Environment.DEVELOPMENT
    request_timeout: int = 10
    max_retries: int = 3
    rate_limit_per_minute: int = 30

    def __post_init__(self):
        """
        Validate configuration after initialization.
        Raises ValueError for invalid configurations.
        """
        self.validate_config()

    def validate_config(self):
        """
        Comprehensive configuration validation method.
        Checks for required settings and their validity.
        """
        # Validate base URL
        if not self.base_url or not self.base_url.startswith('https://'):
            raise ValueError("Invalid base URL. Must be a valid HTTPS URL.")

        # Validate request timeout
        if not 1 <= self.request_timeout <= 60:
            raise ValueError("Request timeout must be between 1 and 60 seconds.")

        # Validate max retries
        if not 0 <= self.max_retries <= 5:
            raise ValueError("Max retries must be between 0 and 5.")

        # Validate rate limit
        if not 1 <= self.rate_limit_per_minute <= 100:
            raise ValueError("Rate limit must be between 1 and 100 requests per minute.")

        # Optional API key validation for production
        if self.environment == Environment.PRODUCTION and not self.api_key:
            raise ValueError("API key is required for production environment.")

    @classmethod
    def from_env(cls) -> 'CoinGeckoConfig':
        """
        Create configuration from environment variables.
        Allows flexible configuration management.
        """
        return cls(
            api_key=os.getenv('COINGECKO_API_KEY'),
            base_url=os.getenv('COINGECKO_BASE_URL', 'https://api.coingecko.com/api/v3'),
            environment=Environment(os.getenv('COINGECKO_ENV', 'development')),
            request_timeout=int(os.getenv('COINGECKO_REQUEST_TIMEOUT', 10)),
            max_retries=int(os.getenv('COINGECKO_MAX_RETRIES', 3)),
            rate_limit_per_minute=int(os.getenv('COINGECKO_RATE_LIMIT', 30))
        )