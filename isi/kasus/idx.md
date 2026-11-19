---
judul: Toolkit riset IDX — pipeline screening otomatis
tanggal: 2026-11-02
jenis: kasus
ringkas: Skrip menyaring ratusan emiten tiap pagi, menolak yang gagal gerbang halal, lalu mencatat setiap keputusan ke buku simulasi. Aturannya diuji, bukan cuma dipercaya.
peran: Sistem & strategi
durasi: ±4 bulan
stack: Python · SQLite · cron
status: Jalan tiap hari
---

## Masalah

Menyaring saham manual selalu berakhir sama: daftar hari ini berbeda dari daftar
kemarin, alasannya tidak tercatat, dan tidak ada yang bisa menjawab pertanyaan
paling penting — **apakah metodenya benar, atau cuma kebetulan sedang bagus?**

Tanpa jejak, setiap keputusan jadi cerita ulang. Yang rugi diingat sebagai
"pasar sedang jelek", yang untung diingat sebagai "analisis saya jeli".

Jadi yang saya bangun adalah **sistem yang bisa disalahkan** — yang mencatat
alasannya sendiri, dan menyimpan hasilnya walau hasilnya jelek.

## Tiga keputusan yang menentukan bentuk sistemnya

### 1. Skor, bukan daftar

Setiap emiten dinilai dengan komponen berbobot — bandarmologi, valuasi, volume,
teknikal, ROE, arus dana, momentum — lalu diurutkan. Aturannya sama tiap hari,
jadi perbedaan hasil hanya bisa berasal dari data, bukan dari suasana hati.

### 2. Gerbang halal yang menelusuri lini usaha

Label indeks syariah tidak cukup. Setiap kandidat ditelusuri bidang usahanya lewat
rantai sumber: data sektor, profil emiten, lalu pencarian langsung — dengan
kutipan sebagai bukti. Yang tidak bisa diverifikasi berstatus `unknown` dan
otomatis ditolak.

### 3. Buku simulasi sebagai hakim

Tiga buku berjalan berdampingan dengan aturan berbeda. Semua mulai dari modal
simulasi yang sama, punya batas rugi sejak posisi dibuka, dan hasilnya
dibandingkan tanpa pembelaan.

## Keadaan mesin

Diperiksa 19 Nov 2026 dari state skrip di server.

| bagian | keadaan |
| --- | --- |
| job terjadwal hari bursa | 16 aktif |
| emiten ter-cache | 625 |
| hasil audit gerbang halal | 115 lolos · 8 ditolak · 8 perlu dicek |
| kandidat ditolak (contoh terakhir) | 7 dari 25 |
| intervensi manusia | 0 |

Angka ini berubah; tanggalnya sengaja dicantumkan supaya bisa diperiksa.

Aturan strateginya saya uji di buku simulasi, terpisah dari halaman ini. Hasilnya
sengaja tidak dipublikasikan di sini — halaman ini tentang alatnya, bukan
tentang sinyal.

## Yang masih belum beres

- **Buktinya masih pendek.** Rekam jejaknya baru berjalan sejak 23 Oktober 2026 —
  itu belum membuktikan apa pun. Yang bisa dinilai sekarang adalah mesinnya,
  bukan hasilnya.
- **Harga memakai penutupan, bukan real-time.** Cukup untuk menguji aturan, tidak
  cukup untuk mengeksekusi.
- **Token bersifat pribadi.** Sistem ini bergantung pada akun data pribadi, jadi
  tidak bisa dibuka untuk umum tanpa lisensi data yang benar.
