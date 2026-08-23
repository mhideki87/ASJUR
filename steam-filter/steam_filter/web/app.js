'use strict';

const $ = (sel) => document.querySelector(sel);
const PAGE = 60;
const STORAGE_KEY = 'steam-filter:filters';

const state = { offset: 0, total: 0, loading: false, onlineCount: 0, lastGames: [] };

// ------------------------------------------------------------------ helpers

async function api(path, options) {
  const resp = await fetch(path, options);
  let data = null;
  try { data = await resp.json(); } catch (_) { /* resposta sem corpo */ }
  if (!resp.ok) {
    const msg = (data && (data.detail || data.message)) || `HTTP ${resp.status}`;
    throw new Error(typeof msg === 'string' ? msg : JSON.stringify(msg));
  }
  return data;
}

function banner(text, kind = 'info') {
  const el = $('#banner');
  if (!text) { el.className = 'banner hidden'; el.textContent = ''; return; }
  el.className = `banner ${kind}`;
  el.innerHTML = text;
}

const hours = (minutes) => (!minutes ? '—' : minutes < 60 ? `${minutes} min` : `${Math.round(minutes / 60)} h`);

function ago(ts) {
  if (!ts) return 'nunca';
  const days = Math.floor((Date.now() / 1000 - ts) / 86400);
  if (days <= 0) return 'hoje';
  if (days === 1) return 'ontem';
  if (days < 30) return `${days} d atrás`;
  if (days < 365) return `${Math.floor(days / 30)} mes(es) atrás`;
  return `${Math.floor(days / 365)} ano(s) atrás`;
}

const escapeHtml = (s) => String(s ?? '').replace(/[&<>"']/g, (c) =>
  ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

// ------------------------------------------------------------------ filtros

function readFilters() {
  return {
    search: $('#f-search').value.trim(),
    ownership: $('#f-ownership').value,
    min_friends: Number($('#f-min-friends').value),
    online: $('#f-online').checked,
    min_friends_online: $('#f-online').checked ? Number($('#f-min-online').value) : 0,
    multiplayer: $('#f-multiplayer').value,
    include_unknown_details: $('#f-unknown').checked,
    played_recently_by_friends: $('#f-recent').checked,
    unplayed_by_me: $('#f-unplayed').checked,
    sort: $('#f-sort').value,
  };
}

function applyFilters(f) {
  if (!f) return;
  $('#f-search').value = f.search || '';
  $('#f-ownership').value = f.ownership || 'mine';
  $('#f-min-friends').value = f.min_friends ?? 1;
  $('#f-online').checked = !!f.online;
  $('#f-min-online').value = f.min_friends_online || 1;
  $('#f-multiplayer').value = f.multiplayer || 'any';
  $('#f-unknown').checked = f.include_unknown_details !== false;
  $('#f-recent').checked = !!f.played_recently_by_friends;
  $('#f-unplayed').checked = !!f.unplayed_by_me;
  $('#f-sort').value = f.sort || 'friends';
  syncFilterLabels();
}

function syncFilterLabels() {
  $('#f-min-friends-out').textContent = $('#f-min-friends').value;
  $('#f-min-online-out').textContent = $('#f-min-online').value;
  $('#f-min-online-wrap').hidden = !$('#f-online').checked;
}

function saveFilters() {
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(readFilters())); } catch (_) { /* ignora */ }
}

function loadFilters() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) applyFilters(JSON.parse(raw));
  } catch (_) { /* ignora */ }
}

// -------------------------------------------------------------------- jogos

function tagsFor(game) {
  const tags = [];
  if (game.details_state !== 'ok') {
    tags.push('<span class="tag unknown" title="Categorias ainda não baixadas da loja">categoria ?</span>');
  }
  const flags = [
    ['is_online_coop', 'co-op online'],
    ['is_local_coop', 'co-op local'],
    ['is_pvp', 'PvP'],
    ['is_remote_together', 'remote together'],
  ];
  for (const [key, label] of flags) if (game[key]) tags.push(`<span class="tag on">${label}</span>`);
  if (!tags.some((t) => t.includes('tag on')) && game.is_multiplayer) {
    tags.push('<span class="tag on">multiplayer</span>');
  }
  if (game.details_state === 'ok' && !game.is_multiplayer) {
    tags.push('<span class="tag">single-player</span>');
  }
  return tags.join('');
}

