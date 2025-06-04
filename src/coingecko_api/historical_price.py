from typing import Dict, List, Optional
from datetime import datetime, timedelta
import requests

class CoinGeckoHistoricalPriceClient:
    """
    A client for retrieving historical cryptocurrency price data from CoinGecko API.

    Attributes:
        base_url (str): Base URL for CoinGecko API
    """
    def __init__(self, base_url: str = 'https://api.coingecko.com/api/v3'):
        self.base_url = base_url

    def get_historical_prices(
        self, 
        coin_id: str, 
        currency: str = 'usd', 
        days: int = 30, 
        interval: Optional[str] = None
    ) -> List[Dict[str, float]]:
        """
        Retrieve historical price data for a specific cryptocurrency.

        Args:
            coin_id (str): CoinGecko ID of the cryptocurrency
            currency (str, optional): Target currency. Defaults to 'usd'
            days (int, optional): Number of historical days to retrieve. Defaults to 30
            interval (str, optional): Data interval (daily, hourly). Defaults to None

        Returns:
            List[Dict[str, float]]: Historical price data points

        Raises:
            ValueError: If invalid parameters are provided
            requests.RequestException: If there's an API request error
        """
        if days < 1:
            raise ValueError("Days must be a positive integer")

        # Validate coin_id and currency
        if not coin_id or not currency:
            raise ValueError("Coin ID and currency must be provided")

        # Construct the API endpoint
        endpoint = f'{self.base_url}/coins/{coin_id}/market_chart'
        params = {
            'vs_currency': currency,
            'days': days
        }

        # Add interval if specified
        if interval:
            if interval not in ['daily', 'hourly']:
                raise ValueError("Interval must be 'daily' or 'hourly'")
            params['interval'] = interval

        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()

            # Extract price data (timestamp, price)
            historical_prices = [
                {'timestamp': point[0], 'price': point[1]} 
                for point in data.get('prices', [])
            ]

            return historical_prices

        except requests.RequestException as e:
            raise RuntimeError(f'Error fetching historical prices: {e}')

    def get_price_on_date(
        self, 
        coin_id: str, 
        date: datetime, 
        currency: str = 'usd'
    ) -> Optional[float]:
        """
        Get the price of a cryptocurrency on a specific date.

        Args:
            coin_id (str): CoinGecko ID of the cryptocurrency
            date (datetime): Target date for price retrieval
            currency (str, optional): Target currency. Defaults to 'usd'

        Returns:
            Optional[float]: Price on the specified date, or None if not found
        """
        # Validate inputs
        if not coin_id or not date or not currency:
            raise ValueError("Coin ID, date, and currency must be provided")

        # Calculate days ago
        days_ago = (datetime.now() - date).days

        try:
            historical_prices = self.get_historical_prices(
                coin_id, 
                currency=currency, 
                days=days_ago + 1
            )

            # Find the closest price point to the specified date
            for price_data in historical_prices:
                price_date = datetime.fromtimestamp(price_data['timestamp'] / 1000)
                if price_date.date() == date.date():
                    return price_data['price']

            return None

        except Exception as e:
            raise RuntimeError(f'Error retrieving price for date: {e}')