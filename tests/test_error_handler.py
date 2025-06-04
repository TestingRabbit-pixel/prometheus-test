import pytest
from src.coingecko_api.error_handler import ErrorHandler, CoinGeckoAPIError

def test_parse_error_with_error_key():
    error_response = {'error': 'Invalid request'}
    api_error = ErrorHandler.parse_error(error_response)
    
    assert isinstance(api_error, CoinGeckoAPIError)
    assert 'Invalid request' in api_error.message
    assert api_error.error_response == error_response

def test_parse_error_with_message_key():
    error_response = {'message': 'Resource not found'}
    api_error = ErrorHandler.parse_error(error_response)
    
    assert isinstance(api_error, CoinGeckoAPIError)
    assert 'Resource not found' in api_error.message
    assert api_error.error_response == error_response

def test_parse_error_with_unknown_format():
    error_response = {'status': 404}
    api_error = ErrorHandler.parse_error(error_response)
    
    assert isinstance(api_error, CoinGeckoAPIError)
    assert 'unknown error' in api_error.message.lower()
    assert api_error.error_response == error_response

def test_handle_network_error():
    connection_error = ConnectionError('Connection failed')
    api_error = ErrorHandler.handle_network_error(connection_error)
    
    assert isinstance(api_error, CoinGeckoAPIError)
    assert 'Unable to connect' in api_error.message

def test_coingecko_api_error_attributes():
    error = CoinGeckoAPIError(
        message='Test error', 
        status_code=400, 
        error_response={'error': 'test'}
    )
    
    assert error.message == 'Test error'
    assert error.status_code == 400
    assert error.error_response == {'error': 'test'}