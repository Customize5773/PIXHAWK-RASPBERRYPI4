# 04 — MAVLink Routing (mavlink-router)

`mavlink-router` adalah router MAVLink ringan yang membaca stream dari Pixhawk
(USB) dan membagikannya ke banyak endpoint sekaligus — QGroundControl di topside
**dan** skrip `pymavlink` lokal — tanpa saling merebut port serial.

## Kenapa butuh router?

Port serial `/dev/ttyACM0` hanya bisa dibuka oleh **satu** proses. Kalau QGC
memakainya, skrip Python tidak bisa, dan sebaliknya. `mavlink-router` membuka
serial **satu kali** lalu mem-*fan-out* datanya lewat UDP.

```
/dev/ttyACM0 ──► mavlink-router ──┬──► UDP :14550  (QGC topside)
                                  └──► UDP :14551  (skrip pymavlink lokal)
```

## 1. Install mavlink-router

Jalankan skrip (clone, build via meson/ninja, install):

```bash
./scripts/install_mavlink_router.sh
```

Skrip ini:
- Meng-install dependency build (`meson`, `ninja-build`, `pkg-config`, `git`, `g++`).
- Clone `https://github.com/mavlink-router/mavlink-router` (dengan submodule).
- Build & `sudo ninja install` sehingga binary `mavlink-routerd` tersedia.

Verifikasi:

```bash
mavlink-routerd --version
```

## 2. Pasang konfigurasi

Salin `main.conf` dari repo ke lokasi default:

```bash
sudo mkdir -p /etc/mavlink-router
sudo cp config/mavlink-router/main.conf /etc/mavlink-router/main.conf
```

Isi `config/mavlink-router/main.conf`:

```ini
[General]
TcpServerPort=5760
ReportStats=false

# Sumber: Pixhawk 2.4.8 via USB
[UartEndpoint pixhawk]
Device = /dev/ttyACM0
Baud = 115200

# Topside: QGroundControl (ganti 192.168.2.1 dengan IP laptop topside)
[UdpEndpoint qgc]
Mode = Normal
Address = 192.168.2.1
Port = 14550

# Lokal: konsumsi skrip pymavlink di Raspberry Pi
[UdpEndpoint onboard]
Mode = Normal
Address = 127.0.0.1
Port = 14551
```

**Sesuaikan:**
- `Device` → ubah bila Pixhawk muncul sebagai `/dev/ttyACM1`.
- `Address` pada `[UdpEndpoint qgc]` → **IP laptop topside** (lihat
  [05 - Ground Station](05-ground-station.md)).

## 3. Jalankan sebagai service (systemd)

Agar router otomatis jalan saat boot:

```bash
sudo cp config/systemd/mavlink-router.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now mavlink-router
```

Cek status & log:

```bash
systemctl status mavlink-router
journalctl -u mavlink-router -f
```

## 4. Uji manual (tanpa systemd)

Untuk debugging, jalankan langsung di foreground:

```bash
mavlink-routerd -c /etc/mavlink-router/main.conf
```

Hentikan dengan `Ctrl+C`.

## Verifikasi

- Log mavlink-router menunjukkan endpoint UART terbuka dan menerima heartbeat.
- Dari Pi: `python3 examples/heartbeat_listener.py` (connect ke `udpin:127.0.0.1:14551`)
  mencetak HEARTBEAT.
- Dari topside: QGC otomatis mendeteksi kendaraan di UDP `14550`.

Jika tidak ada heartbeat, lihat [06 - Troubleshooting](06-troubleshooting.md).

Lanjut ke → [05 - Ground Station](05-ground-station.md).
