# PIXHAWK-RASPBERRYPI4

Setup dan tooling untuk membangun jalur komunikasi antara **Pixhawk 2.4.8**
(flight controller, firmware **ArduSub**) dan **Raspberry Pi 4 Model B**
(companion computer) untuk keperluan **ROV** (Remotely Operated Vehicle).

Repo ini menyediakan **dokumentasi lengkap**, **skrip setup otomatis**, **file
konfigurasi**, dan **contoh kode `pymavlink`** — semuanya memakai pendekatan
manual (bukan image jadi seperti BlueOS) supaya setiap komponen jalur MAVLink
transparan dan mudah dipahami.

## Arsitektur

```
        [ QGroundControl - Laptop / PC topside ]
                        │
                        │  UDP :14550  (via tether Ethernet)
                        ▼
        [ Raspberry Pi 4 Model B ]  ── mavlink-router (router MAVLink)
             │                     └── UDP :14551 (lokal) ──► skrip pymavlink
             │  USB  (/dev/ttyACM0)
             ▼
        [ Pixhawk 2.4.8 - ArduSub ]
             │
             └── ESC + thruster, sensor kedalaman (bar30), IMU, dll.
```

`mavlink-router` berjalan di Raspberry Pi, membaca stream MAVLink dari Pixhawk
lewat **USB**, lalu mem-*fan-out* ke dua arah:

- **QGroundControl** di topside (UDP `14550`) lewat tether Ethernet — untuk
  kontrol manual, kalibrasi, dan monitoring.
- **Endpoint lokal** (UDP `127.0.0.1:14551`) — dikonsumsi skrip `pymavlink` di
  Pi untuk otomasi/telemetry, **tanpa** merebut port serial dari QGC.

## Hardware yang dibutuhkan

| Komponen                     | Keterangan                                             |
| ---------------------------- | ------------------------------------------------------ |
| Pixhawk 2.4.8                | Flight controller, di-flash firmware ArduSub           |
| Raspberry Pi 4 Model B       | Companion computer (2GB+ RAM cukup)                    |
| microSD 16GB+                | Untuk Raspberry Pi OS                                   |
| Kabel USB (micro-USB → USB-A)| Pixhawk (port USB) ↔ Raspberry Pi 4                     |
| Tether Ethernet + adapter    | Jalur data Pi ↔ topside (Fathom-X / kabel Ethernet)   |
| Power supply 5V/3A (Pi)      | Catu daya stabil untuk Raspberry Pi                    |
| ESC + thruster, bar30, dll.  | Aktuator & sensor ROV (terhubung ke Pixhawk)           |

## Quick Start

Ikuti berurutan:

1. **Wiring & hardware** — sambungkan Pixhawk ke Pi via USB.
   → [`docs/01-hardware-wiring.md`](docs/01-hardware-wiring.md)
2. **Flash firmware ArduSub** ke Pixhawk lewat QGroundControl.
   → [`docs/02-firmware-ardusub.md`](docs/02-firmware-ardusub.md)
3. **Siapkan Raspberry Pi** (OS + dependencies):
   ```bash
   git clone https://github.com/customize5773/pixhawk-raspberrypi4.git
   cd pixhawk-raspberrypi4
   ./scripts/setup_pi.sh
   ```
   → [`docs/03-raspberry-pi-setup.md`](docs/03-raspberry-pi-setup.md)
4. **Install & konfigurasi mavlink-router**:
   ```bash
   ./scripts/install_mavlink_router.sh
   sudo cp config/mavlink-router/main.conf /etc/mavlink-router/main.conf
   sudo cp config/systemd/mavlink-router.service /etc/systemd/system/
   sudo systemctl enable --now mavlink-router
   ```
   → [`docs/04-mavlink-routing.md`](docs/04-mavlink-routing.md)
5. **Hubungkan QGroundControl** dari laptop topside (UDP `14550`).
   → [`docs/05-ground-station.md`](docs/05-ground-station.md)
6. **Verifikasi & jalankan contoh**:
   ```bash
   ./scripts/check_connection.sh
   python3 examples/heartbeat_listener.py
   python3 examples/read_telemetry.py
   ```

## Struktur repo

```
.
├── docs/        # panduan langkah demi langkah
├── scripts/     # skrip setup & pengecekan (bash)
├── config/      # konfigurasi mavlink-router + systemd service
└── examples/    # contoh kontrol/telemetry pakai pymavlink
```

## Dokumentasi

| Dokumen | Isi |
| ------- | --- |
| [01 - Hardware & Wiring](docs/01-hardware-wiring.md) | Koneksi USB Pixhawk ↔ Pi, power, tether, catatan grounding |
| [02 - Firmware ArduSub](docs/02-firmware-ardusub.md) | Flash ArduSub via QGC, parameter dasar ROV |
| [03 - Setup Raspberry Pi](docs/03-raspberry-pi-setup.md) | OS, dependencies, deteksi `/dev/ttyACM0`, akses serial |
| [04 - MAVLink Routing](docs/04-mavlink-routing.md) | Build/install mavlink-router, `main.conf`, systemd |
| [05 - Ground Station](docs/05-ground-station.md) | Konfigurasi QGroundControl topside, jaringan tether |
| [06 - Troubleshooting](docs/06-troubleshooting.md) | Masalah umum & solusinya |

## Catatan keamanan

- Selalu uji ROV **di darat / di ember** dulu sebelum diturunkan ke air.
- `examples/manual_control.py` default bernilai **netral** (tidak menggerakkan
  thruster). Gerakan hanya terjadi bila argumen diberikan secara eksplisit.
- Pastikan kill switch / disarm mudah dijangkau saat pengujian.

## Lisensi

Lihat [LICENSE](LICENSE).
