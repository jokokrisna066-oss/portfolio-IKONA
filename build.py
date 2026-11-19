#!/usr/bin/env python3
"""build.py — markdown -> HTML statis untuk situs IKONA.

Menulis di markdown, menghasilkan HTML biasa. Tidak ada framework, tidak ada
JS tambahan, tidak ada build di server: hasilnya berkas statis yang bisa
diunggah apa adanya.

Pakai:
    python3 build.py              # bangun semua
    python3 build.py --bersih     # hapus hasil, bangun ulang
    python3 build.py --periksa    # gagal kalau ada tautan/berkas rusak

Sumber : isi/            (markdown)
Hasil  : index.html, artikel/*.html, artikel/index.html
Template: tpl/           (kerangka halaman)
"""
import argparse
import html
import json
import re
import shutil
import sys
from datetime import date, datetime
from pathlib import Path

import markdown

AKAR = Path(__file__).resolve().parent
ISI = AKAR / "isi"
TPL = AKAR / "tpl"
ARTIKEL = AKAR / "artikel"

# Judul situs, dipakai di <title> dan header
NAMA = "IKONA"

# ----------------------------------------------------------------------------
# frontmatter: sederhana, sengaja. Hanya kunci: nilai, tanpa dependensi YAML.
# ----------------------------------------------------------------------------

def pisah_frontmatter(teks: str) -> tuple[dict, str]:
    """Ambil blok --- di awal berkas. Mengembalikan (meta, sisa_teks)."""
    if not teks.startswith("---"):
        return {}, teks
    akhir = teks.find("\n---", 3)
    if akhir == -1:
        raise ValueError("frontmatter dibuka dengan --- tapi tidak ditutup")
    blok = teks[3:akhir].strip()
    sisa = teks[akhir + 4:].lstrip("\n")
    meta = {}
    for baris in blok.splitlines():
        if not baris.strip() or baris.lstrip().startswith("#"):
            continue
        if ":" not in baris:
            raise ValueError(f"baris frontmatter tanpa titik dua: {baris!r}")
        k, v = baris.split(":", 1)
        meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta, sisa


def wajib(meta: dict, kunci: list[str], berkas: Path) -> None:
    kurang = [k for k in kunci if not meta.get(k)]
    if kurang:
        raise ValueError(f"{berkas.name}: frontmatter kurang {' ,'.join(kurang)}")


# ----------------------------------------------------------------------------
# markdown -> html
# ----------------------------------------------------------------------------

MD = markdown.Markdown(
    extensions=["extra", "smarty", "toc", "attr_list", "md_in_html"],
    extension_configs={"toc": {"toc_depth": "2-3"}},
)

SLUG_OK = re.compile(r"[^a-z0-9]+")


def slug(teks: str) -> str:
    return SLUG_OK.sub("-", teks.lower()).strip("-")


def render_md(teks: str) -> tuple[str, str]:
    """Mengembalikan (html, daftar_isi)."""
    MD.reset()
    keluaran = MD.convert(teks)
    return keluaran, getattr(MD, "toc", "")


# ----------------------------------------------------------------------------
# pemakaian ulang potongan template
# ----------------------------------------------------------------------------

def baca(nama: str) -> str:
    return (TPL / nama).read_text(encoding="utf-8")


def ganti(tpl: str, nilai: dict) -> str:
    """Isi {{kunci}}. Sengaja tidak memakai mesin template — cukup untuk ini."""
    for k, v in nilai.items():
        tpl = tpl.replace("{{" + k + "}}", v)
    return tpl


# ----------------------------------------------------------------------------
# membangun
# ----------------------------------------------------------------------------

