import time
from functools import wraps

def timer(func):
    """Decorator for timing functions."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

def validate_year(func):
    """Decorator for validating the year."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        year = kwargs.get("year") if "year" in kwargs else args[3]

        if not isinstance(year, int) or not (1000 <= year <= 2025):
            raise ValueError(f"year must be an integer between 1000 and 2025, got {year}")

        return func(*args, **kwargs)
    return wrapper

def log_access(func):
    """Decorator for logging access."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        print(f"[LOG] catalogue() called in {self.title}")
        return func(*args, **kwargs)
    return wrapper

def singleton(cls):
    """Decorator for singleton class."""
    instances = {}
    @wraps(cls)
    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper