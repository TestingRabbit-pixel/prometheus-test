"""Specific exceptions for different CoinGecko API error scenarios."""

from .base import CoinGeckoAPIError

class RateLimitError(CoinGeckoAPIError):
    """Raised when the API rate limit is exceeded."""
    
    def __init__(self, message: str = "API rate limit exceeded", status_code: int = 429):
        """
        Initialize rate limit error.
        
        Args:
            message (str, optional): Custom error message
            status_code (int, optional): HTTP status code for rate limiting
        """
        super().__init__(message, status_code)

class AuthenticationError(CoinGeckoAPIError):
    """Raised when authentication fails or API credentials are invalid."""
    
    def __init__(self, message: str = "Authentication failed", status_code: int = 401):
        """
        Initialize authentication error.
        
        Args:
            message (str, optional): Custom error message
            status_code (int, optional): HTTP status code for authentication errors
        """
        super().__init__(message, status_code)

class ResourceNotFoundError(CoinGeckoAPIError):
    """Raised when a requested resource is not found."""
    
    def __init__(self, message: str = "Requested resource not found", status_code: int = 404):
        """
        Initialize resource not found error.
        
        Args:
            message (str, optional): Custom error message
            status_code (int, optional): HTTP status code for not found errors
        """
        super().__init__(message, status_code)

class InvalidRequestError(CoinGeckoAPIError):
    """Raised when the API request is malformed or invalid."""
    
    def __init__(self, message: str = "Invalid API request", status_code: int = 400):
        """
        Initialize invalid request error.
        
        Args:
            message (str, optional): Custom error message
            status_code (int, optional): HTTP status code for bad request
        """
        super().__init__(message, status_code)

class NetworkError(CoinGeckoAPIError):
    """Raised for network-related issues during API communication."""
    
    def __init__(self, message: str = "Network communication error", status_code: int = None):
        """
        Initialize network error.
        
        Args:
            message (str, optional): Custom error message
            status_code (int, optional): HTTP status code if applicable
        """
        super().__init__(message, status_code)