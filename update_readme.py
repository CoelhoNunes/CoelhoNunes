import os
import json
import random
import requests

# ─── CONFIG ─────────────────────────────────────────────────────

# Your profile repo’s README and template
README_PATH   = "README.md"
TEMPLATE_PATH = "README_TEMPLATE.md"

# The ML-News-Bot-o-Matic repo details
API_URL      = "https://api.github.com"
OWNER        = "CoelhoNunes"
REPO         = "ML-News-Bot-o-Matic"
DATA_DIR     = "data"   # directory in that repo containing JSON digests

# Template markers
TAG_START = "<!-- START_ML_UPDATE -->"
TAG_END   = "<!-- END_ML_UPDATE -->"

# ─── AUTH ────────────────────────────────────────────────────────

# Use your PAT so you don’t get rate-limited
GH_PAT = os.getenv("GH_PAT")
headers = {"Authorization": f"token {GH_PAT}"} if GH_PAT else {}

# ─── LIST JSON FILES IN ML REPO ──────────────────────────────────

contents_url = f"{API_URL}/repos/{OWNER}/{REPO}/contents/{DATA_DIR}"
resp = requests.get(contents_url, headers=headers)
resp.raise_for_status()
items = resp.json()

# Filter to just the .json files
json_files = [i for i in items if i["type"] == "file" and i["name"].endswith(".json")]
if not json_files:
    raise RuntimeError(f"No JSON files found in `{DATA_DIR}/` of {OWNER}/{REPO}")

# ─── PICK ONE AND DOWNLOAD ───────────────────────────────────────

chosen = random.choice(json_files)
download_url = chosen["download_url"]

r2 = requests.get(download_url, headers=headers)
r2.raise_for_status()
data = r2.json()

# If your digest is a list of entries, choose one; else treat as single
if isinstance(data, list):
    entry = random.choice(data)
elif isinstance(data, dict):
    entry = data
else:
    raise RuntimeError("Unexpected JSON structure in digest file")

# ─── EXTRACT FIELDS ─────────────────────────────────────────────

title   = entry.get("title", "Untitled")
url     = entry.get("url", entry.get("link", "#"))
summary = entry.get("summary", "No summary available.")
date    = entry.get("timestamp", entry.get("date", "Unknown date"))

# ─── BUILD CENTERED INJECTION BLOCK ────────────────────────────

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

# ─── INJECT INTO YOUR README ────────────────────────────────────

with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
    template = f.read()

start = template.find(TAG_START)
end   = template.find(TAG_END)
if start == -1 or end == -1:
    raise RuntimeError("Missing START/END tags in README_TEMPLATE.md")

new_readme = (
    template[: start + len(TAG_START)]
  + "\n"
  + injection
  + "\n"
  + template[end:]
)

with open(README_PATH, "w", encoding="utf-8") as f:
    f.write(new_readme)
