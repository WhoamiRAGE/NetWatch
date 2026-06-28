def is_randomized_mac(mac):
    if not mac or mac == "Unknown":
        return False
    try:
        first_byte = int(mac.split(":")[0], 16)
        return bool(first_byte & 0x02)
    except Exception:
        return False


def detect_device(vendor, hostname, ports):
    hostname = hostname.lower()
    vendor = vendor.lower()

    if hostname == "_gateway":
        return "Router"

    if is_randomized_mac(vendor):
        # vendor parametresi burada MAC değil, ama port/hostname'e bakabiliriz
        pass

    if "apple" in vendor:
        return "Apple Device"

    if "xiaomi" in vendor:
        return "Xiaomi Device"

    if "samsung" in vendor:
        return "Samsung Device"

    if "intel" in vendor:
        return "PC / Laptop"

    if "huawei" in vendor:
        return "Huawei Device"

    if "randomized" in vendor:
        if 62078 in ports:
            return "iOS Device"
        if 5353 in ports:
            return "Mobile Device"
        return "Mobile Device (Random MAC)"

    if 445 in ports:
        return "Windows PC"

    if 22 in ports:
        return "Linux Device"

    if 80 in ports or 443 in ports:
        return "Network Device"

    return "Unknown"
