from netwatch.network import get_network_speed


def test_get_network_speed():
    download, upload = get_network_speed()
    assert isinstance(download, float)
    assert isinstance(upload, float)
    assert download >= 0
    assert upload >= 0
