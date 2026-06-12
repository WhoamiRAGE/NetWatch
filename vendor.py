from manuf import manuf

parser = manuf.MacParser()

def get_vendor(mac):
    if mac == "Unknown":
        return "Unknown"

    vendor = parser.get_manuf(mac)

    if vendor:
        return vendor

    return "Unknown"
