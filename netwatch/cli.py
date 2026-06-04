import sys
from netwatch.dashboard import run

VERSION = "0.1.0"


def main():
    if "--version" in sys.argv:
        print(f"NetWatch {VERSION}")
        return

    run()
