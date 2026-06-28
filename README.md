# NetWatch

A terminal-based network monitoring tool for Linux.

## Features

- Real-time ping, download/upload speed and wifi info
- Local network scan (active hosts, MAC, vendor, open ports)
- Automatic subnet detection
- Device type detection (router, mobile, Windows, Linux...)
- Fast results with parallel scanning

## Installation

```bash
curl -fsSL https://raw.githubusercontent.com/WhoamiRAGE/NetWatch/main/install.sh | bash
```

Or manually:

```bash
git clone https://github.com/WhoamiRAGE/NetWatch.git
cd NetWatch
pip install -e . --break-system-packages
```

## Usage

```bash
netwatch                             # Live dashboard
netwatch scan                        # Scan local network
netwatch scan --range 10.0.0.0/24   # Scan a specific range
netwatch wifi                        # Show wifi info
netwatch --version
netwatch --help
```

## Requirements

- Python 3.10+
- Linux
- `iw` (for wifi info)
- Root recommended for full scan results (MAC addresses)

## License

MIT
