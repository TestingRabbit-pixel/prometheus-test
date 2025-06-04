import os
from typing import Optional
from dataclasses import dataclass, field

@dataclass
class CoinGeckoConfig:
    """
    Configuration class for CoinGecko API settings.
    
    Supports configuration via environment variables and direct initialization.
    Provides validation and default settings for API interactions.
    """
    
    # Base API URL
    api_base_url: str = field(default="https://api.coingecko.com/api/v3")
    
    # API key (optional)
    api_key: Optional[str] = field(default=None)
    
    # Request timeout in seconds
    timeout: int = field(default=10)
    
    # Rate limit configuration
    max_requests_per_minute: int = field(default=30)
    
    @classmethod
    def from_env(cls) -> 'CoinGeckoConfig':
        """
        Create a configuration instance from environment variables.
        
        Environment variables:
        - COINGECKO_API_BASE_URL: Optional base URL
        - COINGECKO_API_KEY: Optional API key
        - COINGECKO_TIMEOUT: Optional request timeout
        - COINGECKO_MAX_REQUESTS: Optional max requests per minute
        
        Returns:
            CoinGeckoConfig: Configured instance
        """
        return cls(
            api_base_url=os.getenv('COINGECKO_API_BASE_URL', 'https://api.coingecko.com/api/v3'),
            api_key=os.getenv('COINGECKO_API_KEY'),
            timeout=int(os.getenv('COINGECKO_TIMEOUT', 10)),
            max_requests_per_minute=int(os.getenv('COINGECKO_MAX_REQUESTS', 30))
        )
    
    def validate(self) -> None:
        """
        Validate configuration settings.
        
        Raises:
            ValueError: If configuration is invalid
        """
        if not self.api_base_url or not isinstance(self.api_base_url, str):
            raise ValueError("Invalid API base URL")
        
        if self.timeout <= 0:
            raise ValueError("Timeout must be a positive integer")
        
        if self.max_requests_per_minute <= 0:
            raise ValueError("Max requests per minute must be a positive integer")