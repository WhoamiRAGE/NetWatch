from manuf import manuf

parser = manuf.MacParser()


def get_vendor(mac):
    if not mac or mac == "Unknown":
        return "Unknown"

    try:
        vendor = parser.get_manuf(mac)

        if vendor:
            return vendor

        first_byte = int(mac.split(":")[0], 16)

        if first_byte & 0x02:
            return "Randomized"

        return "Unknown"

    except Exception:
        return "Unknown"
