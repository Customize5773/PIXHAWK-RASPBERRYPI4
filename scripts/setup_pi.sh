#!/usr/bin/env bash
#
# setup_pi.sh — Menyiapkan Raspberry Pi 4 sebagai companion computer ROV.
# Meng-install dependency Python + pymavlink dan memberi akses serial.
#
# Penggunaan:  ./scripts/setup_pi.sh
# Lihat docs/03-raspberry-pi-setup.md
#
set -euo pipefail

echo "==> [1/4] Update daftar paket & upgrade sistem"
sudo apt-get update
sudo apt-get full-upgrade -y

echo "==> [2/4] Install dependency dasar"
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    build-essential

echo "==> [3/4] Install pymavlink (untuk skrip contoh)"
# --break-system-packages diperlukan di Raspberry Pi OS terbaru (PEP 668).
if pip3 install --help 2>/dev/null | grep -q -- "--break-system-packages"; then
    pip3 install --break-system-packages -r "$(dirname "$0")/../examples/requirements.txt"
else
    pip3 install -r "$(dirname "$0")/../examples/requirements.txt"
fi

echo "==> [4/4] Tambahkan user '$USER' ke grup 'dialout' (akses serial tanpa sudo)"
if id -nG "$USER" | grep -qw dialout; then
    echo "    User sudah anggota grup dialout."
else
    sudo usermod -aG dialout "$USER"
    echo "    Ditambahkan. LOGOUT/LOGIN ulang atau reboot agar aktif."
fi

echo
echo "Selesai. Langkah berikutnya:"
echo "  - Reboot bila keanggotaan grup baru ditambahkan: sudo reboot"
echo "  - Lalu install mavlink-router: ./scripts/install_mavlink_router.sh"
