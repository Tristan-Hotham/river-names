/* Avon means river: the map. The Inked World base map with every named river and stream in the UK, coloured by the
 * generic word in its name (burn, beck, brook, allt, nant...) or, in the roots view, the courses of the rivers whose names
 * share a Brittonic or older root (Avon, Esk, Derwent, Calder...). Dr Tristan Hotham, Independent researcher, 2026. MIT licence. */
(function () {
  'use strict';
  const qs = new URLSearchParams(location.search);
  const BASE = window.INKBASE;
  const V = '?v=20261108';
  const ENGINE = ['js/curated.js', 'js/ink-palette.js', 'js/ink-icons.js', 'js/ink-houses.js', 'js/ink-map.js', 'js/ink-extras.js'];
  const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const norm = s => String(s).normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
  const small = matchMedia('(max-width:800px)').matches;
  const START = small ? [[-7.6, 50.0], [1.8, 58.7]] : [[-8.6, 49.9], [2.2, 59.0]];
  const GCOL = { brook: '#A3261B', beck: '#1F5F8B', burn: '#5E8F2E', bourne: '#D07A2A', water: '#6FA7C9', gill: '#6B3E8E', sike: '#8E8E3A', dyke: '#7A6A52',
    rhyne: '#C2577A', lode: '#B8862B', fleet: '#B9AC8E', allt: '#2E9C9A', abhainn: '#164B57', nant: '#C94F3A', afon: '#7A1F14', river: '#8C7B66', other: '#B9AC8E' };
  const RCOL = { avon: '#A3261B', isca: '#1F5F8B', ouse: '#6FA7C9', derwent: '#2F7F4A', dee: '#6B3E8E', don: '#8E5E9E', tam: '#2B2119', calder: '#B8862B',
    leven: '#4E9A6E', alaun: '#D07A2A', frome: '#C2577A', kennet: '#7A6A52', colne: '#8E8E3A', wye: '#3D6E9E', trent: '#7A1F14', severn: '#C94F3A' };
  const ORIG = ['', 'Brittonic or older', 'English', 'uncertain'];
  let map = null, D = null, RP = null, PL = null;
  let mode = qs.get('view') === 'roots' || qs.get('root') ? 'roots' : 'words', curRoot = qs.get('root') || 'all', curGen = qs.get('word') || 'all';

  document.getElementById('theme').addEventListener('click', () => {
    const r = document.documentElement, dark = r.dataset.theme ? r.dataset.theme === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
    r.dataset.theme = dark ? 'light' : 'dark';
  });
  const ct = document.getElementById('cartouche');
  const fold = f => ct.classList.toggle('folded', f);
  if (small) fold(true);
  document.getElementById('ctToggle').addEventListener('click', () => fold(!ct.classList.contains('folded')));
  document.getElementById('ctFold').addEventListener('click', () => fold(true));
  function loadScripts(list) {
    return list.reduce((p, src) => p.then(() => new Promise((res, rej) => {
      const el = document.createElement('script'); el.src = BASE + src + V; el.onload = res; el.onerror = () => rej(new Error('script ' + src)); document.head.appendChild(el);
    })), Promise.resolve());
  }

  // ---------------- popups
  let popup = null;
  function showPopup(r, lngLat) {
    const G = D.generics[r[3]], Rt = r[4] >= 0 ? D.roots[r[4]] : null;
    let h = `<b class="t">${esc(r[2])}</b>` + (r[9] ? `<div class="nt">${esc(r[9])}</div>` : '') + '<table>';
    if (r[3] !== D.generics.length - 1) h += `<tr><td>Word</td><td><span class="sw" style="background:${GCOL[G[0]]}"></span>${esc(G[1])}: ${esc(G[2])} ${esc(G[3])}</td></tr>`;
    if (Rt) h += `<tr><td>Root</td><td><span class="sw" style="background:${RCOL[Rt[0]]}"></span>${esc(Rt[1])}</td></tr><tr><td>Meaning</td><td>${esc(Rt[2])} (${esc(Rt[3])})</td></tr>`;
    if (r[7]) h += `<tr><td>Name</td><td>${ORIG[r[7]]} (one of the 60 largest English rivers in the data)</td></tr>`;
    h += `<tr><td>Where</td><td>${esc(r[6])}</td></tr></table>`;
    if (Rt && Rt[4]) h += `<p class="nt">${esc(Rt[4])}</p>`;
    h += `<p class="nt">Readings after Ekwall's English River-Names (1928), Watts (2004) and Mills (2011). The dot marks the middle of the river's mapped stretches.</p>`;
    h += `<div class="lk"><a href="https://www.openstreetmap.org/${esc(r[8])}" target="_blank" rel="noopener">OpenStreetMap</a></div>`;
    if (popup) popup.remove();
    popup = new maplibregl.Popup({ maxWidth: '320px', offset: 8, anchor: small ? 'top' : undefined }).setLngLat(lngLat).setHTML(h).addTo(map);
    if (small) map.easeTo({ center: lngLat, offset: [0, -220], duration: 600 });
  }

  // ---------------- views
  function apply() {
    const gi = D.generics.findIndex(g => g[0] === curGen), ri = D.roots.findIndex(r => r[0] === curRoot);
    const words = mode === 'words';
    map.setLayoutProperty('wc', 'visibility', document.getElementById('ckWc').checked ? 'visible' : 'none');
    map.setFilter('wc', words ? (curGen === 'all' ? ['!=', ['get', 'g'], D.generics.length - 1] : ['==', ['get', 'g'], gi]) : ['>=', ['get', 'r'], 0]);
    map.setPaintProperty('wc', 'circle-color', words ? ['match', ['get', 'g'], ...D.generics.flatMap((g, i) => [i, GCOL[g[0]] || '#999']), '#999']
      : ['match', ['get', 'r'], ...D.roots.flatMap((r, i) => [i, RCOL[r[0]]]), '#999']);
    map.setPaintProperty('wc', 'circle-opacity', words ? 0.85 : 0.0);
    map.setPaintProperty('wc', 'circle-stroke-opacity', words ? 1 : 0);
    map.setLayoutProperty('rp', 'visibility', !words && document.getElementById('ckRp').checked ? 'visible' : 'none');
    map.setFilter('rp', curRoot === 'all' ? ['>=', ['get', 'r'], 0] : ['==', ['get', 'r'], ri]);
    map.setLayoutProperty('rl', 'visibility', !words ? 'visible' : 'none');
    map.setFilter('rl', curRoot === 'all' ? ['>=', ['get', 'r'], 0] : ['==', ['get', 'r'], ri]);
    document.querySelectorAll('.chip[data-mode]').forEach(b => b.setAttribute('aria-pressed', b.dataset.mode === mode));
    document.querySelectorAll('input[name=view]').forEach(b => { b.checked = b.value === mode; });
    document.getElementById('chipsWords').hidden = !words; document.getElementById('chipsRoots').hidden = words;
    document.querySelectorAll('.chip[data-g]').forEach(b => b.setAttribute('aria-pressed', b.dataset.g === curGen));
    document.querySelectorAll('.chip[data-r]').forEach(b => b.setAttribute('aria-pressed', b.dataset.r === curRoot));
    const k = document.getElementById('key');
    if (words) k.innerHTML = '<b>Word for the stream</b>' + D.generics.filter(g => g[0] !== 'other').map(g => `<div class="row"><i class="dot" style="background:${GCOL[g[0]]}"></i>${esc(g[1])} <span class="nt">${esc(g[2])}</span></div>`).join('');
    else if (curRoot === 'all') k.innerHTML = '<b>Root of the name</b>' + D.roots.map(r => `<div class="row"><i class="dot" style="background:${RCOL[r[0]]}"></i>${esc(r[1].split(', ').slice(0, 3).join(', '))}</div>`).join('');
    else { const r = D.roots[ri]; k.innerHTML = `<b>${esc(r[1])}</b><div class="row">${esc(r[2])}</div><div class="row nt">${esc(r[4])}</div>`; }
    const u = new URL(location.href);
    u.searchParams.set('view', mode); if (words) { u.searchParams.delete('root'); curGen === 'all' ? u.searchParams.delete('word') : u.searchParams.set('word', curGen); }
    else { u.searchParams.delete('word'); curRoot === 'all' ? u.searchParams.delete('root') : u.searchParams.set('root', curRoot); }
    history.replaceState(null, '', u);
  }

  function setupSearch() {
    const q = document.getElementById('q'), sug = document.getElementById('sug');
    let items = [], k = -1;
    const rivers = D.rows.filter(r => r[5] || r[4] >= 0).map(r => ({ t: 'r', name: r[2], sub: r[6], lon: r[0], lat: r[1], r }));
    const towns = PL.places.map(p => ({ t: 'p', name: p[0], sub: p[4], lon: p[1], lat: p[2] }));
    const show = () => {
      const v = norm(q.value.trim()); sug.innerHTML = ''; k = -1;
      if (!v) { sug.style.display = 'none'; return; }
      const m = arr => arr.filter(p => norm(p.name).startsWith(v) || norm(p.name).startsWith('river ' + v)).concat(arr.filter(p => !norm(p.name).startsWith(v) && !norm(p.name).startsWith('river ' + v) && norm(p.name).includes(v)));
      items = m(rivers).slice(0, 8).concat(m(towns).slice(0, 8)).slice(0, 14);
      items.forEach((p, i) => { const li = document.createElement('li'); li.setAttribute('role', 'option');
        li.innerHTML = `${esc(p.name)} <span>${p.t === 'r' ? 'river · ' : ''}${esc(p.sub)}</span>`;
        li.addEventListener('mousedown', e => { e.preventDefault(); pick(i); }); sug.appendChild(li); });
      sug.style.display = items.length ? 'block' : 'none';
    };
    const pick = i => {
      const p = items[i]; if (!p) return; q.value = p.name; sug.style.display = 'none'; fold(true);
      map.flyTo({ center: [p.lon, p.lat], zoom: Math.max(map.getZoom(), p.t === 'r' ? 10 : 11), duration: 1300 });
      if (p.t === 'r') map.once('moveend', () => showPopup(p.r, [p.lon, p.lat]));
    };
    q.addEventListener('input', show);
    q.addEventListener('keydown', e => {
      const lis = [...sug.children];
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') { e.preventDefault(); k = Math.max(0, Math.min(lis.length - 1, k + (e.key === 'ArrowDown' ? 1 : -1))); lis.forEach((l, i) => l.setAttribute('aria-selected', i === k)); }
      else if (e.key === 'Enter') { e.preventDefault(); if (!items.length) show(); pick(k < 0 ? 0 : k); }
      else if (e.key === 'Escape') sug.style.display = 'none';
    });
    q.addEventListener('blur', () => setTimeout(() => sug.style.display = 'none', 150));
  }

  function setupLayers() {
    const feats = D.rows.map((r, i) => ({ type: 'Feature', properties: { i, g: r[3], r: r[4], v: r[5], n: r[2] }, geometry: { type: 'Point', coordinates: [r[0], r[1]] } }));
    map.addSource('wc', { type: 'geojson', data: { type: 'FeatureCollection', features: feats }, attribution: 'Waterways: OpenStreetMap contributors (ODbL)' });
    const rfeats = RP.pts.map(p => ({ type: 'Feature', properties: { r: p[2] }, geometry: { type: 'Point', coordinates: [p[0], p[1]] } }));
    map.addSource('rp', { type: 'geojson', data: { type: 'FeatureCollection', features: rfeats } });
    map.addLayer({ id: 'rp', type: 'circle', source: 'rp', paint: { 'circle-radius': ['interpolate', ['linear'], ['zoom'], 5, 1.8, 9, 3.2, 13, 5],
      'circle-color': ['match', ['get', 'r'], ...D.roots.flatMap((r, i) => [i, RCOL[r[0]]]), '#999'], 'circle-opacity': 0.9 } });
    map.addLayer({ id: 'wc', type: 'circle', source: 'wc', paint: {
      'circle-radius': ['interpolate', ['linear'], ['zoom'], 5, ['case', ['==', ['get', 'v'], 1], 2.2, 1.3], 9, ['case', ['==', ['get', 'v'], 1], 4.5, 3], 13, 6.5],
      'circle-color': '#2B2119', 'circle-stroke-color': '#FBF5E4', 'circle-stroke-width': ['interpolate', ['linear'], ['zoom'], 6, 0, 9, 0.8] } });
    map.addLayer({ id: 'rl', type: 'symbol', source: 'wc', minzoom: 6.5, filter: ['>=', ['get', 'r'], 0],
      layout: { 'text-field': ['get', 'n'], 'text-font': ['Ink Italic'], 'text-size': ['interpolate', ['linear'], ['zoom'], 6.5, 11, 12, 15], 'text-offset': [0, 0.8], 'text-anchor': 'top', 'text-optional': true },
      paint: { 'text-color': '#1F3A5A', 'text-halo-color': 'rgba(251,245,228,0.95)', 'text-halo-width': 1.6 } });
    map.addLayer({ id: 'wcl', type: 'symbol', source: 'wc', minzoom: 10.5,
      layout: { 'text-field': ['get', 'n'], 'text-font': ['Ink Italic'], 'text-size': 12, 'text-offset': [0, 0.8], 'text-anchor': 'top', 'text-optional': true },
      paint: { 'text-color': '#1F3A5A', 'text-halo-color': 'rgba(251,245,228,0.95)', 'text-halo-width': 1.4 } });
    const click = e => {
      if (mode === 'roots') { const f = map.queryRenderedFeatures(e.point, { layers: ['rp'] })[0]; if (f) { const ri = f.properties.r;
        const cand = D.rows.filter(r => r[4] === ri); let best = null, bd = 1e9;
        cand.forEach(r => { const d = (r[0] - e.lngLat.lng) ** 2 + (r[1] - e.lngLat.lat) ** 2; if (d < bd) { bd = d; best = r; } });
        if (best) { showPopup(best, e.lngLat); return; } } }
      const f = map.queryRenderedFeatures([[e.point.x - 6, e.point.y - 6], [e.point.x + 6, e.point.y + 6]], { layers: ['wc'] })[0];
      if (f) showPopup(D.rows[f.properties.i], f.geometry.coordinates);
    };
    map.on('click', click);
    for (const id of ['wc', 'rp']) { map.on('mouseenter', id, () => map.getCanvas().style.cursor = 'pointer'); map.on('mouseleave', id, () => map.getCanvas().style.cursor = ''); }
    const lp = document.getElementById('lp'), btn = document.getElementById('lyrBtn');
    btn.addEventListener('click', () => { const o = lp.classList.toggle('open'); btn.setAttribute('aria-expanded', o); });
    document.querySelectorAll('.chip[data-mode]').forEach(b => b.addEventListener('click', () => { mode = b.dataset.mode; apply(); }));
    document.querySelectorAll('.chip[data-g]').forEach(b => b.addEventListener('click', () => { curGen = b.dataset.g; apply(); }));
    document.querySelectorAll('.chip[data-r]').forEach(b => b.addEventListener('click', () => { curRoot = b.dataset.r; apply(); }));
    document.querySelectorAll('input[name=view]').forEach(b => b.addEventListener('change', () => { if (b.checked) { mode = b.value; apply(); } }));
    ['ckWc', 'ckRp'].forEach(id => document.getElementById(id).addEventListener('change', apply));
    document.getElementById('ckLab').addEventListener('change', e => map.setLayoutProperty('wcl', 'visibility', e.target.checked ? 'visible' : 'none'));
    const boxes = [...lp.querySelectorAll('input[data-g]')], modern = document.getElementById('modern');
    const base = () => {
      const m = modern.checked;
      boxes.forEach(b => { const g = b.dataset.g; const inkOnly = ['mountains', 'forests', 'sea', 'tint'].includes(g); try { InkMap.setGroup(map, g, b.checked && !(m && inkOnly)); } catch (e) { } });
      try { InkMap.setGroup(map, 'paper', !m); InkMap.setGroup(map, 'modern', m); InkMap.setGroup(map, 'coast', !m); if (m) InkMap.setGroup(map, 'roads', false); } catch (e) { }
    };
    boxes.forEach(b => b.addEventListener('change', base)); modern.addEventListener('change', base); base();
    apply();
  }

  Promise.all([fetch('data/rivers.json').then(r => r.json()), fetch('data/rootpts.json').then(r => r.json()), fetch('data/places.json').then(r => r.json())]).then(([j, rp, p]) => {
    D = j; RP = rp; PL = p;
    const opts = { base: BASE, winter: false };
    if (qs.get('tj')) opts.tilejson = qs.get('tj');
    if (qs.get('dem')) opts.dem = qs.get('dem');
    if (qs.get('demmax')) opts.demMax = +qs.get('demmax');
    const at = (qs.get('at') || '').split(',').map(Number);
    opts.mapOptions = at.length === 3 && at.every(isFinite) ? { center: [at[1], at[0]], zoom: at[2] } : { bounds: START, fitBoundsOptions: { padding: 6 } };
    return loadScripts(ENGINE).then(() => InkMap.create('map', opts));
  }).then(m => {
    map = m; window.__map = m;
    const n = document.getElementById('nojs'); if (n) n.remove();
    m.addControl(new maplibregl.NavigationControl({ showCompass: false }), 'bottom-right');
    const foldAt = () => document.querySelectorAll('.maplibregl-ctrl-attrib.maplibregl-compact').forEach(at => { at.classList.remove('maplibregl-compact-show'); at.removeAttribute('open'); });
    m.once('idle', foldAt); m.on('resize', () => setTimeout(foldAt, 50)); setTimeout(foldAt, 1500);
    setupLayers(); setupSearch();
    const first = e => { if (e.target.closest && e.target.closest('.cartouche,.ov,.lp,.keys,.mfs-btn,.maplibregl-ctrl,.maplibregl-popup')) return; fold(true); };
    document.getElementById('mapWrap').addEventListener('pointerdown', first, { capture: true, passive: true, once: true });
    document.querySelectorAll('a[data-root]').forEach(a => a.addEventListener('click', e => { e.preventDefault(); mode = 'roots'; curRoot = a.dataset.root; apply(); document.getElementById('mapWrap').scrollIntoView({ behavior: 'smooth' }); }));
    if (qs.get('open')) { const r = D.rows.find(r => r[8] === qs.get('open')); if (r) showPopup(r, [r[0], r[1]]); }
  }).catch(e => { console.error(e); const n = document.getElementById('nojs'); if (n) n.textContent = 'The map could not load: ' + e.message; });
})();
