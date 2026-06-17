import json, time, urllib.request

BASE = "http://localhost:8700"

def post(path, payload, timeout=120):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(BASE + path, data=data,
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=timeout) as r:
        body = json.loads(r.read().decode())
    return time.time() - t0, body

text = ("Coherence is the degree to which a system stays aligned under stress. "
        "Shared truth lowers internal drift, and as drift rises the channel capacity "
        "for meaning collapses. The framework models social decline the same way a "
        "thermodynamic system decays toward disorder when no work is applied.")

dt, r = post("/nlp/summarize", {"text": text})
print(f"[summarize] {dt:.1f}s -> {r['summary']!r}")

dt, r = post("/nlp/ner", {"text": "David Lowe runs the POF 2828 project from Oklahoma City."})
print(f"[ner] {dt:.1f}s -> {r['count']} ents: {[(e['word'], e['entity']) for e in r['entities']]}")

dt, r = post("/nlp/sentiment", {"text": "This framework is a remarkable and coherent achievement."})
print(f"[sentiment] {dt:.1f}s -> {r['label']} ({r['score']})")

dt, r = post("/nlp/classify", {"text": "Entropy increases in every closed system over time.",
                               "labels": ["physics", "theology", "cooking"]})
print(f"[classify] {dt:.1f}s -> {list(zip(r['labels'], r['scores']))}")

dt, r = post("/nlp/qa", {"question": "What lowers internal drift?",
                         "context": text})
print(f"[qa] {dt:.1f}s -> {r['answer']!r} ({r['score']})")

print("ALL_ENDPOINTS_OK")
