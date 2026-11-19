---
judul: Kenapa situs ini sengaja tidak memakai framework
tanggal: 2026-11-19
jenis: blog
ringkas: Tiga halaman statis, satu permintaan, nol JavaScript. Saya ukur dua-duanya sebelum memutuskan — dan angka yang menentukan, bukan tren.
---

Klien dan teman sering bertanya kenapa portofolio ini bukan Next.js. Pertanyaan
yang wajar: saya memang membangun aplikasi Next.js untuk pekerjaan lain.

Jawabannya bukan karena saya belum bisa. Jawabannya karena saya mengukur dulu.

## Angka yang saya ukur

Saya jalankan dua-duanya di mesin yang sama, lalu catat yang terjadi.

| | situs ini | aplikasi Next.js saya |
| --- | --- | --- |
| permintaan saat dibuka | **1** | 10 |
| JavaScript terkirim | **0 KB** | **118 KB** |
| transfer total | ~31 KB | 125 KB |
| first contentful paint | **172 ms** | — |
| DOMContentLoaded | **68 ms** | 194 ms |

Aplikasi Next.js itu **perlu** 118 KB itu. Ia punya formulir, unggah berkas,
tab, dan state yang berubah. Situs ini tidak punya satu pun dari itu — satu-satunya
JavaScript di sini 20 baris, untuk menandai menu mana yang sedang dibaca saat
menggulir.

118 KB untuk menggantikan 20 baris bukan pertukaran yang menguntungkan.

## Yang sering dianggap masalah, tapi bukan

Kekhawatiran berikutnya biasanya soal perawatan: tanpa komponen, CSS-nya
berulang di tiap halaman, bukan?

Saya periksa. Dari tiga halaman, deklarasi CSS yang identik di ketiganya:
**satu baris.** Palet `:root` memang disalin tiga kali — enam baris. Itu 2% dari
berkas pertama, bukan masalah.

"Berulang" jadi masalah ketika halamannya ratusan. Di tiga halaman, itu bukan
biaya — itu kesederhanaan.

## Kapan jawabannya berubah

Saya tidak akan mempertahankan pilihan ini demi gengsi. Tiga hal membaliknya:

1. **Ada bagian yang butuh data.** Daftar proyek dari API, atau halaman yang
   tumbuh tanpa saya sentuh HTML-nya.
2. **Isinya berubah terus, dan saya lelah menyunting HTML.** Itu sebabnya tulisan
   dan studi kasus di situs ini sekarang ditulis di markdown — saya hanya
   menyentuh HTML kalau bentuk halamannya berubah.
3. **Klien yang saya bidik menanyakan stack-nya.** Sewaktu kecil, tidak.

Perhatikan bahwa alasan nomor dua sudah terjadi, dan saya menyelesaikannya
**tanpa** framework: markdown jadi HTML saat dibangun, dan hasilnya tetap berkas
statis. Yang dinamis hanya saat menulis, bukan saat dibaca.

## Yang sebenarnya saya jual di sini

Ada godaan untuk menjadikan situs ini pajangan teknologi. Klien teknis akan
menilai stack-nya, jadi pakai yang modern.

Tapi ada versi argumen itu yang berlawanan arah. Situs yang memutuskan
arsitekturnya dengan angka yang bisa diperiksa membuktikan penilaian. Situs yang
menyalakan framework untuk tiga halaman statis membuktikan bisa menyalakan
framework — dan itu bukan hal yang sama.

Saya menjual kemampuan mengambil proses manual dan membuatnya jalan sendiri,
dengan batas yang jelas. **Keputusan soal alat adalah bagian dari pekerjaan itu.**
Jadi keputusan di sini saya catat di `README`, bukan disembunyikan — supaya bisa
dibantah, dan supaya saya tidak mengulang perdebatan yang sama enam bulan lagi.
