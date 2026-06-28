import os
import sys
from collections import deque
from concurrent.futures import ThreadPoolExecutor, as_completed
from importlib.metadata import version
from time import sleep

from rich.console import Console
from rich.live import Live
from rich.table import Table

from netwatch.dashboard import run
from netwatch.scan import scan_network, resolve_host, get_mac
from netwatch.vendor import get_vendor
from netwatch.ports import scan_ports
from netwatch.device import detect_device
from netwatch.wifi import get_wifi_info
from netwatch.bandwidth import get_interfaces, measure_bandwidth, format_speed, format_bytes


def enrich_host(host):
    mac = get_mac(host)
    vendor = get_vendor(mac)
    hostname = resolve_host(host)
    ports_str = scan_ports(host)
    open_ports = [int(p) for p in ports_str.split(", ") if p.strip().isdigit()]
    device = detect_device(vendor, hostname, open_ports)
    return (host, vendor, mac, device, hostname, ports_str)


def cmd_scan(console, network=None):
    if os.geteuid() != 0:
        console.print("[yellow]Warning: Running without root. MAC addresses may not be visible.[/yellow]\n")

    console.print("[dim]Scanning network...[/dim]")

    try:
        hosts = scan_network(network)
    except Exception as e:
        console.print(f"[red]Scan failed: {e}[/red]")
        return

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
            try:
                results.append(future.result())
            except Exception:
                pass

    results.sort(key=lambda x: list(map(int, x[0].split("."))))

    for row in results:
        table.add_row(*row)

    console.print(table)


def cmd_wifi(console):
    try:
        wifi = get_wifi_info()
    except Exception as e:
        console.print(f"[red]Failed to get wifi info: {e}[/red]")
        return

    if not wifi:
        console.print("[red]No wireless interface found.[/red]")
        return

    table = Table(
        title="Wifi Info",
        header_style="bold cyan",
        border_style="bright_black",
        title_style="bold white",
    )
    table.add_column("Property", style="dim", width=14)
    table.add_column("Value", style="bold green")

    table.add_row("Interface", wifi.get("interface", "Unknown"))
    table.add_row("SSID", wifi.get("ssid", "Unknown"))
    table.add_row("Signal", wifi.get("signal", "Unknown"))
    table.add_row("RX Rate", wifi.get("rx_rate", "Unknown"))
    table.add_row("TX Rate", wifi.get("tx_rate", "Unknown"))

    console.print(table)


def cmd_trace(console, target):
    from netwatch.trace import traceroute

    console.print(f"[dim]Tracing route to {target}...[/dim]\n")

    hops, error = traceroute(target)

    if hops is None:
        console.print(f"[red]{error}[/red]")
        return

    table = Table(
        title=f"Traceroute — {target}",
        header_style="bold cyan",
        border_style="bright_black",
        title_style="bold white",
    )
    table.add_column("Hop", style="dim", width=5)
    table.add_column("IP Address", style="bold")
    table.add_column("Hostname", style="dim")
    table.add_column("RTT", style="yellow")

    for hop in hops:
        rtt_style = "red" if hop["ip"] == "*" else "yellow"
        table.add_row(
            str(hop["hop"]),
            hop["ip"],
            hop["hostname"],
            f"[{rtt_style}]{hop['rtt']}[/{rtt_style}]",
        )

    console.print(table)

    if error:
        console.print(f"[yellow]{error}[/yellow]")


def cmd_bw(console, iface=None):
    interfaces = get_interfaces()

    if not interfaces:
        console.print("[red]No active interfaces found.[/red]")
        return

    if iface and iface not in interfaces:
        console.print(f"[red]Interface '{iface}' not found. Available: {', '.join(interfaces)}[/red]")
        return

    if not iface:
        iface = interfaces[0]

    def make_bw_table():
        stats = measure_bandwidth(iface, interval=1.0)
        if not stats:
            return Table(title="No data")

        table = Table(
            title=f"Bandwidth Monitor — {iface}",
            header_style="bold cyan",
            border_style="bright_black",
            title_style="bold white",
        )
        table.add_column("Metric", style="dim", width=16)
        table.add_column("Value", style="bold green")

        table.add_row("RX Speed", format_speed(stats["rx"]))
        table.add_row("TX Speed", format_speed(stats["tx"]))
        table.add_row("RX Packets/s", str(stats["rx_pkts"]))
        table.add_row("TX Packets/s", str(stats["tx_pkts"]))
        table.add_row("Errors", str(stats["errors"]))
        table.add_row("Drops", str(stats["drops"]))
        table.add_row("", "")
        table.add_row("Total RX", format_bytes(stats["rx_total"]))
        table.add_row("Total TX", format_bytes(stats["tx_total"]))

        if len(interfaces) > 1:
            table.add_row("", "")
            table.add_row("Interfaces", ", ".join(interfaces))

        return table

    try:
        with Live(make_bw_table(), refresh_per_second=1) as live:
            while True:
                live.update(make_bw_table())
    except KeyboardInterrupt:
        pass


