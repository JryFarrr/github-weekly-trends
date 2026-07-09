# Restyle ala genesis.ceo — Desain

**Tanggal:** 2026-07-10 · **Status:** Disetujui

## Tujuan

Mengubah tampilan website "Tren GitHub Mingguan" mengikuti bahasa visual
genesis.ceo: gelap sinematik, hero satu layar dengan animasi ambient, judul
raksasa, aksen irit. Robot 3D Spline milik Genesis diganti animasi
**contribution-graph hidup** (pilihan user).

## Token desain (dari analisis HTML genesis.ceo)

- Ground `#0a0a0a`; hierarki teks putih via alpha: `#ffffffeb` / `#ffffffb3`
  / `#ffffff8c` / `#ffffff59`.
- Aksen dunia GitHub (bukan blurple Genesis): hijau `#3fb950`, emas bintang
  `#d29922`; ramp hijau kontribusi `#0e4429 → #006d32 → #26a641 → #39d353`.
- Judul hero `max(44px, min(9vw, 110px))`, letter-spacing rapat (−0.03em);
  eyebrow 11px uppercase letter-spacing 0.18em; chip/tombol pill radius 999px;
  kartu radius 10px; gradient fade `#0a0a0a00 → #0a0a0ad9 40% → #0a0a0a 70%`.
- Font: mono sistem untuk display/label (identitas terminal dipertahankan),
  system-ui untuk body.
- **Satu tema gelap saja** — komitmen sadar mengikuti referensi; toggle tema
  claude.ai tidak mengubah halaman.

## Hero (satu layar, `min-height: 100svh`)

Canvas animasi di belakang; konten: eyebrow, judul "Tren GitHub Mingguan",
label edisi aktif + dropdown edisi (pill gelap), tautan scroll "Lihat laporan ↓".
Bagian bawah hero memudar ke konten lewat gradient.

## Animasi: contribution-graph hidup (canvas 2D)

- Grid kotak ala GitHub (±12px, gap 3px) memenuhi hero; tiap sel punya
  aktivitas dasar acak; gelombang lambat berjalan melintasi grid mengubah
  intensitas (ramp hijau, alpha rendah agar teks tetap terbaca).
- Partikel bintang ★ emas (maks ~12) sesekali naik perlahan lalu memudar.
- `prefers-reduced-motion: reduce` → render grid statis sekali, tanpa
  gelombang dan bintang. Resize di-handle; skala devicePixelRatio.

## Konten di bawah hero

Struktur dan JS render tetap: rangkuman (lede), chip filter (pill), kartu
`<details>` (surface `rgba(255,255,255,.04)`, border `rgba(255,255,255,.10)`,
terbuka → border hijau samar), angka bintang emas mono, footer.

## Kontrak yang TIDAK berubah

Blok `<script type="application/json" id="data">` (skema & posisi), `<title>`,
favicon 📈, URL artifact. Routine mingguan hanya mengganti isi `#data` — tetap
kompatibel tanpa diubah.
