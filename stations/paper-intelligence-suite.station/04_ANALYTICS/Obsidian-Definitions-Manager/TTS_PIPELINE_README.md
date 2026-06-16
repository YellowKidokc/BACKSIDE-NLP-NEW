# 🎙️ TTS-Ready Pipeline

## What It Does

The **TTS-Ready Pipeline** transforms Markdown text into speech-optimized text by applying formal logic rules that:

- Remove all Markdown formatting symbols
- Convert headings into natural pauses
- Handle lists appropriately
- Strip or verbalize LaTeX math
- Normalize paragraph breaks
- Expand acronyms (first use)
- Remove footnotes, citations, and links
- Split long sentences at natural boundaries
- Insert rhetorical pacing markers

---

## How to Use

### Step 1: Open the App

```bash
cd D:\THEOPHYSICS_MASTER\Apps\Obsidian-Definitions-Manager
QUICK_START.bat
```

### Step 2: Go to TTS Pipeline Tab

Click the **🎙️ TTS Pipeline** tab.

### Step 3: Paste Your Markdown

In the **Input (Markdown)** box:
- Paste any Obsidian markdown
- Include headings, formatting, lists, LaTeX, etc.

### Step 4: Configure Options

**LaTeX Handling:**
- ✅ **Strip LaTeX** - Remove all math (default)
- 🗣️ **Verbalize LaTeX** - Convert simple math to words (e.g., `$E = mc^2$` → "E equals m c squared")

**Content Options:**
- **Keep Bullets** - Preserve list structure (default: on)
- **Expand Acronyms** - Expand first use (e.g., "IIT" → "I I T, integrated information theory")
- **Split Long Sentences** - Break at natural boundaries (default: on)

**Sentence Length:**
- Set maximum words per sentence (default: 30)

### Step 5: Process

Click **▶️ Process Text**

Your TTS-optimized text appears in the **Output** box.

### Step 6: Use the Output

- **📋 Copy Output** - Copy to clipboard
- Feed into any TTS engine (Edge TTS, ElevenLabs, etc.)

---

## Example

### Input (Markdown):
```markdown
# The Logos Principle

The **Logos** is the rational structure underlying reality.

- Physical laws
- Mathematical truths
- Logical consistency

The Master Equation is: $\mathcal{L} = \int \Psi^* \hat{H} \Psi d\tau$

This demonstrates the *fundamental unity* of all things.
```

### Output (TTS-Ready):
```
The Logos Principle

The Logos is the rational structure underlying reality.

- Physical laws

- Mathematical truths

- Logical consistency

The Master Equation is: 

This demonstrates the fundamental unity of all things.
```

---

## Configuration Options

### Strip LaTeX vs Verbalize LaTeX

**Strip LaTeX (Default):**
- Completely removes all math
- Best for narrative content
- Cleanest output

**Verbalize LaTeX:**
- Converts simple math to spoken form
- `$2 + 2 = 4$` → "2 plus 2 equals 4"
- `$\sum$` → "the sum of"
- `$\int$` → "the integral of"
- Greek letters: `$\lambda$` → "lambda"

These are mutually exclusive.

### Keep Bullets

**On (Default):**
- Preserves list markers (`-`, `•`, `1.`)
- Adds natural pause after each item

**Off:**
- Removes all list markers
- Converts to continuous text

### Expand Acronyms

**On (Default):**
- First use: "IIT" → "I I T, integrated information theory"
- Subsequent: "IIT"

Built-in acronyms:
- IIT, TTS, AI, QM, GR, PDF, API, GUI

**Off:**
- Acronyms unchanged

### Split Long Sentences

**On (Default):**
- Breaks sentences longer than max length
- Splits at commas, semicolons, dashes

**Off:**
- Keeps sentences as-is

---

## What Gets Removed

### Formatting Symbols
- `#`, `##`, `###` (headings)
- `**bold**`, `*italic*`, `~~strike~~`
- `` `code` ``, ` ```blocks``` `
- `<HTML>` tags

### Links & Citations
- `[text](url)` → "text"
- `[[wikilink]]` → "wikilink"
- `[1]`, `[2]` (footnotes)
- `https://...` (raw URLs)

### Images
- `![alt](image.png)` → "alt" or removed
- `![[image.png]]` → removed

### LaTeX Math
- `$inline$` → removed or verbalized
- `$$block$$` → removed or verbalized

---

## Formal Logic Pipeline

The pipeline executes 10 transformation rules in sequence:

