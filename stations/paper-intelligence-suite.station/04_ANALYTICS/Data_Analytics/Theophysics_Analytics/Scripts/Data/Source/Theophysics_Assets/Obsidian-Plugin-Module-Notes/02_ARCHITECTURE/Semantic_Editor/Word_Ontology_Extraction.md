---
title: Word-ontology (Epistemic Tagger) - Extraction
version: 1.0
last_updated: 2025-01-15
status: active
tags: [#extraction, #semantic-editor, #implementation]
source_repo: https://github.com/YellowKidokc/Word-ontology
---

# Word-ontology (Epistemic Tagger) - Extraction

**Source Repository**: https://github.com/YellowKidokc/Word-ontology  
**Status**: Working efficiently with PostgreSQL  
**Integration Target**: Semantic Editor / Annotation Layer + Tab 6: Ontology Graph

---

## Overview

An Obsidian plugin that allows you to classify selected text with epistemic types via right-click menu, store these annotations in PostgreSQL, and support multiple "bundle profiles" for different users/contexts.

**Core Concept**: Right-click any text → Classify it → Store in database → Visualize with color-coded highlights

---

## Key Features

### 1. Right-Click Classification
**User Flow**:
1. Highlight any text in any note
2. Right-click to open context menu
3. Select classification type from menu
4. Text is immediately highlighted with color and icon
5. Classification stored in PostgreSQL

**Implementation Notes**:
- Context menu integration with Obsidian API
- Instant visual feedback
- No page reload required
- Works across entire vault

---

### 2. Multiple Bundle Profiles
**Purpose**: Different classification frameworks for different contexts

**Profiles**:

#### Personal Research
Full epistemic categories for knowledge management:
- **Axiom**: Foundational assumptions
- **Canonical**: Established truths
- **Evidence**: Supporting data
- **Coherence**: Logical consistency markers
- **Reference**: External citations

#### YouTube Content
Simplified categories for video script structure:
- **Hook**: Attention-grabbing opening
- **Context**: Background information
- **Main Point**: Core message
- **Example**: Illustrative case
- **Call to Action**: Viewer engagement

#### AI Training Data
Categories for building training datasets:
- **Instruction**: Task description
- **Input**: Data to process
- **Output**: Expected result
- **Explanation**: Reasoning
- **Metadata**: Additional context

**Implementation Notes**:
- Profile switching via settings
- Each profile has its own color scheme
- Categories are profile-specific
- Can create custom profiles

---

### 3. Visual Highlighting System
**Features**:
- **Color-Coded**: Each category has distinct color
- **Superscript Icons**: Small icon indicators
- **Hover Tooltips**: Show classification details
- **Non-Intrusive**: Doesn't break markdown rendering

**Color Scheme (Personal Research)**:
- Axiom: Blue
- Canonical: Gold
- Evidence: Green
- Coherence: Purple
- Reference: Grey

**Icon System**:
- Axiom: `ᴬ`
- Canonical: `ᶜ`
- Evidence: `ᴱ`
- Coherence: `ᶜᴼ`
- Reference: `ᴿ`

---

### 4. PostgreSQL Storage
**Purpose**: Robust, queryable storage for all classifications

**Schema**:
```sql
-- Statements table
CREATE TABLE epistemic.statements (
    id UUID PRIMARY KEY,
    content TEXT NOT NULL,
    source_file TEXT NOT NULL,
    start_offset INT,
    end_offset INT,
    bundle_profile TEXT,
    created_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ
);

-- Types table
CREATE TABLE epistemic.types (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    bundle_profile TEXT NOT NULL,
    description TEXT,
    color TEXT,
    icon TEXT,
    priority INT,
    UNIQUE(name, bundle_profile)
);

-- Statement-type relationships
CREATE TABLE epistemic.statement_types (
    id UUID PRIMARY KEY,
    statement_id UUID REFERENCES epistemic.statements(id),
    type_id UUID REFERENCES epistemic.types(id),
    confidence DECIMAL(3,2),
    tagged_by TEXT,
    tagged_at TIMESTAMPTZ,
    notes TEXT
);
```

**Key Features**:
- UUID-based identification
- Character offset tracking for precise location
- Bundle profile support
- Timestamps for audit trail
- Many-to-many relationship (statement can have multiple types)
- Confidence scoring
- Attribution tracking (who tagged it)

---

### 5. AI-Assisted Classification
**Purpose**: Optional Claude AI integration for automatic suggestions

**Features**:
- AI analyzes selected text
- Suggests appropriate classification
- User can accept or reject
- Learns from user corrections

**Implementation Notes**:
- Claude API integration
- Configurable in settings
- Optional feature (can work without AI)
- Respects API rate limits

---

### 6. Export Functionality
**Purpose**: Export classifications to CSV for analysis

**Export Format**:
```csv
id,content,source_file,type,confidence,tagged_by,created_at
uuid-1,"Text content","/path/to/note.md","axiom",1.0,"user","2025-01-15T10:00:00Z"
```

**Use Cases**:
- Data analysis in Excel/Python
- Backup of classifications
- Sharing with collaborators
- Migration to other systems

---

## Architecture

### File Structure
```
Word-ontology/
├── main.ts                    # Plugin entry point
├── settings.ts                # Settings interface
├── database.ts                # PostgreSQL connection
├── classifier.ts              # Classification logic
├── highlighter.ts             # Visual highlighting
├── context-menu.ts            # Right-click menu
├── ai-assistant.ts            # Claude integration
├── exporter.ts                # CSV export
├── styles.css                 # Visual styling
├── manifest.json              # Plugin metadata
└── package.json               # Dependencies
```

---

## Integration with Unified Plugin

### How It Fits

**Semantic Editor / Annotation Layer**:
- This becomes the foundation of our right-click annotation system
- Expand epistemic types to full annotation kinds
- Keep the visual highlighting
- Keep the PostgreSQL integration

**Tab 6 (Ontology Graph)**:
- Classifications feed into concept relationships
- Types become nodes in ontology
- Statement-type relationships become edges

---

## Adaptation Required

### Expand Epistemic Types

**Current Types** (Personal Research):
- Axiom
- Canonical
- Evidence
- Coherence
- Reference

**Target Types** (Unified Plugin):
- Axiom
- Claim
- Evidence
- Definition
- Term
- Event
- Equation
- External-Reference
- Breakthrough
- Note (general)

### Adapt Database Schema

**Current Schema**:
- `epistemic.statements`
- `epistemic.types`
- `epistemic.statement_types`

**Target Schema**:
- Merge with our `annotations` table
- Add `kind` field (axiom, claim, evidence, etc.)
- Add `properties` JSONB field for kind-specific data
- Keep UUID system
- Keep offset tracking
- Keep timestamps

**Migration Path**:
```sql
-- Map epistemic.statements to annotations
INSERT INTO annotations (
    uuid,
    note_uuid,
    kind,
    text,
    start_offset,
    end_offset,
    created_at,
    modified_at,
    created_by,
    confidence,
    properties
)
SELECT 
    s.id,
    (SELECT uuid FROM notes WHERE file_path = s.source_file),
    t.name,  -- Map type name to kind
    s.content,
    s.start_offset,
    s.end_offset,
    s.created_at,
    s.updated_at,
    st.tagged_by,
    st.confidence,
    '{}'::jsonb
FROM epistemic.statements s
JOIN epistemic.statement_types st ON s.id = st.statement_id
JOIN epistemic.types t ON st.type_id = t.id;
```

---

## Visual Highlighting Integration

### Current System
- CSS classes for each type
- Superscript icons
- Color coding
- Hover tooltips

### Target System (Glass Box)
- Keep all current features
- Add Master Equation state colors:
  - Cyan (Information/ρ): Raw data, unverified
  - Purple (Witness/ψ): Analyzed, interpreted
  - Gold (Grace/G): Finalized, verified
- Add coherence status dots:
  - 🔴 Red: Contains contradiction
  - 🟡 Yellow: Weak support
  - 🟢 Green: Well-supported
  - ⚪ White: Orphaned
  - 🔵 Blue: AI-flagged

### CSS Integration
```css
/* Current epistemic highlighting */
.epistemic-axiom {
    background-color: rgba(59, 130, 246, 0.2);
    border-bottom: 2px solid #3b82f6;
}

/* Add Master Equation state */
.semantic-information {
    border-left: 3px solid #00ffff; /* Cyan */
}

.semantic-witness {
    border-left: 3px solid #9d4edd; /* Purple */
}

.semantic-grace {
    border-left: 3px solid #ffd700; /* Gold */
}

/* Add coherence status */
.coherence-conflict::after {
    content: "🔴";
    font-size: 0.6em;
    vertical-align: super;
}
```

---

## Right-Click Menu Integration

### Current Menu Structure
```
Right-Click Menu
├── Classify as...
│   ├── Axiom
│   ├── Canonical
│   ├── Evidence
│   ├── Coherence
│   └── Reference
└── Remove Classification
```

### Target Menu Structure (Unified Plugin)
```
Right-Click Menu
├── Annotate as...
│   ├── Axiom
│   ├── Claim
│   ├── Evidence
│   ├── Definition
│   ├── Term
│   ├── Event
│   ├── Equation
│   ├── External Reference
│   ├── Breakthrough
│   └── Note
├── Translate to Narrative (if equation)
├── View Support Chain
├── Check Coherence
└── Remove Annotation
```

---

## Bundle Profiles Adaptation

### Current Profiles
- Personal Research
- YouTube Content
- AI Training Data

### Target Profiles (Unified Plugin)
- **Theophysics Research**: Full annotation types
- **Paper Writing**: Simplified for academic writing
- **Teaching**: Focused on pedagogical structure
- **Custom**: User-defined profiles

**Profile Configuration**:
```typescript
interface BundleProfile {
    name: string;
    description: string;
    annotationTypes: AnnotationType[];
    colorScheme: ColorScheme;
    defaultScope: Scope;
}

interface AnnotationType {
    kind: string;
    label: string;
    color: string;
    icon: string;
    hotkey?: string;
}
```

---

## AI Integration Adaptation

### Current AI Features
- Claude suggests classification
- User accepts/rejects
- System learns from corrections

### Target AI Features (Unified Plugin)
- **Claude (Strategic)**:
  - Suggests annotation types
  - Detects breakthroughs
  - Identifies contradictions
  - Proposes relationships

- **GPT (Analytical)**:
  - Extracts equations
  - Parses timeline events
  - Identifies evidence
  - Generates summaries

**AI Workflow**:
1. User highlights text
2. Right-click → "Ask AI"
3. AI analyzes and suggests annotation
4. Shows confidence score
5. User accepts, modifies, or rejects
6. System learns from decision

---

## Export Adaptation

### Current Export
- CSV format
- Basic fields
- Single profile

### Target Export (Unified Plugin)
- **CSV**: For spreadsheet analysis
- **JSON**: For programmatic access
- **Semantic Bundle**: Complete vault export with all annotations
- **Dashboard**: HTML visualization

**Export Formats**:
```typescript
// CSV Export
id,kind,text,source,confidence,created_by,created_at,properties

// JSON Export
{
  "annotations": [...],
  "relationships": [...],
  "metadata": {...}
}

// Semantic Bundle
vault.zip
├── notes/ (markdown with semantic blocks)
├── semantic-graph.json
└── manifest.json
```

---

## Code Components to Extract

### Priority 1: Core Functionality
- [ ] Right-click menu handler
- [ ] Classification logic
- [ ] PostgreSQL connection and queries
- [ ] UUID generation and management
- [ ] Offset tracking system

### Priority 2: Visual System
- [ ] Highlighting CSS
- [ ] Icon rendering
- [ ] Tooltip system
- [ ] Color scheme management

### Priority 3: Database Layer
- [ ] Schema creation scripts
- [ ] Migration system
- [ ] Query builders
- [ ] Sync logic

### Priority 4: AI Integration
- [ ] Claude API wrapper
- [ ] Suggestion system
- [ ] Confidence scoring
- [ ] Learning mechanism

### Priority 5: Export System
- [ ] CSV generator
- [ ] JSON serializer
- [ ] Bundle creator

---

## Migration Checklist

### Features to Preserve
- [ ] Right-click classification
- [ ] Visual highlighting with colors and icons
- [ ] PostgreSQL storage
- [ ] UUID system
- [ ] Offset tracking
- [ ] Bundle profiles
- [ ] AI suggestions
- [ ] Export to CSV
- [ ] Timestamp tracking
- [ ] Attribution tracking

### Enhancements to Add
- [ ] Expand to full annotation types
- [ ] Add semantic block format
- [ ] Add relationship tracking
- [ ] Add coherence calculation
- [ ] Add Master Equation state colors
- [ ] Add coherence status dots
- [ ] Add support chain visualization
- [ ] Add contradiction detection
- [ ] Add breakthrough identification
- [ ] Add integration with other tabs

---

## Testing Strategy

### Unit Tests
- Classification logic
- Database queries
- UUID generation
- Offset calculation
- Color scheme application

### Integration Tests
- Right-click → classify → store → display
- Profile switching
- AI suggestion → user decision → learning
- Export → import → verify

### User Acceptance Tests
- Classify text in any note
- Switch between profiles
- View classifications in different notes
- Export and analyze data
- Use AI suggestions

---

## Performance Considerations

### Current Performance
- Instant classification
- Fast database queries
- Efficient highlighting
- Minimal UI lag

### Optimizations to Maintain
- Batch database operations
- Cache classification types
- Lazy load highlights
- Debounce AI requests
- Index database properly

---

## Documentation to Create

1. **User Guide**:
   - How to classify text
   - Understanding bundle profiles
   - Using AI suggestions
   - Exporting data

2. **Developer Guide**:
   - Classification system architecture
   - Database schema details
   - Adding new annotation types
   - Creating custom profiles

3. **Integration Guide**:
   - How semantic editor connects to other tabs
   - Data flow from annotation to dashboard
   - API reference

---

## Related Documents
- [[Semantic_Editor|Semantic Editor Specification]]
- [[Semantic_Block_Format|Semantic Block Format]]
- [[00_VAULT_SYSTEM/Config/12_Plugins/Theophysics_Obsidian_Plugin/GITHUB_INTEGRATION_PLAN|GitHub Integration Plan]]
- [[Tab_06_Ontology_Graph|Ontology Graph Tab]]

---

## Attribution

```
Original Implementation: Word-ontology (Epistemic Tagger)
Repository: https://github.com/YellowKidokc/Word-ontology
Author: David Lowe (YellowKidokc)

Integrated into: Theophysics Semantic Research Engine
Integration: Semantic Editor / Annotation Layer
Date: 2025-01-15
```

---

**Status**: Ready for extraction and integration  
**Priority**: High - Foundation of annotation system  
**Next Steps**: Extract code, expand types, integrate with semantic blocks
