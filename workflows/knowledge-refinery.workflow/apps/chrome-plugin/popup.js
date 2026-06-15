const API = "http://localhost:8420";
const SERVICES = [
  { name: "BIL", url: "http://localhost:8420/bil/summary?limit=1" },
  { name: "Ollama", url: "http://localhost:11434/api/tags" },
  { name: "Qdrant", url: "http://192.168.1.177:6333/" },
  { name: "Infinity", url: "http://192.168.1.177:7997/" }
];

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

function rows(items, valueKey = "count") {
  if (!items || !items.length) return '<div class="empty">No data yet.</div>';
  return items.slice(0, 5).map((item) => {
    const name = item.name ?? item.domain ?? item.text ?? item.url ?? "";
    const value = item[valueKey] ?? item.score ?? item.events ?? item.avg_signal ?? "";
    return `<div class="row"><span class="name" title="${escapeHtml(name)}">${escapeHtml(name)}</span><span class="value">${escapeHtml(value)}</span></div>`;
  }).join("");
}

function setStatus(ok, label) {
  $("statusDot").className = `status-dot ${ok ? "ok" : "bad"}`;
  $("statusDot").title = label;
  $("apiLabel").textContent = label;
}

async function refresh() {
  $("domains").innerHTML = '<div class="empty">Checking BIL...</div>';
  $("clipboard").innerHTML = '<div class="empty">Checking clipboard signals...</div>';
  checkHealth();

  try {
    const response = await fetch(`${API}/bil/summary?limit=8`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();

    setStatus(true, "online");
    $("eventTotal").textContent = data.events?.total ?? 0;
    $("clipTotal").textContent = data.clipboard?.history_size ?? 0;
    $("searchAvg").textContent = data.search?.clicked_positions?.average ?? "-";
    $("domains").innerHTML = rows(data.domains?.ranked_by_signal, "avg_signal");
    $("clipboard").innerHTML = rows((data.clipboard?.recent || []).map((item) => ({
      name: item.text,
      count: item.repeat_count ? `x${item.repeat_count}` : (item.score ?? item.bil_score ?? "")
    })));
  } catch (error) {
    setStatus(false, "offline");
    $("eventTotal").textContent = "-";
    $("clipTotal").textContent = "-";
    $("searchAvg").textContent = "-";
    $("domains").innerHTML = `<div class="error">BIL is not reachable: ${escapeHtml(error.message)}</div>`;
    $("clipboard").innerHTML = '<div class="empty">Start BIL, then refresh.</div>';
  }
}

async function checkHealth() {
  $("healthRows").innerHTML = '<div class="empty">Checking services...</div>';
  const results = await Promise.all(SERVICES.map(async (service) => {
    try {
      const response = await fetch(service.url, { cache: "no-store" });
      return { ...service, ok: response.ok, detail: response.ok ? "online" : `HTTP ${response.status}` };
    } catch (error) {
      return { ...service, ok: false, detail: "offline" };
    }
  }));
  $("healthRows").innerHTML = results.map((item) => (
    `<div class="row"><span class="name">${escapeHtml(item.name)}</span><span class="value ${item.ok ? "health-ok" : "health-bad"}">${escapeHtml(item.detail)}</span></div>`
  )).join("");
}

function setCaptureStatus(message, isError = false) {
  $("captureStatus").className = isError ? "error compact" : "empty compact";
  $("captureStatus").textContent = message;
}

async function capture(kind) {
  setCaptureStatus("Capturing current tab...");
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (!tab?.id) throw new Error("No active tab found.");

    const pageData = await chrome.tabs.sendMessage(tab.id, {
      type: "collect_brain_capture",
      mode: kind
    });

    const response = await chrome.runtime.sendMessage({
      type: "brain_capture",
      data: {
        ...pageData,
        mode: kind,
        captured_at: new Date().toISOString()
      }
    });

    if (response?.ok) {
      setCaptureStatus(response.message || "Captured.");
    } else {
      throw new Error(response?.error || "Capture failed.");
    }
  } catch (error) {
    setCaptureStatus(error.message, true);
  }
}

$("refreshBtn").addEventListener("click", refresh);
$("dashboardBtn").addEventListener("click", () => {
  chrome.runtime.openOptionsPage();
});
$("capturePageBtn").addEventListener("click", () => capture("page"));
$("captureSelectionBtn").addEventListener("click", () => capture("selection"));

refresh();
