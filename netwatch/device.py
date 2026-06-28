def detect_device(vendor, hostname, ports):
    hostname = hostname.lower()
    vendor = vendor.lower()

    if hostname == "_gateway":
        return "Router"

    if "apple" in vendor:
        return "Apple Device"

    if "xiaomi" in vendor:
        return "Xiaomi Device"

    if "samsung" in vendor:
        return "Samsung Device"

    if "intel" in vendor:
        return "PC / Laptop"

    if 445 in ports:
        return "Windows PC"

    if 22 in ports:
        return "Linux Device"

    return "Unknown"
