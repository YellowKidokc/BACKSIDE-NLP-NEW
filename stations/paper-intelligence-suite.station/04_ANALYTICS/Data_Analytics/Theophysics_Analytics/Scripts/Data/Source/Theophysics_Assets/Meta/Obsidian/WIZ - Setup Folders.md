---
uuid: 9519724d-b8be-5c00-9c8e-e5f1ee5c4885
title: WIZ   Setup Folders
author: David Lowe
type: note
created: '2025-11-22'
updated: '2025-11-22'
status: draft
file_path: Logos zright\Obsidian\WIZ - Setup Folders.md
uuid_generated_at: '2025-11-22T01:23:49.990653'
uuid_version: '1.0'
tags: []
pillars: []
category: theophysics-general
---

<%*
/** Setup Folders **/
const want = await tp.system.prompt("Create default folders? (y/N)", "y");
if ((want||"").toLowerCase() !== "y") { tR = "Cancelled."; return; }

const base = "Research";
const seriesList = ["TH","JS","TR","HP","QW","DD","EX"];

const mk = async (p)=>{ try { await app.vault.createFolder(p); } catch(e){} };
await mk(base);
for (const s of seriesList) await mk(`${base}/${s}`);

await mk("MOCs/Characters");
await mk("MOCs/Topics");

tR = "✅ Folders ensured:\n- Research/(TH,JS,TR,HP,QW,DD,EX)\n- MOCs/Characters\n- MOCs/Topics";
%>
