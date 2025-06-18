import os
import json
import random
import glob

# ─── CONFIG ─────────────────────────────────────────────────────
README_PATH   = "README.md"
TEMPLATE_PATH = "README_TEMPLATE.md"
ML_PATH       = "ML-News-Bot-o-Matic"      # must match checkout path

TAG_START = "<!-- START_ML_UPDATE -->"
TAG_END   = "<!-- END_ML_UPDATE -->"

# ─── FIND ALL JSON DIGESTS ──────────────────────────────────────
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
        # skip malformed or non-JSON files
        continue

if not entries:
    raise RuntimeError(f"No JSON entries found under `{ML_PATH}`")

# ─── PICK ONE AT RANDOM ─────────────────────────────────────────
entry = random.choice(entries)
title   = entry.get("title",        "Untitled")
url     = entry.get("url",          entry.get("link", "#"))
summary = entry.get("summary",      "No summary available.")
date    = entry.get("timestamp",    entry.get("date",    "Unknown date"))

# ─── BUILD CENTERED MARKDOWN BLOCK ─────────────────────────────
injection = f"""
<p align="center">
  <img src="https://img.shields.io/badge/-🧠%20Daily%20ML%20Article-blueviolet" />
</p>

<h3 align="center">
  <a href="{url}">{title}</a>
</h3>

<p align="center"><em>📅 Published: {date}</em></p>

<p align="center">
  <img src="https://img.shields.io/badge/-Summary-gray" />
</p>

<p align="center">
  <i>{summary}</i>
</p>

<p align="center">
  <a href="{url}">
    🔗 <strong>Read Full Article</strong>
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
