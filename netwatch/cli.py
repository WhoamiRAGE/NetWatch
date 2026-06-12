import sys
from importlib.metadata import version

from rich.console import Console
from rich.table import Table

from netwatch.dashboard import run
from netwatch.scan import scan_network, resolve_host, get_mac
from netwatch.vendor import get_vendor
from netwatch.ports import scan_ports
from netwatch.device import detect_device

def main():
    if "--version" in sys.argv:
        print(f"NetWatch {version('netwatch')}")
        return

    if len(sys.argv) > 1 and sys.argv[1] == "scan":
        console = Console()

        table = Table(title="Network Scan")
        table.add_column("IP Address")
        table.add_column("Vendor")
        table.add_column("MAC Address")
        table.add_column("Device Type")
        table.add_column("Hostname")
        table.add_column("Open Ports")
        hosts = scan_network()

        if not hosts:
            console.print("No active hosts found.")
            return

        console.print(f"Found {len(hosts)} active hosts\n")

        for host in hosts:
            mac = get_mac(host)

            table.add_row(
    host,
    get_vendor(mac),
    mac,
    resolve_host(host),
    scan_ports(host)
)

        console.print(table)
        return

    run()


if __name__ == "__main__":
    main()
