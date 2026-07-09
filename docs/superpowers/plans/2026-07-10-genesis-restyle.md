# Genesis Restyle Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restyle `site/trends.html` mengikuti bahasa visual genesis.ceo (gelap sinematik, hero satu layar, animasi contribution-graph hidup) tanpa mengubah kontrak data, lalu republish ke URL artifact yang sama.

**Architecture:** Tetap satu file HTML self-contained. Bagian yang berubah: CSS (token gelap tunggal), markup header → hero full-viewport dengan `<canvas>`, tambahan JS animasi canvas. Blok `#data` dan fungsi render kartu tidak berubah strukturnya.

**Tech Stack:** HTML/CSS/vanilla JS, Canvas 2D, Claude Artifact.

## Global Constraints

- Blok `<script type="application/json" id="data">` harus byte-identik dengan sebelumnya (kontrak routine).
- Tidak ada resource eksternal (CSP artifact); `<title>` tetap "Tren GitHub Mingguan"; favicon tetap 📈; URL artifact tetap `https://claude.ai/code/artifact/2d2694a7-a929-446b-b3f6-2f1924648362`.
- Satu tema gelap: ground `#0a0a0a`; teks `#ffffffeb/#ffffffb3/#ffffff8c/#ffffff59`; aksen `#3fb950`; emas `#d29922`; ramp hijau `#0e4429 #006d32 #26a641 #39d353`.
- Judul hero `font-size: max(44px, min(9vw, 110px))`, letter-spacing −0.03em; eyebrow 11px/0.18em uppercase; pill radius 999px; kartu radius 10px.
- `prefers-reduced-motion: reduce` → grid statis, tanpa gelombang/bintang.

---

### Task 1: Restyle trends.html

**Files:**
- Modify: `site/trends.html`

**Interfaces:**
- Produces: file final untuk Task 2; fungsi `render()`, id `edisi|ringkasan|filter|cards|data` tetap ada dengan perilaku sama.

- [ ] **Step 1: Simpan acuan blok #data** — Run: `python3 -c "import re; open('/tmp_data_ref.txt','w').write(re.search(r'<script type=\"application/json\" id=\"data\">.*?</script>', open('site/trends.html').read(), 16).group(0))"` (pakai path scratchpad untuk file ref).

- [ ] **Step 2: Ganti CSS** — hapus token dual-theme dan media query; token baru sesuai Global Constraints; komponen: hero (`min-height:100svh; display:grid; place-content:center`), canvas absolut `inset:0`, fade `linear-gradient(#0a0a0a00 0%, #0a0a0ad9 40%, #0a0a0a 70%)` di bawah hero, chips pill `background:rgba(255,255,255,.06)` aktif `background:#ffffffeb; color:#0a0a0a`, kartu `background:rgba(255,255,255,.04); border:1px solid rgba(255,255,255,.10); border-radius:10px`, kartu open `border-color:rgba(63,185,80,.55)`.

- [ ] **Step 3: Ganti markup header → hero**

```html
<section class="hero">
  <canvas id="graph" aria-hidden="true"></canvas>
  <div class="hero-fade"></div>
  <div class="hero-copy">
    <p class="eyebrow">Laporan mingguan · github trending</p>
    <h1>Tren GitHub<br>Mingguan</h1>
    <p class="hero-sub" id="hero-sub"></p>
    <div class="hero-actions">
      <select id="edisi" aria-label="Pilih edisi"></select>
      <a class="cta" href="#laporan">Lihat laporan ↓</a>
    </div>
  </div>
</section>
<div class="wrap" id="laporan"> …ringkasan, filter, cards, footer tetap… </div>
```

`#hero-sub` diisi label edisi aktif dari `render()` (`ed.label`).

- [ ] **Step 4: Tambah JS canvas** (sebelum script render, atau digabung):

