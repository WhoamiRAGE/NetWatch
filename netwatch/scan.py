import socket
import ipaddress
import subprocess
from concurrent.futures import ThreadPoolExecutor


def ping_host(ip):
    result = subprocess.run(
        ["ping", "-c", "1", "-W", "1", str(ip)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    if result.returncode == 0:
        return str(ip)

    return None


def scan_network(network="192.168.100.0/23"):
    active_hosts = []

    with ThreadPoolExecutor(max_workers=64) as executor:
        results = executor.map(
            ping_host,
            ipaddress.ip_network(network).hosts()
        )

    for host in results:
        if host:
            active_hosts.append(host)

    return active_hosts
def resolve_host(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return "Unknown"
