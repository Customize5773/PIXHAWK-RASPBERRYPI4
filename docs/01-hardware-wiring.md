# 01 — Hardware & Wiring

Panduan menyambungkan **Pixhawk 2.4.8** ke **Raspberry Pi 4 Model B** untuk ROV.
Repo ini memakai koneksi **USB** (plug-and-play) sesuai keputusan setup.

## Daftar hardware

| Komponen | Catatan |
| -------- | ------- |
| Pixhawk 2.4.8 | Flight controller utama |
| Raspberry Pi 4 Model B | Companion computer |
| Kabel USB (micro-USB → USB-A) | Dari port **USB** Pixhawk ke port USB Raspberry Pi |
| Power 5V/3A untuk Pi | Gunakan catu daya stabil (BEC/UBEC berkualitas atau power module) |
| Tether Ethernet | Jalur data ke topside (mis. pasangan Fathom-X, atau kabel Ethernet langsung untuk uji darat) |

## Koneksi USB Pixhawk ↔ Raspberry Pi

```
Pixhawk 2.4.8  ──(port USB / micro-USB)──►  Raspberry Pi 4 (port USB-A)
```

1. Colokkan ujung **micro-USB** ke port USB pada Pixhawk (port yang sama untuk
   flashing firmware).
2. Colokkan ujung **USB-A** ke salah satu port USB Raspberry Pi 4.
3. Saat Pixhawk menyala dan terhubung, ia akan muncul di Pi sebagai
   perangkat serial **`/dev/ttyACM0`** (kadang `/dev/ttyACM1`).

> Koneksi USB menyediakan jalur data **dan** memberi daya ke logic Pixhawk.
> Untuk operasi nyata, Pixhawk tetap butuh power module untuk ESC/servo rail.

## Power

- **Raspberry Pi 4** butuh 5V dengan arus stabil (idealnya 3A). Tegangan drop
  saat under-voltage sering menyebabkan port USB tidak stabil dan `/dev/ttyACM0`
  hilang-timbul. Gunakan UBEC/BEC berkualitas.
- **Pixhawk** diberi daya lewat power module (untuk membaca tegangan/arus
  baterai). Jangan hanya mengandalkan daya dari USB Pi untuk beban penuh.

## Grounding (penting untuk ROV)

- Pastikan **ground bersama** (common ground) antara sistem power Pi dan
  Pixhawk untuk menghindari noise pada jalur USB/serial.
- Pisahkan kabel daya thruster (arus besar) dari kabel sinyal/USB untuk
  mengurangi interferensi.
- Di dalam enclosure ROV, rapikan kabel dan hindari loop ground yang panjang.

## Tether ke topside

- Raspberry Pi terhubung ke topside lewat **Ethernet** melalui tether.
  Untuk uji darat, cukup kabel Ethernet langsung Pi ↔ laptop.
- Konfigurasi IP jaringan dibahas di [05 - Ground Station](05-ground-station.md).

## Verifikasi cepat

Setelah semuanya tersambung dan Pi menyala, cek perangkat serial muncul:

```bash
ls -l /dev/ttyACM*
# harusnya menampilkan /dev/ttyACM0
```

Jika tidak muncul, lihat [06 - Troubleshooting](06-troubleshooting.md).

Lanjut ke → [02 - Firmware ArduSub](02-firmware-ardusub.md).
