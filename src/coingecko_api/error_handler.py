from typing import Dict, Any, Optional
import logging

class CoinGeckoAPIError(Exception):
    """Base exception for CoinGecko API errors."""
    def __init__(self, message: str, status_code: Optional[int] = None, 
                 error_response: Optional[Dict[str, Any]] = None):
        """
        Initialize a CoinGecko API error.

        Args:
            message (str): A user-friendly error message
            status_code (int, optional): HTTP status code of the error
            error_response (dict, optional): Raw error response from the API
        """
        self.message = message
        self.status_code = status_code
        self.error_response = error_response
        super().__init__(self.message)

class ErrorHandler:
    """
    Handles parsing and transformation of API error responses.
    """

    @staticmethod
    def parse_error(error_response: Dict[str, Any]) -> CoinGeckoAPIError:
        """
        Parse and transform an API error response into a user-friendly error.

        Args:
            error_response (dict): Raw error response from the API

        Returns:
            CoinGeckoAPIError: Transformed, user-friendly error
        """
        # Common error parsing strategies
        try:
            # Check for specific CoinGecko error formats
            if 'error' in error_response:
                error_message = str(error_response.get('error', 'Unknown API error'))
                return CoinGeckoAPIError(
                    message=f"CoinGecko API Error: {error_message}",
                    error_response=error_response
                )
            
            # Generic error parsing
            if 'message' in error_response:
                return CoinGeckoAPIError(
                    message=f"API Error: {error_response['message']}",
                    error_response=error_response
                )
            
            # Fallback generic error
            return CoinGeckoAPIError(
                message="An unknown error occurred with the CoinGecko API",
                error_response=error_response
            )
        
        except Exception as e:
            # Logging unexpected error parsing failures
            logging.error(f"Unexpected error parsing API error: {str(e)}")
            return CoinGeckoAPIError(
                message="Failed to parse API error response",
                error_response=error_response
            )

    @staticmethod
    def handle_network_error(exception: Exception) -> CoinGeckoAPIError:
        """
        Handle network-related errors and convert them to a user-friendly error.

        Args:
            exception (Exception): The original network exception

        Returns:
            CoinGeckoAPIError: A transformed, user-friendly network error
        """
        error_map = {
            'ConnectionError': 'Unable to connect to CoinGecko API. Please check your internet connection.',
            'Timeout': 'Request to CoinGecko API timed out. Please try again later.',
            'RequestException': 'An error occurred while making the API request.'
        }

        # Match the exception type to a predefined message
        error_message = error_map.get(
            exception.__class__.__name__, 
            f"Network Error: {str(exception)}"
        )

        return CoinGeckoAPIError(message=error_message)