1. **Strip Formatting** - Remove all Markdown control characters
2. **Convert Headings** - Transform to plain text + pause
3. **Convert Lists** - Preserve bullets + add pauses
4. **Handle LaTeX** - Strip or verbalize based on config
5. **Normalize Paragraphs** - Collapse multiple blank lines
6. **Expand Acronyms** - First use only
7. **Remove Citations** - Strip footnotes, links, URLs
8. **Handle Emphasis** - Convert to subtle pauses
9. **Split Long Sentences** - Break at natural boundaries
10. **Insert Pacing** - Add rhetorical pauses

Each rule is deterministic and reversible.

---

## Use Cases

### 1. Convert Papers for Audio

Transform your Theophysics papers into audio-ready text:
- Strip complex LaTeX
- Remove figure references
- Normalize structure

### 2. Prepare Sermons/Talks

Convert notes into spoken delivery:
- Keep rhetorical pauses
- Expand acronyms
- Split long explanations

### 3. Generate Podcast Scripts

Transform research into narrative:
- Remove citations
- Verbalize key equations
- Natural pacing

### 4. Accessibility

Make content speech-friendly:
- Screen readers
- TTS engines
- Voice assistants

---

## Integration

### With Other Apps

The output is plain text - use it anywhere:
- **Edge TTS** - Microsoft's text-to-speech
- **ElevenLabs** - High-quality AI voices
- **Google Cloud TTS** - Multi-language support
- **Amazon Polly** - AWS text-to-speech
- **Screen Readers** - NVDA, JAWS, etc.

### With Obsidian

1. Copy your Obsidian markdown
2. Paste into TTS Pipeline
3. Process
4. Copy output
5. Feed into TTS engine

---

## Statistics

After processing, you see:
- **Input words** → **Output words**
- **Reduction percentage**

Example:
```
✅ Processed: 523 → 412 words (21.2% reduction)
```

This shows how much cleaner the text became.

---

## Tips

### For Best Results

1. **Use heading structure** - They become natural pauses
2. **Keep paragraphs short** - TTS handles short units better
3. **Avoid complex nested lists** - They can confuse TTS
4. **Test with your TTS engine** - Adjust settings based on output

### For Academic Content

- ✅ Strip LaTeX (unless simple equations)
- ✅ Expand acronyms
- ✅ Split long sentences
- Keep bullets for structured arguments

### For Narrative Content

- ✅ Strip LaTeX
- ✅ Keep bullets (if using lists)
- ✅ Split long sentences
- Verbalize only very simple math

---

## Troubleshooting

**Output looks too choppy:**
- Turn off "Split Long Sentences"
- Increase max sentence length

**Too much content removed:**
- Turn off "Strip LaTeX"
- Turn on "Verbalize LaTeX"
- Check "Keep Bullets"

**Acronyms not expanding:**
- Ensure "Expand Acronyms" is checked
- Add custom acronyms to `core/tts_preprocessor.py` if needed

**Math not verbalizing correctly:**
- Only simple math is supported
- Complex LaTeX is best stripped
- Consider adding custom verbalization rules

---

## Technical Details

### Location

```
D:\THEOPHYSICS_MASTER\Apps\Obsidian-Definitions-Manager\
├── core\
│   └── tts_preprocessor.py    ← Core logic
└── ui\
    └── tabs\
        └── tts_tab.py          ← UI interface
```

### Extensibility

To add custom acronyms, edit `core/tts_preprocessor.py`:

```python
self.acronym_expansions = {
    'IIT': 'I I T, integrated information theory',
    'YOUR_ACRONYM': 'expansion here',
}
```

To add custom LaTeX verbalization, edit `_verbalize_latex()` method.

---

## Language-Agnostic Design

The pipeline is formal logic - it works for:
- Any Markdown dialect
- Any TTS engine
- Any language (with appropriate replacements)

It's a **universal preprocessing layer** between your notes and speech synthesis.

---

## Future Enhancements

Possible additions:
- **Custom pause markers** - User-defined pause points
- **Tone indicators** - Mark emphasis, questions, exclamations
- **Speed hints** - Slow down/speed up sections
- **Pronunciation dictionary** - Custom word pronunciations
- **SSML output** - Speech Synthesis Markup Language
- **Batch processing** - Process multiple files
- **Templates** - Save/load config presets

---

## Support

If something isn't working right, check:
1. Input text is valid Markdown
2. Configuration options make sense
3. Output is actually being generated

For bugs or feature requests, document the issue with:
- Input text
- Configuration used
- Expected output
- Actual output

