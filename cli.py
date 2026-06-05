import sys

from netwatch.dashboard import run
from netwatch.scan import scan_network

VERSION = "0.2.0"


def main():
    if "--version" in sys.argv:
        print(f"NetWatch {VERSION}")
        return

    if len(sys.argv) > 2 and sys.argv[1] == "scan":
    hosts = scan_network(sys.argv[2])

    for host in hosts:
        print(host)

    return
