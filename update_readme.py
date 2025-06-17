# scripts/update_readme.py
import os
import json
import random
from datetime import datetime

# Paths
README_PATH = "README.md"
TEMPLATE_PATH = "README_TEMPLATE.md"
ARTICLES_DIR = "ML-News-Bot-o-Matic/articles"

TAG_START = "<!-- START_ML_UPDATE -->"
TAG_END = "<!-- END_ML_UPDATE -->"

# Randomly select article
files = [f for f in os.listdir(ARTICLES_DIR) if f.endswith(".json")]
chosen_file = random.choice(files)

with open(os.path.join(ARTICLES_DIR, chosen_file), "r", encoding="utf-8") as f:
    data = json.load(f)

# Format the update block
update_md = f"""## 🧑‍💻 Daily ML Article

**[{data['title']}]({data['url']})**  
📵 _Published: {data.get('date', datetime.utcnow().strftime('%Y-%m-%d'))}_

> {data.get('summary', 'No summary available...')}

🔗 [Read Full Article]({data['url']})
"""

# Read template
with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
    content = f.read()

start = content.find(TAG_START)
end = content.find(TAG_END)

if start != -1 and end != -1:
    new_content = (
        content[:start + len(TAG_START)] +
        "\n" + update_md + "\n" +
        content[end:]
    )

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)
else:
    raise ValueError("Update tags not found in README template.")
