import os
import json
import random
import glob

# ─── CONFIG ─────────────────────────────────────────────────────

# Where your profile README lives
README_PATH     = "README.md"
TEMPLATE_PATH   = "README_TEMPLATE.md"

# Path to the ML-News-Bot digest checkout
ML_PATH         = "ML-News-Bot-o-Matic"

# These two dirs might contain your JSON arrays
DIGEST_DIRS     = [
    os.path.join(ML_PATH, "data"),
    os.path.join(ML_PATH, "digests"),
]

TAG_START = "<!-- START_ML_UPDATE -->"
TAG_END   = "<!-- END_ML_UPDATE -->"

# ─── LOAD ALL JSON ENTRIES ───────────────────────────────────────

entries = []
for d in DIGEST_DIRS:
    if not os.path.isdir(d):
        continue
    for filepath in glob.glob(os.path.join(d, "*.json")):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            # if file is a list of items, extend; if single, append
            if isinstance(data, list):
                entries.extend(data)
            elif isinstance(data, dict):
                entries.append(data)
        except Exception:
            continue

if not entries:
    raise RuntimeError("No JSON entries found in ML-News-Bot-o-Matic/data or /digests")

# ─── PICK A RANDOM ENTRY ─────────────────────────────────────────

entry = random.choice(entries)
title   = entry.get("title", "Untitled")
url     = entry.get("url", entry.get("link", "#"))
summary = entry.get("summary", "No summary available.")
date    = entry.get("timestamp", entry.get("date", "Unknown date"))

# ─── BUILD YOUR INJECTION HTML ───────────────────────────────────

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

new_readme = (
    template[: start + len(TAG_START)] +
    injection +
    template[end:]
)

with open(README_PATH, "w", encoding="utf-8") as f:
    f.write(new_readme)
