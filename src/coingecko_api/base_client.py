import asyncio
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
import aiohttp
import json

logger = logging.getLogger(__name__)

@dataclass
class BaseAPIConfig:
    """Configuration for the CoinGecko API client."""
    base_url: str = "https://api.coingecko.com/api/v3"
    timeout: int = 10
    retries: int = 3
    backoff_factor: float = 0.5

class CoinGeckoBaseClient:
    """Base client for interacting with the CoinGecko API."""

    def __init__(self, config: BaseAPIConfig = BaseAPIConfig()):
        """
        Initialize the CoinGecko base client.

        Args:
            config (BaseAPIConfig, optional): Configuration for the API client. 
                                              Defaults to default BaseAPIConfig.
        """
        self._config = config
        self._session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        """Async context manager entry point."""
        self._session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit point."""
        if self._session:
            await self._session.close()

    async def _request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Make an asynchronous request to the CoinGecko API.

        Args:
            method (str): HTTP method (GET, POST, etc.)
            endpoint (str): API endpoint
            params (dict, optional): Query parameters
            headers (dict, optional): Request headers

        Returns:
            dict: Parsed JSON response

        Raises:
            aiohttp.ClientError: For network-related errors
            json.JSONDecodeError: For JSON parsing errors
        """
        url = f"{self._config.base_url}{endpoint}"
        headers = headers or {}
        params = params or {}

        for attempt in range(self._config.retries):
            try:
                if not self._session:
                    self._session = aiohttp.ClientSession()

                async with self._session.request(
                    method, 
                    url, 
                    params=params, 
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=self._config.timeout)
                ) as response:
                    response.raise_for_status()
                    return await response.json()

            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                logger.warning(f"Request failed (Attempt {attempt + 1}): {e}")
                
                # Exponential backoff
                if attempt < self._config.retries - 1:
                    await asyncio.sleep(self._config.backoff_factor * (2 ** attempt))
                else:
                    raise

    async def close(self):
        """Close the HTTP session."""
        if self._session:
            await self._session.close()
            self._session = None