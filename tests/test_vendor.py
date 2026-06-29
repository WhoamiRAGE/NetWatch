from netwatch.vendor import get_vendor


def test_unknown_mac():
    assert get_vendor("Unknown") == "Unknown"


def test_empty_mac():
    assert get_vendor("") == "Unknown"


def test_valid_mac():
    result = get_vendor("54:f6:e2:62:8e:e8")
    assert isinstance(result, str)
