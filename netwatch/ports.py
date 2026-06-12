import socket

COMMON_PORTS = [
    22,    # SSH
    53,    # DNS
    80,    # HTTP
    139,   # NetBIOS
    443,   # HTTPS
    445,   # SMB
    8080,  # Web
    8008,  # Chromecast
    8009,  # Chromecast
]

def scan_ports(ip):
    open_ports = []

    for port in COMMON_PORTS:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.3)

        try:
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(str(port))
        except Exception:
            pass

        sock.close()

    return ", ".join(open_ports) if open_ports else "-"
