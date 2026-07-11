#!/usr/bin/env python3
"""Bungkus site/trends.html (fragment artifact) jadi index.html utuh untuk Vercel.
Jalankan setiap kali site/trends.html berubah: python3 build_index.py"""
src = open("site/trends.html").read()
cut = src.index("</title>") + len("</title>")
open("index.html", "w").write(
    '<!doctype html>\n<html lang="id">\n<head>\n'
    '<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
    + src[:cut] + "\n</head>\n<body>"
    + src[cut:] + "\n</body>\n</html>\n"
)
print("index.html ditulis")
