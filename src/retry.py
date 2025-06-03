import time
import random
from functools import wraps
from typing import Any, Callable, Optional, Tuple, Type

class RetryError(Exception):
    """Exception raised when all retry attempts are exhausted."""
    pass

def retry(
    max_attempts: int = 3, 
    backoff_base: float = 1.0, 
    backoff_multiplier: float = 2.0,
    jitter: float = 0.1, 
    retryable_exceptions: Optional[Tuple[Type[Exception], ...]] = None
) -> Callable:
    """
    A decorator that implements exponential backoff retry mechanism.

    Args:
        max_attempts (int): Maximum number of retry attempts. Defaults to 3.
        backoff_base (float): Base time (in seconds) for initial wait. Defaults to 1.0.
        backoff_multiplier (float): Factor to increase wait time between retries. Defaults to 2.0.
        jitter (float): Random variation to prevent synchronized retries. Defaults to 0.1.
        retryable_exceptions (tuple): Exceptions that trigger a retry. Defaults to None.

    Returns:
        Decorated function with retry capabilities.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            attempts = 0
            default_retryable_exceptions = (
                ConnectionError, 
                TimeoutError, 
                RuntimeError
            )
            
            exceptions_to_retry = retryable_exceptions or default_retryable_exceptions

            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                
                except exceptions_to_retry as e:
                    attempts += 1
                    
                    # Exit if max attempts reached
                    if attempts >= max_attempts:
                        raise RetryError(f"Function {func.__name__} failed after {max_attempts} attempts") from e
                    
                    # Calculate exponential backoff with jitter
                    wait_time = backoff_base * (backoff_multiplier ** attempts)
                    jittered_wait = wait_time * (1 + random.uniform(-jitter, jitter))
                    
                    print(f"Retry {attempts}/{max_attempts} for {func.__name__}. Waiting {jittered_wait:.2f} seconds.")
                    time.sleep(jittered_wait)
        
        return wrapper
    return decorator