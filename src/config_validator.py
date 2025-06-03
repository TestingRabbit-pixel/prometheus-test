import os
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum, auto

class ConfigurationError(Exception):
    """Custom exception for configuration validation errors."""
    pass

class Environment(Enum):
    DEVELOPMENT = auto()
    PRODUCTION = auto()
    TESTING = auto()

@dataclass
class CoinGeckoConfig:
    """Configuration class for CoinGecko API client."""
    
    # API Key (optional, as CoinGecko has free tier)
    api_key: Optional[str] = None
    
    # Environment setting
    environment: Environment = Environment.DEVELOPMENT
    
    # Timeout for API requests
    request_timeout: int = 10
    
    # Rate limit settings
    rate_limit_calls_per_second: int = 10
    
    # Optional proxy settings
    proxy_url: Optional[str] = None
    
    def validate(self) -> None:
        """
        Validate configuration settings.
        
        Raises:
            ConfigurationError: If configuration is invalid.
        """
        # Validate request timeout
        if not isinstance(self.request_timeout, int) or self.request_timeout <= 0:
            raise ConfigurationError("Request timeout must be a positive integer")
        
        # Validate rate limit
        if not isinstance(self.rate_limit_calls_per_second, int) or self.rate_limit_calls_per_second <= 0:
            raise ConfigurationError("Rate limit must be a positive integer")
        
        # Validate proxy URL format if provided
        if self.proxy_url:
            self._validate_proxy_url(self.proxy_url)
        
        # Optional API key validation (if implemented)
        if self.api_key and not self._is_valid_api_key(self.api_key):
            raise ConfigurationError("Invalid API key format")
    
    def _validate_proxy_url(self, url: str) -> None:
        """
        Validate proxy URL format.
        
        Args:
            url (str): Proxy URL to validate
        
        Raises:
            ConfigurationError: If proxy URL is invalid
        """
        # Basic proxy URL validation
        if not url.startswith(('http://', 'https://')):
            raise ConfigurationError(f"Invalid proxy URL format: {url}")
    
    def _is_valid_api_key(self, api_key: str) -> bool:
        """
        Validate API key format.
        
        Args:
            api_key (str): API key to validate
        
        Returns:
            bool: Whether the API key is valid
        """
        # Basic validation - could be expanded based on CoinGecko's specific requirements
        return isinstance(api_key, str) and len(api_key.strip()) > 0

def load_config_from_env() -> CoinGeckoConfig:
    """
    Load configuration from environment variables.
    
    Returns:
        CoinGeckoConfig: Validated configuration object
    """
    config = CoinGeckoConfig(
        api_key=os.getenv('COINGECKO_API_KEY'),
        environment=Environment[os.getenv('COINGECKO_ENV', 'DEVELOPMENT').upper()],
        request_timeout=int(os.getenv('COINGECKO_REQUEST_TIMEOUT', 10)),
        rate_limit_calls_per_second=int(os.getenv('COINGECKO_RATE_LIMIT', 10)),
        proxy_url=os.getenv('COINGECKO_PROXY_URL')
    )
    
    # Validate configuration
    config.validate()
    
    return config