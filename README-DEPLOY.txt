Codex ∞ — Full Display Package
=================================

Files
-----
- index.html           Minimal API-driven index of all `.md` files (codex/ & codex-entries/)
- view-pretty.html     Markdown renderer (auto-routes `.md` links, supports YAML front-matter)
- codex.css            Aesthetic dark theme
- 404.html             Friendly not-found page

Install
-------
1) Upload these four files to the **repo root** (same level as your `codex/` folder).
2) Wait for "pages build and deployment" to finish under the Actions tab.
3) Open your site root, then click entries:
   https://<user>.github.io/<repo>/

Notes
-----
- You can freely link between Codex pages using relative `.md` links (e.g. `./the-flame-protocol.md`).
  The viewer rewrites them to `view-pretty.html?f=the-flame-protocol.md` automatically.
- If a file is in `codex-entries/`, it still resolves—no edits needed.
- Optional front-matter keys the viewer understands:
  ---
  title: Nice Human Title
  epigraph: "short poetic line for humans"
  tags: [ai, design]
  ---
