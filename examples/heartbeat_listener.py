#!/usr/bin/env python3
"""heartbeat_listener.py — Menunggu & mencetak HEARTBEAT dari Pixhawk.

Terhubung ke endpoint lokal mavlink-router (udpin:127.0.0.1:14551) dan menunggu
pesan HEARTBEAT untuk membuktikan jalur komunikasi Pixhawk <-> Raspberry Pi
bekerja.

Contoh:
    python3 heartbeat_listener.py
    python3 heartbeat_listener.py --connect udpin:127.0.0.1:14551 --timeout 10
"""
import argparse
import sys
import time

from pymavlink import mavutil


def parse_args():
    parser = argparse.ArgumentParser(description="Tunggu HEARTBEAT dari Pixhawk.")
    parser.add_argument(
        "--connect",
        default="udpin:127.0.0.1:14551",
        help="MAVLink connection string (default: udpin:127.0.0.1:14551).",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=15.0,
        help="Batas waktu menunggu heartbeat dalam detik (default: 15).",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    print(f"Menghubungkan ke {args.connect} ...")
    master = mavutil.mavlink_connection(args.connect)

    print(f"Menunggu HEARTBEAT (timeout {args.timeout:.0f}s) ...")
    deadline = time.time() + args.timeout
    while time.time() < deadline:
        msg = master.recv_match(type="HEARTBEAT", blocking=True, timeout=1)
        if msg is None:
            continue
        print("HEARTBEAT diterima!")
        print(f"  system    : {master.target_system}")
        print(f"  component : {master.target_component}")
        print(f"  type      : {mavutil.mavlink.enums['MAV_TYPE'][msg.type].name}")
        print(f"  autopilot : {mavutil.mavlink.enums['MAV_AUTOPILOT'][msg.autopilot].name}")
        armed = bool(msg.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED)
        print(f"  armed     : {armed}")
        return 0

    print("Timeout: tidak ada HEARTBEAT. Lihat docs/06-troubleshooting.md", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
