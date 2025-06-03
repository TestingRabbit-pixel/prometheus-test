from typing import Optional, Any


class CoinGeckoAPIError(Exception):
    """Base exception for CoinGecko API errors."""

    def __init__(self, message: str, error_code: Optional[int] = None, response_data: Optional[Any] = None):
        """
        Initialize a CoinGecko API error.

        Args:
            message (str): A descriptive error message.
            error_code (Optional[int]): The specific error code, if available.
            response_data (Optional[Any]): The raw response data from the API.
        """
        self.message = message
        self.error_code = error_code
        self.response_data = response_data
        super().__init__(self.message)

    def __str__(self) -> str:
        """
        Provide a detailed string representation of the error.

        Returns:
            str: A formatted error message.
        """
        error_str = self.message
        if self.error_code is not None:
            error_str += f" (Error Code: {self.error_code})"
        return error_str


class NetworkError(CoinGeckoAPIError):
    """Raised when there are network connectivity issues."""

    def __init__(self, message: str = "Network connection failed"):
        """
        Initialize a network error.

        Args:
            message (str, optional): A description of the network error.
        """
        super().__init__(message)


class RateLimitError(CoinGeckoAPIError):
    """Raised when API rate limits are exceeded."""

    def __init__(self, message: str = "API rate limit exceeded", 
                 retry_after: Optional[int] = None):
        """
        Initialize a rate limit error.

        Args:
            message (str, optional): A description of the rate limit error.
            retry_after (Optional[int]): Suggested time to wait before retrying.
        """
        self.retry_after = retry_after
        super().__init__(message)


class AuthenticationError(CoinGeckoAPIError):
    """Raised when authentication with the API fails."""

    def __init__(self, message: str = "Authentication failed"):
        """
        Initialize an authentication error.

        Args:
            message (str, optional): A description of the authentication error.
        """
        super().__init__(message)


class DataNotFoundError(CoinGeckoAPIError):
    """Raised when requested data is not found."""

    def __init__(self, message: str = "Requested data not found"):
        """
        Initialize a data not found error.

        Args:
            message (str, optional): A description of the data not found error.
        """
        super().__init__(message)


class ValidationError(CoinGeckoAPIError):
    """Raised when input validation fails."""

    def __init__(self, message: str = "Invalid input parameters"):
        """
        Initialize a validation error.

        Args:
            message (str, optional): A description of the validation error.
        """
        super().__init__(message)