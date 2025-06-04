from typing import List, Dict, Union
from enum import Enum
import requests
from datetime import datetime, timedelta

class TimeGranularity(Enum):
    """Enum representing supported time granularities for historical price data."""
    DAILY = 'daily'
    HOURLY = 'hourly'

class HistoricalPriceService:
    """Service for retrieving historical cryptocurrency price data."""

    def __init__(self, base_url: str = 'https://api.coingecko.com/api/v3'):
        """
        Initialize the HistoricalPriceService.

        :param base_url: Base URL for CoinGecko API
        """
        self.base_url = base_url

    def get_historical_prices(
        self, 
        coin_id: str, 
        currency: str, 
        days: int, 
        granularity: TimeGranularity = TimeGranularity.DAILY
    ) -> List[Dict[str, Union[int, float]]]:
        """
        Retrieve historical prices for a specific cryptocurrency.

        :param coin_id: ID of the cryptocurrency
        :param currency: Target currency for price conversion
        :param days: Number of days of historical data to retrieve
        :param granularity: Time granularity of price data
        :return: List of historical price data points
        :raises ValueError: If invalid parameters are provided
        :raises requests.RequestException: For network or API errors
        """
        # Validate input parameters
        if not coin_id or not currency:
            raise ValueError("Coin ID and currency must be provided")
        
        if days <= 0:
            raise ValueError("Days must be a positive integer")

        # Construct API endpoint based on granularity
        endpoint = f"{self.base_url}/coins/{coin_id}/market_chart"
        
        params = {
            'vs_currency': currency,
            'days': days,
            'interval': granularity.value
        }

        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()  # Raise an exception for bad status codes
            
            data = response.json()
            
            # Process and return prices based on the endpoint response
            prices = data.get('prices', [])
            return [
                {
                    'timestamp': int(price[0] / 1000),  # Convert milliseconds to seconds
                    'price': price[1]
                } for price in prices
            ]
        
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to retrieve historical prices: {str(e)}")