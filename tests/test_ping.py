import pytest
from netwatch.ping import get_ping


def test_get_ping_returns_value():
    try:
        result = get_ping()
        assert result == "Timeout" or isinstance(result, float)
    except PermissionError:
        pytest.skip("Raw socket requires root")


def test_get_ping_positive():
    try:
        result = get_ping()
        if isinstance(result, float):
            assert result > 0
    except PermissionError:
        pytest.skip("Raw socket requires root")
