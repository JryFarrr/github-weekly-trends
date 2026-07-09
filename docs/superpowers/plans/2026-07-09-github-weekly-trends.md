# GitHub Weekly Trends Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Website bahasa Indonesia berisi tren mingguan GitHub (rangkuman, use case, faktor viral) di satu URL Artifact tetap, di-update otomatis oleh routine tiap Minggu 00:00 WIB.

**Architecture:** Satu file HTML self-contained yang menyimpan seluruh arsip sebagai JSON embedded, dipublish sebagai Claude Artifact. Sebuah scheduled cloud agent (routine) meregenerasi dan me-republish file itu ke URL yang sama tiap minggu. Tanpa server, tanpa dependency.

**Tech Stack:** HTML/CSS/vanilla JS (native `<details>`, `prefers-color-scheme`), curl untuk fetch, Claude Artifact untuk hosting, Claude Code routine untuk cron.

## Global Constraints

- Seluruh teks website berbahasa Indonesia.
- Artifact CSP: TIDAK BOLEH ada request eksternal (no CDN/font/gambar remote); semua inline.
- Cron: `0 0 * * 0`, timezone `Asia/Jakarta`.
- Jika fetch GitHub gagal saat routine jalan: JANGAN republish artifact.
- Website harus theme-aware (dark/light) dan responsif; konten lebar pakai `overflow-x: auto`.

---

### Task 1: Ambil data trending mingguan

**Files:**
- Create: `<scratchpad>/trending.html` (mentah), `<scratchpad>/repos/*.html` (halaman repo teratas)

**Interfaces:**
- Produces: data untuk Task 2 — per repo: `name` (owner/repo), `url`, `lang`, `desc`, `stars_total`, `stars_week` (angka "X stars this week").

- [ ] **Step 1: Fetch daftar trending mingguan**

Run: `curl -sL -A "Mozilla/5.0" "https://github.com/trending?since=weekly" -o <scratchpad>/trending.html && grep -c 'article class="Box-row"' <scratchpad>/trending.html`
Expected: angka ~25 (jumlah repo). Jika 0 → coba tanpa `-A`, atau pakai WebFetch. Jika tetap gagal → berhenti, laporkan.

- [ ] **Step 2: Parse ~10 repo teratas**

Ekstrak dari HTML: nama repo (`href="/owner/repo"` dalam `h2`), deskripsi (`<p class="col-9...">`), bahasa (`itemprop="programmingLanguage"`), total stars, dan "N stars this week" (`<span class="d-inline-block float-sm-right">`). Cara tercepat: baca file mentah langsung (bukan tulis parser) karena hanya 10 entri sekali seminggu.

- [ ] **Step 3: Fetch konteks tiap repo teratas**

Run per repo: `curl -sL -A "Mozilla/5.0" "https://github.com/{owner}/{repo}" -o <scratchpad>/repos/{repo}.html`
Baca bagian README/About untuk memahami apa proyek itu dan use case-nya. Cukup 8–10 repo.

### Task 2: Tulis analisis bahasa Indonesia

**Files:**
- Create: `<scratchpad>/edition.json`

**Interfaces:**
- Consumes: data Task 1.
- Produces: satu objek edisi dengan skema persis:

```json
{
  "week_end": "2026-07-09",
  "label": "3–9 Juli 2026",
  "summary": "2–4 kalimat narasi tema besar minggu ini, bahasa Indonesia.",
  "repos": [
    {
      "name": "owner/repo",
      "url": "https://github.com/owner/repo",
      "lang": "Python",
      "stars_week": 3200,
      "stars_total": 15000,
      "desc": "deskripsi asli repo (boleh diterjemahkan)",
      "apa": "1–2 kalimat: apa proyek ini.",
      "use_case": "1–3 kalimat: dipakai untuk kasus apa, oleh siapa.",
      "kenapa_viral": "1–3 kalimat: faktor viralnya (rilis besar, tren AI, HN, backing perusahaan, dst)."
    }
  ]
}
```

- [ ] **Step 1: Tulis `edition.json`** — isi lengkap semua field untuk 8–10 repo; `kenapa_viral` berdasar sinyal nyata (tanggal rilis, README, momentum bintang), bukan spekulasi kosong.
- [ ] **Step 2: Validasi** — Run: `python3 -m json.tool <scratchpad>/edition.json > /dev/null && echo OK`. Expected: `OK`.

### Task 3: Bangun website & publish Artifact

**Files:**
- Create: `site/trends.html` (di repo proyek, di-commit)

**Interfaces:**
- Consumes: `edition.json` (Task 2), skema di atas.
- Produces: URL artifact tetap untuk Task 4.

- [ ] **Step 1: Load skill `artifact-design`** (wajib sebelum menulis halaman).

- [ ] **Step 2: Tulis `site/trends.html`** dengan struktur:

```html
<title>Tren GitHub Mingguan</title>
<style>/* inline, theme-aware:
   @media (prefers-color-scheme: dark) + :root[data-theme=...] overrides */</style>
<header>judul + dropdown <select id="edisi"> (arsip)</header>
<section id="ringkasan">narasi mingguan</section>
<nav id="filter">tombol filter per bahasa (JS toggle)</nav>
<main id="cards">
  <!-- per repo: <details class="card" data-lang="Python">
       <summary>nama ⭐N minggu ini · bahasa</summary>
       <p>apa</p><p>use case</p><p>kenapa viral</p>
       <a href="...">buka repo</a></details> -->
</main>
<script type="application/json" id="data">{"editions":[ ...arsip, terbaru di indeks 0... ]}</script>
<script>/* vanilla JS: parse #data, render edisi terpilih, filter bahasa */</script>
```

Semua render dari JSON via JS agar routine mingguan cukup mengganti isi `#data` + republish.

- [ ] **Step 3: Cek self-contained** — Run: `grep -Eo 'src="http[^"]*"|href="http[^"]*"' site/trends.html | grep -v github.com`. Expected: kosong (link `<a>` ke github.com boleh; resource eksternal tidak ada).
- [ ] **Step 4: Publish Artifact** — tool Artifact, `file_path: site/trends.html`, favicon 📈, catat URL.
- [ ] **Step 5: Commit** — `git add site docs && git commit -m "feat: first edition of weekly trends site"`.

### Task 4: Pasang routine mingguan

**Files:**
- Create: `routine-prompt.md` (di repo proyek — salinan prompt routine untuk referensi/edit)

**Interfaces:**
- Consumes: URL artifact dari Task 3.

- [ ] **Step 1: Tulis `routine-prompt.md`** berisi instruksi lengkap untuk agent mingguan (fetch trending → analisis ID → baca artifact lama di URL X → prepend edisi baru ke `editions` → republish ke URL X; jika fetch gagal, jangan republish).
- [ ] **Step 2: Buat routine** — invoke skill `schedule`: cron `0 0 * * 0` `Asia/Jakarta`, prompt = isi `routine-prompt.md`.
- [ ] **Step 3: Commit** — `git add routine-prompt.md && git commit -m "feat: add weekly routine prompt"`.
- [ ] **Step 4: Verifikasi** — list routine terjadwal, pastikan muncul dengan cron yang benar.

**Self-review:** Semua bagian spec terpetakan (website→T3, routine→T4, data→T1, analisis→T2, error handling→Global Constraints, edisi perdana→T1–T3). Tidak ada placeholder. Skema `edition.json` konsisten dipakai T2→T3→routine-prompt.
