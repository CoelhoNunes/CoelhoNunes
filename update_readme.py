import os
import json
import random
import glob

# ─── CONFIG ─────────────────────────────────────────────────────
README_PATH   = "README.md"
TEMPLATE_PATH = "README_TEMPLATE.md"
ML_PATH       = "ML-News-Bot-o-Matic"      # must match your checkout path

TAG_START = "<!-- START_ML_UPDATE -->"
TAG_END   = "<!-- END_ML_UPDATE -->"

# ─── GATHER ALL JSON DIGESTS ────────────────────────────────────
pattern = os.path.join(ML_PATH, "**", "*.json")
files = glob.glob(pattern, recursive=True)

raw_entries = []
for fp in files:
    try:
        with open(fp, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            raw_entries.extend(data)
        elif isinstance(data, dict):
            raw_entries.append(data)
    except Exception:
        continue

# ─── FILTER ONLY DICT ENTRIES ───────────────────────────────────
entries = [e for e in raw_entries if isinstance(e, dict)]

if not entries:
    raise RuntimeError(f"No valid JSON objects found under `{ML_PATH}`")

# ─── PICK ONE AT RANDOM ─────────────────────────────────────────
entry = random.choice(entries)
title   = entry.get("title",   "Untitled")
url     = entry.get("url",     entry.get("link", "#"))
summary = entry.get("summary", "No summary available.")
date    = entry.get("timestamp", entry.get("date", "Unknown date"))

# ─── BUILD “ML SPOTLIGHT” CARD ───────────────────────────────────
injection = f"""
<p align="center">
  <img src="https://img.shields.io/badge/🚀-ML%20Spotlight-brightgreen?style=for-the-badge" alt="ML Spotlight"/>
</p>

<p align="center">
  <a href="{url}" target="_blank" rel="noopener noreferrer">
    **{title}**
  </a>
</p>

<p align="center"><em>📅 Published: {date}</em></p>

<p align="center"><em>“{summary}”</em></p>

<p align="center">
  <a href="{url}" target="_blank" rel="noopener noreferrer">
    <img src="https://img.shields.io/badge/🔗%20Continue%20Reading-blue?style=for-the-badge" alt="Continue Reading"/>
  </a>
</p>
"""

# ─── INJECT INTO README ──────────────────────────────────────────
with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
    template = f.read()

start = template.find(TAG_START)
end   = template.find(TAG_END)
if start == -1 or end == -1:
    raise RuntimeError("Missing START/END tags in README_TEMPLATE.md")

new_md = (
    template[: start + len(TAG_START)] +
    "\n" + injection + "\n" +
    template[end:]
)

with open(README_PATH, "w", encoding="utf-8") as f:
    f.write(new_md)
