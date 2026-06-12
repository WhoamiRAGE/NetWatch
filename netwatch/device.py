def detect_device(vendor, hostname, ports):
    hostname = hostname.lower()

    if hostname == "_gateway":
        return "📡 Router"

    if "apple" in vendor.lower():
        return "🍎 Apple Device"

    if "xiaomi" in vendor.lower():
        return "📱 Xiaomi Device"

    if 445 in ports:
        return "🖥 Windows PC"

    if 22 in ports:
        return "🐧 Linux Device"

    return "❓ Unknown"
