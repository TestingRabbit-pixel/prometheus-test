import unittest
from datetime import datetime, timedelta
from src.historical_price_transformer import HistoricalPriceTransformer

class TestHistoricalPriceTransformer(unittest.TestCase):
    def setUp(self):
        # Sample historical price data
        self.sample_data = [
            [1609459200000, 29000.50],  # Jan 1, 2021
            [1612137600000, 33000.75],  # Feb 1, 2021
            [1614556800000, 48000.25],  # Mar 1, 2021
            [1617235200000, 58000.00]   # Apr 1, 2021
        ]

    def test_validate_historical_data_valid(self):
        """Test validation of valid historical price data"""
        self.assertTrue(HistoricalPriceTransformer.validate_historical_data(self.sample_data))

    def test_validate_historical_data_invalid(self):
        """Test validation of invalid historical price data"""
        invalid_data = [
            [None, 29000.50],  # Invalid timestamp
            ['2021-01-01', 33000.75],  # Wrong timestamp type
            [1612137600000, -100]  # Negative price
        ]
        self.assertFalse(HistoricalPriceTransformer.validate_historical_data(invalid_data))

    def test_transform_historical_data(self):
        """Test transformation of historical price data"""
        transformed_data = HistoricalPriceTransformer.transform_historical_data(self.sample_data)
        
        self.assertEqual(len(transformed_data), len(self.sample_data))
        
        for point, original_point in zip(transformed_data, self.sample_data):
            self.assertIn('timestamp', point)
            self.assertIn('datetime', point)
            self.assertIn('price', point)
            
            self.assertEqual(point['timestamp'], original_point[0])
            self.assertEqual(point['price'], original_point[1])
            
            # Check datetime is correctly formatted
            self.assertIsNotNone(datetime.fromisoformat(point['datetime']))

    def test_filter_historical_data(self):
        """Test filtering of historical price data"""
        transformed_data = HistoricalPriceTransformer.transform_historical_data(self.sample_data)
        
        # Filter by date range (strict filtering)
        start_date = datetime(2021, 2, 1)
        end_date = datetime(2021, 4, 1)
        filtered_data = HistoricalPriceTransformer.filter_historical_data(
            transformed_data, 
            start_date=start_date, 
            end_date=end_date
        )
        self.assertEqual(len(filtered_data), 1)  # Only Mar 1st point is strictly between Feb and Apr

        # Filter by price range
        price_filtered_data = HistoricalPriceTransformer.filter_historical_data(
            transformed_data, 
            min_price=40000, 
            max_price=60000
        )
        self.assertEqual(len(price_filtered_data), 2)  # Two points in this price range

if __name__ == '__main__':
    unittest.main()