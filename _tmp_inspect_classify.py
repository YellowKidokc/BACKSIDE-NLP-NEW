import re
src = open(r'X:\04_STATIONS\classify-documents.station\classify_runner.py', encoding='utf-8', errors='replace').read()
m = re.search(r'def classify_file.*', src, re.S)
body = m.group(0) if m else src
keys = re.findall(r"['\"]([a-z_]+)['\"]\s*:", body)
seen = []
for k in keys:
    if k not in seen:
        seen.append(k)
print("output keys:", seen)
