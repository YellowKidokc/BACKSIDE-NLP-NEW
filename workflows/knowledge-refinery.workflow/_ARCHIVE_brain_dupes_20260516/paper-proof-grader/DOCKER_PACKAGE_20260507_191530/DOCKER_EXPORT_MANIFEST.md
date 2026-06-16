# Theophysics Paper Intelligence Docker Export

Image tags:
- theophysics/paper-intelligence:local
- theophysics/paper-intelligence:gtq-all25-20260507-191530

Archive:
- C:\Users\lowes\Documents\Codex\2026-05-06\oh-do-we-not-do-we\docker_image_export\theophysics-paper-intelligence-local-20260507_191530.tar

SHA256:
- A7C712B4040BC7072ABCF541949121D9BDFADBC5AD18C2652C75C6EE651B23F6

Restore:
```powershell
docker load -i "C:\Users\lowes\Documents\Codex\2026-05-06\oh-do-we-not-do-we\docker_image_export\theophysics-paper-intelligence-local-20260507_191530.tar"
```

Run all 25 GTQ:
```powershell
docker run --rm -v "C:\Users\lowes\OneDrive\Desktop\genesis-to-quantum:/data/input:ro" -v "C:\path\to\output:/data/output" theophysics/paper-intelligence:gtq-all25-20260507-191530 grade --pattern "gtq-*.html"
docker run --rm -v "C:\path\to\output:/data/output" theophysics/paper-intelligence:gtq-all25-20260507-191530 report
```

Known completed Docker output:
- \\dlowenas\brain\proof-explorer\reports\gtq_docker_all25_20260507_191530
