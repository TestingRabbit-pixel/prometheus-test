import pytest
import time
from src.retry import retry

def test_retry_successful_function():
    @retry(max_attempts=3)
    def always_succeeds():
        return True
    
    assert always_succeeds() is True

def test_retry_fails_after_max_attempts():
    attempts = 0
    
    @retry(max_attempts=3)
    def always_fails():
        nonlocal attempts
        attempts += 1
        raise ValueError("Always fails")
    
    with pytest.raises(ValueError):
        always_fails()
    
    assert attempts == 3

def test_retry_eventually_succeeds():
    attempts = 0
    
    @retry(max_attempts=3)
    def flaky_function():
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise RuntimeError("Not yet successful")
        return True
    
    assert flaky_function() is True
    assert attempts == 3

def test_retry_custom_exception():
    @retry(max_attempts=3, exceptions=ValueError)
    def custom_exception_function():
        raise ValueError("Custom exception")
    
    with pytest.raises(ValueError):
        custom_exception_function()

def test_retry_backoff_timing():
    start_time = time.time()
    attempts = 0
    
    @retry(max_attempts=3, delay=0.1, backoff_factor=2.0)
    def timing_function():
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise RuntimeError("Not yet successful")
        return True
    
    timing_function()
    
    end_time = time.time()
    total_delay = 0.1 + 0.2  # First two retry delays
    
    assert attempts == 3
    assert end_time - start_time >= total_delay