function cardHtml(game) {
  const online = game.friends_online > 0;
  const countLabel = online
    ? `${game.friends_online} online / ${game.friends} 👥`
    : `${game.friends} 👥`;
  const mine = game.i_own
    ? `você: ${hours(game.my_playtime)}`
    : '<b>você não tem</b>';
  return `
  <article class="card" data-appid="${game.appid}">
    <div class="thumb">
      <span class="thumb-fallback">${escapeHtml(game.name || game.appid)}</span>
      <img loading="lazy" src="${game.header}" alt="" onerror="this.remove()">
      <span class="count ${online ? 'online' : ''}" title="Amigos que têm o jogo">${countLabel}</span>
    </div>
    <div class="body">
      <h3>${escapeHtml(game.name || game.appid)}</h3>
      <div class="tags">${tagsFor(game)}</div>
      <div class="meta">
        <span>${mine}</span>
        ${game.friends_recent ? `<span>${game.friends_recent} amigo(s) jogaram nas 2 sem.</span>` : ''}
        ${game.metacritic ? `<span>MC ${game.metacritic}</span>` : ''}
      </div>
      <div class="card-actions">
        <button class="btn tiny" data-action="friends">Quem tem</button>
        <a class="btn tiny" href="${game.store_url}" target="_blank" rel="noreferrer">Loja</a>
        ${game.i_own ? `<a class="btn tiny" href="${game.run_url}">Jogar</a>` : ''}
      </div>
    </div>
  </article>`;
}

async function loadGames(reset = true) {
  if (state.loading) return;
  state.loading = true;
  if (reset) state.offset = 0;

  const f = readFilters();
  const params = new URLSearchParams({
    ownership: f.ownership,
    min_friends: f.min_friends,
    min_friends_online: f.min_friends_online,
    multiplayer: f.multiplayer,
    search: f.search,
    unplayed_by_me: f.unplayed_by_me,
    played_recently_by_friends: f.played_recently_by_friends,
    include_unknown_details: f.include_unknown_details,
    online: f.online || f.sort === 'friends_online',
    sort: f.sort,
    limit: PAGE,
    offset: state.offset,
  });

  $('#results-note').textContent = 'carregando…';
  try {
    const data = await api(`/api/games?${params}`);
    state.total = data.total;
    state.onlineCount = data.online_friends || 0;
    const grid = $('#grid');
    const html = data.games.map(cardHtml).join('');
    if (reset) { grid.innerHTML = html; state.lastGames = data.games.slice(); }
    else { grid.insertAdjacentHTML('beforeend', html); state.lastGames.push(...data.games); }

    state.offset += data.games.length;
    $('#results-count').textContent = `${data.total} jogo(s)`;
    $('#results-note').textContent = data.online_error
      ? `amigos online indisponíveis: ${data.online_error}`
      : (f.online ? `${state.onlineCount} amigo(s) online agora` : '');
    $('#btn-more').classList.toggle('hidden', state.offset >= data.total);
    $('#empty').classList.toggle('hidden', data.total > 0);
    if (data.total === 0) {
      $('#empty').innerHTML = 'Nenhum jogo com esses filtros.<br>Tente baixar o mínimo de amigos, ' +
        'trocar para "Meus + dos amigos" ou sincronizar de novo.';
    }
  } catch (err) {
    banner(`Erro ao listar jogos: ${escapeHtml(err.message)}`, 'error');
  } finally {
    state.loading = false;
  }
}

// ------------------------------------------------------------------ overview

async function loadOverview() {
  try {
    const o = await api('/api/overview');
    $('#chip-games').textContent = `${o.my_games || 0} jogos meus`;
    $('#chip-friends').textContent = `${o.friends_public || 0}/${o.friends || 0} amigos legíveis`;
    $('#me-line').textContent = o.me_name
      ? `${o.me_name} · última sincronização ${ago(o.last_sync_at)}`
      : 'Ainda não sincronizado';

    const parts = [];
    if (o.friends_private) parts.push(`${o.friends_private} amigo(s) com biblioteca privada não entram na contagem.`);
    if (o.details_pending) parts.push(`${o.details_pending} jogo(s) sem categoria — <a href="#">continuar detalhes</a>.`);
    $('#coverage-hint').innerHTML = parts.join('<br>');

    if (!o.is_ready) {
      banner('Configure a <b>chave da Steam Web API</b> e o seu <b>SteamID</b> para começar.', 'warn');
      $('#dlg-config').open || $('#dlg-config').showModal();
    } else if (!o.last_sync_at) {
      banner('Tudo configurado. Clique em <b>Sincronizar</b> para baixar sua biblioteca e a dos amigos.', 'info');
    }
    return o;
  } catch (err) {
    banner(`Erro ao carregar estado: ${escapeHtml(err.message)}`, 'error');
    return null;
  }
}

async function loadOnlineChip() {
  try {
    const data = await api('/api/online');
    $('#chip-online').textContent = `${data.count} online`;
  } catch (_) {
    $('#chip-online').textContent = '— online';
  }
}

