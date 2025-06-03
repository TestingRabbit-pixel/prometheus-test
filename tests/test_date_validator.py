import pytest
from datetime import datetime, timedelta
from src.date_validator import DateRangeValidator, DateRangeValidationError

class TestDateRangeValidator:
    def test_valid_date_range(self):
        """Test valid date range scenarios"""
        # Using datetime objects
        now = datetime.now()
        start = now - timedelta(days=30)
        end = now
        
        start_validated, end_validated = DateRangeValidator.validate_date_range(start, end)
        assert start_validated == start.replace(hour=0, minute=0, second=0, microsecond=0)
        assert end_validated == end.replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Using date strings
        start_str = "2023-01-01"
        end_str = "2023-02-01"
        
        start_validated, end_validated = DateRangeValidator.validate_date_range(start_str, end_str)
        assert start_validated == datetime(2023, 1, 1)
        assert end_validated == datetime(2023, 2, 1)
    
    def test_future_date_error(self):
        """Test that future dates raise an error"""
        now = datetime.now()
        future_start = now + timedelta(days=1)
        future_end = now + timedelta(days=2)
        
        with pytest.raises(DateRangeValidationError, match="Dates cannot be in the future"):
            DateRangeValidator.validate_date_range(future_start, future_end)
    
    def test_invalid_date_order(self):
        """Test that end date before start date raises an error"""
        now = datetime.now()
        start = now
        end = now - timedelta(days=1)
        
        with pytest.raises(DateRangeValidationError, match="Start date must be before or equal to end date"):
            DateRangeValidator.validate_date_range(start, end)
    
    def test_excessive_date_range(self):
        """Test that date range exceeding max historical period raises an error"""
        now = datetime.now()
        start = now - timedelta(days=366)
        end = now
        
        with pytest.raises(DateRangeValidationError, match="Historical data range cannot exceed 365 days"):
            DateRangeValidator.validate_date_range(start, end)
    
    def test_invalid_date_format(self):
        """Test that invalid date formats raise an error"""
        with pytest.raises(DateRangeValidationError, match="Invalid date format"):
            DateRangeValidator.validate_date_range("invalid_date", datetime.now())
    
    def test_exact_max_range(self):
        """Test that the maximum allowed historical range works"""
        now = datetime.now()
        start = now - timedelta(days=365)
        
        start_validated, end_validated = DateRangeValidator.validate_date_range(start, now)
        assert (end_validated - start_validated).days <= 365