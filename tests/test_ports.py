from netwatch.ports import scan_ports


def test_scan_ports_returns_string():
    result = scan_ports("127.0.0.1")
    assert isinstance(result, str)


def test_scan_ports_format():
    result = scan_ports("127.0.0.1")
    if result != "-":
        for port in result.split(", "):
            assert port.isdigit()
