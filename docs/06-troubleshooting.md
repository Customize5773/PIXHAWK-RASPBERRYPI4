# 06 — Troubleshooting

Masalah umum saat setup komunikasi Pixhawk 2.4.8 ↔ Raspberry Pi 4 dan solusinya.

## `/dev/ttyACM0` tidak muncul

**Gejala:** `ls /dev/ttyACM*` kosong.

- Pastikan Pixhawk menyala dan kabel USB tersambung dengan benar.
- Coba port USB lain / kabel lain (banyak kabel micro-USB hanya untuk charging,
  bukan data).
- Cek log kernel:
  ```bash
  dmesg | grep -iE "ttyACM|usb"
  lsusb
  ```
- Under-voltage pada Pi bisa memutus USB. Gunakan power 5V/3A stabil dan cek:
  ```bash
  vcgencmd get_throttled   # 0x0 berarti sehat
  ```
- Jika muncul sebagai `/dev/ttyACM1`, sesuaikan `Device` di `main.conf`.

## Permission denied saat akses serial

**Gejala:** `Permission denied: '/dev/ttyACM0'`.

- User harus masuk grup `dialout`:
  ```bash
  sudo usermod -aG dialout "$USER"
  ```
- **Logout/login ulang atau reboot** agar keanggotaan grup aktif.
- Verifikasi: `groups` harus memuat `dialout`.

## Tidak ada HEARTBEAT

**Gejala:** `heartbeat_listener.py` menggantung; QGC tidak mendeteksi kendaraan.

- Pastikan **hanya mavlink-router** yang membuka `/dev/ttyACM0` (bukan QGC/skrip
  langsung ke serial). Hentikan proses lain:
  ```bash
  sudo lsof /dev/ttyACM0
  ```
- Cek service router jalan & log-nya:
  ```bash
  systemctl status mavlink-router
  journalctl -u mavlink-router -f
  ```
- Cek baud di `main.conf` (`115200`) sesuai. Untuk USB biasanya toleran, tapi
  konsistenkan.
- Pastikan skrip connect ke **`udpin:127.0.0.1:14551`** (endpoint lokal), bukan
  ke serial.

## QGC tidak mendeteksi kendaraan

- Pastikan `Address` di `[UdpEndpoint qgc]` = IP laptop topside yang benar.
- Uji jaringan: `ping` dua arah antara Pi dan laptop berhasil.
- Cek firewall laptop tidak memblokir UDP `14550`.
- Restart mavlink-router setelah mengubah `main.conf`:
  ```bash
  sudo systemctl restart mavlink-router
  ```

## mavlink-router gagal build

- Pastikan dependency terpasang: `meson`, `ninja-build`, `pkg-config`, `g++`, `git`.
- Ambil submodule saat clone: `git clone --recurse-submodules ...`
  (skrip `install_mavlink_router.sh` sudah menanganinya).
- Versi meson terlalu lama → update via pip: `pip3 install --user meson`.

## Konflik dua endpoint / data ganda

- Pastikan tidak menjalankan `mavlink-routerd` manual **dan** service systemd
  bersamaan (dua-duanya membuka serial → konflik).
  ```bash
  sudo systemctl stop mavlink-router   # sebelum uji manual
  ```

## Skrip pymavlink error import

- Install ulang di environment yang benar:
  ```bash
  pip3 install -r examples/requirements.txt
  ```
- Jika pakai virtualenv, aktifkan dulu sebelum menjalankan skrip.

## Referensi

- ArduSub: <https://www.ardusub.com/>
- mavlink-router: <https://github.com/mavlink-router/mavlink-router>
- pymavlink: <https://mavlink.io/en/mavgen_python/>
