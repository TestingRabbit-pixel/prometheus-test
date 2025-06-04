"""
Test suite for CoinGecko API custom exceptions.

This module verifies the behavior of custom exceptions 
defined for handling different API error scenarios.
"""

import pytest
from src.exceptions.base import CoinGeckoAPIError
from src.exceptions.specific import (
    RateLimitError, 
    AuthenticationError, 
    ResourceNotFoundError, 
    InvalidRequestError, 
    NetworkError
)

def test_base_exception():
    """Test the base CoinGecko API error."""
    message = "Test error message"
    status_code = 500
    
    error = CoinGeckoAPIError(message, status_code)
    
    assert str(error) == f"CoinGeckoAPIError: {message} (Status Code: {status_code})"
    assert error.message == message
    assert error.status_code == status_code

def test_rate_limit_error():
    """Test rate limit exception."""
    error = RateLimitError()
    
    assert isinstance(error, CoinGeckoAPIError)
    assert error.status_code == 429
    assert error.message == "API rate limit exceeded"

def test_authentication_error():
    """Test authentication exception."""
    error = AuthenticationError("Invalid credentials")
    
    assert isinstance(error, CoinGeckoAPIError)
    assert error.status_code == 401
    assert error.message == "Invalid credentials"

def test_resource_not_found_error():
    """Test resource not found exception."""
    error = ResourceNotFoundError("Coin not found")
    
    assert isinstance(error, CoinGeckoAPIError)
    assert error.status_code == 404
    assert error.message == "Coin not found"

def test_invalid_request_error():
    """Test invalid request exception."""
    error = InvalidRequestError("Missing required parameter")
    
    assert isinstance(error, CoinGeckoAPIError)
    assert error.status_code == 400
    assert error.message == "Missing required parameter"

def test_network_error():
    """Test network error exception."""
    error = NetworkError("Connection timeout")
    
    assert isinstance(error, CoinGeckoAPIError)
    assert error.status_code is None
    assert error.message == "Connection timeout"

def test_exception_inheritance():
    """Verify that all specific exceptions inherit from base exception."""
    exceptions = [
        RateLimitError(),
        AuthenticationError(),
        ResourceNotFoundError(),
        InvalidRequestError(),
        NetworkError()
    ]
    
    for error in exceptions:
        assert isinstance(error, CoinGeckoAPIError)