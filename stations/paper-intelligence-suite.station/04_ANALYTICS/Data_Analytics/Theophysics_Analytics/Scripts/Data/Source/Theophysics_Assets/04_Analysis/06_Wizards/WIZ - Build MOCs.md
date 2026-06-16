<%*
/** Build MOCs **/
const chars = ["GF","JC","HS","ADV"];
const topicsCsv = await tp.system.prompt("Comma-separated topics to ensure MOCs for (e.g., trinity,entanglement,consciousness)", "trinity,entanglement,consciousness");
const topics = topicsCsv.split(",").map(s=>s.trim()).filter(Boolean);

const mk = async(p,c)=>{ try{ await app.vault.create(p,c);}catch(e){ /* exists */ } };

for (const c of chars){
  const p = `MOCs/Characters/${c}.md`;
  const content = [
    `# ${c} - Character MOC`,
    "",
    "```dataview",
    "TABLE file.link AS Paper, series, paper_number, topics",
    'FROM ""',
    `WHERE contains(characters, "${c}")`,
    "SORT series asc, paper_number asc",
    "```",
    ""
  ].join("\n");
  if (!app.vault.getAbstractFileByPath(p)) await mk(p, content);
  else await app.vault.modify(app.vault.getAbstractFileByPath(p), content);
}

for (const t of topics){
  const p = `MOCs/Topics/${t}.md`;
  const content = [
    `# Topic: ${t}`,
    "",
    "```dataview",
    "TABLE file.link AS Paper, series, paper_number, characters",
    'FROM ""',
    `WHERE contains(topics, "${t}")`,
    "SORT series asc, paper_number asc",
    "```",
    ""
  ].join("\n");
  if (!app.vault.getAbstractFileByPath(p)) await mk(p, content);
  else await app.vault.modify(app.vault.getAbstractFileByPath(p), content);
}

tR = "MOCs ensured for Characters (GF,JC,HS,ADV) and your listed Topics.";
%>
