# 05 — Ground Station (QGroundControl topside)

Menghubungkan **QGroundControl (QGC)** di laptop/PC topside ke ROV melalui
Raspberry Pi lewat tether Ethernet. QGC menerima MAVLink di UDP `14550` yang
diteruskan oleh `mavlink-router`.

## Topologi jaringan

```
[ Laptop topside ]  eth  ─── tether ───  eth  [ Raspberry Pi 4 ]  USB  [ Pixhawk ]
   192.168.2.1                                   192.168.2.2
        ▲                                             │
        └──────────── UDP :14550 (MAVLink) ◄──── mavlink-router
```

Gunakan subnet statis sederhana, mis. `192.168.2.0/24`:

| Perangkat | IP | Keterangan |
| --------- | -- | ---------- |
| Laptop topside | `192.168.2.1` | Menjalankan QGroundControl |
| Raspberry Pi 4 | `192.168.2.2` | Menjalankan mavlink-router |

## 1. Set IP statis di Raspberry Pi

Contoh dengan `dhcpcd` (Raspberry Pi OS). Tambahkan di `/etc/dhcpcd.conf`:

```ini
interface eth0
static ip_address=192.168.2.2/24
```

Lalu:

```bash
sudo systemctl restart dhcpcd
ip addr show eth0
```

> Untuk instalasi Raspberry Pi OS berbasis NetworkManager, gunakan
> `nmcli` untuk menetapkan IP statis pada `eth0`.

## 2. Set IP statis di laptop topside

Set adapter Ethernet laptop ke IP `192.168.2.1`, netmask `255.255.255.0`.
(Windows: Network Settings → IPv4 manual; Linux: `nmcli`/netplan; macOS: System
Settings → Network.)

Uji konektivitas:

```bash
ping 192.168.2.2   # dari laptop, harus membalas
```

## 3. Pastikan mavlink-router mengarah ke topside

Di `config/mavlink-router/main.conf`, endpoint QGC harus menunjuk IP laptop:

```ini
[UdpEndpoint qgc]
Mode = Normal
Address = 192.168.2.1
Port = 14550
```

Restart service bila diubah:

```bash
sudo systemctl restart mavlink-router
```

## 4. Hubungkan QGroundControl

QGC secara default mendengarkan UDP `14550` dan otomatis mendeteksi kendaraan.
Jika perlu link manual:

1. QGC → **Application Settings** → **Comm Links** → **Add**.
2. Type: **UDP**, Port: `14550`.
3. (Opsional) tambahkan **Target Host** `192.168.2.2:14550`.
4. **Connect**.

Setelah terhubung, QGC menampilkan kendaraan **Sub**, attitude, kedalaman, dan
status baterai.

## Verifikasi end-to-end

- QGC menampilkan telemetry live dari Pixhawk.
- Bersamaan, di Raspberry Pi skrip `python3 examples/read_telemetry.py`
  tetap bisa membaca data (lewat endpoint lokal `14551`) — membuktikan routing
  fan-out bekerja.

Jika QGC tidak mendeteksi kendaraan, lihat [06 - Troubleshooting](06-troubleshooting.md).
