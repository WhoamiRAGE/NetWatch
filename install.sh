#!/usr/bin/env bash

set -e

echo "[*] Installing NetWatch..."

INSTALL_DIR="$HOME/.local/share/netwatch"
BIN_DIR="$HOME/.local/bin"

mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"

if ! command -v git >/dev/null; then
    echo "[!] git is required"
    exit 1
fi

if ! command -v python3 >/dev/null; then
    echo "[!] python3 is required"
    exit 1
fi

rm -rf "$INSTALL_DIR"

git clone https://github.com/WhoamiRAGE/NetWatch.git "$INSTALL_DIR"

cd "$INSTALL_DIR"

python3 -m venv .venv

source .venv/bin/activate

pip install -U pip

pip install .

cat > "$BIN_DIR/netwatch" << EOF
#!/usr/bin/env bash
$INSTALL_DIR/.venv/bin/netwatch "\$@"
EOF

chmod +x "$BIN_DIR/netwatch"

echo
echo "Installed successfully."
echo
echo "Add ~/.local/bin to PATH if needed."
