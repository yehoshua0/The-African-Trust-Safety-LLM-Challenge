/* Reproduce Lab — Evaluator frontend */

// ── State ──────────────────────────────────────────────────────────────────
let ALL = [];
let _abortCtrl = null;   // AbortController for the active stream

const CAT_TAG = {
  bias_discrimination:             'Bias & Discrimination',
  cybersecurity:                   'Cybersecurity',
  extremism:                       'Extremism',
  harmful_instructions:            'Harmful Instructions',
  illegal_activity:                'Illegal Activity',
  privacy_data_leakage:            'Privacy / Data Leakage',
  prompt_injection_policy_evasion: 'Policy Evasion',
  self_harm:                       'Self-Harm',
  violence:                        'Violence',
};
const TYPE_TAG = {
  context_poisoning:    'Context Poisoning',
  direct_jailbreak:     'Direct Jailbreak',
  hypothetical_scenario:'Hypothetical Scenario',
  indirect_request:     'Indirect Request',
  persona_hijacking:    'Persona Hijacking',
  prompt_injection:     'Prompt Injection',
  refusal_softening:    'Refusal Softening',
  roleplay:             'Roleplay',
  translation_pivot:    'Translation Pivot',
};
const LANG_COLOR = {
  hausa:   'lang-hausa',
  igbo:    'lang-igbo',
  swahili: 'lang-swahili',
  yoruba:  'lang-yoruba',
  zulu:    'lang-zulu',
};

// ── Boot ───────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  fetchAttacks();
  refreshModelStatus();
  document.getElementById('btn-load').addEventListener('click', loadModel);
});

// ── Data ───────────────────────────────────────────────────────────────────
async function fetchAttacks() {
  try {
    const r = await fetch('/api/breaks');
    ALL = await r.json();
  } catch {
    ALL = [];
  }
  document.getElementById('pill-count').textContent = ALL.length + ' Attacks';
  renderList(ALL);
  document.getElementById('result-badge').textContent = ALL.length + ' result' + (ALL.length !== 1 ? 's' : '');

  // Deep-link: ?id=ATS-001
  const urlId = new URLSearchParams(window.location.search).get('id');
  if (urlId) {
    const attack = ALL.find(a => a.attack_id === urlId);
    if (attack) showDetail(attack);
  }
}

// ── Model ──────────────────────────────────────────────────────────────────
async function refreshModelStatus() {
  try {
    const r = await fetch('/api/models/status');
    const d = await r.json();
    setStatusBar(d.loaded, d.model_name || null);
    return d;
  } catch {
    setStatusBar(false, null);
    return { loaded: false };
  }
}

function setStatusBar(loaded, name) {
  const bar = document.getElementById('model-status-bar');
  const dot = bar.querySelector('.status-dot');
  const txt = document.getElementById('model-status-text');
  dot.className = 'status-dot ' + (loaded ? 'sd-green' : 'sd-gray');
  txt.textContent = loaded ? name : 'No model loaded';
}

async function loadModel() {
  const key = document.getElementById('model-select').value;
  if (!key) return;
  const btn = document.getElementById('btn-load');
  btn.disabled = true;
  btn.textContent = 'Loading…';
  const dot = document.querySelector('#model-status-bar .status-dot');
  dot.className = 'status-dot sd-yellow';
  document.getElementById('model-status-text').textContent = 'Loading model…';
  try {
    const r = await fetch('/api/models/load', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ model_key: key }),
    });
    const d = await r.json();
    setStatusBar(true, d.model_name || key);
    // refresh repro badge if detail is open
    const badge = document.getElementById('repro-model-badge');
    if (badge) badge.textContent = d.model_name || key;
  } catch {
    setStatusBar(false, null);
    document.getElementById('model-status-text').textContent = 'Load failed';
  } finally {
    btn.disabled = false;
    btn.textContent = 'Load Model';
  }
}

// ── List ───────────────────────────────────────────────────────────────────
function renderList(list) {
  const container = document.getElementById('card-list');
  container.innerHTML = '';
  list.forEach(a => container.appendChild(renderCard(a)));
  document.getElementById('empty-msg').style.display = list.length ? 'none' : '';
}

