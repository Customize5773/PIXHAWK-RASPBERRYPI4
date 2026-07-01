#!/usr/bin/env bash
#
# install_mavlink_router.sh — Build & install mavlink-router dari source.
#
# Penggunaan:  ./scripts/install_mavlink_router.sh
# Lihat docs/04-mavlink-routing.md
#
set -euo pipefail

REPO_URL="https://github.com/mavlink-router/mavlink-router.git"
BUILD_DIR="${HOME}/mavlink-router"

if command -v mavlink-routerd >/dev/null 2>&1; then
    echo "==> mavlink-routerd sudah terpasang: $(mavlink-routerd --version 2>&1 | head -n1)"
    read -r -p "    Install ulang? [y/N] " ans
    case "${ans:-N}" in
        [yY]*) ;;
        *) echo "    Dilewati."; exit 0 ;;
    esac
fi

echo "==> [1/4] Install dependency build"
sudo apt-get update
sudo apt-get install -y \
    git \
    meson \
    ninja-build \
    pkg-config \
    gcc \
    g++ \
    python3-setuptools

echo "==> [2/4] Clone/refresh source (dengan submodule)"
if [ -d "${BUILD_DIR}/.git" ]; then
    git -C "${BUILD_DIR}" pull --recurse-submodules
    git -C "${BUILD_DIR}" submodule update --init --recursive
else
    git clone --recurse-submodules "${REPO_URL}" "${BUILD_DIR}"
fi

echo "==> [3/4] Build (meson + ninja)"
cd "${BUILD_DIR}"
meson setup build . --reconfigure
ninja -C build

echo "==> [4/4] Install ke sistem"
sudo ninja -C build install

echo
echo "Selesai: $(command -v mavlink-routerd) — $(mavlink-routerd --version 2>&1 | head -n1)"
echo "Langkah berikutnya:"
echo "  sudo mkdir -p /etc/mavlink-router"
echo "  sudo cp config/mavlink-router/main.conf /etc/mavlink-router/main.conf"
echo "  sudo cp config/systemd/mavlink-router.service /etc/systemd/system/"
echo "  sudo systemctl enable --now mavlink-router"
