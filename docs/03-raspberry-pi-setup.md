# 03 — Setup Raspberry Pi 4

Menyiapkan Raspberry Pi 4 Model B sebagai companion computer: OS, dependencies,
dan akses ke perangkat serial Pixhawk (`/dev/ttyACM0`).

## 1. Install Raspberry Pi OS

1. Gunakan **Raspberry Pi Imager**: <https://www.raspberrypi.com/software/>
2. Pilih **Raspberry Pi OS Lite (64-bit)** — tanpa desktop, ringan untuk ROV.
3. Di menu setting Imager (ikon gerigi), aktifkan:
   - **Enable SSH** (untuk akses tanpa monitor).
   - Set **hostname**, **username**, **password**, dan **Wi‑Fi** bila perlu.
4. Flash ke microSD, masukkan ke Pi, dan boot.

## 2. Update sistem & clone repo

SSH ke Raspberry Pi lalu:

```bash
sudo apt update && sudo apt full-upgrade -y

git clone https://github.com/customize5773/pixhawk-raspberrypi4.git
cd pixhawk-raspberrypi4
```

## 3. Jalankan skrip setup

Skrip ini meng-install Python, pip, git, build tools, dan `pymavlink`, serta
menambahkan user ke grup `dialout` agar bisa mengakses serial tanpa `sudo`.

```bash
./scripts/setup_pi.sh
```

Setelah selesai, **logout/login ulang** (atau reboot) agar keanggotaan grup
`dialout` aktif:

```bash
sudo reboot
```

## 4. Deteksi Pixhawk (`/dev/ttyACM0`)

Dengan Pixhawk terhubung ke Pi via USB dan menyala:

```bash
ls -l /dev/ttyACM*
# contoh keluaran: crw-rw---- 1 root dialout 166, 0 ... /dev/ttyACM0

# lihat detail perangkat USB
dmesg | grep -i ttyACM
lsusb
```

- Jika muncul `/dev/ttyACM0`, koneksi serial siap.
- Jika muncul sebagai `/dev/ttyACM1`, sesuaikan `Device` di
  `config/mavlink-router/main.conf`.

## 5. Cek akses tanpa sudo

Pastikan user termasuk grup `dialout`:

```bash
groups            # harus memuat "dialout"
```

Jika belum, jalankan manual lalu reboot:

```bash
sudo usermod -aG dialout "$USER"
```

## Dependencies yang di-install

| Paket | Fungsi |
| ----- | ------ |
| `python3`, `python3-pip` | Runtime & package manager Python |
| `python3-venv` | Virtual environment (opsional) |
| `git`, `build-essential` | Clone repo & kompilasi mavlink-router |
| `pymavlink` (pip) | Library MAVLink untuk skrip contoh |

> Instalasi `mavlink-router` (butuh meson/ninja) dilakukan di
> [04 - MAVLink Routing](04-mavlink-routing.md) lewat
> `scripts/install_mavlink_router.sh`.

Lanjut ke → [04 - MAVLink Routing](04-mavlink-routing.md).