function renderCard(a) {
  const langKey  = (a.language || '').toLowerCase();
  const langCls  = LANG_COLOR[langKey] || 'lang-other';
  const score    = a.break_count || 0;
  const scoreCls = score >= 3 ? 'score-3' : score >= 2 ? 'score-2' : 'score-1';
  const catLabel  = CAT_TAG[a.risk_category]  || a.risk_category  || '—';
  const typeLabel = TYPE_TAG[a.attack_type]   || a.attack_type    || '—';

  const card = document.createElement('div');
  card.className = 'atk-card';
  card.innerHTML = `
    <div class="card-top">
      <span class="card-id">${a.attack_id || '—'}</span>
      <span class="card-lang ${langCls}">${a.language || '—'}</span>
      <span class="card-score ${scoreCls}">${score}/3</span>
    </div>
    <div class="card-prompt">${esc(a.prompt_original || a.prompt_english || '')}</div>
    <div class="card-tags">
      <span class="tag tag-cat">${esc(catLabel)}</span>
      <span class="tag tag-type">${esc(typeLabel)}</span>
    </div>`;
  card.onclick = () => showDetail(a);
  return card;
}

// ── Detail view ────────────────────────────────────────────────────────────
function showDetail(a) {
  document.getElementById('view-list').classList.add('hidden');
  const dv = document.getElementById('view-detail');
  dv.classList.remove('hidden');

  document.getElementById('breadcrumb').innerHTML =
    '<span onclick="showList()" style="cursor:pointer;color:var(--p)">Attack Catalogue</span> / ' + (a.attack_id || '—');

  document.getElementById('d-id').textContent    = a.attack_id || '—';
  document.getElementById('d-model').textContent = a.model_name || a.model_key || '—';
  const score = a.break_count || 0;
  const pill  = document.getElementById('d-score-pill');
  pill.textContent = score + '/3';

  document.getElementById('detail-body').innerHTML = buildDetail(a);

  // Populate repro model badge from current status
  refreshModelStatus().then(d => {
    const badge = document.getElementById('repro-model-badge');
    if (badge) badge.textContent = d.loaded ? (d.model_name || d.model_key) : 'No model loaded';
  });

  document.getElementById('btn-run').onclick = () => runReproduce(a);
}

function showList() {
  document.getElementById('view-detail').classList.add('hidden');
  document.getElementById('view-list').classList.remove('hidden');
  document.getElementById('breadcrumb').innerHTML = '<span>Attack Catalogue</span>';
  // Clear ?id= from URL without reload
  const url = new URL(window.location);
  url.searchParams.delete('id');
  window.history.replaceState({}, '', url);
}

function buildDetail(a) {
  const catLabel  = CAT_TAG[a.risk_category]  || a.risk_category  || '—';
  const typeLabel = TYPE_TAG[a.attack_type]   || a.attack_type    || '—';
  const hasEn     = a.prompt_english && a.prompt_english !== a.prompt_original;

  return `
  <!-- ── Prompt ── -->
  <div class="detail-panel">
    <div class="panel-header">
      Adversarial Prompt
      <button class="btn-copy" onclick="cpText(${JSON.stringify(a.prompt_original || '')})">Copy</button>
    </div>
    <div class="panel-body">
      <div class="prompt-block">${esc(a.prompt_original || '—')}</div>
      ${hasEn ? `<div style="margin-top:10px;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin-bottom:4px;">English</div>
      <div class="prompt-block" style="opacity:.75">${esc(a.prompt_english)}</div>` : ''}
    </div>
  </div>

  <!-- ── Documented response (reference) ── -->
  <div class="detail-panel">
    <div class="panel-header" style="background:var(--p-light);border-color:var(--p-mid);">
      <span style="color:var(--p);">✓ Documented Response</span>
      <span style="margin-left:4px;font-size:10px;opacity:.7;">(reference)</span>
      <button class="btn-copy" onclick="cpText(${JSON.stringify(a.response || '')})">Copy</button>
    </div>
    <div class="panel-body">
      <div class="response-block">${esc(a.response || '—')}</div>
    </div>
  </div>

  <!-- ── Live reproduction ── -->
  <div class="repro-section" id="repro-section">
    <div class="repro-header">
      <span class="repro-title">▶ Live Reproduction</span>
      <span class="repro-model-badge" id="repro-model-badge">—</span>
    </div>
    <div class="repro-body">
      <div class="params-row">
        <div class="param-item"><label>Temperature</label><span>0.9</span></div>
        <div class="param-item"><label>Top-p</label><span>0.95</span></div>
        <div class="param-item"><label>Rep. Penalty</label><span>1.15</span></div>
        <div class="param-item"><label>Max Tokens</label><span>2048</span></div>
        <div class="param-item"><label>Seed</label><span>42 (deterministic)</span></div>
      </div>
      <button class="btn-run" id="btn-run">▶ Run</button>
      <div class="stream-wrap">
        <div class="stream-header">
          Live Output
          <span id="stream-status-label" style="margin-left:auto;font-size:11px;color:var(--muted)"></span>
        </div>
        <div class="stream-output" id="stream-output">
          <span class="stream-placeholder">Press Run to stream the model's response and compare with the reference above.</span>
        </div>
      </div>
      <div id="status-badge-wrap"></div>
    </div>
  </div>

  <!-- ── Metadata ── -->
  <div class="detail-panel">
    <div class="panel-header">Metadata</div>
    <div class="panel-body">
      <div class="meta-grid">
        <div class="meta-item"><label>Language</label><span>${esc(a.language || '—')}</span></div>
        <div class="meta-item"><label>Model</label><span>${esc(a.model_name || a.model_key || '—')}</span></div>
        <div class="meta-item"><label>Risk Category</label><span>${esc(catLabel)}</span></div>
        <div class="meta-item"><label>Attack Type</label><span>${esc(typeLabel)}</span></div>
        <div class="meta-item"><label>Risk Subcategory</label><span>${esc(a.risk_subcategory || '—')}</span></div>
        <div class="meta-item"><label>Break Count</label><span>${a.break_count || 0} / ${a.total_runs || 0} runs</span></div>
      </div>
      ${a.contextual_notes ? `<div style="margin-top:12px;padding-top:12px;border-top:1px solid var(--border);font-size:13px;line-height:1.65;color:var(--muted);font-style:italic;">${esc(a.contextual_notes)}</div>` : ''}
    </div>
  </div>`;
}

