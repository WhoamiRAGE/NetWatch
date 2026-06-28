import psutil
import time


def get_interfaces():
    stats = psutil.net_if_stats()
    return [iface for iface, s in stats.items() if s.isup and iface != "lo"]


def measure_bandwidth(iface, interval=1.0):
    counters = psutil.net_io_counters(pernic=True)

    if iface not in counters:
        return None

    before = counters[iface]
    time.sleep(interval)
    after = psutil.net_io_counters(pernic=True)[iface]

    rx = (after.bytes_recv - before.bytes_recv) / interval
    tx = (after.bytes_sent - before.bytes_sent) / interval
    rx_pkts = after.packets_recv - before.packets_recv
    tx_pkts = after.packets_sent - before.packets_sent
    errors = (after.errin + after.errout) - (before.errin + before.errout)
    drops = (after.dropin + after.dropout) - (before.dropin + before.dropout)

    return {
        "rx": rx,
        "tx": tx,
        "rx_pkts": rx_pkts,
        "tx_pkts": tx_pkts,
        "errors": errors,
        "drops": drops,
        "rx_total": after.bytes_recv,
        "tx_total": after.bytes_sent,
    }


def format_speed(bps):
    if bps >= 1024 ** 3:
        return f"{bps / 1024 ** 3:.2f} GB/s"
    if bps >= 1024 ** 2:
        return f"{bps / 1024 ** 2:.2f} MB/s"
    if bps >= 1024:
        return f"{bps / 1024:.2f} KB/s"
    return f"{bps:.0f} B/s"


def format_bytes(b):
    if b >= 1024 ** 3:
        return f"{b / 1024 ** 3:.2f} GB"
    if b >= 1024 ** 2:
        return f"{b / 1024 ** 2:.2f} MB"
    if b >= 1024:
        return f"{b / 1024:.2f} KB"
    return f"{b:.0f} B"
