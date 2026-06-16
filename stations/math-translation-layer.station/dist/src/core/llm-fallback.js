"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.llmFallback = llmFallback;
const openai_1 = __importDefault(require("openai"));
const PRIMARY_MODEL = "gpt-4o-mini";
const SECONDARY_MODEL = "gpt-3.5-turbo";
function parseJsonPayload(raw) {
    const cleaned = raw
        .replace(/^```json\s*/i, "")
        .replace(/^```\s*/i, "")
        .replace(/\s*```$/i, "")
        .trim();
    const parsed = JSON.parse(cleaned);
    if (!parsed.wordEquation || !parsed.spokenExplanation) {
        throw new Error("OpenAI fallback returned incomplete JSON.");
    }
    return {
        wordEquation: parsed.wordEquation,
        spokenExplanation: parsed.spokenExplanation
    };
}
async function requestFallback(model, originalLatex, dictionary, deterministicAttempt) {
    const client = new openai_1.default({
        apiKey: process.env.OPENAI_API_KEY
    });
    const systemPrompt = `You are a math translation assistant for the Theophysics framework.

You translate LaTeX equations into two outputs:
1. Word Equation: Same structure as original, but with plain English labels
2. Spoken Explanation: TTS-ready prose explaining what the mathematical structure means

SYMBOL DICTIONARY:
${JSON.stringify(dictionary.symbols, null, 2)}

RULES FOR WORD EQUATION:
- Preserve the exact structure of the original equation
- Replace symbols with their dictionary labels
- Use × for multiplication, = for equals, − for minus
- Keep fractions, parentheses, superscripts readable

RULES FOR SPOKEN EXPLANATION:
- Write flowing prose, NOT bullet points
- Explain what the mathematical STRUCTURE means (multiplication = all necessary, division = constraint, etc.)
- Use connective words: "which means", "so", "because"
- Make it sound natural when read aloud by TTS
- 2-4 sentences maximum for simple equations
- Can be longer for complex equations, but stay prose`;
    const userPrompt = `Translate this equation:

ORIGINAL LATEX:
${originalLatex}

MY DETERMINISTIC ATTEMPT (may have errors):
Word Equation: ${deterministicAttempt.wordEquation}
Insight: ${deterministicAttempt.insight}

Please provide corrected versions in this exact JSON format:
{
  "wordEquation": "...",
  "spokenExplanation": "..."
}`;
    const response = await client.responses.create({
        model,
        input: [
            {
                role: "system",
                content: systemPrompt
            },
            {
                role: "user",
                content: userPrompt
            }
        ],
        text: {
            format: {
                type: "text"
            }
        },
        temperature: 0.2
    });
    const output = response.output_text?.trim();
    if (!output) {
        throw new Error("OpenAI fallback returned no text output.");
    }
    return parseJsonPayload(output);
}
async function llmFallback(originalLatex, dictionary, deterministicAttempt) {
    if (!process.env.OPENAI_API_KEY) {
        throw new Error("OPENAI_API_KEY is not set.");
    }
    try {
        return await requestFallback(PRIMARY_MODEL, originalLatex, dictionary, deterministicAttempt);
    }
    catch (primaryError) {
        try {
            return await requestFallback(SECONDARY_MODEL, originalLatex, dictionary, deterministicAttempt);
        }
        catch (secondaryError) {
            const primaryMessage = primaryError instanceof Error ? primaryError.message : String(primaryError);
            const secondaryMessage = secondaryError instanceof Error ? secondaryError.message : String(secondaryError);
            throw new Error(`LLM fallback failed. Primary: ${primaryMessage}. Secondary: ${secondaryMessage}.`);
        }
    }
}
