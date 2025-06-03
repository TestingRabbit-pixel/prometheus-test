import requests
from typing import Dict, Union, List
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class PriceResponse:
    """Dataclass to represent cryptocurrency price data."""
    symbol: str
    price: float
    last_updated: str

class CoinGeckoClient:
    """A client for interacting with the CoinGecko API for cryptocurrency prices."""

    BASE_URL = "https://api.coingecko.com/api/v3"

    def __init__(self, timeout: int = 10):
        """
        Initialize the CoinGecko API client.

        Args:
            timeout (int): Request timeout in seconds. Defaults to 10.
        """
        self.timeout = timeout

    def get_simple_price(
        self, 
        ids: List[str], 
        vs_currencies: List[str] = ['usd']
    ) -> Dict[str, Dict[str, Union[float, str]]]:
        """
        Retrieve current prices for specified cryptocurrencies.

        Args:
            ids (List[str]): List of coin ids (e.g., ['bitcoin', 'ethereum'])
            vs_currencies (List[str]): List of target currencies. Defaults to USD.

        Returns:
            Dict of price data for requested cryptocurrencies.

        Raises:
            ValueError: If no ids are provided
            RuntimeError: If API request fails
        """
        if not ids:
            raise ValueError("At least one cryptocurrency id must be provided")

        try:
            params = {
                'ids': ','.join(ids),
                'vs_currencies': ','.join(vs_currencies),
                'include_last_updated_at': 'true'
            }

            response = requests.get(
                f"{self.BASE_URL}/simple/price", 
                params=params, 
                timeout=self.timeout
            )
            response.raise_for_status()

            return response.json()

        except requests.RequestException as e:
            logger.error(f"CoinGecko API request failed: {e}")
            raise RuntimeError(f"Failed to fetch prices: {e}")

    def parse_price_response(
        self, 
        response: Dict[str, Dict[str, Union[float, str]]], 
        target_currency: str = 'usd'
    ) -> List[PriceResponse]:
        """
        Parse price response into structured PriceResponse objects.

        Args:
            response (Dict): Raw price response from get_simple_price
            target_currency (str): Target currency for price conversion. Defaults to USD.

        Returns:
            List of PriceResponse objects
        """
        results = []
        for symbol, data in response.items():
            try:
                price = data.get(target_currency)
                last_updated = data.get('last_updated_at')
                
                if price is not None and last_updated is not None:
                    results.append(PriceResponse(
                        symbol=symbol, 
                        price=float(price), 
                        last_updated=str(last_updated)
                    ))
            except (KeyError, ValueError) as e:
                logger.warning(f"Could not parse price for {symbol}: {e}")

        return results