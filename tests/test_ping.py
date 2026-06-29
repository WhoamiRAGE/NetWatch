from netwatch.ping import get_ping


def test_get_ping_returns_value():
    result = get_ping()
    assert result == "Timeout" or isinstance(result, float)


def test_get_ping_positive():
    result = get_ping()
    if isinstance(result, float):
        assert result > 0