def bangun_indeks(artikel: list[dict]) -> None:
    """Halaman daftar di artikel/index.html."""
    tulis = [a for a in artikel if a["jenis"] == "blog"]
    tulis.sort(key=lambda a: a["tanggal"], reverse=True)
    kartu = "\n".join(
        f'        <a class="item" href="{a["tautan"].split("/",1)[1]}">\n'
        f'          <div class="n">{a["tanggal"].strftime("%d.%m")}</div>\n'
        f'          <div>\n            <h3>{html.escape(a["judul"])}</h3>\n'
        f'            <p>{html.escape(a["ringkas"])}</p>\n          </div>\n'
        f'          <span class="go" aria-hidden="true">→</span>\n        </a>'
        for a in tulis)

    # Halaman daftar memakai kerangka artikel dengan isi berupa daftar
    kepala = baca("artikel.html")
    isi = (
        '<div class="daftar">\n' + (kartu or '<p>Belum ada tulisan.</p>') + "\n</div>"
    )
    ARTIKEL.mkdir(exist_ok=True)
    (ARTIKEL / "index.html").write_text(ganti(kepala, {
        "JUDUL": "Tulisan",
        "RINGKAS": "Catatan soal pekerjaan yang berulang, keputusan teknis, dan apa yang saya pelajari waktu membangunnya.",
        "TANGGAL_ISO": date.today().isoformat(),
        "TANGGAL_TAMPIL": date.today().strftime("%d %b %Y"),
        "JENIS": "blog", "JENIS_LABEL": "Daftar tulisan",
        "KANONIK": "https://ikona.dev/artikel/",
        "TAUTAN": "artikel/index.html", "AKAR": "../",
        "MENIT": "0", "TOC": "", "ISI": isi,
    }), encoding="utf-8")
    print(f"  artikel/index.html ({len(tulis)} tulisan)")


def bangun_artikel() -> list[dict]:
    """Setiap .md di isi/ jadi satu halaman. Sub-folder jadi kategori."""
    kepala = baca("artikel.html")
    hasil = []

    for berkas in sorted(ISI.rglob("*.md")):
        mentah = berkas.read_text(encoding="utf-8")
        meta, teks = pisah_frontmatter(mentah)
        wajib(meta, ["judul", "tanggal", "ringkas"], berkas)

        jenis = meta.get("jenis") or ("kasus" if berkas.parent.name == "kasus" else "blog")
        isi_html, toc = render_md(teks)

        # Halaman kasus di tingkat atas (kasus-cleanscript.html) supaya tautan
        # lama tidak mati; blog masuk ke artikel/.
        if jenis == "kasus":
            keluar = AKAR / f"kasus-{berkas.stem}.html"
            tautan = f"kasus-{berkas.stem}.html"
            awalan = ""
        else:
            keluar = ARTIKEL / f"{berkas.stem}.html"
            keluar.parent.mkdir(exist_ok=True)
            tautan = f"artikel/{berkas.stem}.html"
            awalan = "../"
            # gambar & tautan relatif harus naik satu tingkat dari artikel/
            isi_html = isi_html.replace('src="shots-deploy/', 'src="../shots-deploy/')
            isi_html = isi_html.replace('href="kasus-', 'href="../kasus-')
            isi_html = isi_html.replace('href="shots-deploy/', 'href="../shots-deploy/')

        tgl = datetime.strptime(meta["tanggal"], "%Y-%m-%d").date()
        kanonik = meta.get("kanonik", f"https://ikona.dev/{tautan}")

        # waktu baca kasar: 200 kata per menit
        jumlah_kata = len(re.sub(r"[^\w\s]", " ", teks).split())
        menit = max(1, round(jumlah_kata / 200))

        hal = ganti(kepala, {
            "JUDUL": html.escape(meta["judul"]),
            "RINGKAS": html.escape(meta["ringkas"]),
            "TANGGAL_ISO": tgl.isoformat(),
            "TANGGAL_TAMPIL": tgl.strftime("%d %b %Y"),
            "JENIS": jenis,
            "JENIS_LABEL": "Studi kasus" if jenis == "kasus" else "Tulisan",
            "KANONIK": kanonik,
            "TAUTAN": tautan,
            "AKAR": awalan,
            "MENIT": str(menit),
            "TOC": toc,
            "ISI": isi_html,
        })
        keluar.write_text(hal, encoding="utf-8")
        hasil.append({
            "judul": meta["judul"], "ringkas": meta["ringkas"], "jenis": jenis,
            "tanggal": tgl, "tautan": tautan, "keluar": keluar,
        })
        print(f"  {berkas.relative_to(AKAR)} -> {keluar.relative_to(AKAR)}")
    return hasil


