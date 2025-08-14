import os
import json

CONFIG_PATH = 'hardening_config.json'
CODEX_DIR = 'codex'
REPORT_FILE = 'HARDENING_REPORT.md'
GRAPH_FILE = 'graph.json'

def load_config():
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)

def ensure_links(entry_path, links):
    with open(entry_path, 'r') as f:
        content = f.read()
    if '## Links' not in content:
        content += '\n\n## Links\n'
    for link in links:
        if link not in content:
            content += f'- [[{link}]]\n'
    with open(entry_path, 'w') as f:
        f.write(content)

def main():
    config = load_config()
    os.makedirs(CODEX_DIR, exist_ok=True)
    report_lines = []
    graph = {"nodes": [], "edges": []}
    
    for node, linked_nodes in config.items():
        node_file = os.path.join(CODEX_DIR, node.replace(' ', '_').lower() + '.md')
        if not os.path.exists(node_file):
            with open(node_file, 'w') as f:
                f.write(f'# {node}\n\n## Links\n')
            report_lines.append(f"Created stub for missing node: {node}")
        ensure_links(node_file, linked_nodes)
        graph["nodes"].append(node)
        for ln in linked_nodes:
            graph["edges"].append({"from": node, "to": ln})
    
    with open(REPORT_FILE, 'w') as f:
        f.write('\n'.join(report_lines) if report_lines else "All nodes present and linked.")
    
    with open(GRAPH_FILE, 'w') as f:
        json.dump(graph, f, indent=4)

if __name__ == "__main__":
    main()
