import ipaddress
import subprocess
import re
import socket
from concurrent.futures import ThreadPoolExecutor


def get_local_network():
    output = subprocess.check_output(
        ["ip", "-4", "addr"],
        text=True
    )

    match = re.search(r"inet (\d+\.\d+\.\d+)\.\d+/(\d+)", output)

    if match:
        base = match.group(1)
        prefix = match.group(2)
        return f"{base}.0/{prefix}"

    return "192.168.1.0/24"


def ping_host(ip):
    result = subprocess.run(
        ["ping", "-c", "1", "-W", "1", str(ip)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    if result.returncode == 0:
        return str(ip)

    return None


def resolve_host(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return "Unknown"


def scan_network(network=None):
    if network is None:
        network = get_local_network()

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
