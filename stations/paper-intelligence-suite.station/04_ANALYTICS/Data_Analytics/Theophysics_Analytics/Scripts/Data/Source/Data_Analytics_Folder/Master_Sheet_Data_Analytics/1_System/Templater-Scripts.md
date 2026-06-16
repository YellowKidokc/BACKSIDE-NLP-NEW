---
uuid: 785d1bb7-0b3b-52b2-b52f-2738b3261bea
title: ⚙️ Templater Scripts for THEOPHYSICS
author: David Lowe
type: template
created: '2025-11-22'
updated: '2025-11-22'
status: draft
file_path: 00_VAULT_SYSTEM\05_Workflow\Templater-Scripts.md
uuid_generated_at: '2025-11-22T01:23:02.703660'
uuid_version: '1.0'
tags: []
pillars: []
category: theophysics-general
---

# ⚙️ Templater Scripts for THEOPHYSICS

> Automation scripts for Templater plugin. Save these as `.js` files in your Templater scripts folder.

---

## 📁 Setup Instructions

1. **Install Templater Plugin**: Settings → Community Plugins → Browse → "Templater"
2. **Create Scripts Folder**: Create `O:\THEOPHYSICS\.templater-scripts\` folder
3. **Enable Scripts**: Templater Settings → Script files folder location → Point to `.templater-scripts`
4. **Save Scripts**: Copy each script below into separate `.js` files
5. **Use Scripts**: Access via Templater commands or hotkeys

---

## 🏷️ Script 1: Apply Sample Tags

**File**: `apply-sample-tags.js`

**Purpose**: Reads checked tags from Tags-Samples.md and applies them to current note

```javascript
// Apply Sample Tags Script
async function applyTags(tp) {
    // Read Tags-Samples.md
    const samplesFile = app.vault.getAbstractFileByPath('Tags-Samples.md');
    if (!samplesFile) {
        new Notice('Tags-Samples.md not found!');
        return '';
    }
    
    const content = await app.vault.read(samplesFile);
    
    // Extract all tags from the reference table
    const tagMatches = content.match(/#[\w\/]+/g) || [];
    const uniqueTags = [...new Set(tagMatches)];
    
    // Let user select tags
    const selectedTags = await tp.system.suggester(
        uniqueTags,
        uniqueTags,
        true, // Allow multiple selection
        "Select tags to apply"
    );
    
    if (!selectedTags || selectedTags.length === 0) {
        return '';
    }
    
    // Format as YAML array
    const tagArray = selectedTags.map(tag => tag.replace('#', '')).join(', ');
    
    // Get current file
    const activeFile = app.workspace.getActiveFile();
    if (!activeFile) {
        new Notice('No active file!');
        return '';
    }
    
    // Read current content
    let fileContent = await app.vault.read(activeFile);
    
    // Check if YAML frontmatter exists
    const yamlRegex = /^---\n([\s\S]*?)\n---/;
    const yamlMatch = fileContent.match(yamlRegex);
    
    if (yamlMatch) {
        // Update existing YAML
        const existingYaml = yamlMatch[1];
        const tagLineRegex = /tags:\s*\[(.*?)\]/;
        
        if (existingYaml.match(tagLineRegex)) {
            // Merge with existing tags
            const existingTags = existingYaml.match(tagLineRegex)[1];
            const mergedTags = existingTags ? `${existingTags}, ${tagArray}` : tagArray;
            fileContent = fileContent.replace(
                tagLineRegex,
                `tags: [${mergedTags}]`
            );
        } else {
            // Add tags line to existing YAML
            const newYaml = existingYaml + `\ntags: [${tagArray}]`;
            fileContent = fileContent.replace(yamlRegex, `---\n${newYaml}\n---`);
        }
    } else {
        // Create new YAML frontmatter
        const yaml = `---\ntags: [${tagArray}]\ndate: ${tp.date.now("YYYY-MM-DD")}\n---\n\n`;
        fileContent = yaml + fileContent;
    }
    
    // Write back to file
    await app.vault.modify(activeFile, fileContent);
    
    new Notice(`Applied ${selectedTags.length} tags!`);
    return '';
}

module.exports = applyTags;
```

---

## 📋 Script 2: Parse Pasted Headers

**File**: `parse-pasted-headers.js`

**Purpose**: Parses headers from clipboard and creates structured note

```javascript
// Parse Pasted Headers Script
async function parseHeaders(tp) {
    // Get clipboard content
    const pasted = await tp.system.clipboard();
    
    if (!pasted) {
        new Notice('Clipboard is empty!');
        return '';
    }
    
    // Extract headers (## Header format)
    const headerRegex = /^#{1,6}\s+(.+)$/gm;
    const headers = [];
    let match;
    
    while ((match = headerRegex.exec(pasted)) !== null) {
        const level = match[0].match(/^#+/)[0].length;
        const text = match[1].trim();
        headers.push({ level, text });
    }
    
    if (headers.length === 0) {
        new Notice('No headers found in clipboard!');
        return pasted; // Return original content
    }
    
    // Build structured output
    let output = `---\ntags: []\ndate: ${tp.date.now("YYYY-MM-DD")}\nsource: imported\n---\n\n`;
    output += `# ${headers[0].text}\n\n`;
    
    // Add table of contents
    output += `## Table of Contents\n\n`;
    for (const header of headers.slice(1)) {
        const indent = '  '.repeat(header.level - 2);
        const link = header.text.toLowerCase().replace(/\s+/g, '-').replace(/[^\w-]/g, '');
        output += `${indent}- [[#${link}|${header.text}]]\n`;
    }
    output += `\n---\n\n`;
    
    // Add sections
    for (const header of headers.slice(1)) {
        output += `${'#'.repeat(header.level)} ${header.text}\n\n`;
        output += `<!-- Content for ${header.text} -->\n\n`;
    }
    
    new Notice(`Parsed ${headers.length} headers!`);
    return output;
}

module.exports = parseHeaders;
```

---

## 🔄 Script 3: Bulk Tag Folder

**File**: `bulk-tag-folder.js`

**Purpose**: Applies tags to all notes in a selected folder

```javascript
// Bulk Tag Folder Script
async function bulkTagFolder(tp) {
    // Get all folders
    const folders = app.vault.getAllLoadedFiles()
        .filter(f => f.children)
        .map(f => f.path)
        .sort();
    
    // Let user select folder
    const selectedFolder = await tp.system.suggester(
        folders,
        folders,
        false,
        "Select folder to tag"
    );
    
    if (!selectedFolder) {
        return '';
    }
    
    // Get tags to apply
    const tagInput = await tp.system.prompt("Enter tags (comma-separated, no #)");
    if (!tagInput) {
        return '';
    }
    
    const tags = tagInput.split(',').map(t => t.trim());
    
    // Get all markdown files in folder
    const files = app.vault.getMarkdownFiles()
        .filter(f => f.path.startsWith(selectedFolder));
    
    if (files.length === 0) {
        new Notice('No markdown files in folder!');
        return '';
    }
    
    // Confirm action
    const confirm = await tp.system.suggester(
        ['Yes', 'No'],
        [true, false],
        false,
        `Tag ${files.length} files with: ${tags.join(', ')}?`
    );
    
    if (!confirm) {
        return '';
    }
    
    // Apply tags to each file
    let count = 0;
    for (const file of files) {
        let content = await app.vault.read(file);
        
        // Check for YAML
        const yamlRegex = /^---\n([\s\S]*?)\n---/;
        const yamlMatch = content.match(yamlRegex);
        
        if (yamlMatch) {
            const existingYaml = yamlMatch[1];
            const tagLineRegex = /tags:\s*\[(.*?)\]/;
            
            if (existingYaml.match(tagLineRegex)) {
                // Merge tags
                const existingTags = existingYaml.match(tagLineRegex)[1];
                const mergedTags = existingTags ? `${existingTags}, ${tags.join(', ')}` : tags.join(', ');
                content = content.replace(tagLineRegex, `tags: [${mergedTags}]`);
            } else {
                // Add tags line
                const newYaml = existingYaml + `\ntags: [${tags.join(', ')}]`;
                content = content.replace(yamlRegex, `---\n${newYaml}\n---`);
            }
        } else {
            // Create YAML
            const yaml = `---\ntags: [${tags.join(', ')}]\n---\n\n`;
            content = yaml + content;
        }
        
        await app.vault.modify(file, content);
        count++;
    }
    
    new Notice(`Tagged ${count} files!`);
    return '';
}

module.exports = bulkTagFolder;
```

---

## 📊 Script 4: Generate Paper Template

**File**: `new-paper-template.js`

**Purpose**: Creates a new paper with proper YAML and structure

```javascript
// New Paper Template Script
async function newPaper(tp) {
    // Get paper details
    const paperNum = await tp.system.prompt("Paper number (e.g., 14)");
    const paperTitle = await tp.system.prompt("Paper title");
    const paperSubtitle = await tp.system.prompt("Paper subtitle (optional)");
    
    if (!paperNum || !paperTitle) {
        new Notice('Paper number and title required!');
        return '';
    }
    
    // Select paper category
    const category = await tp.system.suggester(
        ['Foundation', 'Mathematical', 'Validation', 'Synthesis'],
        ['foundation', 'mathematical', 'validation', 'synthesis'],
        false,
        "Select paper category"
    );
    
    // Select relevant χ variables
    const chiVars = ['Grace', 'MutualInfo', 'Entropy', 'SelfReference', 'Time', 
                     'Knowledge', 'Relationality', 'Quantum', 'Force', 'Coherence'];
    const selectedVars = await tp.system.suggester(
        chiVars,
        chiVars,
        true,
        "Select relevant χ variables"
    );
    
    // Build tags
    const tags = [
        'pillar/physics',
        'pillar/mathematics',
        `paper/P${paperNum}_${paperTitle.toUpperCase().replace(/\s+/g, '_').substring(0, 20)}`
    ];
    
    if (selectedVars) {
        tags.push(...selectedVars.map(v => `χ_var/${v}`));
    }
    
    // Generate template
    const template = `---
tags: [${tags.join(', ')}]
paper_id: P${paperNum}_${paperTitle.toUpperCase().replace(/\s+/g, '_')}
paper_number: ${paperNum}
title: "${paperTitle}"
subtitle: "${paperSubtitle || ''}"
category: ${category}
status: draft
date: ${tp.date.now("YYYY-MM-DD")}
author: David Lowe
---

# Paper #${paperNum}: ${paperTitle}

${paperSubtitle ? `## ${paperSubtitle}` : ''}

---

## Abstract

<!-- 200-300 word summary -->

---

## I. Introduction

### Background

### Problem Statement

### Proposed Solution

---

## II. Theoretical Framework

### Core Concepts

### Mathematical Formulation

### Connection to Master Equation

---

## III. Detailed Analysis

### Component 1

### Component 2

### Component 3

---

## IV. Implications

### For Physics

### For Theology

### For Philosophy

---

## V. Testable Predictions

1. **Prediction 1**: 
2. **Prediction 2**: 
3. **Prediction 3**: 

---

## VI. Conclusion

### Summary

### Future Work

---

## References

1. 
2. 
3. 

---

## Appendices

### Appendix A: Mathematical Derivations

### Appendix B: Supporting Data

---

**Status**: ${category} layer paper
**Next Steps**: Complete theoretical framework
**Related Papers**: [[Paper-${parseInt(paperNum) - 1}]], [[Paper-${parseInt(paperNum) + 1}]]
`;
    
    new Notice(`Paper #${paperNum} template created!`);
    return template;
}

module.exports = newPaper;
```

---

## 🔍 Script 5: Find Untagged Notes

**File**: `find-untagged.js`

**Purpose**: Lists all notes without tags and offers to tag them

```javascript
// Find Untagged Notes Script
async function findUntagged(tp) {
    // Get all markdown files
    const allFiles = app.vault.getMarkdownFiles();
    const untagged = [];
    
    // Check each file for tags
    for (const file of allFiles) {
        const cache = app.metadataCache.getFileCache(file);
        const hasTags = cache?.frontmatter?.tags || cache?.tags;
        
        if (!hasTags || (Array.isArray(hasTags) && hasTags.length === 0)) {
            untagged.push(file);
        }
    }
    
    if (untagged.length === 0) {
        new Notice('All notes are tagged! 🎉');
        return '';
    }
    
    // Build report
    let report = `# Untagged Notes Report\n\n`;
    report += `**Total Untagged**: ${untagged.length}\n`;
    report += `**Date**: ${tp.date.now("YYYY-MM-DD HH:mm")}\n\n`;
    report += `---\n\n`;
    
    // Group by folder
    const byFolder = {};
    for (const file of untagged) {
        const folder = file.parent.path || 'Root';
        if (!byFolder[folder]) {
            byFolder[folder] = [];
        }
        byFolder[folder].push(file);
    }
    
    // Add to report
    for (const [folder, files] of Object.entries(byFolder).sort()) {
        report += `## ${folder} (${files.length})\n\n`;
        for (const file of files) {
            report += `- [[${file.basename}]]\n`;
        }
        report += `\n`;
    }
    
    new Notice(`Found ${untagged.length} untagged notes!`);
    return report;
}

module.exports = findUntagged;
```

---

## 🎯 Script 6: Quick YAML Insert

**File**: `quick-yaml.js`

**Purpose**: Quickly insert common YAML templates

```javascript
// Quick YAML Insert Script
async function quickYAML(tp) {
    const templates = {
        'Physics Paper': `---
tags: [pillar/physics, logos/field, χ_var/Grace]
paper_id: 
status: draft
date: ${tp.date.now("YYYY-MM-DD")}
---`,
        
        'Theology Note': `---
tags: [pillar/theology, logos/grace]
scripture_ref: 
topic: 
date: ${tp.date.now("YYYY-MM-DD")}
---`,
        
        'Master Equation Component': `---
tags: [pillar/mathematics, logos/master, math_role/operator]
equation_id: 
component: 
date: ${tp.date.now("YYYY-MM-DD")}
---`,
        
        'Miracle Analysis': `---
tags: [pillar/theology, pillar/physics, miracle/healing]
scripture_ref: 
miracle_type: 
physics_mechanism: 
date: ${tp.date.now("YYYY-MM-DD")}
---`,
        
        'Experiment Protocol': `---
tags: [pillar/physics, experiment/APCT, χ_var/Coherence]
experiment_id: 
status: Design Phase
priority: High
date: ${tp.date.now("YYYY-MM-DD")}
---`,
        
        'Deep Law': `---
tags: [law/Law01, logos/field, χ_var/Grace]
law_number: 
law_name: 
date: ${tp.date.now("YYYY-MM-DD")}
---`
    };
    
    const selected = await tp.system.suggester(
        Object.keys(templates),
        Object.values(templates),
        false,
        "Select YAML template"
    );
    
    if (!selected) {
        return '';
    }
    
    return selected + '\n\n';
}

module.exports = quickYAML;
```

---

## 📝 Usage Instructions

### Applying Scripts

1. **Via Command Palette**: `Ctrl/Cmd + P` → Type script name
2. **Via Hotkey**: Assign in Templater settings
3. **Via Template**: Insert `<% tp.user.script-name(tp) %>` in template

### Example Template Using Scripts

```markdown
<% tp.user.quick-yaml(tp) %>

# <% tp.file.title %>

<% tp.user.apply-sample-tags(tp) %>

<!-- Your content here -->
```

---

## 🔧 Customization Tips

- **Modify Tag Lists**: Edit tag arrays in scripts
- **Change YAML Fields**: Update template strings
- **Add New Templates**: Copy and modify existing scripts
- **Combine Scripts**: Call multiple scripts in sequence

---

## 🚨 Troubleshooting

**Script not found?**
- Check Templater settings → Script folder path
- Ensure `.js` extension on files
- Restart Obsidian

**Script errors?**
- Check console: `Ctrl/Cmd + Shift + I`
- Verify file paths in script
- Test with simple script first

**Tags not applying?**
- Check YAML syntax
- Ensure Tags-Samples.md exists
- Verify tag format (no spaces)

---

## 🎧 Script 7: Insert Audio Link

**File**: `insert-audio-link.js`

**Purpose**: Adds a formatted audio link callout at the top of papers/notes

**Usage**:
1. Place cursor where you want the audio link
2. Run Templater command
3. Enter the audio file URL (Google Drive, etc.)
4. Script inserts formatted callout box

```javascript
// Insert Audio Link Template
async function insertAudioLink(tp) {
    // Prompt for the audio link URL
    const audioUrl = await tp.system.prompt("Enter the audio file URL (Google Drive, etc.):");
    
    if (!audioUrl) {
        new Notice('No URL provided - audio link not inserted');
        return '';
    }
    
    // Return the formatted audio callout
    return `---

> 🎧 **Prefer to listen?** [Click here to have this paper read to you](${audioUrl})

---`;
}

module.exports = insertAudioLink;
```

**Output Example**:
```markdown
---

> 🎧 **Prefer to listen?** [Click here to have this paper read to you](https://drive.google.com/...)

---
```

---

**Last Updated**: 2025-10-17
**Total Scripts**: 7
**Categories**: Tagging, Parsing, Bulk Operations, Templates, Maintenance, Quick Actions, Audio Links
