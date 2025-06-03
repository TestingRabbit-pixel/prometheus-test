from typing import Dict, Any, Optional
import os
import re

class ConfigValidationError(Exception):
    """Custom exception for configuration validation errors."""
    pass

class CoinGeckoConfigValidator:
    """Validates CoinGecko API configuration settings."""

    @staticmethod
    def validate_config(config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and sanitize the configuration dictionary.
        
        Args:
            config (Dict[str, Any]): Configuration dictionary to validate
        
        Returns:
            Dict[str, Any]: Validated and sanitized configuration
        
        Raises:
            ConfigValidationError: If configuration is invalid
        """
        # Validate presence of required keys
        required_keys = ['API_BASE_URL', 'API_KEY']
        for key in required_keys:
            if key not in config or not config[key]:
                raise ConfigValidationError(f"Missing required configuration key: {key}")
        
        # Validate API base URL format
        CoinGeckoConfigValidator._validate_url(config['API_BASE_URL'])
        
        # Validate API key (if applicable)
        if config.get('API_KEY'):
            CoinGeckoConfigValidator._validate_api_key(config['API_KEY'])
        
        # Validate optional timeout
        if 'REQUEST_TIMEOUT' in config:
            CoinGeckoConfigValidator._validate_timeout(config['REQUEST_TIMEOUT'])
        
        # Validate rate limit settings
        if 'RATE_LIMIT' in config:
            CoinGeckoConfigValidator._validate_rate_limit(config['RATE_LIMIT'])
        
        return config

    @staticmethod
    def _validate_url(url: str) -> None:
        """
        Validate URL format.
        
        Args:
            url (str): URL to validate
        
        Raises:
            ConfigValidationError: If URL is invalid
        """
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        if not url_pattern.match(url):
            raise ConfigValidationError(f"Invalid URL format: {url}")

    @staticmethod
    def _validate_api_key(api_key: Optional[str]) -> None:
        """
        Validate API key format.
        
        Args:
            api_key (Optional[str]): API key to validate
        
        Raises:
            ConfigValidationError: If API key is invalid
        """
        if not api_key:
            return
        
        # Remove whitespace and validate minimum length
        sanitized_key = api_key.strip()
        if len(sanitized_key) < 10:
            raise ConfigValidationError("API key is too short")

    @staticmethod
    def _validate_timeout(timeout: Any) -> None:
        """
        Validate request timeout.
        
        Args:
            timeout (Any): Timeout value to validate
        
        Raises:
            ConfigValidationError: If timeout is invalid
        """
        try:
            timeout_float = float(timeout)
            if timeout_float <= 0 or timeout_float > 120:  # Reasonable timeout range
                raise ConfigValidationError(f"Invalid timeout value: {timeout}")
        except (TypeError, ValueError):
            raise ConfigValidationError(f"Timeout must be a numeric value, got {type(timeout)}")

    @staticmethod
    def _validate_rate_limit(rate_limit: Any) -> None:
        """
        Validate rate limit settings.
        
        Args:
            rate_limit (Any): Rate limit configuration to validate
        
        Raises:
            ConfigValidationError: If rate limit is invalid
        """
        try:
            limit_float = float(rate_limit)
            if limit_float <= 0 or limit_float > 100:  # Reasonable rate limit range
                raise ConfigValidationError(f"Invalid rate limit value: {rate_limit}")
        except (TypeError, ValueError):
            raise ConfigValidationError(f"Rate limit must be a numeric value, got {type(rate_limit)}")

    @classmethod
    def load_from_env(cls) -> Dict[str, Any]:
        """
        Load configuration from environment variables.
        
        Returns:
            Dict[str, Any]: Validated configuration from environment
        """
        config = {
            'API_BASE_URL': os.getenv('COINGECKO_API_BASE_URL', 'https://api.coingecko.com/api/v3'),
            'API_KEY': os.getenv('COINGECKO_API_KEY', ''),
            'REQUEST_TIMEOUT': os.getenv('COINGECKO_REQUEST_TIMEOUT', 30),
            'RATE_LIMIT': os.getenv('COINGECKO_RATE_LIMIT', 50)
        }
        
        return cls.validate_config(config)