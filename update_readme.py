import os
import json
import random
import glob

# ─── CONFIG ─────────────────────────────────────────────────────
README_PATH   = "README.md"
TEMPLATE_PATH = "README_TEMPLATE.md"
ML_PATH       = "ML-News-Bot-o-Matic"      # must match the checkout path

TAG_START = "<!-- START_ML_UPDATE -->"
TAG_END   = "<!-- END_ML_UPDATE -->"

# ─── GATHER ALL JSON DIGESTS ────────────────────────────────────
pattern = os.path.join(ML_PATH, "**", "*.json")
files = glob.glob(pattern, recursive=True)

entries = []
for fp in files:
    try:
        with open(fp, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            entries.extend(data)
        elif isinstance(data, dict):
            entries.append(data)
    except Exception:
        continue

if not entries:
    raise RuntimeError(f"No JSON entries found under `{ML_PATH}`")

# ─── PICK ONE AT RANDOM ─────────────────────────────────────────
entry   = random.choice(entries)
title   = entry.get("title", "Untitled")
url     = entry.get("url", entry.get("link", "#"))
date    = entry.get("timestamp", entry.get("date", "Unknown date"))

# ─── BUILD THE INJECTION BLOCK ─────────────────────────────────
injection = f"""
<p align="center">
  <a href="{url}" target="_blank" rel="noopener noreferrer">
    <strong>{title}</strong>
  </a>
</p>

<p align="center"><em>📅 Published: {date}</em></p>

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
