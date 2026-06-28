import subprocess


COMMON_OIDS = {
    "System Description": "1.3.6.1.2.1.1.1.0",
    "System Name":        "1.3.6.1.2.1.1.5.0",
    "System Uptime":      "1.3.6.1.2.1.1.3.0",
    "System Contact":     "1.3.6.1.2.1.1.4.0",
    "System Location":    "1.3.6.1.2.1.1.6.0",
}

INTERFACE_OIDS = {
    "ifDescr":  "1.3.6.1.2.1.2.2.1.2",
    "ifOperStatus": "1.3.6.1.2.1.2.2.1.8",
    "ifHighSpeed": "1.3.6.1.2.1.31.1.1.1.15",
}


def _run(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        return result.stdout.strip()
    except Exception:
        return ""


def snmp_get(host, oids, community="public", port=161):
    results = {}
    for label, oid in oids.items():
        out = _run(["snmpget", "-v2c", "-c", community, f"{host}:{port}", oid])
        if out:
            value = out.split("=", 1)[-1].strip()
            value = value.split(":", 1)[-1].strip().strip('"')
            results[label] = value
        else:
            results[label] = "N/A"
    return results


def snmp_get_interfaces(host, community="public", port=161):
    names = {}
    statuses = {}
    speeds = {}

    for store, oid in [(names, INTERFACE_OIDS["ifDescr"]),
                       (statuses, INTERFACE_OIDS["ifOperStatus"]),
                       (speeds, INTERFACE_OIDS["ifHighSpeed"])]:
        out = _run(["snmpwalk", "-v2c", "-c", community, f"{host}:{port}", oid])
        for line in out.splitlines():
            if "=" not in line:
                continue
            key, _, val = line.partition("=")
            idx = key.strip().split(".")[-1]
            val = val.strip().split(":", 1)[-1].strip().strip('"')
            store[idx] = val

    interfaces = []
    for idx in names:
        status_val = statuses.get(idx, "?")
        status_str = "up" if status_val.strip() == "1" or "up" in status_val.lower() else "down"
        try:
            speed_mbps = int(speeds.get(idx, 0))
            speed_str = f"{speed_mbps} Mbps" if speed_mbps > 0 else "?"
        except Exception:
            speed_str = "?"
        interfaces.append({
            "index": idx,
            "name": names[idx],
            "status": status_str,
            "speed": speed_str,
        })

    return interfaces
