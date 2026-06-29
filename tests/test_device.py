from netwatch.device import detect_device


def test_router_by_hostname():
    assert detect_device("HuaweiTe", "_gateway", []) == "Router"


def test_apple_by_vendor():
    assert detect_device("Apple", "unknown", []) == "Apple Device"


def test_xiaomi_by_vendor():
    assert detect_device("XiaomiCo", "unknown", []) == "Xiaomi Device"


def test_windows_by_port():
    assert detect_device("Unknown", "unknown", [445]) == "Windows PC"


def test_linux_by_port():
    assert detect_device("Unknown", "unknown", [22]) == "Linux Device"


def test_unknown_device():
    assert detect_device("Unknown", "unknown", []) == "Unknown"
