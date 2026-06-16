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

tR = "Folders ensured:\n- Research/(TH,JS,TR,HP,QW,DD,EX)\n- MOCs/Characters\n- MOCs/Topics";
%>
