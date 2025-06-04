import time
import pytest
from src.retry import retry, RetryError

def test_retry_successful_function():
    @retry(max_attempts=3)
    def always_succeeds():
        return "Success"
    
    assert always_succeeds() == "Success"

def test_retry_fails_after_max_attempts():
    attempts = 0
    
    @retry(max_attempts=3)
    def always_fails():
        nonlocal attempts
        attempts += 1
        raise ConnectionError("Connection failed")
    
    with pytest.raises(RetryError):
        always_fails()
    
    assert attempts == 3

def test_retry_eventually_succeeds():
    attempts = 0
    
    @retry(max_attempts=3)
    def flaky_function():
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise ConnectionError("Temporary failure")
        return "Success"
    
    assert flaky_function() == "Success"
    assert attempts == 3

def test_retry_custom_exception():
    class CustomError(Exception):
        pass
    
    @retry(retryable_exceptions=(CustomError,))
    def function_with_custom_error():
        raise CustomError("Custom error")
    
    with pytest.raises(RetryError):
        function_with_custom_error()

def test_retry_backoff_timing():
    attempts = 0
    start_time = time.time()
    
    @retry(max_attempts=3, backoff_base=0.1, backoff_multiplier=2.0, jitter=0.1)
    def backoff_function():
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise ConnectionError("Retry me")
        return "Success"
    
    result = backoff_function()
    
    end_time = time.time()
    total_wait_time = end_time - start_time
    
    assert result == "Success"
    assert attempts == 3
    
    # Check that total wait time is reasonable (between theoretical min and max)
    # Theoretical wait times: 0.1 * (2^1 * (1 ± 0.1)), 0.1 * (2^2 * (1 ± 0.1))
    assert total_wait_time > 0.2  # Minimum expected wait time
    assert total_wait_time < 1.0  # Maximum expected wait time