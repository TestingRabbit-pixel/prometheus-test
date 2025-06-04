import pytest
import time
from src.retry import retry, RetryError

def test_retry_successful_function():
    @retry(max_attempts=3)
    def always_succeeds():
        return "Success"
    
    result = always_succeeds()
    assert result == "Success"

def test_retry_fails_after_max_attempts():
    attempts = 0

    @retry(max_attempts=3)
    def always_fails():
        nonlocal attempts
        attempts += 1
        raise ConnectionError("Simulated network error")

    with pytest.raises(RetryError):
        always_fails()
    
    assert attempts == 3

def test_retry_eventually_succeeds():
    attempts = 0

    @retry(max_attempts=3)
    def intermittent_success():
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise ConnectionError("Temporary error")
        return "Final Success"

    result = intermittent_success()
    assert result == "Final Success"
    assert attempts == 3

def test_retry_custom_exception():
    class CustomError(Exception):
        pass

    attempts = 0

    @retry(max_attempts=3, retryable_exceptions=(CustomError,))
    def custom_error_function():
        nonlocal attempts
        attempts += 1
        raise CustomError("Custom error")

    with pytest.raises(RetryError):
        custom_error_function()
    
    assert attempts == 3

def test_retry_backoff_timing():
    import time

    start_time = time.time()
    attempts = 0

    @retry(max_attempts=3, backoff_base=0.1, backoff_multiplier=2.0)
    def slow_function():
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise ConnectionError("Temporary network error")
        return "Success"

    result = slow_function()
    end_time = time.time()

    assert result == "Success"
    assert attempts == 3
    
    # Check if total wait time is reasonable (allow for some variance)
    total_wait = end_time - start_time
    assert total_wait >= 0.2 and total_wait <= 1.0  # More flexible timing