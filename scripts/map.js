(async function () {
  const listEl = document.getElementById('codexList');
  const searchEl = document.getElementById('search');
  const clearEl = document.getElementById('clearSearch');

  // Start with embedded index (never blank)
  let index = Array.isArray(window.CodexIndex) ? window.CodexIndex : [];

  // Try to hydrate from codex/_index.json; fallback to embedded on any error
  try {
    const res = await fetch('codex/_index.json', { cache: 'no-store' });
    if (res.ok) {
      const json = await res.json();
      if (Array.isArray(json) && json.length) index = json;
    }
  } catch (_) {}

  function render(items) {
    listEl.innerHTML = '';
    if (!items.length) {
      listEl.innerHTML = '<p class="text-zinc-400">No entries found.</p>';
      return;
    }
    for (const it of items) {
      const card = document.createElement('article');
      card.className = 'bg-zinc-900/60 rounded-2xl p-5 shadow-lg border border-zinc-800';
      card.innerHTML = `
        <h3 class="text-lg font-semibold">${it.title}</h3>
        <p class="mt-1 text-zinc-400">${it.summary || ''}</p>
        <div class="mt-3 flex flex-wrap gap-2 text-xs text-zinc-400">${(it.tags||[]).map(t=>`<span class="px-2 py-1 bg-zinc-800 rounded-md">${t}</span>`).join('')}</div>
        <a class="mt-4 inline-block underline" href="${it.path}">Open</a>
      `;
      listEl.appendChild(card);
    }
  }

  function applyFilter() {
    const q = (searchEl.value || '').toLowerCase();
    if (!q) return render(index);
    const filtered = index.filter(it =>
      (it.title||'').toLowerCase().includes(q) ||
      (it.summary||'').toLowerCase().includes(q) ||
      (it.tags||[]).some(t => t.toLowerCase().includes(q))
    );
    render(filtered);
  }

  searchEl?.addEventListener('input', applyFilter);
  clearEl?.addEventListener('click', () => { searchEl.value=''; applyFilter(); });

  render(index);
})();