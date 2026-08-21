#!/usr/bin/env bash
set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="$HOME/.local/bin"
VENV_DIR="$REPO_DIR/.venv"

echo "==> NetWatch installer"
echo "    repo: $REPO_DIR"

# 1. Ensure ~/.local/bin exists
mkdir -p "$BIN_DIR"

# 2. Create virtual environment if not present
if [ ! -d "$VENV_DIR" ]; then
    echo "==> Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# 3. Install package editable
echo "==> Installing NetWatch (editable install)..."
"$VENV_DIR/bin/pip" install --upgrade pip >/dev/null 2>&1
"$VENV_DIR/bin/pip" install -e "$REPO_DIR"

# 4. Create launcher script
echo "==> Installing 'netwatch' launcher to $BIN_DIR..."
cat << 'LAUNCHER' > "$BIN_DIR/netwatch"
#!/usr/bin/env bash
exec "$HOME/NetWatch/.venv/bin/netwatch" "$@"
LAUNCHER
chmod +x "$BIN_DIR/netwatch"

# 5. Helper function to update PATH in shell rc files
add_to_path() {
    local rcfile="$1"
    if [ -f "$rcfile" ]; then
        if ! grep -q 'export PATH="$HOME/.local/bin:$PATH"' "$rcfile"; then
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$rcfile"
            echo "    Added to $rcfile"
        fi
    fi
}

echo "==> Setting up PATH for 'netwatch'..."
add_to_path "$HOME/.bashrc"
add_to_path "$HOME/.zshrc"
add_to_path "$HOME/.profile"

# Export PATH for current installer process
export PATH="$BIN_DIR:$PATH"

echo "==> Done."
echo ""
echo "Open a new terminal (or run 'export PATH=\"\$HOME/.local/bin:\$PATH\"'), then run:  netwatch"
