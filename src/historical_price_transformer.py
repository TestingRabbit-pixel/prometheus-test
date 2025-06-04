from typing import Dict, List, Union, Optional
from datetime import datetime
import logging

class HistoricalPriceTransformer:
    """
    Transforms and validates historical price data from CoinGecko API.
    
    Handles data validation, cleaning, and transformation of historical 
    cryptocurrency price data.
    """
    
    @staticmethod
    def validate_historical_data(data: List[List[Union[int, float]]]) -> bool:
        """
        Validate the structure and content of historical price data.
        
        Args:
            data (List[List[Union[int, float]]]): Raw historical price data
        
        Returns:
            bool: True if data is valid, False otherwise
        """
        if not isinstance(data, list):
            logging.error("Historical data must be a list")
            return False
        
        # Check each data point
        for point in data:
            if not isinstance(point, list) or len(point) != 2:
                logging.error(f"Invalid data point format: {point}")
                return False
            
            timestamp, price = point
            
            # Validate timestamp
            try:
                datetime.fromtimestamp(timestamp / 1000)  # Convert milliseconds to seconds
            except (TypeError, ValueError):
                logging.error(f"Invalid timestamp: {timestamp}")
                return False
            
            # Validate price
            if not isinstance(price, (int, float)) or price < 0:
                logging.error(f"Invalid price: {price}")
                return False
        
        return True
    
    @staticmethod
    def transform_historical_data(data: List[List[Union[int, float]]]) -> List[Dict[str, Union[int, float]]]:
        """
        Transform historical price data into a more usable format.
        
        Args:
            data (List[List[Union[int, float]]]): Raw historical price data
        
        Returns:
            List[Dict[str, Union[int, float]]]: Transformed historical price data
        
        Raises:
            ValueError: If input data is invalid
        """
        if not HistoricalPriceTransformer.validate_historical_data(data):
            raise ValueError("Invalid historical price data")
        
        transformed_data = []
        for point in data:
            timestamp, price = point
            transformed_point = {
                'timestamp': timestamp,
                'datetime': datetime.fromtimestamp(timestamp / 1000).isoformat(),
                'price': price
            }
            transformed_data.append(transformed_point)
        
        return transformed_data
    
    @staticmethod
    def filter_historical_data(
        data: List[Dict[str, Union[int, float]]],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None
    ) -> List[Dict[str, Union[int, float]]]:
        """
        Filter historical price data based on optional criteria.
        
        Args:
            data (List[Dict[str, Union[int, float]]]): Transformed historical price data
            start_date (Optional[datetime]): Minimum date for filtering
            end_date (Optional[datetime]): Maximum date for filtering
            min_price (Optional[float]): Minimum price for filtering
            max_price (Optional[float]): Maximum price for filtering
        
        Returns:
            List[Dict[str, Union[int, float]]]: Filtered historical price data
        """
        def meets_filter_criteria(point):
            point_datetime = datetime.fromisoformat(point['datetime'])
            
            # Check date range
            if start_date and point_datetime < start_date:
                return False
            
            if end_date and point_datetime > end_date:
                return False
            
            # Check price range
            if min_price is not None and point['price'] < min_price:
                return False
            
            if max_price is not None and point['price'] > max_price:
                return False
            
            return True
        
        return [point for point in data if meets_filter_criteria(point)]