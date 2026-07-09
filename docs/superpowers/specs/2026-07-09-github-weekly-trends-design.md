# GitHub Weekly Trends — Desain

**Tanggal:** 2026-07-09 · **Status:** Disetujui

## Tujuan

Website berbahasa Indonesia yang merangkum tren mingguan repositori GitHub —
apa yang trending, use case-nya, dan faktor yang membuatnya viral — diperbarui
otomatis tiap Minggu 00:00 WIB (Asia/Jakarta), dapat diakses user lewat satu
URL tetap.

## Arsitektur (disetujui user)

Dua komponen, tanpa server dan tanpa API key:

1. **Website = Claude Artifact** (satu file HTML self-contained, URL tetap di claude.ai).
2. **Updater = scheduled cloud agent (routine)** dengan cron Minggu 00:00 Asia/Jakarta.

Alternatif yang ditolak: GitHub Actions + Pages (butuh repo + API key berbayar),
cron lokal di Mac (rapuh — Mac harus menyala).

## Website

- Bahasa Indonesia penuh; tema gelap/terang; responsif.
- **Rangkuman mingguan:** narasi tema besar minggu tersebut.
- **Kartu repo** (top ~10 dari `github.com/trending?since=weekly`): nama, ⭐ minggu
  ini, bahasa pemrograman, deskripsi; expand untuk *apa itu*, *use case*, *kenapa viral*.
- **Filter** per bahasa pemrograman (client-side JS).
- **Arsip** edisi sebelumnya: data tiap minggu disimpan sebagai JSON di dalam
  HTML itu sendiri; dropdown untuk berpindah edisi. Tanpa database.

## Routine mingguan

Cron `0 0 * * 0` zona `Asia/Jakarta`. Tiap jalan:

1. Fetch `https://github.com/trending?since=weekly` → daftar repo + bintang minggu ini.
2. Fetch halaman/README repo teratas untuk konteks use case.
3. Tulis analisis bahasa Indonesia (rangkuman, use case, faktor viral per repo).
4. Baca artifact lama (WebFetch URL-nya) → ambil JSON arsip, tambahkan edisi baru.
5. Re-publish HTML ke URL artifact yang sama.

**Error handling:** jika fetch GitHub gagal, jangan menimpa artifact — edisi
lama tetap tayang; routine berhenti dengan catatan gagal.

## Eksekusi perdana

Edisi pertama digenerate manual pada sesi ini agar website langsung bisa
diakses, lalu routine dipasang untuk minggu-minggu berikutnya.

## Di luar cakupan (YAGNI)

Database, backend, autentikasi, notifikasi email/push, tren harian/bulanan.
