from time import sleep

from rich.live import Live
from rich.table import Table

from netwatch.ping import get_ping
from netwatch.network import get_network_speed
from netwatch.wifi import get_wifi_info


def format_speed(speed):
    if speed > 1024 * 1024:
        return f"{speed / (1024 * 1024):.2f} MB/s"

    if speed > 1024:
        return f"{speed / 1024:.2f} KB/s"

    return f"{speed:.0f} B/s"


def make_table():
    download, upload = get_network_speed()
    wifi = get_wifi_info()

    table = Table(
        title="NetWatch",
        show_header=True,
        header_style="bold cyan",
        border_style="bright_black",
        title_style="bold white",
    )

    table.add_column("Metric", style="dim", width=12)
    table.add_column("Value", style="bold green")

    table.add_row("Ping", f"{get_ping()} ms")
    table.add_row("Download", format_speed(download))
    table.add_row("Upload", format_speed(upload))

    if wifi:
        table.add_row("", "")
        table.add_row("Interface", wifi.get("interface", "Unknown"))
        table.add_row("SSID", wifi.get("ssid", "Unknown"))
        table.add_row("Signal", wifi.get("signal", "Unknown"))
        table.add_row("RX Rate", wifi.get("rx_rate", "Unknown"))
        table.add_row("TX Rate", wifi.get("tx_rate", "Unknown"))

    return table


def run():
    try:
        with Live(make_table(), refresh_per_second=2) as live:
            while True:
                live.update(make_table())
                sleep(1)
    except KeyboardInterrupt:
        pass
