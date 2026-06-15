"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __exportStar = (this && this.__exportStar) || function(m, exports) {
    for (var p in m) if (p !== "default" && !Object.prototype.hasOwnProperty.call(exports, p)) __createBinding(exports, m, p);
};
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.translate = translate;
exports.translateEquation = translateEquation;
exports.translateDocument = translateDocument;
const extract_1 = require("./extract");
const parser_1 = require("./parser");
const renderer_1 = require("./renderer");
const quality_gate_1 = require("./quality-gate");
const structural_insight_1 = require("./structural-insight");
const translator_1 = require("./translator");
const renderers_1 = require("../renderers");
const dictionaries_1 = require("../dictionaries");
__exportStar(require("./extract"), exports);
__exportStar(require("./parser"), exports);
__exportStar(require("./renderer"), exports);
__exportStar(require("./translator"), exports);
__exportStar(require("./types"), exports);
let envLoaded = false;
function maybeLoadEnvFile() {
    if (envLoaded) {
        return;
    }
    envLoaded = true;
    const loader = process.loadEnvFile;
    if (typeof loader === "function") {
        try {
            loader();
        }
        catch {
            // Ignore missing .env files and continue with the process environment.
        }
    }
}
function dedupe(values) {
    return Array.from(new Set(values.filter(Boolean)));
}
function translate(request) {
    const ast = (0, parser_1.parseMath)(request.input, {
        format: request.format,
        displayMode: request.displayMode
    });
    const translated = (0, translator_1.translateMath)(ast, {
        dictionary: request.dictionary,
        mode: request.mode
    });
    return (0, renderer_1.withRenderedOutput)(translated, {
        renderer: request.renderer
    });
}
async function translateEquation(input, options = {}) {
    const format = options.format ?? "tex";
    const dictionaryId = options.dictionary ?? "theophysics";
    const enableFallback = options.enableFallback ?? true;
    const ast = (0, parser_1.parseMath)(input, {
        format,
        displayMode: options.displayMode
    });
    const translated = (0, translator_1.translateMath)(ast, {
        dictionary: dictionaryId,
        mode: "structural"
    });
    const original = (0, renderers_1.renderLatexStructural)(ast);
    let wordEquation = (0, renderers_1.renderWordEquation)(translated.ast);
    let spokenExplanation = (0, structural_insight_1.generateInsight)(translated.ast);
    const quality = (0, quality_gate_1.assessQuality)(translated.ast, wordEquation);
    const diagnostics = dedupe([
        ...ast.meta.parseIssues.map((issue) => issue.message),
        ...translated.diagnostics.map((diagnostic) => diagnostic.message),
        ...quality.structuralIssues
    ]);
    let usedFallback = false;
    if (quality.useFallback && enableFallback) {
        maybeLoadEnvFile();
        try {
            const { llmFallback } = await Promise.resolve().then(() => __importStar(require("./llm-fallback")));
            const dictionary = (0, dictionaries_1.loadDictionary)(dictionaryId);
            const fallback = await llmFallback(input, dictionary.data, {
                wordEquation,
                insight: spokenExplanation
            });
            wordEquation = fallback.wordEquation;
            spokenExplanation = fallback.spokenExplanation;
            usedFallback = true;
        }
        catch (error) {
            diagnostics.push(error instanceof Error
                ? `Fallback unavailable: ${error.message}`
                : `Fallback unavailable: ${String(error)}`);
        }
    }
    if (usedFallback) {
        diagnostics.push("LLM fallback applied after deterministic confidence fell below threshold.");
    }
    return {
        original,
        wordEquation,
        spokenExplanation,
        summary: translated.summary,
        equationId: translated.equationId,
        confidence: quality.confidence,
        usedFallback,
        diagnostics: dedupe(diagnostics)
    };
}
function translateDocument(content, options) {
    return (0, extract_1.extractMathBlocks)(content).map((block) => {
        const translated = translate({
            input: block.latex,
            format: options.format ?? "tex",
            dictionary: options.dictionary,
            mode: options.mode,
            renderer: options.renderer,
            displayMode: block.isBlock
        });
        return {
            original: block.latex,
            translation: translated.output,
            position: block.start,
            summary: translated.summary,
            equationId: translated.equationId
        };
    });
}
