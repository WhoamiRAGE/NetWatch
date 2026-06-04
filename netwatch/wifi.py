import subprocess
import re


def get_signal():
    try:
        output = subprocess.check_output(
            ["iw", "dev", "wlan0", "link"],
            stderr=subprocess.DEVNULL,
            text=True
        )

        match = re.search(r"signal:\s*(-\d+)", output)

        if match:
            return f"{match.group(1)} dBm"

    except Exception:
        pass

    return "Unknown"