def kartu_beranda(artikel: list[dict], batas: int = 3) -> str:
    """Pratinjau di beranda: TETAP seperti sekarang — kartu ringkas, bukan isi penuh."""
    potong = baca("kartu.html")
    kasus = [a for a in artikel if a["jenis"] == "kasus"]
    kasus.sort(key=lambda a: a["tanggal"], reverse=True)
    bagian = []
    for i, a in enumerate(kasus[:batas], start=1):
        bagian.append(ganti(potong, {
            "N": f"{i:02d}", "JUDUL": html.escape(a["judul"]),
            "RINGKAS": html.escape(a["ringkas"]), "TAUTAN": a["tautan"],
        }))
    return "\n".join(bagian)


def bangun_beranda(artikel: list[dict]) -> None:
    """Isi penanda di index.html — berkasnya sendiri tidak ditimpa."""
    berkas = AKAR / "index.html"
    teks = berkas.read_text(encoding="utf-8")

    def isi(penanda: str, nilai: str) -> str:
        pola = re.compile(
            r"(<!-- BUILD:" + penanda + r" -->)(.*?)(<!-- /BUILD:" + penanda + r" -->)",
            re.S,
        )
        if not pola.search(teks):
            raise ValueError(f"penanda BUILD:{penanda} tidak ditemukan di index.html")
        return pola.sub(lambda m: m.group(1) + "\n" + nilai + "\n" + m.group(3), teks)

    baru = isi("KARTU", kartu_beranda(artikel)) if artikel else teks
    if baru != teks:
        berkas.write_text(baru, encoding="utf-8")
        print("  index.html: pratinjau kartu diperbarui")


def periksa(artikel: list[dict]) -> int:
    """Cek tautan internal & berkas yang dirujuk. Mengembalikan jumlah masalah."""
    masalah = []
    for hal in list(AKAR.glob("*.html")) + list(ARTIKEL.glob("*.html")):
        teks = hal.read_text(encoding="utf-8")
        for href in re.findall(r'(?:href|src)="([^"]+)"', teks):
            if href.startswith(("http", "mailto:", "data:", "#")):
                continue
            jalur = (hal.parent / href.split("#")[0]).resolve()
            if href.endswith("/"):
                continue
            if not jalur.exists():
                masalah.append(f"{hal.name}: -> {href}")
    if masalah:
        print("\nTAUTAN/BERKAS RUSAK:")
        for m in masalah:
            print("  " + m)
    else:
        print("\nSemua tautan internal & berkas yang dirujuk ada.")
    return len(masalah)


def main() -> int:
    p = argparse.ArgumentParser(description="bangun situs IKONA dari markdown")
    p.add_argument("--bersih", action="store_true", help="hapus hasil sebelum membangun")
    p.add_argument("--periksa", action="store_true", help="cek tautan setelah membangun")
    a = p.parse_args()

    if not ISI.exists():
        print(f"folder isi/ tidak ada di {AKAR}", file=sys.stderr)
        return 1

    if a.bersih:
        for f in ARTIKEL.glob("*.html"):
            f.unlink()
        for f in AKAR.glob("kasus-*.html"):
            f.unlink()
        print("hasil lama dibersihkan")

    print("membangun:")
    artikel = bangun_artikel()
    bangun_indeks(artikel)
    bangun_beranda(artikel)
    print(f"\n{len(artikel)} halaman dari markdown "
          f"({sum(1 for x in artikel if x['jenis']=='kasus')} studi kasus, "
          f"{sum(1 for x in artikel if x['jenis']=='blog')} tulisan)")

    if a.periksa:
        return 1 if periksa(artikel) else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
