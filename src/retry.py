import time
from functools import wraps
from typing import Callable, Any, Optional, Type

def retry(
    max_attempts: int = 3, 
    delay: float = 1.0, 
    backoff_factor: float = 2.0, 
    exceptions: Optional[Type[Exception]] = None
):
    """
    A decorator that retries a function if it raises an exception.
    
    :param max_attempts: Maximum number of retry attempts
    :param delay: Initial delay between retries in seconds
    :param backoff_factor: Factor to increase delay between retries
    :param exceptions: Exception or tuple of exceptions to catch (defaults to all)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            current_attempt = 0
            current_delay = delay
            
            while current_attempt < max_attempts:
                try:
                    return func(*args, **kwargs)
                except (exceptions or Exception) as e:
                    current_attempt += 1
                    
                    if current_attempt == max_attempts:
                        raise
                    
                    time.sleep(current_delay)
                    current_delay *= backoff_factor
            
            raise RuntimeError("Max retry attempts exceeded")
        
        return wrapper
    
    return decorator