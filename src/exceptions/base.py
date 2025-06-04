"""Base exceptions for CoinGecko API errors."""

class CoinGeckoAPIError(Exception):
    """Base exception for all CoinGecko API related errors.
    
    This serves as the root exception for more specific API error types.
    All other API-specific exceptions will inherit from this base class.
    
    Attributes:
        message (str): A descriptive error message
        status_code (int, optional): HTTP status code associated with the error
    """
    
    def __init__(self, message: str, status_code: int = None):
        """
        Initialize the base CoinGecko API error.
        
        Args:
            message (str): Detailed error description
            status_code (int, optional): HTTP status code 
        """
        super().__init__(message)
        self.message = message
        self.status_code = status_code
    
    def __str__(self) -> str:
        """
        Provide a string representation of the error.
        
        Returns:
            str: Formatted error message
        """
        status_info = f" (Status Code: {self.status_code})" if self.status_code else ""
        return f"{self.__class__.__name__}: {self.message}{status_info}"