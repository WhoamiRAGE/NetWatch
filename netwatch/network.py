import psutil
import time


_last = psutil.net_io_counters()
_last_time = time.time()


def get_network_speed():
    global _last, _last_time

    current = psutil.net_io_counters()
    now = time.time()

    elapsed = now - _last_time

    download = (current.bytes_recv - _last.bytes_recv) / elapsed
    upload = (current.bytes_sent - _last.bytes_sent) / elapsed

    _last = current
    _last_time = now

    return download, upload
