from dataclasses import dataclass
from typing import Optional

@dataclass
class CoinGeckoConfig:
    """
    Configuration class for CoinGecko API integration.
    
    Attributes:
        api_key (Optional[str]): Optional API key for authenticated requests
        base_url (str): Base URL for CoinGecko API
        request_timeout (int): Timeout for API requests in seconds
        log_level (str): Logging level for the application
    """
    api_key: Optional[str] = None
    base_url: str = "https://api.coingecko.com/api/v3"
    request_timeout: int = 10
    log_level: str = "INFO"

    def validate(self) -> bool:
        """
        Validate configuration parameters.
        
        Returns:
            bool: True if configuration is valid, False otherwise
        """
        if not isinstance(self.base_url, str):
            raise ValueError("Base URL must be a string")
        
        if not isinstance(self.request_timeout, int) or self.request_timeout <= 0:
            raise ValueError("Request timeout must be a positive integer")
        
        valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if self.log_level not in valid_log_levels:
            raise ValueError(f"Invalid log level. Must be one of {valid_log_levels}")
        
        return True

def load_config() -> CoinGeckoConfig:
    """
    Load configuration from environment variables or default settings.
    
    Returns:
        CoinGeckoConfig: Configured CoinGecko API settings
    """
    import os
    
    return CoinGeckoConfig(
        api_key=os.getenv("COINGECKO_API_KEY"),
        base_url=os.getenv("COINGECKO_API_BASE_URL", "https://api.coingecko.com/api/v3"),
        request_timeout=int(os.getenv("COINGECKO_REQUEST_TIMEOUT", 10)),
        log_level=os.getenv("COINGECKO_LOG_LEVEL", "INFO")
    )