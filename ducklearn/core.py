"""Core functionality for Ducklearn."""

from collections.abc import Iterable


def safe_average(values: Iterable[float]) -> float | None:  # pragma: no cover
    """
    Compute the average of an iterable of numeric values.

    Args:
        values: An iterable containing numeric items.

    Returns:
        The numeric average of all items, or ``None`` if the iterable is empty.

    Raises:
        TypeError: If any element in the iterable is not a number.

    Examples:
        >>> safe_average([1, 2, 3])
        2.0
        >>> safe_average([])
        None
        >>> safe_average([1, "x"])
        Traceback (most recent call last):
            ...
        TypeError
    """
    values_list = list(values)

    if not values_list:
        return None

    try:
        total = sum(values_list)
    except TypeError as exc:
        raise TypeError("safe_average received a non-numeric value") from exc

    return total / len(values_list)
