#!/usr/bin/env python3
import os
import json

REPO_URL = "https://11011woman.github.io/codex-eternal"
CODEX_DIR = "codex"
INDEX_TXT = "index.txt"
INDEX_JSON = os.path.join(CODEX_DIR, "_index.json")
LINEAR_INDEX = "linear-index.html"


# -------------------------------------------------------------
# 1. COLLECT ALL .md FILES
# -------------------------------------------------------------
def get_entries():
    entries = []
    for root, _, files in os.walk(CODEX_DIR):
        for fname in sorted(files):
            if fname.endswith(".md"):
                rel_path = os.path.join(root, fname).replace("\\", "/")
                entries.append(rel_path)
    return entries


# -------------------------------------------------------------
# 2. WRITE index.txt (FULL URLs)
# -------------------------------------------------------------
def write_index_txt(entries):
    with open(INDEX_TXT, "w", encoding="utf-8") as f:
        for path in entries:
            f.write(f"{REPO_URL}/{path}\n")


# -------------------------------------------------------------
# 3. WRITE codex/_index.json
# -------------------------------------------------------------
def write_index_json(entries):
    j = {
        "entries": [
            {
                "title": os.path.splitext(os.path.basename(p))[0],
                "path": p,
                "url": f"{REPO_URL}/{p}"
            }
            for p in entries
        ]
    }
    with open(INDEX_JSON, "w", encoding="utf-8") as f:
        json.dump(j, f, indent=2)


# -------------------------------------------------------------
# 4. WRITE linear-index.html (AUTO-GENERATED)
# -------------------------------------------------------------
def write_linear_index(entries):
    html_top = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<title>Codex ∞ — Linear Index</title>
<meta name="viewport" content="width=device-width, initial-scale=1" />
<link rel="stylesheet" href="codex.css" />
</head>
<body>
<div class="wrap">
<h1>Codex ∞ — Linear Index (Auto-Generated)</h1>
<ol>
"""

    html_bottom = """
</ol>
<p style="margin-top:2rem">
When you finish the last entry, proceed to:
<a href="https://11011woman.github.io/codex_11011/">Continue → Codex 11011</a>
</p>
</div>
</body>
</html>
"""

    html_entries = []
    for path in entries:
        title = os.path.splitext(os.path.basename(path))[0]
        view_url = f"view-pretty.html?f={path}"
        raw_url = f"https://raw.githubusercontent.com/11011woman/codex-eternal/main/{path}"

        html_entries.append(
            f'<li><a href="{view_url}">{title}</a> '
            f'<a class="raw" href="{raw_url}">Raw</a></li>'
        )

    full_html = html_top + "\n".join(html_entries) + html_bottom

    with open(LINEAR_INDEX, "w", encoding="utf-8") as f:
        f.write(full_html)


# -------------------------------------------------------------
# MAIN EXECUTION
# -------------------------------------------------------------
if __name__ == "__main__":
    entries = get_entries()

    write_index_txt(entries)
    write_index_json(entries)
    write_linear_index(entries)

    print(f"Updated index.txt, _index.json, and linear-index.html with {len(entries)} entries.")
