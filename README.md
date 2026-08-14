# NetWatch

[![PyPI version](https://img.shields.io/pypi/v/netwatch-cli.svg)](https://pypi.org/project/netwatch-cli/)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Lightweight real-time network monitoring tool for Linux terminals.

![NetWatch dashboard](https://private-user-images.githubusercontent.com/183109999/603031657-0034caf3-da4c-4c5f-b633-c245292ff83b.png)

## Features

- Live dashboard: ping, speed, and wifi info in one view
- Local network scanning (with optional CIDR range)
- Bandwidth monitor, per-interface or default
- Traceroute to any host
- SNMP query against a device
- Wifi interface info
- Terminal UI powered by Rich
- Lightweight and fast

## Installation

### Quick install (from source)

```bash
git clone git@github.com:WhoamiRAGE/NetWatch.git
cd NetWatch
./install.sh
```

This creates a virtual environment, installs NetWatch into it, installs a `netwatch` launcher command to `~/.local/bin`, and wires that directory into your shell's `PATH` (bash, zsh, and fish are all handled automatically). Open a new terminal afterward and run `netwatch`.

### From PyPI

```bash
pip install netwatch-cli
```

### Manual (from source)

```bash
git clone git@github.com:WhoamiRAGE/NetWatch.git
cd NetWatch

python -m venv .venv
source .venv/bin/activate

pip install -e .
```

## Usage

```
netwatch                       Live dashboard (ping, speed, wifi)
netwatch scan                  Scan local network for active hosts
netwatch scan --range <CIDR>   Scan a specific network range
netwatch wifi                  Show wifi interface info
netwatch trace <host>          Traceroute to a host
netwatch bw                    Bandwidth monitor (default interface)
netwatch bw <interface>        Bandwidth monitor for specific interface
netwatch snmp <host>           Query device via SNMP
netwatch --version             Show version
netwatch --help                Show this help message
```

## Roadmap

- [ ] Packet loss monitoring
- [ ] Average ping statistics
- [ ] Min / Max ping
- [ ] JSON output
- [ ] Nix Flake support

## Requirements

- Linux
- Python 3.10+
- Network access

## Status

Actively in development.

## License

MIT — see [LICENSE](LICENSE).
