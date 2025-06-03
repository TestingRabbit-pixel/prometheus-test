import pytest
from datetime import datetime, timedelta
from src.historical_price_transformer import HistoricalPriceTransformer

def test_validate_historical_data_valid():
    """Test validation of valid historical price data."""
    valid_data = [
        [1609459200000, 29000.50],
        [1609545600000, 29500.75],
        [1609632000000, 30000.25]
    ]
    assert HistoricalPriceTransformer.validate_historical_data(valid_data) is True

def test_validate_historical_data_invalid_structure():
    """Test validation of data with invalid structure."""
    invalid_data_1 = [1, 2, 3]  # Not a list of lists
    invalid_data_2 = [[1609459200000]]  # Incomplete data point
    invalid_data_3 = [[1609459200000, 'price']]  # Invalid price type
    
    assert HistoricalPriceTransformer.validate_historical_data(invalid_data_1) is False
    assert HistoricalPriceTransformer.validate_historical_data(invalid_data_2) is False
    assert HistoricalPriceTransformer.validate_historical_data(invalid_data_3) is False

def test_transform_historical_data():
    """Test transformation of historical price data."""
    input_data = [
        [1609459200000, 29000.50],
        [1609545600000, 29500.75]
    ]
    
    transformed_data = HistoricalPriceTransformer.transform_historical_data(input_data)
    
    assert len(transformed_data) == 2
    assert all('timestamp' in point and 'datetime' in point and 'price' in point for point in transformed_data)
    assert transformed_data[0]['price'] == 29000.50
    assert transformed_data[0]['timestamp'] == 1609459200000

def test_transform_historical_data_invalid():
    """Test transformation with invalid data raises ValueError."""
    invalid_data = [[1, 'invalid']]
    
    with pytest.raises(ValueError):
        HistoricalPriceTransformer.transform_historical_data(invalid_data)

def test_filter_historical_data():
    """Test filtering of historical price data."""
    input_data = [
        {'timestamp': 1609459200000, 'datetime': '2021-01-01T00:00:00', 'price': 29000.50},
        {'timestamp': 1609545600000, 'datetime': '2021-01-02T00:00:00', 'price': 29500.75},
        {'timestamp': 1609632000000, 'datetime': '2021-01-03T00:00:00', 'price': 30000.25}
    ]
    
    # Filter by date range
    start_date = datetime(2021, 1, 2)
    end_date = datetime(2021, 1, 3)
    filtered_by_date = HistoricalPriceTransformer.filter_historical_data(
        input_data, 
        start_date=start_date, 
        end_date=end_date
    )
    assert len(filtered_by_date) == 2
    
    # Filter by price range
    filtered_by_price = HistoricalPriceTransformer.filter_historical_data(
        input_data, 
        min_price=29250, 
        max_price=30100
    )
    
    # Debug print
    print("Filtered by price:", [point['price'] for point in filtered_by_price])
    
    assert len(filtered_by_price) == 2
    assert all(29250 <= point['price'] <= 30100 for point in filtered_by_price)

def test_filter_historical_data_no_filter():
    """Test filtering with no filter criteria returns all data."""
    input_data = [
        {'timestamp': 1609459200000, 'datetime': '2021-01-01T00:00:00', 'price': 29000.50},
        {'timestamp': 1609545600000, 'datetime': '2021-01-02T00:00:00', 'price': 29500.75}
    ]
    
    filtered_data = HistoricalPriceTransformer.filter_historical_data(input_data)
    assert len(filtered_data) == len(input_data)