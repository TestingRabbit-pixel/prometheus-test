import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv

class InvalidConfigurationError(ValueError):
    """Custom exception for invalid configuration."""
    pass

class CoinGeckoConfig:
    """
    Configuration management for CoinGecko API client.
    
    Supports configuration through:
    1. Environment variables
    2. Explicit parameters
    3. Default values
    """
    
    def __init__(
        self, 
        api_base_url: Optional[str] = None, 
        api_key: Optional[str] = None,
        timeout: Optional[int] = None,
        max_retries: Optional[int] = None
    ):
        """
        Initialize CoinGecko API configuration.
        
        Args:
            api_base_url (Optional[str]): Base URL for CoinGecko API
            api_key (Optional[str]): API key for authentication
            timeout (Optional[int]): Request timeout in seconds
            max_retries (Optional[int]): Maximum number of request retries
        
        Raises:
            InvalidConfigurationError: If configuration parameters are invalid
        """
        # Load .env file if it exists
        load_dotenv()
        
        # Priority: Explicit parameters > Environment Variables > Default Values
        self.api_base_url = (
            api_base_url or 
            os.getenv('COINGECKO_API_BASE_URL', 'https://api.coingecko.com/api/v3')
        )
        
        self.api_key = (
            api_key or 
            os.getenv('COINGECKO_API_KEY')
        )
        
        self.timeout = (
            timeout or 
            int(os.getenv('COINGECKO_API_TIMEOUT', 10))
        )
        
        self.max_retries = (
            max_retries or 
            int(os.getenv('COINGECKO_MAX_RETRIES', 3))
        )
        
        # Validate configuration during initialization
        if not self.validate():
            raise InvalidConfigurationError("Invalid configuration parameters")
    
    def get_config(self) -> Dict[str, Any]:
        """
        Get current configuration as a dictionary.
        
        Returns:
            Dict[str, Any]: Configuration dictionary
        """
        return {
            'api_base_url': self.api_base_url,
            'api_key': '****' if self.api_key else None,  # Mask API key
            'timeout': self.timeout,
            'max_retries': self.max_retries
        }
    
    def validate(self) -> bool:
        """
        Validate the current configuration.
        
        Returns:
            bool: Whether the configuration is valid
        
        Raises:
            InvalidConfigurationError: If configuration is invalid
        """
        # Validate API base URL
        if not self.api_base_url or not isinstance(self.api_base_url, str):
            return False
        
        # Validate timeout
        if not isinstance(self.timeout, int) or self.timeout <= 0:
            return False
        
        # Validate max retries
        if not isinstance(self.max_retries, int) or self.max_retries < 0:
            return False
        
        return True