// ---------------------------------------------------------------------- sync

let syncTimer = null;

function renderSync(snap) {
  const bar = $('#sync-bar');
  if (!snap || (!snap.running && snap.status === 'idle')) { bar.classList.add('hidden'); return; }
  bar.classList.remove('hidden');
  $('#sync-phase').textContent = snap.phase;
  $('#sync-msg').textContent = snap.message || '';
  $('#sync-fill').style.width = `${snap.percent || (snap.running ? 3 : 100)}%`;
  $('#btn-cancel').classList.toggle('hidden', !snap.running);
  $('#btn-sync').disabled = snap.running;

  if (!snap.running) {
    if (snap.status === 'error') banner(`Sincronização falhou: ${escapeHtml(snap.message)}`, 'error');
    else if (snap.warnings && snap.warnings.length) banner(snap.warnings.map(escapeHtml).join('<br>'), 'warn');
    else banner('');
    setTimeout(() => bar.classList.add('hidden'), 4000);
  }
}

async function pollSync() {
  try {
    const snap = await api('/api/sync/status');
    renderSync(snap);
    if (!snap.running) {
      clearInterval(syncTimer);
      syncTimer = null;
      await loadOverview();
      await loadGames(true);
      await loadOnlineChip();
    }
  } catch (_) { /* tenta de novo no proximo tick */ }
}

async function startSync(mode) {
  banner('');
  try {
    const snap = await api('/api/sync', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mode }),
    });
    renderSync(snap);
    if (!syncTimer) syncTimer = setInterval(pollSync, 900);
  } catch (err) {
    banner(`Não foi possível sincronizar: ${escapeHtml(err.message)}`, 'error');
  }
}

// -------------------------------------------------------------------- modais

async function showGameFriends(appid) {
  const dlg = $('#dlg-game');
  $('#dlg-game-title').textContent = 'Carregando…';
  $('#dlg-game-body').innerHTML = '';
  dlg.showModal();
  try {
    const data = await api(`/api/games/${appid}/friends`);
    $('#dlg-game-title').textContent = `${data.name} — ${data.friends.length} amigo(s)`;
    $('#dlg-game-body').innerHTML = data.friends.length
      ? data.friends.map((f) => `
        <div class="friend">
          <span class="dot ${f.playing ? 'playing' : f.online ? 'on' : ''}"></span>
          <img src="${f.avatar || ''}" alt="" onerror="this.style.visibility='hidden'">
          <span class="name">
            <a href="${f.profileurl || '#'}" target="_blank" rel="noreferrer">${escapeHtml(f.personaname)}</a>
            <div class="state ${f.online ? 'on' : ''}">${escapeHtml(f.playing ? `jogando ${f.playing}` : f.state || '')}</div>
          </span>
          <span class="hours">${hours(f.playtime_forever)}${f.playtime_2weeks ? ` · ${hours(f.playtime_2weeks)} nas 2 sem.` : ''}</span>
        </div>`).join('')
      : '<p class="muted">Nenhum amigo com biblioteca pública tem esse jogo.</p>';
  } catch (err) {
    $('#dlg-game-body').innerHTML = `<p class="muted">Erro: ${escapeHtml(err.message)}</p>`;
  }
}

async function showFriendsPanel() {
  const dlg = $('#dlg-friends');
  $('#dlg-friends-body').innerHTML = 'Carregando…';
  dlg.showModal();
  try {
    const { friends } = await api('/api/friends');
    const label = { public: 'biblioteca pública', private: 'biblioteca privada', error: 'erro ao ler' };
    $('#dlg-friends-body').innerHTML = friends.map((f) => `
      <div class="friend">
        <span class="dot ${f.library_state === 'public' ? 'on' : ''}"></span>
        <img src="${f.avatar || ''}" alt="" onerror="this.style.visibility='hidden'">
        <span class="name">
          <a href="${f.profileurl || '#'}" target="_blank" rel="noreferrer">${escapeHtml(f.personaname || f.steamid)}</a>
          <div class="state">${label[f.library_state] || 'não sincronizado'}</div>
        </span>
        <span class="hours">${f.library_state === 'public' ? `${f.shared_with_me} em comum · ${f.games_count} jogos` : ''}</span>
      </div>`).join('') || '<p class="muted">Nenhum amigo sincronizado ainda.</p>';
  } catch (err) {
    $('#dlg-friends-body').innerHTML = `<p class="muted">Erro: ${escapeHtml(err.message)}</p>`;
  }
}

