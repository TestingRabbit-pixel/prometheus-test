import pytest
import requests_mock
from src.base_client import BaseAPIClient

def test_base_client_initialization():
    """Test BaseAPIClient initialization."""
    base_url = "https://api.example.com"
    client = BaseAPIClient(base_url)
    
    assert client.base_url == base_url
    assert client.timeout == 10
    assert client.logger is not None

def test_successful_get_request():
    """Test a successful GET request."""
    base_url = "https://api.example.com"
    client = BaseAPIClient(base_url)
    
    with requests_mock.Mocker() as m:
        mock_response = {"data": "test"}
        m.get(f"{base_url}/test_endpoint", json=mock_response, status_code=200)
        
        result = client._make_request("GET", "test_endpoint")
        assert result == mock_response

def test_request_timeout():
    """Test request timeout handling."""
    base_url = "https://api.example.com"
    client = BaseAPIClient(base_url, timeout=1)
    
    with requests_mock.Mocker() as m:
        m.get(f"{base_url}/timeout_endpoint", exc=requests.exceptions.Timeout)
        
        with pytest.raises(RuntimeError, match="timed out"):
            client._make_request("GET", "timeout_endpoint")

def test_http_error_handling():
    """Test HTTP error handling."""
    base_url = "https://api.example.com"
    client = BaseAPIClient(base_url)
    
    with requests_mock.Mocker() as m:
        m.get(f"{base_url}/error_endpoint", status_code=404)
        
        with pytest.raises(RuntimeError, match="HTTP error"):
            client._make_request("GET", "error_endpoint")

def test_request_with_params():
    """Test request with query parameters."""
    base_url = "https://api.example.com"
    client = BaseAPIClient(base_url)
    
    with requests_mock.Mocker() as m:
        mock_response = {"data": "test"}
        m.get(f"{base_url}/params_endpoint", json=mock_response, status_code=200)
        
        result = client._make_request("GET", "params_endpoint", params={"key": "value"})
        assert result == mock_response