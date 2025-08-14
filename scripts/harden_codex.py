#!/usr/bin/env python3
import os, re, json, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
CODEX = ROOT / "codex"
INDEX = CODEX / "_index.json"
CONFIG = ROOT / "hardening_config.json"
GRAPH = ROOT / "graph.json"
REPORT = ROOT / "HARDENING_REPORT.md"

def load_json(p):
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return None

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
    fm = f"---\nid: {re.sub(r'[^a-z0-9\-]+','-', title.lower()).strip('-')}\ntitle: {title}\ntags: [{', '.join(tags)}]\n---\n\n"
    body = f"## Summary\n{summary}\n\n## Body\n(Placeholder — to be expanded.)\n\n## Links\n"
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

def ensure_links_section(md, rels, current_filename):
    fm, body = parse_front_matter(md)
    if "## Links" not in body:
        body = body.rstrip() + "\n\n## Links\n"
    existing = set()
    for m in re.finditer(r'\[.*?\]\((.*?)\)', body):
        existing.add(m.group(1))
    to_add = []
    for r in rels:
        path = f"./{r}"
        if path not in existing:
            title_guess = r.replace('-', ' ').replace('.md','').title()
            to_add.append(f"- See also: [{title_guess}]({path})")
    if to_add:
        body = body.rstrip() + "\n" + "\n".join(to_add) + "\n"
    if md.startswith("---"):
        parts = md.split("---", 2)
        return parts[0] + "---" + parts[1] + "---\n" + body
    else:
        return md + "\n" + body

def build_graph(index, relmap):
    nodes = []
    id_by_file = {}
    for it in index or []:
        nodes.append({
            "id": it.get("id") or it["path"],
            "title": it["title"],
            "path": it["path"],
            "tags": it.get("tags", [])
        })
        id_by_file[it["path"].split('/')[-1]] = it.get("id") or it["path"]
    edges = []
    for src, rels in relmap.items():
        for dst in rels:
            if src == dst:
                continue
            if src in id_by_file and dst in id_by_file:
                edges.append({"source": id_by_file[src], "target": id_by_file[dst]})
    return {"nodes": nodes, "edges": edges}

def main():
    cfg = load_json(CONFIG)
    if not cfg:
        raise SystemExit("Missing hardening_config.json")
    options = cfg.get("options", {})
    relmap = cfg.get("links", {})
    ensure = cfg.get("ensure_entries", {})
    index = load_json(INDEX) or []
    existing_files = {p.name for p in CODEX.glob("*.md")}
    created = []
    if options.get("create_missing_stubs"):
        for fname, meta in ensure.items():
            if ensure_stub(fname, meta["title"], meta["summary"], meta.get("tags", [])):
                created.append(fname)
    updated = []
    for fname in existing_files | set(relmap.keys()):
        p = CODEX / fname
        if not p.exists():
            ensure_stub(fname, fname.replace('-', ' ').replace('.md','').title(),
                        "Auto-generated placeholder.", ["auto","placeholder"])
        md = read(p)
        rels = relmap.get(fname, [])
        if options.get("append_links_section") and rels:
            new_md = ensure_links_section(md, rels[: options.get("max_links_per_entry", 6)], fname)
            if new_md != md:
                write(p, new_md)
                updated.append(fname)
    graph_obj = {}
    if options.get("write_graph_json") and index:
        graph_obj = build_graph(index, relmap)
        save_json(GRAPH, graph_obj)
    if options.get("write_report"):
        report = []
        report.append("# Codex Web Hardening Report")
        report.append(f"- Updated: {datetime.datetime.utcnow().isoformat()}Z")
        report.append(f"- Files updated: {len(updated)}")
        if created:
            report.append(f"- Stubs created: {', '.join(created)}")
        report.append("\n## Link Coverage")
        for src, rels in sorted(relmap.items()):
            report.append(f"- {src} → {', '.join(rels) if rels else '(none)'}")
        if graph_obj:
            report.append(f"\n- Nodes: {len(graph_obj.get('nodes', []))}, Edges: {len(graph_obj.get('edges', []))}")
        write(REPORT, "\n".join(report))
    print("Hardening complete.")

if __name__ == "__main__":
    main()