async function openConfig() {
  const dlg = $('#dlg-config');
  try {
    const c = await api('/api/config');
    $('#c-api-key').placeholder = c.api_key_set ? c.api_key : 'cole a chave aqui';
    $('#c-steam-id').value = c.steam_id || '';
    $('#c-api-rate').value = c.api_rate_per_sec;
    $('#c-store-rate').value = c.store_rate_per_sec;
    $('#c-store-budget').value = c.store_budget_per_sync;
    $('#c-details-min').value = c.details_min_friends;
    $('#c-concurrency').value = c.friend_concurrency;
    $('#config-msg').textContent = c.api_key_from_env ? 'chave vindo do .env (o .env tem prioridade)' : '';
  } catch (err) {
    $('#config-msg').textContent = err.message;
  }
  if (!dlg.open) dlg.showModal();
}

async function saveConfig(event) {
  event.preventDefault();
  const payload = {
    api_key: $('#c-api-key').value,
    steam_id: $('#c-steam-id').value,
    api_rate_per_sec: Number($('#c-api-rate').value) || undefined,
    store_rate_per_sec: Number($('#c-store-rate').value) || undefined,
    store_budget_per_sync: Number($('#c-store-budget').value),
    details_min_friends: Number($('#c-details-min').value) || undefined,
    friend_concurrency: Number($('#c-concurrency').value) || undefined,
  };
  try {
    await api('/api/config', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    $('#c-api-key').value = '';
    $('#config-msg').textContent = 'salvo';
    banner('');
    await loadOverview();
  } catch (err) {
    $('#config-msg').textContent = `erro: ${err.message}`;
  }
}

function pickRandom() {
  if (!state.lastGames.length) { banner('Nada para sortear com esses filtros.', 'warn'); return; }
  const game = state.lastGames[Math.floor(Math.random() * state.lastGames.length)];
  banner(
    `🎲 <b>${escapeHtml(game.name)}</b> — ${game.friends} amigo(s) têm` +
    `${game.friends_online ? `, ${game.friends_online} online agora` : ''}. ` +
    `<a href="${game.store_url}" target="_blank" rel="noreferrer">loja</a>` +
    `${game.i_own ? ` · <a href="${game.run_url}">jogar</a>` : ''}`,
    'info',
  );
  const card = document.querySelector(`.card[data-appid="${game.appid}"]`);
  if (card) card.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

// ------------------------------------------------------------------- eventos

function debounce(fn, ms) {
  let handle;
  return (...args) => { clearTimeout(handle); handle = setTimeout(() => fn(...args), ms); };
}

function wire() {
  const rerun = debounce(() => { saveFilters(); loadGames(true); }, 220);
  for (const id of ['#f-search', '#f-ownership', '#f-min-friends', '#f-online', '#f-min-online',
                    '#f-multiplayer', '#f-unknown', '#f-recent', '#f-unplayed', '#f-sort']) {
    const el = $(id);
    el.addEventListener('input', () => { syncFilterLabels(); rerun(); });
    el.addEventListener('change', () => { syncFilterLabels(); rerun(); });
  }

  $('#btn-more').addEventListener('click', () => loadGames(false));
  $('#btn-random').addEventListener('click', pickRandom);
  $('#btn-reset').addEventListener('click', () => {
    applyFilters({ ownership: 'mine', min_friends: 1, multiplayer: 'any', sort: 'friends',
                   include_unknown_details: true });
    saveFilters();
    loadGames(true);
  });

  $('#btn-sync').addEventListener('click', () => startSync('full'));
  $('#btn-cancel').addEventListener('click', () => api('/api/sync/cancel', { method: 'POST' }));
  $('#btn-config').addEventListener('click', openConfig);
  $('#btn-friends-panel').addEventListener('click', showFriendsPanel);
  $('#form-config').addEventListener('submit', saveConfig);

  $('#coverage-hint').addEventListener('click', (e) => {
    if (e.target.tagName === 'A') { e.preventDefault(); startSync('details'); }
  });

  $('#grid').addEventListener('click', (event) => {
    const btn = event.target.closest('[data-action="friends"]');
    if (!btn) return;
    showGameFriends(btn.closest('.card').dataset.appid);
  });

  for (const btn of document.querySelectorAll('[data-close]')) {
    btn.addEventListener('click', () => btn.closest('dialog').close());
  }
}

async function boot() {
  loadFilters();
  syncFilterLabels();
  wire();
  const overview = await loadOverview();
  await loadGames(true);
  loadOnlineChip();
  setInterval(loadOnlineChip, 60000);
  if (overview && overview.sync && overview.sync.running && !syncTimer) {
    syncTimer = setInterval(pollSync, 900);
  }
}

boot();