def cmd_snmp(console, host, community="public"):
    from netwatch.snmp import snmp_get, snmp_get_interfaces, COMMON_OIDS

    console.print(f"[dim]Querying {host} via SNMP...[/dim]\n")

    info = snmp_get(host, COMMON_OIDS, community)

    table = Table(
        title=f"SNMP Info — {host}",
        header_style="bold cyan",
        border_style="bright_black",
        title_style="bold white",
    )
    table.add_column("Property", style="dim", width=20)
    table.add_column("Value", style="bold green")

    for k, v in info.items():
        table.add_row(k, v)

    console.print(table)

    console.print("\n[dim]Fetching interface table...[/dim]\n")
    interfaces = snmp_get_interfaces(host, community)

    if interfaces:
        iface_table = Table(
            title="Interfaces",
            header_style="bold cyan",
            border_style="bright_black",
            title_style="bold white",
        )
        iface_table.add_column("Index", style="dim", width=6)
        iface_table.add_column("Name", style="bold")
        iface_table.add_column("Status", style="green")
        iface_table.add_column("Speed")

        for iface in interfaces:
            status_style = "green" if iface["status"] == "up" else "red"
            iface_table.add_row(
                iface["index"],
                iface["name"],
                f"[{status_style}]{iface['status']}[/{status_style}]",
                iface["speed"],
            )

        console.print(iface_table)
    else:
        console.print("[yellow]No interface data available.[/yellow]")


def print_help(console):
    console.print("""
[bold white]NetWatch[/bold white] — Linux Network Monitoring Tool

[bold cyan]Usage:[/bold cyan]
  netwatch                             Live dashboard (ping, speed, wifi)
  netwatch scan                        Scan local network for active hosts
  netwatch scan --range <CIDR>         Scan a specific network range
  netwatch wifi                        Show wifi interface info
  netwatch trace <host>                Traceroute to a host
  netwatch bw                          Bandwidth monitor (default interface)
  netwatch bw <interface>              Bandwidth monitor for specific interface
  netwatch snmp <host> [community]     Query device via SNMP
  netwatch --version                   Show version
  netwatch --help                      Show this help message
""")


def main():
    console = Console()

    if "--version" in sys.argv:
        print(f"NetWatch {version('netwatch')}")
        return

    if "--help" in sys.argv or "-h" in sys.argv:
        print_help(console)
        return

    if len(sys.argv) > 1:
        cmd = sys.argv[1]

        if cmd == "scan":
            network = None
            if "--range" in sys.argv:
                idx = sys.argv.index("--range")
                if idx + 1 < len(sys.argv):
                    network = sys.argv[idx + 1]
                else:
                    console.print("[red]--range requires a value, e.g. --range 192.168.1.0/24[/red]")
                    return
            cmd_scan(console, network)
            return

        if cmd == "wifi":
            cmd_wifi(console)
            return

        if cmd == "trace":
            if len(sys.argv) < 3:
                console.print("[red]Usage: netwatch trace <host/ip>[/red]")
                return
            cmd_trace(console, sys.argv[2])
            return

        if cmd == "bw":
            iface = sys.argv[2] if len(sys.argv) > 2 else None
            cmd_bw(console, iface)
            return

        if cmd == "snmp":
            if len(sys.argv) < 3:
                console.print("[red]Usage: netwatch snmp <host> [community][/red]")
                return
            community = sys.argv[3] if len(sys.argv) > 3 else "public"
            cmd_snmp(console, sys.argv[2], community)
            return

        console.print(f"[red]Unknown command: {cmd}[/red]")
        print_help(console)
        return

    try:
        run()
    except Exception as e:
        console.print(f"[red]Dashboard error: {e}[/red]")


if __name__ == "__main__":
    main()
