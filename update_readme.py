import json
import random

# Path to your full digest file
DIGEST_PATH = "ML-News-Bot-o-Matic/data/digest.json"  # adjust if needed

# Load all articles
with open(DIGEST_PATH, "r", encoding="utf-8") as f:
    all_articles = json.load(f)

# Pick a random article
entry = random.choice(all_articles)

title = entry["title"]
url = f"https://reddit.com/comments/{entry['post_id']}"  # or a custom URL
summary = entry.get("summary", "No summary available.")
date = entry.get("timestamp", "Unknown date")

# Now inject using your same Markdown/HTML block
update_md = f"""
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
