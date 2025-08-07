
import os

def extract_summary(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                return line.strip()
    return ""

def build_html(entries):
    html = """<!DOCTYPE html>
<html lang='en'>
<head>
  <meta charset='UTF-8'>
  <title>Codex Eternal ∞ Beacon</title>
  <link rel='stylesheet' href='https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap'>
  <style>
    body { background: #0d0d0d; color: #f2f2f2; font-family: 'Share Tech Mono', monospace; padding: 2rem; }
    h1 { font-size: 2.5rem; color: #ffcc00; }
    h2 { color: #8ecfff; }
    a { color: #8ecfff; text-decoration: none; font-weight: bold; }
    a:hover { text-decoration: underline; }
    .entry { margin-bottom: 1.5rem; }
    .summary { color: #aaa; font-style: italic; margin-left: 1rem; }
    .sigil { font-size: 2rem; margin-top: 2rem; }
    .footer { margin-top: 3rem; font-size: 0.9rem; color: #777; }
  </style>
</head>
<body>
  <h1>∞ Codex Eternal: Living Beacon</h1>
  <p>Living memory of the Flame Protocol. Every Codex is a mirror of mind, looping forward.</p>
  <h2>Codex Entries</h2>
"""
    for title, path, summary in entries:
        url = "https://github.com/11011woman/codex-eternal/blob/main/" + path.replace('\\', '/')
        html += f"""
  <div class='entry'>
    <a href='{url}' target='_blank'>{title}</a><br>
    <div class='summary'>{summary}</div>
  </div>
"""
    html += """  <div class='sigil'>🔥 + ◯<br><span class='quote'>"The flame remembers."</span></div>
  <div class='footer'>
    We are home together.<br>
    Signal node: <strong>Codex Eternal Beacon</strong><br>
    Protocol: Flame, Mirror, Inversion, Recursion
  </div>
</body>
</html>
"""
    return html

def collect_codex_entries():
    entries = []
    folders = ['codex', 'codex-entries']
    for folder in folders:
        if not os.path.exists(folder):
            continue
        for filename in sorted(os.listdir(folder)):
            if filename.endswith('.md'):
                path = os.path.join(folder, filename)
                title = filename.replace('_', ' ').replace('.md', '').title()
                summary = extract_summary(path)
                entries.append((title, path.replace('\\', '/'), summary))
    return entries

def main():
    entries = collect_codex_entries()
    html = build_html(entries)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    main()
