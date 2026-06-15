const API = "http://localhost:8420";

const $ = (id) => document.getElementById(id);

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, (ch) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;"
  }[ch]));
}

function rows(items, options = {}) {
  if (!items || !items.length) return '<div class="empty">No data yet.</div>';
  return items.slice(0, options.limit ?? 10).map((item) => {
    const name = item.name ?? item.domain ?? item.text ?? item.url ?? "";
    const value = options.signal && item.avg_signal != null
      ? `avg ${item.avg_signal}`
      : (item.count ?? item.events ?? item.score ?? item.avg_signal ?? item.repeat_count ?? "");
    return `<div class="row"><span class="name" title="${escapeHtml(name)}">${escapeHtml(name)}</span><span class="value">${escapeHtml(value)}</span></div>`;
  }).join("");
}

function pills(items) {
  if (!items || !items.length) return '<div class="empty">No data yet.</div>';
  return items.slice(0, 24).map((item) => (
    `<span class="pill">${escapeHtml(item.name)} ${escapeHtml(item.count ?? "")}</span>`
  )).join("");
}

function setServiceState(state, label) {
  const el = $("serviceState");
  el.className = `service-state ${state}`;
  el.textContent = label;
}

async function refresh() {
  setServiceState("checking", "Checking");
  try {
    const response = await fetch(`${API}/bil/summary?limit=16`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    const models = Object.keys(data.models || {});

    setServiceState("online", "Online");
    $("eventTotal").textContent = data.events?.total ?? 0;
    $("eventSub").textContent = `${data.events?.today ?? 0} today`;
    $("clipTotal").textContent = data.clipboard?.history_size ?? 0;
    $("searchAvg").textContent = data.search?.clicked_positions?.average ?? "-";
    $("modelTotal").textContent = models.length || "-";
    $("domainScores").innerHTML = rows(data.domains?.ranked_by_signal, { signal: true, limit: 14 });
    $("positiveDomains").innerHTML = rows(data.domains?.positive, { limit: 9 });
    $("bounceDomains").innerHTML = rows(data.domains?.quick_bounce, { limit: 9 });
    $("queries").innerHTML = rows(data.search?.queries, { limit: 9 });
    $("keywords").innerHTML = pills(data.keywords);
    $("clipboard").innerHTML = rows((data.clipboard?.recent || []).map((item) => ({
      name: item.text,
      count: item.repeat_count ? `x${item.repeat_count}` : (item.score ?? item.bil_score ?? "")
    })), { limit: 12 });
  } catch (error) {
    setServiceState("offline", "Offline");
    ["domainScores", "positiveDomains", "bounceDomains", "queries", "keywords", "clipboard"].forEach((id) => {
      $(id).innerHTML = `<div class="error">BIL is not reachable: ${escapeHtml(error.message)}</div>`;
    });
  }
}

async function scoreCandidate(event) {
  event.preventDefault();
  const body = {
    url: $("candidateUrl").value,
    title: $("candidateTitle").value,
    content: $("candidateContent").value,
    engine: "dashboard",
    score: 1
  };

  try {
    const response = await fetch(`${API}/bil/decide`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    $("decisionOut").textContent = JSON.stringify(await response.json(), null, 2);
  } catch (error) {
    $("decisionOut").textContent = `BIL is not reachable: ${error.message}`;
  }
}

$("refreshBtn").addEventListener("click", refresh);
$("scoreForm").addEventListener("submit", scoreCandidate);
refresh();
