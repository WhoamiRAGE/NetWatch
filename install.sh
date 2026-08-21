#!/usr/bin/env bash
set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="$HOME/.local/bin"
VENV_DIR="$REPO_DIR/.venv"

echo "==> NetWatch quraşdırılması başladı..."
echo "    Repo: $REPO_DIR"

# 1. ~/.local/bin qovluğunu yarat
mkdir -p "$BIN_DIR"

# 2. Virtual environment yaradılması və paketlərin quraşdırılması
if [ ! -d "$VENV_DIR" ]; then
    echo "==> Python venv yaradılır..."
    python3 -m venv "$VENV_DIR"
fi

echo "==> NetWatch quraşdırılır (editable install)..."
"$VENV_DIR/bin/pip" install --upgrade pip >/dev/null
"$VENV_DIR/bin/pip" install -e "$REPO_DIR"

# 3. Executable launcher simvolik linki və ya wrapper yaratmaq
echo "==> Launcher $BIN_DIR/netwatch ünvanına yerləşdirilir..."
cat <<EOF > "$BIN_DIR/netwatch"
#!/usr/bin/env bash
exec "$VENV_DIR/bin/netwatch" "\$@"
EOF
chmod +x "$BIN_DIR/netwatch"

# 4. PATH konfiqurasiyasını Shell fayllarına əlavə etmək
add_to_path() {
    local rcfile="$1"
    if [ -f "$rcfile" ]; then
        if ! grep -q 'export PATH="$HOME/.local/bin:$PATH"' "$rcfile"; then
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$rcfile"
            echo "    PATH $rcfile faylına əlavə olundu."
        fi
    fi
}

echo "==> PATH konfiqurasiyası yoxlanılır..."
add_to_path "$HOME/.bashrc"
add_to_path "$HOME/.zshrc"
add_to_path "$HOME/.profile"

# 5. Cari sessiya üçün PATH-i yeniləmək
export PATH="$HOME/.local/bin:$PATH"

echo ""
echo "==> Quraşdırılma tamamlandı!"
echo "==> Test edilir..."

if command -v netwatch >/dev/null 2>&1; then
    echo "SUCCESS: 'netwatch' artıq sistemdə hazırdır."
    echo "İndi birbaşa 'netwatch' yazıb işə sala bilərsən."
else
    echo "Qeyd: 'source ~/.bashrc' və ya 'export PATH=\"\$HOME/.local/bin:\$PATH\"' icra edin."
fi