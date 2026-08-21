# NetWatch

[![PyPI version](https://img.shields.io/pypi/v/netwatch-cli.svg)](https://pypi.org/project/netwatch-cli/)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A lightweight, real-time network monitoring tool for the Linux terminal — ping, bandwidth, wifi, scanning, traceroute, and SNMP queries, all in one CLI.
<img width="731" height="566" alt="Screenshot_20260821_202507" src="https://github.com/user-attachments/assets/282ad490-ff62-444e-a5f5-faf9510e1526" />
<img width="390" height="337" alt="Screenshot_20260821_202546" src="https://github.com/user-attachments/assets/b6f7f967-3685-46b2-b695-344ceb572d9e" />

![NetWatch dashboard](https://private-user-images.githubusercontent.com/183109999/603031657-0034caf3-da4c-4c5f-b633-c245292ff83b.png)

## Why NetWatch

Most network diagnostics on Linux mean reaching for half a dozen separate tools — `ping`, `iftop`, `traceroute`, `iwconfig`, `snmpwalk` — each with its own output format. NetWatch wraps the common ones into a single, fast CLI with a clean terminal UI, so day-to-day network troubleshooting stays in one place.

## Features

- **Live dashboard** — ping, speed, and wifi info in one view
- **Network scanning** — discover active hosts on your LAN, with optional CIDR range
- **Bandwidth monitor** — real-time RX/TX speed, packet rate, errors, and totals, per interface or default
- **Traceroute** — hop-by-hop path to any host
- **SNMP queries** — pull device info without a separate SNMP client
- **Wifi info** — interface details at a glance
- Built on [Rich](https://github.com/Textualize/rich) for a fast, clean terminal UI

## Installation

### Quick install (from source)

```bash
git clone git@github.com:WhoamiRAGE/NetWatch.git
cd NetWatch
./install.sh
```

This creates a virtual environment, installs NetWatch into it, installs a `netwatch` launcher to `~/.local/bin`, and wires that directory into your shell's `PATH` — bash, zsh, and fish are all handled automatically. Open a new terminal afterward and run `netwatch`.

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
netwatch bw <interface>        Bandwidth monitor for a specific interface
netwatch snmp <host>           Query a device via SNMP
netwatch --version             Show version
netwatch --help                Show this help message
```

## Requirements

- Linux
- Python 3.10+
- Network access

## Contributing

Issues and pull requests are welcome — see [Issues](https://github.com/WhoamiRAGE/NetWatch/issues).

## License

MIT — see [LICENSE](LICENSE).
