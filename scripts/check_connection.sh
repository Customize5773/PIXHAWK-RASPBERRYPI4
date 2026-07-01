#!/usr/bin/env bash
#
# check_connection.sh — Verifikasi koneksi Pixhawk <-> Raspberry Pi.
# Mendeteksi perangkat serial USB lalu mengecek HEARTBEAT lewat mavlink-router.
#
# Penggunaan:  ./scripts/check_connection.sh
# Lihat docs/06-troubleshooting.md
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "==> [1/3] Cek perangkat serial USB (/dev/ttyACM*)"
if ls /dev/ttyACM* >/dev/null 2>&1; then
    ls -l /dev/ttyACM*
else
    echo "    TIDAK ADA /dev/ttyACM*. Cek kabel/power Pixhawk."
    echo "    Lihat docs/06-troubleshooting.md"
    exit 1
fi

echo "==> [2/3] Cek service mavlink-router"
if systemctl is-active --quiet mavlink-router; then
    echo "    mavlink-router AKTIF."
else
    echo "    PERINGATAN: service mavlink-router tidak aktif."
    echo "    Jalankan: sudo systemctl start mavlink-router"
    echo "    (Melanjutkan cek heartbeat — mungkin router dijalankan manual.)"
fi

echo "==> [3/3] Cek HEARTBEAT via endpoint lokal (udpin:127.0.0.1:14551)"
python3 "${SCRIPT_DIR}/../examples/heartbeat_listener.py" --timeout 10
