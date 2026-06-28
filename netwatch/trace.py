import subprocess
import re
import socket


def resolve_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return None


def traceroute(target, max_hops=30):
    hops = []

    try:
        result = subprocess.run(
            ["traceroute", "-n", "-m", str(max_hops), "-w", "1", target],
            capture_output=True,
            text=True,
            timeout=60,
        )

        for line in result.stdout.splitlines()[1:]:
            match = re.match(
                r"\s*(\d+)\s+(?:(\d+\.\d+\.\d+\.\d+)\s+([\d.]+)\s+ms|\*)",
                line
            )
            if not match:
                continue

            hop_num = match.group(1)
            ip = match.group(2)
            rtt = match.group(3)

            if ip:
                hostname = resolve_hostname(ip)
                hops.append({
                    "hop": int(hop_num),
                    "ip": ip,
                    "hostname": hostname or "",
                    "rtt": f"{rtt} ms",
                })
            else:
                hops.append({
                    "hop": int(hop_num),
                    "ip": "*",
                    "hostname": "",
                    "rtt": "* * *",
                })

    except FileNotFoundError:
        return None, "traceroute not found. Install it: sudo pacman -S traceroute"
    except subprocess.TimeoutExpired:
        return hops, "Timeout"
    except Exception as e:
        return None, str(e)

    return hops, None
