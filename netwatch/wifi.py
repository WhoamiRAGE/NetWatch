import subprocess
import re


def get_wireless_interface():
    try:
        result = subprocess.run(
            ["iw", "dev"],
            capture_output=True, text=True
        )
        match = re.search(r"Interface\s+(\S+)", result.stdout)
        if match:
            return match.group(1)
    except Exception:
        pass
    return None


def get_signal():
    iface = get_wireless_interface()
    if not iface:
        return "No wireless interface"

    try:
        output = subprocess.check_output(
            ["iw", "dev", iface, "link"],
            stderr=subprocess.DEVNULL,
            text=True
        )

        match = re.search(r"signal:\s*(-\d+)", output)
        if match:
            return f"{match.group(1)} dBm"

    except Exception:
        pass

    return "Unknown"


def get_wifi_info():
    iface = get_wireless_interface()
    if not iface:
        return {}

    try:
        output = subprocess.check_output(
            ["iw", "dev", iface, "link"],
            stderr=subprocess.DEVNULL,
            text=True
        )

        info = {"interface": iface}

        match = re.search(r"signal:\s*(-\d+)", output)
        if match:
            info["signal"] = f"{match.group(1)} dBm"

        match = re.search(r"SSID:\s*(\S+)", output)
        if match:
            info["ssid"] = match.group(1)

        match = re.search(r"rx bitrate:\s*([\d.]+\s*\S+)", output)
        if match:
            info["rx_rate"] = match.group(1)

        match = re.search(r"tx bitrate:\s*([\d.]+\s*\S+)", output)
        if match:
            info["tx_rate"] = match.group(1)

        return info

    except Exception:
        return {"interface": iface}
