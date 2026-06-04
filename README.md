# NetWatch

<img width="287" height="288" alt="image" src="https://github.com/user-attachments/assets/a7db2d9c-779d-4e17-b220-18ea3f3e4caf" />


A lightweight Linux network monitoring tool written in Python.

## Features

* Live ping monitoring
* Download speed monitoring
* Upload speed monitoring
* Real-time terminal dashboard
* Simple CLI interface

## Installation

### From Source

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

* [ ] Packet loss monitoring
* [ ] Average ping statistics
* [ ] Min / Max ping
* [ ] Wi-Fi signal strength
* [ ] JSON output
* [ ] Interface selection
* [ ] Nix Flake support

## Requirements

* Linux
* Python 3.10+
* Network access

## License

MIT
