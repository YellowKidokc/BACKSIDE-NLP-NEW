import fs from "fs";
import path from "path";
import { db } from "./db";
import { axioms } from "@shared/schema";
import { eq } from "drizzle-orm";

const SCORED_DIR = "O:\\_Theophysics_v4\\Data Vault\\AXIOMS_SCORED_FORMATTED";

function parseYamlFrontmatter(text: string): Record<string, any> {
  const match = text.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return {};
  const yaml: Record<string, any> = {};
  for (const line of match[1].split("\n")) {
    const kv = line.match(/^(\w[\w_]*)\s*:\s*(.+)$/);
    if (kv) {
      let val: any = kv[2].trim().replace(/^["']|["']$/g, "");
      if (/^\d+\.\d+$/.test(val)) val = val;
      else if (/^\d+$/.test(val)) val = val;
      yaml[kv[1]] = val;
    }
  }
  return yaml;
}

function getSection(text: string, heading: string): string {
  // Try callout format first: > [!note] heading
  const calloutRe = new RegExp(
    `>\\s*\\[!\\w+\\][-]?\\s*${heading}\\n([\\s\\S]*?)(?=\\n>\\s*\\[!|\\n---|\n#|$)`
  );
  let match = text.match(calloutRe);
  if (match) {
    return match[1]
      .split("\n")
      .map((l) => l.replace(/^>\s?/, ""))
      .join("\n")
      .trim();
  }

  // Try markdown heading: ### heading
  const headingRe = new RegExp(
    `### ${heading}\\n([\\s\\S]*?)(?=\\n###|\\n---|$)`
  );
  match = text.match(headingRe);
  return match ? match[1].trim() : "";
}

function getStrongestWeakest(text: string): { strongest: string; weakest: string } {
  const section = getSection(text, "Strongest / Weakest") || getSection(text, "Strongest \\/ Weakest");
  const strongMatch = section.match(new RegExp("\\*\\*Strongest:\\*\\*\\s*(.*?)(?=\\n|\\*\\*Weakest)", "s"));
  const weakMatch = section.match(new RegExp("\\*\\*Weakest:\\*\\*\\s*(.*?)$", "s"));
  return {
    strongest: strongMatch ? strongMatch[1].trim() : "",
    weakest: weakMatch ? weakMatch[1].trim() : "",
  };
}

async function seed7q() {
  console.log("Seeding 7Q data...");

  const files = fs.readdirSync(SCORED_DIR).filter((f) => f.endsWith("_7q.md"));
  console.log(`Found ${files.length} 7Q files`);

  let updated = 0;
  let skipped = 0;

  for (const file of files) {
    const content = fs.readFileSync(path.join(SCORED_DIR, file), "utf-8");
    const yaml = parseYamlFrontmatter(content);

    if (!yaml.axiom_id) {
      console.log(`  SKIP ${file} — no axiom_id`);
      skipped++;
      continue;
    }

    const nodeId = yaml.axiom_id;
    const { strongest, weakest } = getStrongestWeakest(content);

    const updateData: Record<string, any> = {
      q0Posture: yaml.q0_posture || null,
      q1Identity: yaml.q1_identity || null,
      q2Domain: yaml.q2_domain || null,
      q3Assertion: yaml.q3_assertion || null,
      q4Evidence: yaml.q4_evidence || null,
      q5Dependencies: yaml.q5_dependencies || null,
      q6Consequences: yaml.q6_consequences || null,
      q7Falsification: yaml.q7_falsification || null,
      avg7qScore: yaml.avg_7q_score || null,
      isoStatus: yaml.iso_status || null,
      sevenqConfidence: yaml.confidence || null,
      killCount: yaml.kill_count ? parseInt(yaml.kill_count, 10) : 0,
      claimCount: yaml.claim_count ? parseInt(yaml.claim_count, 10) : 0,
      sevenqType: yaml.type || null,
      strongestQ: strongest || null,
      weakestQ: weakest || null,
      theoryResonanceMap: getSection(content, "Theory Resonance Map") || null,
      decisivePrediction: getSection(content, "Decisive Untested Prediction") || null,
      whatSurvives: getSection(content, "What Survives") || null,
      whatDies: getSection(content, "What Dies") || null,
      executiveSummary: getSection(content, "Executive Summary") || null,
      sevenqCoreClaim: getSection(content, "Core Claim") || null,
    };

    const result = await db
      .update(axioms)
      .set(updateData)
      .where(eq(axioms.nodeId, nodeId));

    console.log(`  ${nodeId} — ${file}`);
    updated++;
  }

  console.log(`\nDone: ${updated} updated, ${skipped} skipped`);
  process.exit(0);
}

seed7q().catch((e) => {
  console.error("Seed error:", e);
  process.exit(1);
});
