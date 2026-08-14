# NetWatch

[![PyPI version](https://img.shields.io/pypi/v/netwatch-cli.svg)](https://pypi.org/project/netwatch-cli/)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Lightweight real-time network monitoring tool for Linux terminals.

![NetWatch dashboard](https://private-user-images.githubusercontent.com/183109999/603031657-0034caf3-da4c-4c5f-b633-c245292ff83b.png)

## Features

- Real-time ping monitoring
- Live upload/download tracking
- Terminal dashboard powered by Rich
- Lightweight and fast
- Simple CLI interface

## Installation

### Quick install (from source)

```bash
git clone git@github.com:WhoamiRAGE/NetWatch.git
cd NetWatch
./install.sh
```

This creates a virtual environment, installs NetWatch into it, installs a `net` launcher command to `~/.local/bin`, and wires that directory into your shell's `PATH` (bash, zsh, and fish are all handled automatically). Open a new terminal afterward and run `net`.

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

Start the dashboard:

```bash
net
```

Show version:

```bash
net --version
```

## Roadmap

- [ ] Packet loss monitoring
- [ ] Average ping statistics
- [ ] Min / Max ping
- [ ] Wi-Fi signal strength
- [ ] JSON output
- [ ] Interface selection
- [ ] Nix Flake support

## Requirements

- Linux
- Python 3.10+
- Network access

## Status

Actively in development.

## License

MIT — see [LICENSE](LICENSE).
