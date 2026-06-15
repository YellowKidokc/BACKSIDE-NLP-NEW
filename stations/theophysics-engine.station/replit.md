# Theophysics Engine

## Overview
An advanced axiom modeling and simulation interface for the Theophysics framework. Displays 188 axioms in a chain, with deep drill-down into formal statements, common sense explanations, cross-domain mappings, judge & jury arguments, and dependency graphs.

## Architecture
- **Frontend**: React + Tailwind CSS + shadcn/ui, dark sci-fi aesthetic
- **Backend**: Express.js API with PostgreSQL (Drizzle ORM)
- **Routing**: wouter for client-side, Express for API routes
- **Data**: Real axiom data seeded into PostgreSQL

## Key Entities
- **Categories**: 35+ categories (Axioms, Definitions, Lemmas, Theorems, etc.)
- **Axioms**: 188 nodes in a chain with formal statements, mappings, objections, verdicts
- **Dependencies**: Upstream axiom relationships
- **Enables**: Downstream axiom relationships  
- **Perspectives**: Alternative philosophical viewpoints on each axiom

## API Routes
- `GET /api/categories` - List all categories
- `GET /api/axioms` - List all axioms (optional `?category=slug` filter)
- `GET /api/axioms/:nodeId` - Get axiom with dependencies, enables, perspectives
- `POST /api/axioms` - Create new axiom
- `PATCH /api/axioms/:nodeId` - Update axiom
- `POST /api/categories` - Create category
- `POST /api/dependencies` - Create dependency link
- `POST /api/enables` - Create enable link
- `POST /api/perspectives` - Create perspective

## User Preferences
- Dark mode sci-fi aesthetic (deep space blue palette)
- Cloudflare deployment target (Pages + Workers + R2 + D1)
- Interactive, clickable, expandable UI
- Every axiom section should be deeply explorable

## Recent Changes
- Full-stack implementation with PostgreSQL database
- Seeded with real axiom data from user's Theophysics content
- Categories sidebar, axiom spine list, deep drill-down views
- Judge & Jury courtroom analysis sections
- Common Sense Truth layer after formal statements
