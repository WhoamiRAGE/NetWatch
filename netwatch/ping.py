from ping3 import ping


def get_ping(host="1.1.1.1"):
    result = ping(host, timeout=2)

    if result is None:
        return "Timeout"

    return round(result * 1000, 2)
