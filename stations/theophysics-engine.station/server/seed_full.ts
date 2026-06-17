/**
 * Full seeder: reads all 191 axiom files from D:\_001-188\_001-188\
 * and upserts them into the database with all fields populated.
 */
import fs from "fs";
import path from "path";
import { db } from "./db";
import { axioms, axiomDependencies, axiomEnables } from "@shared/schema";
import { eq } from "drizzle-orm";

const SOURCE_DIR = "D:\\_001-188\\_001-188";

// ── YAML frontmatter parser ──────────────────────────────────────

function parseFrontmatter(text: string): Record<string, any> {
  const match = text.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return {};
  const yaml: Record<string, any> = {};
  let currentKey = "";
  let inArray = false;
  const arrayItems: string[] = [];

  for (const line of match[1].split("\n")) {
    if (inArray) {
      if (line.startsWith("- ")) {
        arrayItems.push(line.slice(2).trim().replace(/^["']|["']$/g, ""));
        continue;
      } else {
        yaml[currentKey] = [...arrayItems];
        arrayItems.length = 0;
        inArray = false;
      }
    }

    const kvMatch = line.match(/^(\w[\w_]*)\s*:\s*(.*)$/);
    if (kvMatch) {
      currentKey = kvMatch[1];
      const val = kvMatch[2].trim();
      if (val === "" || val === "[]") {
        // Could be start of array or empty
        if (val === "[]") {
          yaml[currentKey] = [];
        }
        // else wait for possible array items
        continue;
      }
      yaml[currentKey] = val.replace(/^["']|["']$/g, "");
    } else if (line.startsWith("- ")) {
      inArray = true;
      arrayItems.push(line.slice(2).trim().replace(/^["']|["']$/g, ""));
    }
  }
  if (inArray) {
    yaml[currentKey] = [...arrayItems];
  }
  return yaml;
}

// ── Section extractors ───────────────────────────────────────────

function getBody(text: string): string {
  const match = text.match(/^---[\s\S]*?---\n([\s\S]*)$/);
  return match ? match[1] : text;
}

function getSection(body: string, heading: string): string {
  const re = new RegExp(`^## ${heading}\\n([\\s\\S]*?)(?=\\n## |$)`, "m");
  const match = body.match(re);
  return match ? match[1].trim() : "";
}

function getAfterLabel(body: string, label: string): string {
  const re = new RegExp(`\\*\\*${label}\\*\\*\\s*(.+)`, "m");
  const match = body.match(re);
  return match ? match[1].trim() : "";
}

function getMapping(body: string, name: string): string {
  // Match "- Physics mapping: ..." or "- Physics: ..."
  const re = new RegExp(`-\\s*${name}(?:\\s+mapping)?\\s*:\\s*(.+)`, "i");
  const match = body.match(re);
  return match ? match[1].trim() : "";
}

function parseObjections(section: string): { objection: string; response: string }[] {
  const results: { objection: string; response: string }[] = [];
  const parts = section.split(/### Objection \d+/);
  for (const part of parts) {
    if (!part.trim()) continue;
    // Title line: ": Advaita Vedanta - Undifferentiated Brahman"
    const titleMatch = part.match(/^[:\s]*(.+?)[\n]/);
    // Italicized objection quote
    const quoteMatch = part.match(new RegExp('\\*"(.+?)"\\*', "s"));
    // Response after **Response:**
    const responseMatch = part.match(/\*\*Response:\*\*\s*([\s\S]*?)$/);

    if (quoteMatch && responseMatch) {
      const title = titleMatch ? titleMatch[1].trim().replace(/^[:\s]+/, "") : "";
      const objText = title ? `${title}: ${quoteMatch[1]}` : quoteMatch[1];
      results.push({
        objection: objText,
        response: responseMatch[1].trim(),
      });
    }
  }
  return results;
}

function parseNotClaiming(body: string): string[] {
  const section = body.match(/\*\*Not claiming[^*]*\*\*[:\s]*\n([\s\S]*?)(?=\n## |\n\*\*|\n$)/i);
  if (!section) return [];
  return section[1]
    .split("\n")
    .filter((l) => l.startsWith("- "))
    .map((l) => l.slice(2).trim());
}

function parseDefeatConditions(section: string): string[] {
  if (!section) return [];
  return section
    .split("\n")
    .filter((l) => l.startsWith("- "))
    .map((l) => l.slice(2).trim());
}

function parseDependsList(yaml: Record<string, any>): string[] {
  if (Array.isArray(yaml.depends_on)) return yaml.depends_on;
  return [];
}

function parseEnablesList(yaml: Record<string, any>): string[] {
  if (Array.isArray(yaml.enables)) return yaml.enables;
  return [];
}

function extractBridgeCount(body: string): number {
  const match = body.match(/Bridge Count:\s*(\d+)/);
  return match ? parseInt(match[1], 10) : 0;
}

function guessObjectType(nodeId: string): string {
  if (nodeId.startsWith("A")) return "Axiom";
  if (nodeId.startsWith("D")) return "Definition";
  if (nodeId.startsWith("LN")) return "Lemma";
  if (nodeId.startsWith("E")) return "Equation";
  if (nodeId.startsWith("P")) return "Proposition";
  if (nodeId.startsWith("T")) return "Theorem";
  if (nodeId.startsWith("ID") || nodeId.startsWith("BR")) return "Bridge";
  if (nodeId.startsWith("C")) return "Corollary";
  if (nodeId.startsWith("O")) return "Ontological";
  if (nodeId.startsWith("BC")) return "Boundary";
  if (nodeId.startsWith("R")) return "Bridge"; // Religion comparison results
  if (nodeId.startsWith("PRED")) return "Prediction";
  if (nodeId.startsWith("PROT")) return "Protocol";
  if (nodeId.startsWith("FALS")) return "Falsification";
  if (nodeId.startsWith("OPEN")) return "Open Question";
  return "Axiom";
}

function guessCategorySlug(yaml: Record<string, any>, nodeId: string): string {
  const domains = Array.isArray(yaml.domain) ? yaml.domain : [];
  if (domains.includes("ontology")) return "Existence_Ontology";
  if (domains.includes("information")) return "Information_Theory";
  if (domains.includes("consciousness")) return "Consciousness";
  if (domains.includes("grace") || domains.includes("salvation")) return "Salvation_Grace";
  if (domains.includes("soul")) return "Human_Soul";
  if (domains.includes("morality") || domains.includes("ethics")) return "Sin_Problem";
  if (domains.includes("eschatology")) return "Eschatology";
  if (domains.includes("unification")) return "Core_Theorems";
  if (domains.includes("cosmology")) return "God_Nature";
  if (domains.includes("apologetics") || domains.includes("religion_test")) return "Apologetics";
  if (domains.includes("verification") || domains.includes("falsification")) return "07_Evidence";
  if (domains.includes("integration")) return "Core_Theorems";
  return "01_Axioms";
}

// ── Main seed function ───────────────────────────────────────────

async function seedFull() {
  console.log("Full seed from", SOURCE_DIR);

  const files = fs.readdirSync(SOURCE_DIR).filter((f) => f.endsWith(".md"));
  console.log(`Found ${files.length} axiom files\n`);

  let count = 0;

  for (const file of files) {
    const content = fs.readFileSync(path.join(SOURCE_DIR, file), "utf-8");
    const yaml = parseFrontmatter(content);
    const body = getBody(content);

    const nodeId = yaml.axiom_id;
    if (!nodeId) {
      console.log(`  SKIP ${file} — no axiom_id`);
      continue;
    }

    const chainPos = parseInt(yaml.chain_position, 10) || count + 1;
    const title = yaml.title || file.replace(/^\d+_/, "").replace(/_/g, " ").replace(".md", "");

    // Extract sections
    const formalStatement = getSection(body, "Formal Statement").split("\n")[0] || null;
    const intendedMeaning = body.match(/\*\*Intended meaning[^*]*\*\*[:\s]*\n?([\s\S]*?)(?=\n\*\*|\n## )/i)?.[1]?.trim() || null;
    const notClaiming = parseNotClaiming(body);
    const defeatSection = getSection(body, "Defeat Conditions");
    const defeatConditions = parseDefeatConditions(defeatSection);
    const objectionsSection = getSection(body, "Standard Objections");
    const standardObjections = parseObjections(objectionsSection);
    const defenseSummary = getSection(body, "Defense Summary") || null;
    const collapseAnalysis = getSection(body, "Collapse Analysis") || null;
    const physicsLayer = getSection(body, "Physics Layer") || null;
    const mathLayer = getSection(body, "Mathematical Layer") || getSection(body, "Math Layer") || null;

    // Prosecution / cross-exam
    const prosecutionSection = getSection(body, "Prosecution \\(Worldview Cross-Examination\\)") || getSection(body, "Prosecution");

    // Mappings (from Spine Master section)
    const physicsMapping = getMapping(body, "Physics") || null;
    const theologyMapping = getMapping(body, "Theology") || null;
    const consciousnessMapping = getMapping(body, "Consciousness") || null;
    const quantumMapping = getMapping(body, "Quantum") || null;
    const scriptureMapping = getMapping(body, "Scripture") || null;
    const evidenceMapping = getMapping(body, "Evidence") || null;
    const informationMapping = getMapping(body, "Information") || null;

    const bridgeCount = extractBridgeCount(body);
    const objectType = guessObjectType(nodeId);
    const categorySlug = guessCategorySlug(yaml, nodeId);

    // Common sense — try to extract from file or use formal statement
    const commonSenseTruth = null; // Not in these files — comes from a different source

    const axiomData = {
      nodeId,
      title: title.replace(/^["']|["']$/g, ""),
      chainPosition: chainPos,
      totalChain: 191,
      objectType,
      stage: String(yaml.stage || "1"),
      status: yaml.status === "primitive" ? "Validated" : (yaml.status || "Pending"),
      crRating: "Critical",
      bridgeCount,
      conflicts: 0,
      formalStatement,
      intendedMeaning,
      notClaiming: notClaiming.length > 0 ? notClaiming : null,
      physicsMapping,
      theologyMapping,
      consciousnessMapping,
      quantumMapping,
      scriptureMapping,
      evidenceMapping,
      informationMapping,
      physicsLayer,
      mathLayer,
      prosecutorDefense: defenseSummary,
      standardObjections: standardObjections.length > 0 ? standardObjections : null,
      verdict: defenseSummary,
      defeatConditions: defeatConditions.length > 0 ? defeatConditions : null,
      collapseAnalysis,
      categorySlug,
      sourceFiles: [file],
    };

    // Upsert — update if exists, insert if not
    const existing = await db.select().from(axioms).where(eq(axioms.nodeId, nodeId)).limit(1);
    if (existing.length > 0) {
      await db.update(axioms).set(axiomData).where(eq(axioms.nodeId, nodeId));
      console.log(`  UPD ${nodeId} — ${title}`);
    } else {
      await db.insert(axioms).values(axiomData);
      console.log(`  INS ${nodeId} — ${title}`);
    }

    // Dependencies
    const depsList = parseDependsList(yaml);
    for (const dep of depsList) {
      const depExists = await db
        .select()
        .from(axiomDependencies)
        .where(eq(axiomDependencies.axiomNodeId, nodeId))
        .limit(100);
      if (!depExists.find((d) => d.dependsOnNodeId === dep)) {
        await db.insert(axiomDependencies).values({
          axiomNodeId: nodeId,
          dependsOnNodeId: dep,
          relationship: "assumes",
        });
      }
    }

    // Enables
    const enablesList = parseEnablesList(yaml);
    for (const en of enablesList) {
      const enExists = await db
        .select()
        .from(axiomEnables)
        .where(eq(axiomEnables.axiomNodeId, nodeId))
        .limit(100);
      if (!enExists.find((e) => e.enablesNodeId === en)) {
        await db.insert(axiomEnables).values({
          axiomNodeId: nodeId,
          enablesNodeId: en,
        });
      }
    }

    count++;
  }

  console.log(`\nDone: ${count} axioms processed`);
  process.exit(0);
}

seedFull().catch((e) => {
  console.error("Seed error:", e);
  process.exit(1);
});
