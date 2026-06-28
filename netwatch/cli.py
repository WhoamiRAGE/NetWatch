import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from importlib.metadata import version

from rich.console import Console
from rich.table import Table

from netwatch.dashboard import run
from netwatch.scan import scan_network, resolve_host, get_mac
from netwatch.vendor import get_vendor
from netwatch.ports import scan_ports
from netwatch.device import detect_device


def enrich_host(host):
    mac = get_mac(host)
    vendor = get_vendor(mac)
    hostname = resolve_host(host)
    ports_str = scan_ports(host)
    open_ports = [int(p) for p in ports_str.split(", ") if p.strip().isdigit()]
    device = detect_device(vendor, hostname, open_ports)
    return (host, vendor, mac, device, hostname, ports_str)


def main():
    if "--version" in sys.argv:
        print(f"NetWatch {version('netwatch')}")
        return

    if len(sys.argv) > 1 and sys.argv[1] == "scan":
        console = Console()

        console.print("[dim]Scanning network...[/dim]")
        hosts = scan_network()

        if not hosts:
            console.print("[red]No active hosts found.[/red]")
            return

        console.print(f"[green]Found {len(hosts)} active hosts[/green]\n")

        table = Table(
            title="Network Scan",
            header_style="bold cyan",
            border_style="bright_black",
            title_style="bold white",
        )
        table.add_column("IP Address", style="bold")
        table.add_column("Vendor", style="green")
        table.add_column("MAC Address", style="dim")
        table.add_column("Device Type")
        table.add_column("Hostname", style="dim")
        table.add_column("Open Ports", style="yellow")

        with ThreadPoolExecutor(max_workers=32) as executor:
            futures = {executor.submit(enrich_host, h): h for h in hosts}
            results = []
            for future in as_completed(futures):
                results.append(future.result())

        results.sort(key=lambda x: list(map(int, x[0].split("."))))

        for row in results:
            table.add_row(*row)

        console.print(table)
        return

    run()


if __name__ == "__main__":
    main()
