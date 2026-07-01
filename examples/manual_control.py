#!/usr/bin/env python3
"""manual_control.py — Kontrol thruster ROV pakai MANUAL_CONTROL (ArduSub).

Mengirim pesan MANUAL_CONTROL berulang untuk menggerakkan ROV. Sumbu mengikuti
konvensi ArduSub:
    x = maju/mundur (forward)   [-1000..1000]
    y = geser kiri/kanan (lateral)
    z = naik/turun (throttle)   [0..1000], 500 = netral (hover)
    r = yaw (putar)             [-1000..1000]

KEAMANAN: Default SEMUA netral (x=y=r=0, z=500) sehingga TIDAK ada gerakan.
Gerakan hanya terjadi bila argumen diberikan eksplisit. Kendaraan harus di-ARM
dulu (lihat arm_disarm.py). Uji dengan propeller dilepas.

Contoh:
    # tidak bergerak (hanya mengirim netral, aman untuk uji link):
    python3 manual_control.py --duration 3

    # maju pelan 2 detik:
    python3 manual_control.py --x 200 --duration 2

    # naik pelan (z > 500) 2 detik:
    python3 manual_control.py --z 600 --duration 2
"""
import argparse
import sys
import time

from pymavlink import mavutil


def clamp(value, low, high):
    return max(low, min(high, value))


def parse_args():
    parser = argparse.ArgumentParser(description="Kontrol manual thruster ROV.")
    parser.add_argument("--x", type=int, default=0, help="Forward/back [-1000..1000] (default 0).")
    parser.add_argument("--y", type=int, default=0, help="Lateral kiri/kanan [-1000..1000] (default 0).")
    parser.add_argument("--z", type=int, default=500, help="Throttle naik/turun [0..1000], 500=netral.")
    parser.add_argument("--r", type=int, default=0, help="Yaw [-1000..1000] (default 0).")
    parser.add_argument("--duration", type=float, default=2.0, help="Durasi kirim (detik, default 2).")
    parser.add_argument("--rate", type=float, default=10.0, help="Frekuensi kirim (Hz, default 10).")
    parser.add_argument(
        "--connect",
        default="udpin:127.0.0.1:14551",
        help="MAVLink connection string (default: udpin:127.0.0.1:14551).",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    x = clamp(args.x, -1000, 1000)
    y = clamp(args.y, -1000, 1000)
    z = clamp(args.z, 0, 1000)
    r = clamp(args.r, -1000, 1000)

    print(f"Menghubungkan ke {args.connect} ...")
    master = mavutil.mavlink_connection(args.connect)
    master.wait_heartbeat()
    print(f"Terhubung: system {master.target_system}, component {master.target_component}")

    if x == 0 and y == 0 and r == 0 and z == 500:
        print("Semua sumbu netral — mengirim perintah 'diam' (tidak ada gerakan).")

    print(f"Mengirim MANUAL_CONTROL x={x} y={y} z={z} r={r} "
          f"selama {args.duration:.1f}s @ {args.rate:.0f}Hz ...")

    period = 1.0 / args.rate
    end = time.time() + args.duration
    try:
        while time.time() < end:
            master.mav.manual_control_send(
                master.target_system,
                x, y, z, r,
                0,  # buttons: tidak ada tombol ditekan
            )
            time.sleep(period)
    except KeyboardInterrupt:
        print("\nDihentikan pengguna.")
    finally:
        # Selalu akhiri dengan perintah netral agar ROV berhenti.
        master.mav.manual_control_send(
            master.target_system, 0, 0, 500, 0, 0
        )
        print("Perintah netral dikirim. Selesai.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
