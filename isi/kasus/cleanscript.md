---
judul: CleanScript — mesin pembersih data Excel/CSV
tanggal: 2026-11-02
jenis: kasus
ringkas: File kotor masuk, workbook rapi keluar. 21 format tanggal, CSV titik-koma, sel error Excel — dibersihkan otomatis, dan yang tidak bisa diperbaiki dilaporkan bukan dihapus.
peran: Desain & backend
durasi: ±6 minggu
stack: Python · Pandas · FastAPI
status: Dipakai sendiri
---

## Masalah

Pemilik usaha mengirim file yang terlihat wajar di Excel. Di dalamnya: tanggal yang
setengahnya teks, angka dengan "Rp" dan titik ribuan, baris judul di atas header,
dan kolom yang isinya campur antara nilai dan `#REF!`.

Membersihkan manual butuh 30–60 menit per file — dan hasilnya tidak bisa diaudit.
Kalau ada satu baris hilang, tidak ada yang tahu.

**Yang saya jaga: setiap perubahan harus bisa ditunjuk balik ke baris asalnya.**
Cepat tapi tidak bisa dilacak, buat saya belum selesai.

## Tiga keputusan yang menentukan bentuk aplikasi

### 1. Deteksi format, bukan menebak

Parser mendukung 21 format tanggal: nama bulan Indonesia (termasuk `Peb`, `Agt`,
`Nop`), nama hari, format ringkas `YYYYMMDD`, serial Excel 20000–60000, dan ISO+Z
yang dipaksa year-first supaya `2026-10-12T08:15:30Z` tidak terbaca Desember.

### 2. Sampling 200 nilai, bukan seluruh file

Deteksi kolom angka memakai sampel. Efeknya pada file 5.000 × 20: inspeksi
**7,8 detik → 4,5 detik**. Placeholder seperti `#REF!`, `-`, `N/A` tidak dihitung
sebagai "bukan angka", supaya satu kolom uang yang punya 3 sel rusak tetap
terdeteksi sebagai uang.

### 3. Audit, bukan hapus diam-diam

Baris bermasalah tidak dibuang. Ia masuk sheet keempat — `Data_Perlu_Dicek` —
berisi lokasi baris, kolom, nilai asli, dan jenis masalahnya. Tanggal mustahil
seperti `31/02/2026` dibiarkan apa adanya dengan tanda, bukan dikoreksi tanpa izin.

## Bukti

File 5.000 baris × 20 kolom, campuran tanggal rusak, angka berformat, dan sel error.

<figure>
<img src="shots-deploy/02-clean.png" width="1280" height="577" alt="Layar CleanScript: file kotor_penjualan.csv 12 baris 7 kolom, terdeteksi 2 baris kosong dan 4 baris duplikat, tabel menampilkan tanggal campur format dan angka Rp 1.250.000">
<figcaption>Tangkapan layar asli dari aplikasi yang berjalan, memakai file uji <span class="mono">kotor_penjualan.csv</span>.</figcaption>
</figure>

<figure>
<img src="shots-deploy/03-hasil.png" width="1280" height="577" alt="Layar pengaturan aturan pembersihan CleanScript: hapus baris kosong, rapikan spasi, normalisasi kapitalisasi, hapus duplikat identik, standarisasi tanggal, normalisasi angka dan uang, serta opsi AI insight DeepSeek">
<figcaption>Aturan yang bisa dipilih sebelum dijalankan. Tidak ada yang diubah tanpa Anda centang — AI hanya menjelaskan, tidak pernah mengubah data sendiri.</figcaption>
</figure>

| ukuran | hasil |
| --- | --- |
| inspeksi file 5.000 × 20 | 7,8 s → **4,5 s** |
| test otomatis | **114 lulus** |
| sheet keluaran | Data_Cleaned · Cleaning_Report · Data_Summary · Data_Perlu_Dicek |
| format tanggal didukung | 21 |

Contoh hasil nyata pada `kotor_penjualan.csv`: 12 baris → 7 baris, 5 baris dibuang
(2 kosong + 3 duplikat berbeda), 7 baris diubah, 1 sel masuk `Data_Perlu_Dicek`.
Serial Excel `45678` → `2025-01-21`.

## Yang masih belum beres

- **Nomor HP belum diseragamkan.** Kolom nomor telepon keluar apa adanya —
  `0812-3456-7890`, `081298765432`, `0813 1111 2222` tetap berbeda-beda. Padahal
  itu kolom yang paling sering mau dipakai untuk kirim WhatsApp massal.
- **Jam rusak membuang tanggal valid.** `2026-10-12 25:99` tetap jadi 2026-10-12,
  tapi penanda jamnya hilang tanpa catatan.
- **File 10 MB ke atas.** Di atas 5.000 baris, waktu proses mulai terasa; target
  berikutnya adalah pemrosesan bertahap, bukan sekaligus.
