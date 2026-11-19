# IKONA — portofolio

Situs portofolio statis, tiga halaman, tanpa build step. Buka `index.html`
langsung di browser atau host sebagai berkas statis.

## Isi

- `index.html` — beranda: layanan & harga, kerja, cara kerja, tentang, kontak
- `kasus-cleanscript.html` — studi kasus 01: pembersih data Excel/CSV
- `kasus-idx.html` — studi kasus 02: pipeline riset pasar saham
- `og.png` — kartu pratinjau 1200×630 untuk WhatsApp/X/LinkedIn
- `og-card.html` — sumber kartu itu (buka di browser, tangkap layar bila perlu dirender ulang)
- `shots-deploy/` — tangkapan layar asli aplikasi, dipakai di halaman studi kasus
- `arsip/` — tema yang tidak dipakai, disimpan sebagai riwayat desain

## Konvensi

**Tidak ada build step.** CSS ditulis inline di tiap halaman supaya berkasnya bisa
dibuka langsung tanpa server. Kalau mengubah satu halaman, periksa halaman lain —
`og.png` dibuat dari `og-card.html` secara manual, jadi hero dan kartunya bisa
ketinggalan satu sama lain.

**Angka di halaman harus bisa diperiksa.** Setiap angka yang bisa dihitung
(jumlah tes, jumlah job, cacah data) diambil dari keadaan sebenarnya, bukan
perkiraan. Bila angka berasal dari pemeriksaan pada tanggal tertentu,
tanggalnya ditulis di halaman. Jangan menambah angka yang tidak bisa ditunjukkan.

**Palet.** Kertas `#F6F4EC`, tinta `#141413`, garis `#DCD6C4`, aksen terakota
`#A8492F`. Terakota adalah aksen "perhatikan" — pakai satu kali per layar,
jangan menyebar. Seluruh pasangan warna sudah lolos WCAG AA.

**Sentuh.** Semua kontrol minimal 44px. Header melekat setinggi 98px di layar
kecil, karena itu `html{scroll-padding-top:104px}` wajib ada supaya tautan
anchor tidak tertutup.

## Sebelum mengirim tautan ke siapa pun

- [ ] Nomor WhatsApp sudah nomor asli (cari `62XXXXXXXXXX` — ada 5 tempat)
- [ ] Alamat email sudah alamat asli (cari `halo@ikona.dev`)
- [ ] `rel="canonical"` menunjuk domain yang benar (sekarang `ikona.dev`)
- [ ] Kartu pratinjau `og.png` masih cocok dengan hero di `index.html`

## Menyunting

Berkasnya HTML biasa. Yang perlu diperhatikan:

- **Halaman kasus memakai struktur nomor sendiri** (01 Masalah, 02 Keputusan, dst).
  Beranda juga bernomor (01 Layanan, 02 Kerja, 03 Cara kerja, 04 Tentang). Kalau
  menambah bagian di tengah, nomor setelahnya harus ikut diubah.
- **`<main>` dan `<header>`**: tiap halaman hanya boleh punya satu `<main>` dan
  satu `<header>` puncak. Landmark ganda membingungkan pembaca layar.
