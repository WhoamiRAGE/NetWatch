# NetWatch

<img width="244" height="166" alt="image" src="https://github.com/user-attachments/assets/0034caf3-da4c-4c5f-b633-c245292ff83b" />



Lightweight real-time network monitoring tool for Linux terminals.

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
