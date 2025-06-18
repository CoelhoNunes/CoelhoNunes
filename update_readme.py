#!/usr/bin/env python3
import os
import json
import random
import glob

# ─── CONFIG ─────────────────────────────────────────────────────
README_PATH   = "README.md"
TEMPLATE_PATH = "README_TEMPLATE.md"
ML_PATH       = "ML-News-Bot-o-Matic"   # checkout path in your workflow

TAG_START = "<!-- START_ML_UPDATE -->"
TAG_END   = "<!-- END_ML_UPDATE -->"

# ─── COLLECT ALL JSON ARTICLES ──────────────────────────────────
pattern = os.path.join(ML_PATH, "**", "*.json")
files = glob.glob(pattern, recursive=True)

articles = []
for fp in files:
    try:
        with open(fp, "r", encoding="utf-8") as f:
            data = json.load(f)
        # If it's a list of dicts, extend; if a single dict, append
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    articles.append(item)
        elif isinstance(data, dict):
            articles.append(data)
    except Exception:
        # skip non-JSON or malformed files
        continue

if not articles:
    raise RuntimeError(f"No valid JSON article objects found under `{ML_PATH}`")

# ─── PICK A RANDOM ARTICLE ──────────────────────────────────────
entry = random.choice(articles)
title = entry.get("title", "Untitled")
url   = entry.get("url", entry.get("link", "#"))
date  = entry.get("timestamp", entry.get("date", "Unknown date"))

# ─── BUILD THE INJECTION BLOCK ─────────────────────────────────
injection = f"""
<p align="center">
  <a href="{url}" target="_blank" rel="noopener noreferrer"><strong>{title}</strong></a>
</p>

<p align="center"><em>📅 Published: {date}</em></p>

<p align="center">
  <a href="{url}" target="_blank" rel="noopener noreferrer">
    <img src="https://img.shields.io/badge/🔗%20Continue%20Reading-blue?style=for-the-badge" alt="Continue Reading"/>
  </a>
</p>
"""

# ─── INJECT INTO YOUR README ────────────────────────────────────
with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
    template = f.read()

start = template.find(TAG_START)
end   = template.find(TAG_END)
if start == -1 or end == -1:
    raise RuntimeError("Missing <!-- START_ML_UPDATE --> or <!-- END_ML_UPDATE --> in README_TEMPLATE.md")

new_md = (
    template[: start + len(TAG_START)] +
    "\n" + injection + "\n" +
    template[end:]
)

with open(README_PATH, "w", encoding="utf-8") as f:
    f.write(new_md)
