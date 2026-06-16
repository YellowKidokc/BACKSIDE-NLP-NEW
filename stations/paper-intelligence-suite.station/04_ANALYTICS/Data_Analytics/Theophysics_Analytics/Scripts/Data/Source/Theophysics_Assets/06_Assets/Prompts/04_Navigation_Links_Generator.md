---
uuid: fcd0e7e9-994a-5687-8daf-b2ac74c51c1c
title: Navigation Links Generator for Logos Papers
author: David Lowe
type: note
created: '2025-11-22'
updated: '2025-11-22'
status: draft
file_path: 00_VAULT_SYSTEM\Assets\Prompts\04_Navigation_Links_Generator.md
uuid_generated_at: '2025-11-22T01:23:03.436654'
uuid_version: '1.0'
tags: []
pillars: []
category: theophysics-general
---

# Navigation Links Generator for Logos Papers

## Purpose
Generate consistent navigation footers for all Logos Papers, enabling easy browsing between papers in the series with proper relative paths.

## Context
The Logos Papers is a sequential 12-paper series. Each paper needs navigation links to:
- Previous paper (except Paper 1)
- Home/Index page
- Next paper (except Paper 12)

Links must use correct relative paths and proper filename format.

## Instructions

You are tasked with generating or updating navigation sections for Logos Papers.

## Standard Navigation Format

### Template
```markdown
## NAVIGATION

[Previous: Paper [##] - [Title]](./Paper%20[##]%20-%20[Title]%20-%20FULL.md) | [Home](../00-Series-Index.md) | [Next: Paper [##] - [Title]](./Paper%20[##]%20-%20[Title]%20-%20FULL.md)

---

**License:** CC BY-NC 4.0  
**DOI:** [To be assigned upon publication]  
**Correspondence:** David Lowe, [contact information]
```

### Key Elements
1. **Section header**: "## NAVIGATION" (level 2 heading)
2. **Three links** separated by " | " (space-pipe-space)
3. **Link format**: `[Link Text](relative/path)`
4. **Spacing**: Blank line before, horizontal rule after
5. **License footer**: CC BY-NC 4.0 and DOI placeholder

## Paper Titles and Numbers

Use exact titles:

1. **Paper 01** - The Logos Principle
2. **Paper 02** - The Quantum Bridge
3. **Paper 03** - The Algorithm of Reality
4. **Paper 04** - The Hard Problem of Consciousness
5. **Paper 05** - The Soul Observer
6. **Paper 06** - A Physics of Principalities
7. **Paper 07** - The Grace Function
8. **Paper 08** - The Stretched Out Heavens
9. **Paper 09** - The Moral Universe
10. **Paper 10** - Creatio ex Silico
11. **Paper 11** - Protocols for Validation
12. **Paper 12** - The Decalogue of the Cosmos

## Filename Format

All papers use this format:
```
Paper [##] - [Title] - FULL.md
```

