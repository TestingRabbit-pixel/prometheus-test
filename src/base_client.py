import logging
import requests
from typing import Dict, Any, Optional

class BaseAPIClient:
    """
    Base API client for making HTTP requests with robust error handling and logging.
    
    This class provides a standardized interface for making API requests with 
    comprehensive logging and error management.
    """
    
    def __init__(
        self, 
        base_url: str, 
        timeout: int = 10, 
        log_level: int = logging.INFO
    ):
        """
        Initialize the base API client.
        
        Args:
            base_url (str): Base URL for the API
            timeout (int, optional): Request timeout in seconds. Defaults to 10.
            log_level (int, optional): Logging level. Defaults to logging.INFO.
        """
        self.base_url = base_url
        self.timeout = timeout
        
        # Configure logging
        logging.basicConfig(
            level=log_level, 
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Make an HTTP request with robust error handling and logging.
        
        Args:
            method (str): HTTP method (GET, POST, etc.)
            endpoint (str): API endpoint
            params (dict, optional): Query parameters
            headers (dict, optional): Request headers
        
        Returns:
            dict: Parsed JSON response
        
        Raises:
            ValueError: For invalid method
            RuntimeError: For network or API errors
        """
        url = f"{self.base_url}/{endpoint}"
        
        # Default headers
        request_headers = headers or {}
        request_headers.setdefault('Accept', 'application/json')
        
        # Log request details
        self.logger.info(f"Sending {method} request to {url}")
        if params:
            self.logger.debug(f"Request params: {params}")
        
        try:
            response = requests.request(
                method=method.upper(), 
                url=url, 
                params=params, 
                headers=request_headers,
                timeout=self.timeout
            )
            
            # Raise an exception for HTTP errors
            response.raise_for_status()
            
            # Log successful response
            self.logger.info(f"Received {response.status_code} response")
            
            return response.json()
        
        except requests.exceptions.Timeout:
            self.logger.error(f"Request to {url} timed out")
            raise RuntimeError(f"Request to {url} timed out after {self.timeout} seconds")
        
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP error occurred: {e}")
            raise RuntimeError(f"HTTP error: {e}")
        
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Network error occurred: {e}")
            raise RuntimeError(f"Network error: {e}")
        
        except ValueError as e:
            self.logger.error(f"JSON parsing error: {e}")
            raise RuntimeError(f"Could not parse response: {e}")