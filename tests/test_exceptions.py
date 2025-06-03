import pytest
from src.exceptions import (
    CoinGeckoAPIError, 
    NetworkError, 
    RateLimitError, 
    AuthenticationError, 
    DataNotFoundError, 
    ValidationError
)


def test_base_coingecko_api_error():
    """Test the base CoinGecko API error with all parameters."""
    error = CoinGeckoAPIError(
        message="Test error", 
        error_code=404, 
        response_data={"details": "Some error"}
    )
    
    assert str(error) == "Test error (Error Code: 404)"
    assert error.message == "Test error"
    assert error.error_code == 404
    assert error.response_data == {"details": "Some error"}


def test_network_error():
    """Test the NetworkError exception."""
    error = NetworkError()
    assert str(error) == "Network connection failed"
    
    custom_error = NetworkError("Connection timeout")
    assert str(custom_error) == "Connection timeout"


def test_rate_limit_error():
    """Test the RateLimitError exception."""
    error = RateLimitError()
    assert str(error) == "API rate limit exceeded"
    
    error_with_retry = RateLimitError(retry_after=60)
    assert error_with_retry.retry_after == 60


def test_authentication_error():
    """Test the AuthenticationError exception."""
    error = AuthenticationError()
    assert str(error) == "Authentication failed"
    
    custom_error = AuthenticationError("Invalid API key")
    assert str(custom_error) == "Invalid API key"


def test_data_not_found_error():
    """Test the DataNotFoundError exception."""
    error = DataNotFoundError()
    assert str(error) == "Requested data not found"
    
    custom_error = DataNotFoundError("Cryptocurrency not found")
    assert str(custom_error) == "Cryptocurrency not found"


def test_validation_error():
    """Test the ValidationError exception."""
    error = ValidationError()
    assert str(error) == "Invalid input parameters"
    
    custom_error = ValidationError("Invalid currency")
    assert str(custom_error) == "Invalid currency"


def test_inheritance():
    """Test the inheritance hierarchy of exceptions."""
    # All custom exceptions should inherit from CoinGeckoAPIError
    assert issubclass(NetworkError, CoinGeckoAPIError)
    assert issubclass(RateLimitError, CoinGeckoAPIError)
    assert issubclass(AuthenticationError, CoinGeckoAPIError)
    assert issubclass(DataNotFoundError, CoinGeckoAPIError)
    assert issubclass(ValidationError, CoinGeckoAPIError)