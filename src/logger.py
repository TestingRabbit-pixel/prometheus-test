import logging
import os
from typing import Optional, Union

class APILogger:
    """
    A comprehensive logging utility for CoinGecko API interactions.
    
    Provides configurable logging with different log levels and 
    support for console and file logging.
    """
    
    def __init__(
        self, 
        name: str = 'coingecko_api', 
        log_level: Union[str, int] = logging.INFO,
        log_file: Optional[str] = None
    ):
        """
        Initialize a logger with optional file logging.
        
        Args:
            name (str): Name of the logger. Defaults to 'coingecko_api'.
            log_level (Union[str, int]): Logging level. Defaults to INFO.
            log_file (Optional[str]): Path to log file. If None, only console logging.
        """
        # Create logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        
        # Clear existing handlers to prevent duplicates
        self.logger.handlers.clear()
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_format)
        self.logger.addHandler(console_handler)
        
        # File handler (optional)
        if log_file:
            # Ensure directory exists
            os.makedirs(os.path.dirname(log_file) or '.', exist_ok=True)
            
            file_handler = logging.FileHandler(log_file, mode='a')
            file_handler.setLevel(log_level)
            file_format = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
            )
            file_handler.setFormatter(file_format)
            self.logger.addHandler(file_handler)
    
    def debug(self, message: str):
        """Log a debug message."""
        self.logger.debug(message)
    
    def info(self, message: str):
        """Log an info message."""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Log a warning message."""
        self.logger.warning(message)
    
    def error(self, message: str, exc_info: bool = False):
        """
        Log an error message.
        
        Args:
            message (str): Error message
            exc_info (bool): Whether to include exception info. Defaults to False.
        """
        self.logger.error(message, exc_info=exc_info)
    
    def critical(self, message: str, exc_info: bool = False):
        """
        Log a critical message.
        
        Args:
            message (str): Critical message
            exc_info (bool): Whether to include exception info. Defaults to False.
        """
        self.logger.critical(message, exc_info=exc_info)


def get_logger(
    name: str = 'coingecko_api', 
    log_level: Union[str, int] = logging.INFO,
    log_file: Optional[str] = None
) -> APILogger:
    """
    Factory function to create and return a configured logger.
    
    Args:
        name (str): Name of the logger. Defaults to 'coingecko_api'.
        log_level (Union[str, int]): Logging level. Defaults to INFO.
        log_file (Optional[str]): Path to log file. If None, only console logging.
    
    Returns:
        APILogger: Configured logger instance.
    """
    return APILogger(name, log_level, log_file)