import os
from typing import Optional, Union
from dataclasses import dataclass

@dataclass
class CoinGeckoConfig:
    """
    Configuration class for CoinGecko API settings.
    
    Supports configuration via environment variables with sensible defaults.
    """
    api_base_url: str = 'https://api.coingecko.com/api/v3'
    api_key: Optional[str] = None
    request_timeout: int = 10
    cache_enabled: bool = True
    rate_limit_per_minute: int = 30

    def __post_init__(self):
        """
        Post-initialization method to parse environment variables.
        Allows overriding default settings via environment variables.
        """
        # Base URL parsing
        self.api_base_url = os.getenv('COINGECKO_API_BASE_URL', self.api_base_url)
        
        # API Key parsing (optional)
        self.api_key = os.getenv('COINGECKO_API_KEY', self.api_key)
        
        # Request timeout parsing
        try:
            timeout_env = os.getenv('COINGECKO_REQUEST_TIMEOUT')
            if timeout_env is not None:
                self.request_timeout = int(timeout_env)
        except ValueError:
            raise ValueError("COINGECKO_REQUEST_TIMEOUT must be an integer")
        
        # Cache enabled parsing
        cache_env = os.getenv('COINGECKO_CACHE_ENABLED', str(self.cache_enabled)).lower()
        self.cache_enabled = cache_env in ['true', '1', 'yes']
        
        # Rate limit parsing
        try:
            rate_limit_env = os.getenv('COINGECKO_RATE_LIMIT_PER_MINUTE')
            if rate_limit_env is not None:
                self.rate_limit_per_minute = int(rate_limit_env)
        except ValueError:
            raise ValueError("COINGECKO_RATE_LIMIT_PER_MINUTE must be an integer")
        
        # Validate configurations
        self._validate_config()
    
    def _validate_config(self):
        """
        Validate configuration parameters.
        Raises ValueError for invalid configurations.
        """
        if self.request_timeout <= 0:
            raise ValueError("Request timeout must be a positive integer")
        
        if self.rate_limit_per_minute <= 0:
            raise ValueError("Rate limit must be a positive integer")

    def get_config_summary(self) -> dict:
        """
        Returns a summary of the current configuration.
        Useful for logging and debugging.
        
        :return: Dictionary containing configuration details
        """
        return {
            'api_base_url': self.api_base_url,
            'api_key_set': self.api_key is not None,
            'request_timeout': self.request_timeout,
            'cache_enabled': self.cache_enabled,
            'rate_limit_per_minute': self.rate_limit_per_minute
        }