import pytest

from ducklearn.core import safe_average


def test_average_normal_case() -> None:
    assert safe_average([1, 2, 3]) == 2.0


def test_average_empty_list() -> None:
    assert safe_average([]) is None


def test_average_raises_on_non_numeric() -> None:
    with pytest.raises(TypeError):
        safe_average([1, "a"])  # type: ignore[list-item]


def test_average_large_numbers() -> None:
    assert safe_average([1e100, 1e100]) == 1e100


# -----------------------------
# Hypothesis property-based test
# -----------------------------
from hypothesis import given
from hypothesis import strategies as st


@given(st.lists(st.floats(allow_nan=False, allow_infinity=False)))
def test_average_property(values: list[float]) -> None:
    # safe_average never crashes
    result = safe_average(values)
    assert result is None or isinstance(result, float)
