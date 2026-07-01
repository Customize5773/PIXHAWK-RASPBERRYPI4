#!/usr/bin/env python3
"""arm_disarm.py — Arm atau disarm Pixhawk (ArduSub) via MAVLink.

PERINGATAN: Meng-arm ROV mengaktifkan thruster. Selalu uji dengan thruster
terlepas dari air / propeller dilepas, dan siapkan cara disarm cepat.

Contoh:
    python3 arm_disarm.py --arm
    python3 arm_disarm.py --disarm
    python3 arm_disarm.py --disarm --force   # disarm paksa
"""
import argparse
import sys

from pymavlink import mavutil


def parse_args():
    parser = argparse.ArgumentParser(description="Arm/disarm Pixhawk ArduSub.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--arm", action="store_true", help="Arm kendaraan.")
    group.add_argument("--disarm", action="store_true", help="Disarm kendaraan.")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Paksa arm/disarm (lewati beberapa pre-arm check).",
    )
    parser.add_argument(
        "--connect",
        default="udpin:127.0.0.1:14551",
        help="MAVLink connection string (default: udpin:127.0.0.1:14551).",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    arm = args.arm  # True=arm, False=disarm

    print(f"Menghubungkan ke {args.connect} ...")
    master = mavutil.mavlink_connection(args.connect)
    master.wait_heartbeat()
    print(f"Terhubung: system {master.target_system}, component {master.target_component}")

    # param2: 0 = normal, 21196 = force (magic number ArduPilot).
    force_magic = 21196 if args.force else 0
    action = "ARM" if arm else "DISARM"
    print(f"Mengirim perintah {action}{' (FORCE)' if args.force else ''} ...")

    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
        0,               # confirmation
        1 if arm else 0,  # param1: 1=arm, 0=disarm
        force_magic,      # param2: force
        0, 0, 0, 0, 0,
    )

    ack = master.recv_match(type="COMMAND_ACK", blocking=True, timeout=5)
    if ack is None:
        print("Tidak ada COMMAND_ACK (timeout). Cek koneksi/pre-arm.", file=sys.stderr)
        return 1

    result = ack.result
    result_name = mavutil.mavlink.enums["MAV_RESULT"][result].name
    print(f"COMMAND_ACK: {result_name}")
    if result == mavutil.mavlink.MAV_RESULT_ACCEPTED:
        print(f"{action} berhasil.")
        return 0

    print(f"{action} ditolak ({result_name}). "
          "Cek pre-arm check di QGC atau gunakan --force.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
