# NetWatch

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

## Example

```text
      NetWatch
┏━━━━━━━━━━┳━━━━━━━━━━┓
┃ Metric   ┃ Value    ┃
┡━━━━━━━━━━╇━━━━━━━━━━┩
│ Ping     │ 69 ms    │
│ Download │ 1.24 MB/s│
│ Upload   │ 0.15 MB/s│
└──────────┴──────────┘
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
