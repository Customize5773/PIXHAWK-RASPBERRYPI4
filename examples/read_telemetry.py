#!/usr/bin/env python3
"""read_telemetry.py — Membaca telemetry dasar ROV dari Pixhawk (ArduSub).

Menampilkan attitude (roll/pitch/yaw), kedalaman (dari SCALED_PRESSURE2 / bar30),
dan status baterai. Terhubung lewat endpoint lokal mavlink-router.

Contoh:
    python3 read_telemetry.py
    python3 read_telemetry.py --connect udpin:127.0.0.1:14551 --count 20
"""
import argparse
import math
import sys

from pymavlink import mavutil


def parse_args():
    parser = argparse.ArgumentParser(description="Baca telemetry dasar ROV.")
    parser.add_argument(
        "--connect",
        default="udpin:127.0.0.1:14551",
        help="MAVLink connection string (default: udpin:127.0.0.1:14551).",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=0,
        help="Jumlah update yang dicetak lalu berhenti (0 = tak terbatas).",
    )
    return parser.parse_args()


def request_data_streams(master):
    """Minta Pixhawk mengirim stream data secara berkala (4 Hz)."""
    master.mav.request_data_stream_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_DATA_STREAM_ALL,
        4,  # rate Hz
        1,  # start
    )


def main():
    args = parse_args()
    print(f"Menghubungkan ke {args.connect} ...")
    master = mavutil.mavlink_connection(args.connect)

    print("Menunggu heartbeat ...")
    master.wait_heartbeat()
    print(f"Terhubung: system {master.target_system}, component {master.target_component}")
    request_data_streams(master)

    telemetry = {
        "roll": None, "pitch": None, "yaw": None,
        "depth_m": None, "voltage_v": None, "current_a": None,
    }

    printed = 0
    print("Membaca telemetry (Ctrl+C untuk berhenti) ...")
    try:
        while True:
            msg = master.recv_match(blocking=True, timeout=5)
            if msg is None:
                print("  (tidak ada data, menunggu ...)")
                continue

            mtype = msg.get_type()
            if mtype == "ATTITUDE":
                telemetry["roll"] = math.degrees(msg.roll)
                telemetry["pitch"] = math.degrees(msg.pitch)
                telemetry["yaw"] = math.degrees(msg.yaw)
            elif mtype == "SCALED_PRESSURE2":
                # bar30: tekanan absolut (hPa) -> kedalaman air tawar (approx).
                # 1 hPa ~ 1.019 cmH2O; gunakan 1013.25 hPa sebagai permukaan.
                depth_cm = (msg.press_abs - 1013.25) * 1.019716
                telemetry["depth_m"] = depth_cm / 100.0
            elif mtype in ("SYS_STATUS",):
                telemetry["voltage_v"] = msg.voltage_battery / 1000.0
                telemetry["current_a"] = msg.current_battery / 100.0
            elif mtype == "BATTERY_STATUS":
                if msg.voltages and msg.voltages[0] != 0xFFFF:
                    telemetry["voltage_v"] = msg.voltages[0] / 1000.0

            def fmt(v, unit=""):
                return f"{v:.2f}{unit}" if v is not None else "n/a"

            line = (
                f"roll={fmt(telemetry['roll'], 'deg')} "
                f"pitch={fmt(telemetry['pitch'], 'deg')} "
                f"yaw={fmt(telemetry['yaw'], 'deg')} | "
                f"depth={fmt(telemetry['depth_m'], 'm')} | "
                f"batt={fmt(telemetry['voltage_v'], 'V')} "
                f"{fmt(telemetry['current_a'], 'A')}"
            )
            print(line)

            printed += 1
            if args.count and printed >= args.count:
                break
    except KeyboardInterrupt:
        print("\nBerhenti.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
