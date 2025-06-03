from datetime import datetime, timedelta
from dateutil.parser import parse
from typing import Union, Optional, Tuple

class DateRangeValidationError(ValueError):
    """Custom exception for date range validation errors."""
    pass

class DateRangeValidator:
    """
    Validates date ranges for historical price data retrieval.
    
    Ensures that date inputs are valid, within acceptable ranges, 
    and adhere to CoinGecko API constraints.
    """
    
    # Maximum historical data retrieval period (currently 365 days)
    MAX_HISTORICAL_DAYS = 365
    
    @classmethod
    def validate_date_range(
        cls, 
        start_date: Union[str, datetime], 
        end_date: Union[str, datetime]
    ) -> Tuple[datetime, datetime]:
        """
        Validate and normalize date range for historical price retrieval.
        
        Args:
            start_date: Start date of the historical price range
            end_date: End date of the historical price range
        
        Returns:
            Tuple of validated and normalized start and end datetimes
        
        Raises:
            DateRangeValidationError: If date range is invalid
        """
        # Convert inputs to datetime if they are strings
        start = cls._parse_date(start_date)
        end = cls._parse_date(end_date)
        
        # Validate chronological order
        if start > end:
            raise DateRangeValidationError("Start date must be before or equal to end date")
        
        # Check maximum historical period
        if (end - start).days > cls.MAX_HISTORICAL_DAYS:
            raise DateRangeValidationError(
                f"Historical data range cannot exceed {cls.MAX_HISTORICAL_DAYS} days"
            )
        
        # Prevent future dates
        now = datetime.now()
        if end > now or start > now:
            raise DateRangeValidationError("Dates cannot be in the future")
        
        return start, end
    
    @classmethod
    def _parse_date(cls, date: Union[str, datetime]) -> datetime:
        """
        Parse and validate individual date input.
        
        Args:
            date: Date to parse (string or datetime)
        
        Returns:
            Validated datetime object
        
        Raises:
            DateRangeValidationError: If date is invalid
        """
        if isinstance(date, datetime):
            return date.replace(hour=0, minute=0, second=0, microsecond=0)
        
        try:
            parsed_date = parse(date)
            return parsed_date.replace(hour=0, minute=0, second=0, microsecond=0)
        except (TypeError, ValueError) as e:
            raise DateRangeValidationError(f"Invalid date format: {date}") from e