import type { Express } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";
import {
  insertAxiomSchema,
  insertCategorySchema,
  insertDependencySchema,
  insertEnableSchema,
  insertPerspectiveSchema,
} from "@shared/schema";

export async function registerRoutes(
  httpServer: Server,
  app: Express
): Promise<Server> {

  app.get("/api/categories", async (_req, res) => {
    const cats = await storage.getCategories();
    res.json(cats);
  });

  app.get("/api/categories/:slug", async (req, res) => {
    const cat = await storage.getCategoryBySlug(req.params.slug);
    if (!cat) return res.status(404).json({ message: "Category not found" });
    res.json(cat);
  });

  app.get("/api/axioms", async (req, res) => {
    const categorySlug = req.query.category as string | undefined;
    if (categorySlug) {
      const list = await storage.getAxiomsByCategory(categorySlug);
      return res.json(list);
    }
    const list = await storage.getAxioms();
    res.json(list);
  });

  app.get("/api/axioms/:nodeId", async (req, res) => {
    const axiom = await storage.getAxiomByNodeId(req.params.nodeId);
    if (!axiom) return res.status(404).json({ message: "Axiom not found" });

    const [dependencies, enables, persp] = await Promise.all([
      storage.getDependencies(axiom.nodeId),
      storage.getEnables(axiom.nodeId),
      storage.getPerspectives(axiom.nodeId),
    ]);

    res.json({ ...axiom, dependencies, enables, perspectives: persp });
  });

  app.post("/api/axioms", async (req, res) => {
    try {
      const parsed = insertAxiomSchema.parse(req.body);
      const axiom = await storage.createAxiom(parsed);
      res.status(201).json(axiom);
    } catch (e: any) {
      res.status(400).json({ message: e.message });
    }
  });

  app.patch("/api/axioms/:nodeId", async (req, res) => {
    try {
      const partial = insertAxiomSchema.partial().parse(req.body);
      const updated = await storage.updateAxiom(req.params.nodeId, partial);
      if (!updated) return res.status(404).json({ message: "Axiom not found" });
      res.json(updated);
    } catch (e: any) {
      res.status(400).json({ message: e.message });
    }
  });

  app.post("/api/dependencies", async (req, res) => {
    try {
      const parsed = insertDependencySchema.parse(req.body);
      const dep = await storage.createDependency(parsed);
      res.status(201).json(dep);
    } catch (e: any) {
      res.status(400).json({ message: e.message });
    }
  });

  app.post("/api/enables", async (req, res) => {
    try {
      const parsed = insertEnableSchema.parse(req.body);
      const en = await storage.createEnable(parsed);
      res.status(201).json(en);
    } catch (e: any) {
      res.status(400).json({ message: e.message });
    }
  });

  app.post("/api/perspectives", async (req, res) => {
    try {
      const parsed = insertPerspectiveSchema.parse(req.body);
      const p = await storage.createPerspective(parsed);
      res.status(201).json(p);
    } catch (e: any) {
      res.status(400).json({ message: e.message });
    }
  });

  app.post("/api/categories", async (req, res) => {
    try {
      const parsed = insertCategorySchema.parse(req.body);
      const cat = await storage.createCategory(parsed);
      res.status(201).json(cat);
    } catch (e: any) {
      res.status(400).json({ message: e.message });
    }
  });

  return httpServer;
}
