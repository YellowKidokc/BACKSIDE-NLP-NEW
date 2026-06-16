---
uuid: 4d076d0f-75a0-5b45-b3b0-93adc052d757
title: Docker Support
author: David Lowe
type: note
created: '2025-11-22'
updated: '2025-11-22'
status: draft
file_path: Logos zright\Meta\Docker Support.md
uuid_generated_at: '2025-11-22T01:23:48.613422'
uuid_version: '1.0'
tags: []
pillars: []
category: theophysics-general
---

Quartz comes shipped with a Docker image that will allow you to preview your Quartz locally without installing Node.

You can run the below one-liner to run Quartz in Docker.

```sh
docker run --rm -itp 8080:8080 -p 3001:3001 -v ./content:/usr/src/app/content $(docker build -q .)
```
