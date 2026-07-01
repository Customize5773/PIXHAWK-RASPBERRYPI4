# 02 — Firmware ArduSub

Pixhawk untuk ROV memakai firmware **ArduSub** (bagian dari ArduPilot,
khusus kendaraan bawah air). Firmware ini di-flash **satu kali** ke Pixhawk;
Raspberry Pi tidak perlu di-flash.

## Kenapa ArduSub?

- Mendukung frame ROV (Vectored, BlueROV2, dll.) dan kontrol thruster.
- Mode depth-hold, stabilize, manual — cocok untuk ROV.
- Kompatibel dengan MAVLink sehingga bisa dirouting oleh Raspberry Pi.

## Cara flash (via QGroundControl)

Flashing paling mudah dilakukan dari **komputer topside** memakai QGroundControl
(QGC), dengan Pixhawk terhubung langsung ke laptop lewat USB.

1. Install **QGroundControl** di laptop:
   <https://docs.qgroundcontrol.com/master/en/qgc-user-guide/getting_started/download_and_install.html>
2. Sambungkan Pixhawk 2.4.8 ke laptop via USB (lepas dulu dari Raspberry Pi).
3. Buka QGC → **Vehicle Setup** → **Firmware**.
4. Cabut lalu colok ulang USB Pixhawk saat diminta QGC.
5. Pilih **ArduPilot** → jenis kendaraan **Sub (ArduSub)** → versi stabil terbaru.
6. Tunggu proses flashing selesai (jangan cabut USB saat berjalan).

> Alternatif: gunakan firmware `.apj` ArduSub dari
> <https://firmware.ardupilot.org/Sub/> lalu pilih "Advanced settings → custom
> firmware file" di QGC.

## Parameter dasar ROV (via QGC)

Setelah flashing, lakukan setup awal di QGC (**Vehicle Setup**):

- **Frame**: pilih konfigurasi thruster ROV (mis. *Vectored 6 DOF* / sesuai rangka).
- **Sensors**: kalibrasi **Accelerometer** dan **Compass**.
- **Radio/Joystick**: pasangkan joystick untuk kontrol manual (opsional tapi disarankan).
- **Power**: set parameter power module (tegangan/arus baterai).
- **Failsafe**: konfigurasi failsafe baterai & kehilangan link.

Parameter penting yang relevan dengan komunikasi:

| Parameter | Nilai umum | Keterangan |
| --------- | ---------- | ---------- |
| `SERIAL0_BAUD` | `115` (115200) | Baud port USB Pixhawk |
| `BRD_SER1_RTSCTS` | `0` | Nonaktifkan flow control jika tidak dipakai |

> Untuk koneksi USB, baud efektif seringkali fleksibel, namun setel
> `115200` di `main.conf` agar konsisten (lihat [04](04-mavlink-routing.md)).

## Verifikasi

- Di QGC, pastikan Pixhawk terdeteksi sebagai kendaraan **Sub** dan mengirim
  telemetry (attitude, baterai).
- Setelah terverifikasi, pindahkan koneksi USB Pixhawk dari laptop ke
  **Raspberry Pi 4** untuk operasi companion.

Lanjut ke → [03 - Setup Raspberry Pi](03-raspberry-pi-setup.md).