- **[##]**: Two-digit number with leading zero (01-12)
- **[Title]**: Full title from list above
- **Spaces** in filename (URL-encoded as `%20` in links)
- **Suffix**: " - FULL" before .md extension

## URL Encoding

When creating links, encode spaces:
- Space → `%20`

**Example:**
```
File: Paper 01 - The Logos Principle - FULL.md
Link: ./Paper%2001%20-%20The%20Logos%20Principle%20-%20FULL.md
```

## Special Cases

### Paper 01 (First Paper)
**No previous link, only Home and Next:**

```markdown
## NAVIGATION

[Home](../00-Series-Index.md) | [Next: Paper 02 - The Quantum Bridge](./Paper%2002%20-%20The%20Quantum%20Bridge%20-%20FULL.md)

---

**License:** CC BY-NC 4.0  
**DOI:** [To be assigned upon publication]  
**Correspondence:** David Lowe, [contact information]
```

### Paper 12 (Last Paper)
**No next link, only Previous and Home:**

```markdown
## NAVIGATION

[Previous: Paper 11 - Protocols for Validation](./Paper%2011%20-%20Protocols%20for%20Validation%20-%20FULL.md) | [Home](../00-Series-Index.md)

---

**License:** CC BY-NC 4.0  
**DOI:** [To be assigned upon publication]  
**Correspondence:** David Lowe, [contact information]
```

### Papers 02-11 (Middle Papers)
**All three links:**

```markdown
## NAVIGATION

[Previous: Paper [N-1] - [Title]](./Paper%20[N-1]%20-%20[Title]%20-%20FULL.md) | [Home](../00-Series-Index.md) | [Next: Paper [N+1] - [Title]](./Paper%20[N+1]%20-%20[Title]%20-%20FULL.md)

---

**License:** CC BY-NC 4.0  
**DOI:** [To be assigned upon publication]  
**Correspondence:** David Lowe, [contact information]
```

## Complete Examples

### Paper 01 Navigation
```markdown
## NAVIGATION

[Home](../00-Series-Index.md) | [Next: Paper 02 - The Quantum Bridge](./Paper%2002%20-%20The%20Quantum%20Bridge%20-%20FULL.md)

---

**License:** CC BY-NC 4.0  
**DOI:** [To be assigned upon publication]  
**Correspondence:** David Lowe, [contact information]
```

### Paper 05 Navigation
```markdown
## NAVIGATION

[Previous: Paper 04 - The Hard Problem of Consciousness](./Paper%2004%20-%20The%20Hard%20Problem%20of%20Consciousness%20-%20FULL.md) | [Home](../00-Series-Index.md) | [Next: Paper 06 - A Physics of Principalities](./Paper%2006%20-%20A%20Physics%20of%20Principalities%20-%20FULL.md)

---

**License:** CC BY-NC 4.0  
**DOI:** [To be assigned upon publication]  
**Correspondence:** David Lowe, [contact information]
```

### Paper 07 Navigation
```markdown
## NAVIGATION

[Previous: Paper 06 - A Physics of Principalities](./Paper%2006%20-%20A%20Physics%20of%20Principalities%20-%20FULL.md) | [Home](../00-Series-Index.md) | [Next: Paper 08 - The Stretched Out Heavens](./Paper%2008%20-%20The%20Stretched%20Out%20Heavens%20-%20FULL.md)

---

**License:** CC BY-NC 4.0  
**DOI:** [To be assigned upon publication]  
**Correspondence:** David Lowe, [contact information]
```

### Paper 12 Navigation
```markdown
## NAVIGATION

[Previous: Paper 11 - Protocols for Validation](./Paper%2011%20-%20Protocols%20for%20Validation%20-%20FULL.md) | [Home](../00-Series-Index.md)

---

**License:** CC BY-NC 4.0  
**DOI:** [To be assigned upon publication]  
**Correspondence:** David Lowe, [contact information]
```

## Placement in Document

### Position
Place navigation **at the very end** of paper, after:
- Main content
- Conclusion
- References
- Acknowledgments
- Appendices (if any)

### Before Navigation (Typical End Section)
```markdown
---

## 50/50 = 100 (χ)

A ride-or-die partnership.

---

## NAVIGATION

[links here]

---

[license footer]
```

## Validation Checklist

Before finalizing navigation:
- [ ] Section header is "## NAVIGATION" (level 2)
- [ ] Link text includes paper number and title
- [ ] Filenames match exactly (with %20 for spaces)
- [ ] Leading zeros present (01 not 1)
- [ ] " - FULL" suffix in all filenames
- [ ] ".md" extension present
- [ ] Relative paths correct (./ for same folder, ../ for parent)
- [ ] No previous link on Paper 01
- [ ] No next link on Paper 12
- [ ] Home link points to ../00-Series-Index.md
- [ ] Separator is " | " (space-pipe-space)
- [ ] Horizontal rule after links (---)
- [ ] License footer present
- [ ] No typos in paper titles

## Path Reference

Current location: `D:\THEOPHYSICS_MASTER\06_Publication\Logos Paper\BACKUPS\`

**Same folder links:** Use `./`
- Paper 05 linking to Paper 06: `./Paper%2006%20-%20A%20Physics%20of%20Principalities%20-%20FULL.md`

**Parent folder links:** Use `../`
- Any paper linking to Home: `../00-Series-Index.md`

## Common Errors to Avoid

1. **Missing %20 encoding** for spaces in filenames
2. **Wrong number format**: Using "5" instead of "05"
3. **Missing " - FULL"** suffix
4. **Incorrect title**: Double-check against master list
5. **Wrong separators**: Using "," or "·" instead of " | "
6. **Broken relative paths**: Wrong number of ../
7. **Missing license footer**
8. **Incorrect heading level**: Using ### instead of ##

## Bulk Generation

To generate navigation for all papers at once:

```python
papers = [
    (1, "The Logos Principle"),
    (2, "The Quantum Bridge"),
    (3, "The Algorithm of Reality"),
    (4, "The Hard Problem of Consciousness"),
    (5, "The Soul Observer"),
    (6, "A Physics of Principalities"),
    (7, "The Grace Function"),
    (8, "The Stretched Out Heavens"),
    (9, "The Moral Universe"),
    (10, "Creatio ex Silico"),
    (11, "Protocols for Validation"),
    (12, "The Decalogue of the Cosmos")
]

def generate_nav(num, title):
    prev_link = ""
    next_link = ""
    
    if num > 1:
        prev_num = f"{num-1:02d}"
        prev_title = papers[num-2][1]
        prev_link = f"[Previous: Paper {prev_num} - {prev_title}](./Paper%20{prev_num}%20-%20{prev_title.replace(' ', '%20')}%20-%20FULL.md)"
    
    home_link = "[Home](../00-Series-Index.md)"
    
    if num < 12:
        next_num = f"{num+1:02d}"
        next_title = papers[num][1]
        next_link = f"[Next: Paper {next_num} - {next_title}](./Paper%20{next_num}%20-%20{next_title.replace(' ', '%20')}%20-%20FULL.md)"
    
    links = " | ".join(filter(None, [prev_link, home_link, next_link]))
    
    return f"""## NAVIGATION

{links}

---

**License:** CC BY-NC 4.0  
**DOI:** [To be assigned upon publication]  
**Correspondence:** David Lowe, [contact information]
"""

# Generate for each paper
for num, title in papers:
    print(f"=== Paper {num:02d} ===")
    print(generate_nav(num, title))
    print()
```

## Testing Links

After generating navigation, test that:
1. **Files exist** at specified paths
2. **Links work** when clicked in markdown viewer
3. **No 404 errors** if serving locally
4. **Home page exists** at ../00-Series-Index.md

## Updating Navigation

If paper titles or filenames change:
1. Update master title list
2. Regenerate all navigation sections
3. Search/replace old links
4. Verify all links work
5. Commit changes with note about navigation update

## Notes

- Navigation is critical for user experience
- Broken links frustrate readers
- Consistent format enables automated processing
- Test locally before committing
- Update Home/Index page to match navigation structure