```js
const cv = document.getElementById("graph"), ctx = cv.getContext("2d");
const RAMP = ["#0e4429", "#006d32", "#26a641", "#39d353"];
const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
let cells = [], stars = [], W, H, CELL = 15; // 12px + 3px gap
function resize() {
  const dpr = devicePixelRatio || 1, r = cv.parentElement.getBoundingClientRect();
  W = r.width; H = r.height;
  cv.width = W * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  cells = [];
  for (let y = 0; y < H / CELL; y++) for (let x = 0; x < W / CELL; x++)
    cells.push({ x, y, base: Math.random() });
}
function draw(t) {
  ctx.clearRect(0, 0, W, H);
  for (const c of cells) {
    const wave = reduced ? 0 : 0.5 + 0.5 * Math.sin(t / 4000 + c.x * 0.25 + c.y * 0.18 + c.base * 3);
    const v = c.base * 0.45 + wave * 0.55;
    if (v < 0.35) continue;
    ctx.globalAlpha = 0.06 + (v - 0.35) * 0.5;
    ctx.fillStyle = RAMP[Math.min(3, ((v - 0.35) / 0.1625) | 0)];
    ctx.fillRect(c.x * CELL, c.y * CELL, CELL - 3, CELL - 3);
  }
  ctx.globalAlpha = 1;
  if (!reduced) {
    if (stars.length < 12 && Math.random() < 0.02)
      stars.push({ x: Math.random() * W, y: H + 10, s: 8 + Math.random() * 8, v: 0.2 + Math.random() * 0.4, p: Math.random() * 6 });
    ctx.fillStyle = "#d29922"; ctx.font = "12px ui-monospace, monospace"; ctx.textAlign = "center";
    stars = stars.filter(st => st.y > -20);
    for (const st of stars) {
      st.y -= st.v; st.p += 0.01;
      ctx.globalAlpha = Math.max(0, Math.min(0.7, (H - st.y) / H)) * (0.4 + 0.3 * Math.sin(st.p * 4));
      ctx.font = st.s + "px ui-monospace, monospace";
      ctx.fillText("★", st.x + Math.sin(st.p) * 8, st.y);
    }
    ctx.globalAlpha = 1;
    requestAnimationFrame(draw);
  }
}
addEventListener("resize", () => { resize(); if (reduced) draw(0); });
resize(); reduced ? draw(0) : requestAnimationFrame(draw);
```

- [ ] **Step 5: Verifikasi**

Run (path ref sesuai Step 1):
```bash
python3 - <<'EOF'
import re
new = open('site/trends.html').read()
ref = open('<scratchpad>/data_ref.txt').read()
assert ref in new, "#data block changed!"
m = re.search(r'<script type="application/json" id="data">(.*?)</script>', new, re.S)
import json; json.loads(m.group(1))
for i in ["edisi","ringkasan","filter","cards","graph","hero-sub"]: assert f'id="{i}"' in new, i
print("OK")
EOF
grep -Eo 'src="http[^"]*"|href="http[^"]*"' site/trends.html | grep -v github.com || echo "no external resources"
```
Expected: `OK` dan `no external resources`.

- [ ] **Step 6: Commit** — `git add site/trends.html && git commit -m "feat: genesis-style dark restyle with living contribution graph"`

### Task 2: Republish artifact

**Files:**
- (tidak ada file baru)

**Interfaces:**
- Consumes: `site/trends.html` final dari Task 1.

- [ ] **Step 1: Publish** — tool Artifact, `file_path` sama (`site/trends.html`), favicon 📈, label `genesis-restyle`. Karena file path sama di percakapan ini, URL tetap.
- [ ] **Step 2: Cek URL** — hasil publish harus `https://claude.ai/code/artifact/2d2694a7-a929-446b-b3f6-2f1924648362`; jika berbeda, STOP dan selidiki (jangan biarkan dua URL hidup).

**Self-review:** Spec ter-cover (token→GC+S2, hero→S3, animasi→S4, reduced-motion→S4, kontrak #data→S1+S5, republish→T2). Tidak ada placeholder; id konsisten (`graph`, `hero-sub`, `edisi`, `laporan`).
