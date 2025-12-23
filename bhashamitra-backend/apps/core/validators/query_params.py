"""Query parameter validation utilities for safe type conversion."""
from typing import Optional, Any


def safe_int(value: Any, default: int = 0, min_val: Optional[int] = None, max_val: Optional[int] = None) -> int:
    """
    Safely convert a value to integer with bounds checking.

    Args:
        value: The value to convert (string, int, or None)
        default: Default value if conversion fails
        min_val: Minimum allowed value (inclusive)
        max_val: Maximum allowed value (inclusive)

    Returns:
        Integer value within bounds, or default if conversion fails

    Examples:
        >>> safe_int("10", default=5)
        10
        >>> safe_int("abc", default=5)
        5
        >>> safe_int("1000", default=10, max_val=100)
        100
        >>> safe_int("-5", default=1, min_val=0)
        0
    """
    if value is None:
        return default

    try:
        result = int(value)
    except (ValueError, TypeError):
        return default

    # Apply bounds
    if min_val is not None and result < min_val:
        result = min_val
    if max_val is not None and result > max_val:
        result = max_val

    return result


def safe_positive_int(value: Any, default: int = 1, max_val: Optional[int] = None) -> int:
    """
    Safely convert a value to a positive integer (>= 1).

    Args:
        value: The value to convert
        default: Default value if conversion fails (must be >= 1)
        max_val: Maximum allowed value

    Returns:
        Positive integer value
    """
    return safe_int(value, default=default, min_val=1, max_val=max_val)


def safe_limit(value: Any, default: int = 10, max_limit: int = 100) -> int:
    """
    Safely convert a limit/pagination parameter with sensible bounds.

    Args:
        value: The limit value from query params
        default: Default limit (typically 10-20)
        max_limit: Maximum allowed limit to prevent DoS

    Returns:
        Integer limit value between 1 and max_limit
    """
    return safe_int(value, default=default, min_val=1, max_val=max_limit)


def safe_level(value: Any, default: int = 1, max_level: int = 10) -> int:
    """
    Safely convert a level parameter (curriculum levels 1-10).

    Args:
        value: The level value from query params
        default: Default level
        max_level: Maximum curriculum level

    Returns:
        Integer level value between 1 and max_level
    """
    return safe_int(value, default=default, min_val=1, max_val=max_level)
