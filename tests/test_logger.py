import logging
import os
import pytest
import tempfile
from src.logger import get_logger, APILogger

def test_logger_creation():
    """Test basic logger creation."""
    logger = get_logger()
    assert isinstance(logger, APILogger)
    assert logger.logger.name == 'coingecko_api'
    assert logger.logger.level == logging.INFO

def test_logger_with_file():
    """Test logger with file logging."""
    with tempfile.TemporaryDirectory() as tmpdir:
        log_file = os.path.join(tmpdir, 'test.log')
        logger = get_logger(log_file=log_file)
        
        # Log some messages
        logger.info("Test info message")
        logger.error("Test error message")
        
        # Check file exists and has content
        assert os.path.exists(log_file)
        with open(log_file, 'r') as f:
            log_content = f.read()
            assert "Test info message" in log_content
            assert "Test error message" in log_content

def test_logger_log_levels():
    """Test different log levels."""
    logger = get_logger(log_level=logging.DEBUG)
    assert logger.logger.level == logging.DEBUG

def test_logger_methods():
    """Test all logging methods."""
    logger = get_logger()
    
    # These are smoke tests to ensure methods don't raise exceptions
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")

def test_multiple_handlers():
    """Ensure no duplicate handlers are added."""
    logger1 = get_logger()
    logger2 = get_logger()
    
    # Both should refer to the same logger instance
    assert len(logger1.logger.handlers) == len(logger2.logger.handlers)