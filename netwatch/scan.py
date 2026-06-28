import socket
import ipaddress
import subprocess
import re
from concurrent.futures import ThreadPoolExecutor


def get_local_network():
    try:
        result = subprocess.run(
            ["ip", "route"],
            capture_output=True, text=True
        )
        for line in result.stdout.splitlines():
            if "src" in line and "kernel" in line:
                match = re.search(r"(\d+\.\d+\.\d+\.\d+/\d+)", line)
                if match:
                    return match.group(1)
    except Exception:
        pass
    return "192.168.1.0/24"


def ping_host(ip):
    result = subprocess.run(
        ["ping", "-c", "1", "-W", "1", str(ip)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return str(ip) if result.returncode == 0 else None


def scan_network(network=None):
    if network is None:
        network = get_local_network()

    active_hosts = []
    with ThreadPoolExecutor(max_workers=64) as executor:
        results = executor.map(
            ping_host,
            ipaddress.ip_network(network, strict=False).hosts()
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


def get_mac(ip):
    try:
        result = subprocess.run(
            ["ip", "neigh", "show", ip],
            capture_output=True,
            text=True,
        )
        match = re.search(r"lladdr ([0-9a-f:]{17})", result.stdout.lower())
        if match:
            return match.group(1)
    except Exception:
        pass
    return "Unknown"