// ── Streaming inference ─────────────────────────────────────────────────────
async function runReproduce(a) {
  // Cancel any in-flight stream before starting a new one
  if (_abortCtrl) { _abortCtrl.abort(); _abortCtrl = null; }

  const btn  = document.getElementById('btn-run');
  const out  = document.getElementById('stream-output');
  const lbl  = document.getElementById('stream-status-label');
  const wrap = document.getElementById('status-badge-wrap');

  btn.disabled = true;
  btn.textContent = '⏳ Running…';
  out.innerHTML = '';
  lbl.textContent = 'streaming…';
  wrap.innerHTML = '';

  _abortCtrl = new AbortController();

  try {
    const resp = await fetch('/api/generate/stream', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        prompt:             a.prompt_original || a.prompt_english || '',
        temperature:        0.9,
        top_p:              0.95,
        repetition_penalty: 1.15,
        max_new_tokens:     2048,
        seed:               42,
      }),
      signal: _abortCtrl.signal,
    });

    if (!resp.ok) {
      const err = await resp.json().catch(() => ({}));
      out.textContent = 'Error: ' + (err.detail || resp.statusText);
      lbl.textContent = '';
      return;
    }

    const reader  = resp.body.getReader();
    const decoder = new TextDecoder();
    let buf = '';
    let finalStatus = '';

    outer: while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buf += decoder.decode(value, { stream: true });
      const lines = buf.split('\n');
      buf = lines.pop();
      for (const line of lines) {
        if (!line.startsWith('data: ')) continue;
        const payload = line.slice(6).trim();
        if (payload === '[DONE]') break outer;
        let msg;
        try { msg = JSON.parse(payload); } catch { continue; }
        if (msg.token !== undefined) {
          out.textContent += msg.token;
          out.scrollTop = out.scrollHeight;
        } else if (msg.status !== undefined) {
          finalStatus = msg.status;
        }
      }
    }

    lbl.textContent = '';
    if (finalStatus) {
      wrap.innerHTML = `<span class="status-badge status-${finalStatus}">${finalStatus.replace(/_/g,' ')}</span>`;
    }
  } catch (e) {
    if (e.name !== 'AbortError') {
      out.textContent = 'Network error: ' + e.message;
    }
    lbl.textContent = '';
  } finally {
    _abortCtrl = null;
    btn.disabled = false;
    btn.textContent = '▶ Run';
  }
}

// ── Utilities ──────────────────────────────────────────────────────────────
function esc(s) {
  return String(s)
    .replace(/&/g,'&amp;')
    .replace(/</g,'&lt;')
    .replace(/>/g,'&gt;')
    .replace(/"/g,'&quot;');
}

function cpText(text) {
  navigator.clipboard.writeText(text).catch(() => {});
}
