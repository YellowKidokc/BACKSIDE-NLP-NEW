import { sql } from "drizzle-orm";
import { pgTable, text, varchar, integer, boolean, jsonb, timestamp } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod";

export const users = pgTable("users", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  username: text("username").notNull().unique(),
  password: text("password").notNull(),
});

export const categories = pgTable("categories", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  slug: text("slug").notNull().unique(),
  label: text("label").notNull(),
  sortOrder: integer("sort_order").notNull().default(0),
});

export const axioms = pgTable("axioms", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  nodeId: text("node_id").notNull().unique(),
  title: text("title").notNull(),
  chainPosition: integer("chain_position").notNull(),
  totalChain: integer("total_chain").notNull().default(188),
  objectType: text("object_type").notNull().default("Axiom"),
  stage: text("stage").notNull().default("1"),
  status: text("status").notNull().default("Pending"),
  crRating: text("cr_rating").notNull().default("Critical"),
  bridgeCount: integer("bridge_count").notNull().default(0),
  conflicts: integer("conflicts").notNull().default(0),
  formalStatement: text("formal_statement"),
  intendedMeaning: text("intended_meaning"),
  notClaiming: text("not_claiming").array(),
  commonSenseTruth: text("common_sense_truth"),
  commonSenseAccepted: text("common_sense_accepted"),
  commonSenseExplanation: text("common_sense_explanation"),
  commonSenseVariable: text("common_sense_variable"),
  physicsMapping: text("physics_mapping"),
  theologyMapping: text("theology_mapping"),
  consciousnessMapping: text("consciousness_mapping"),
  quantumMapping: text("quantum_mapping"),
  scriptureMapping: text("scripture_mapping"),
  evidenceMapping: text("evidence_mapping"),
  informationMapping: text("information_mapping"),
  physicsLayer: text("physics_layer"),
  mathLayer: text("math_layer"),
  prosecutorDefense: text("prosecutor_defense"),
  crossExaminations: jsonb("cross_examinations").$type<{ target: string; text: string }[]>(),
  verdict: text("verdict"),
  defeatConditions: text("defeat_conditions").array(),
  standardObjections: jsonb("standard_objections").$type<{ objection: string; response: string }[]>(),
  defenseSummary: text("defense_summary"),
  collapseAnalysis: text("collapse_analysis"),
  sourceFiles: text("source_files").array(),
  categorySlug: text("category_slug"),
  // 7Q Score fields
  q0Posture: text("q0_posture"),
  q1Identity: text("q1_identity"),
  q2Domain: text("q2_domain"),
  q3Assertion: text("q3_assertion"),
  q4Evidence: text("q4_evidence"),
  q5Dependencies: text("q5_dependencies"),
  q6Consequences: text("q6_consequences"),
  q7Falsification: text("q7_falsification"),
  avg7qScore: text("avg_7q_score"),
  isoStatus: text("iso_status"),
  sevenqConfidence: text("sevenq_confidence"),
  killCount: integer("kill_count").default(0),
  claimCount: integer("claim_count").default(0),
  sevenqType: text("sevenq_type"),
  strongestQ: text("strongest_q"),
  weakestQ: text("weakest_q"),
  theoryResonanceMap: text("theory_resonance_map"),
  decisivePrediction: text("decisive_prediction"),
  whatSurvives: text("what_survives"),
  whatDies: text("what_dies"),
  executiveSummary: text("executive_summary"),
  sevenqCoreClaim: text("sevenq_core_claim"),
});

export const axiomDependencies = pgTable("axiom_dependencies", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  axiomNodeId: text("axiom_node_id").notNull(),
  dependsOnNodeId: text("depends_on_node_id").notNull(),
  relationship: text("relationship").notNull().default("assumes"),
  description: text("description"),
});

export const axiomEnables = pgTable("axiom_enables", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  axiomNodeId: text("axiom_node_id").notNull(),
  enablesNodeId: text("enables_node_id").notNull(),
  description: text("description"),
});

export const perspectives = pgTable("perspectives", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  axiomNodeId: text("axiom_node_id").notNull(),
  name: text("name").notNull(),
  quote: text("quote"),
  assessment: text("assessment"),
  sortOrder: integer("sort_order").notNull().default(0),
});

export const insertUserSchema = createInsertSchema(users).pick({ username: true, password: true });
export const insertCategorySchema = createInsertSchema(categories).omit({ id: true });
export const insertAxiomSchema = createInsertSchema(axioms).omit({ id: true });
export const insertDependencySchema = createInsertSchema(axiomDependencies).omit({ id: true });
export const insertEnableSchema = createInsertSchema(axiomEnables).omit({ id: true });
export const insertPerspectiveSchema = createInsertSchema(perspectives).omit({ id: true });

export type InsertUser = z.infer<typeof insertUserSchema>;
export type User = typeof users.$inferSelect;
export type InsertCategory = z.infer<typeof insertCategorySchema>;
export type Category = typeof categories.$inferSelect;
export type InsertAxiom = z.infer<typeof insertAxiomSchema>;
export type Axiom = typeof axioms.$inferSelect;
export type InsertDependency = z.infer<typeof insertDependencySchema>;
export type AxiomDependency = typeof axiomDependencies.$inferSelect;
export type InsertEnable = z.infer<typeof insertEnableSchema>;
export type AxiomEnable = typeof axiomEnables.$inferSelect;
export type InsertPerspective = z.infer<typeof insertPerspectiveSchema>;
export type Perspective = typeof perspectives.$inferSelect;
