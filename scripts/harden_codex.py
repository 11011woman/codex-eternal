#!/usr/bin/env python3
import os, re, json, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
CODEX = ROOT / "codex"
INDEX = CODEX / "_index.json"   # optional
CONFIG = ROOT / "hardening_config.json"
GRAPH = ROOT / "graph.json"
REPORT = ROOT / "HARDENING_REPORT.md"

def load_json(p, required=False):
    if not p.exists():
        if required:
            raise FileNotFoundError(f"Missing required file: {p}")
        return None
    return json.loads(p.read_text(encoding="utf-8"))

def save_json(p, obj):
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")

def read(p):
    return p.read_text(encoding="utf-8") if p.exists() else ""

def write(p, s):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s, encoding="utf-8")

def ensure_stub(filename, title, summary, tags):
    p = CODEX / filename
    if p.exists():
        return False
    # Precompute values OUTSIDE the f-string to avoid backslash parsing issues
    safe_id = re.sub(r'[^a-z0-9\-]+', '-', title.lower()).strip('-')
    tag_list = ', '.join(tags)
    fm = (
        "---\n"
        f"id: {safe_id}\n"
        f"title: {title}\n"
        f"tags: [{tag_list}]\n"
        "---\n\n"
    )
    body = (
        "## Summary\n"
        f"{summary}\n\n"
        "## Body\n"
        "(Placeholder — to be expanded.)\n\n"
        "## Links\n"
    )
    write(p, fm + body)
    return True

def parse_front_matter(md):
    m = re.match(r'^---\s*(.*?)\s*---\s*(.*)$', md, re.S)
    if not m:
        return {}, md
    raw, body = m.groups()
    fm = {}
    for line in raw.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm, body

def ensure_links_section(md, rels):
    fm, body = parse_front_matter(md)
    if "## Links" not in body:
        body = body.rstrip() + "\n\n## Links\n"
    # collect existing links to avoid duplicates
    existing = set(m.group(1) for m in re.finditer(r'\[(?:.*?)\]\((.*?)\)', body))
    to_add = []
    for r in rels:
        path = f"./{r}"
        if path not in existing:
            title_guess = r.replace('-', ' ').replace('.md','').title()
            to_add.append(f"- See also: [{title_guess}]({path})")
    if to_add:
        body = body.rstrip() + "\n" + "\n".join(to_add) + "\n"
    # Re-attach front matter if present
    if md.startswith("---"):
        parts = md.split("---", 2)
        return parts[0] + "---" + parts[1] + "---\n" + body
    else:
        return md + "\n" + body

def build_graph(index, relmap):
    nodes = []
    id_by_file = {}
    if index:
        for it in index:
            nid = it.get("id") or it["path"]
            nodes.append({
                "id": nid,
                "title": it.get("title", nid),
                "path": it["path"],
                "tags": it.get("tags", [])
            })
            id_by_file[it["path"].split('/')[-1]] = nid
    else:
        for p in CODEX.glob("*.md"):
            nid = p.stem
            nodes.append({"id": nid, "title": nid.replace('-',' ').title(), "path": f"codex/{p.name}", "tags": []})
            id_by_file[p.name] = nid

    edges = []
    for src, rels in relmap.items():
        for dst in rels:
            if src == dst:
                continue
            if src in id_by_file and dst in id_by_file:
                edges.append({"source": id_by_file[src], "target": id_by_file[dst]})
    return {"nodes": nodes, "edges": edges}

def main():
    cfg = load_json(CONFIG, required=True)
    relmap = cfg.get("links", {})
    ensure_map = cfg.get("ensure_entries", {})
    options = cfg.get("options", {})

    CODEX.mkdir(exist_ok=True)

    index = load_json(INDEX, required=False)

    created = []
    if options.get("create_missing_stubs"):
        for fname, meta in ensure_map.items():
            if ensure_stub(fname, meta["title"], meta["summary"], meta.get("tags", [])):
                created.append(fname)

    updated = []
    target_files = set(p.name for p in CODEX.glob("*.md")) | set(relmap.keys())
    for fname in sorted(target_files):
        p = CODEX / fname
        if not p.exists():
            # create a small placeholder if referenced but missing
            ensure_stub(fname, fname.replace('-', ' ').replace('.md','').title(), "Auto-generated placeholder.", ["auto","placeholder"])
        md = read(p)
        rels = relmap.get(fname, [])
        if options.get("append_links_section") and rels:
            new_md = ensure_links_section(md, rels[: options.get("max_links_per_entry", 6)])
            if new_md != md:
                write(p, new_md)
                updated.append(fname)

    graph_obj = {}
    if options.get("write_graph_json"):
        graph_obj = build_graph(index, relmap)
        save_json(GRAPH, graph_obj)

    if options.get("write_report"):
        lines = []
        lines.append("# Codex Web Hardening Report")
        lines.append(f"- Updated: {datetime.datetime.utcnow().isoformat()}Z")
        lines.append(f"- Files updated: {len(updated)}")
        if created:
            lines.append(f"- Stubs created: {', '.join(created)}")
        lines.append("")
        lines.append("## Link Coverage")
        for src, rels in sorted(relmap.items()):
            lines.append(f"- {src} → {', '.join(rels) if rels else '(none)'}")
        write(REPORT, "\n".join(lines))

    print("Hardening complete.")

if __name__ == "__main__":
    main()
