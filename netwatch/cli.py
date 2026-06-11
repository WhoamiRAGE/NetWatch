import sys
from importlib.metadata import version

from rich.console import Console
from rich.table import Table

from netwatch.dashboard import run
from netwatch.scan import scan_network, resolve_host


def main():
    if "--version" in sys.argv:
        print(f"NetWatch {version('netwatch')}")
        return

    if len(sys.argv) > 1 and sys.argv[1] == "scan":
        console = Console()

        table = Table(title="Network Scan")
        table.add_column("IP Address")
        table.add_column("Hostname")

        hosts = scan_network()

        if not hosts:
            console.print("No active hosts found.")
            return

        console.print(f"Found {len(hosts)} active hosts\n")

        for host in hosts:
            table.add_row(host, resolve_host(host))

        console.print(table)
        return

    run()


if __name__ == "__main__":
    main()
