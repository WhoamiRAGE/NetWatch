from time import sleep

from rich.live import Live
from rich.table import Table

from netwatch.ping import get_ping
from netwatch.network import get_network_speed


def format_speed(speed):
    if speed > 1024 * 1024:
        return f"{speed / (1024 * 1024):.2f} MB/s"

    if speed > 1024:
        return f"{speed / 1024:.2f} KB/s"

    return f"{speed:.0f} B/s"


def make_table():
    download, upload = get_network_speed()

    table = Table(title="NetWatch")

    table.add_column("Metric")
    table.add_column("Value")

    table.add_row("Ping", f"{get_ping()} ms")
    table.add_row("Download", format_speed(download))
    table.add_row("Upload", format_speed(upload))

    return table


def run():
    with Live(make_table(), refresh_per_second=2) as live:
        while True:
            live.update(make_table())
            sleep(1)
