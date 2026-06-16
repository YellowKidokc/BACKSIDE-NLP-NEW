"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.renderMath = renderMath;
exports.withRenderedOutput = withRenderedOutput;
const renderers_1 = require("../renderers");
function renderById(translated, renderer) {
    switch (renderer) {
        case "latex-structural":
            return (0, renderers_1.renderLatexStructural)(translated.ast);
        case "plaintext":
            return translated.mode === "narrative" && translated.narrative
                ? translated.narrative
                : (0, renderers_1.renderPlaintext)(translated.ast);
        case "markdown":
            return translated.mode === "narrative" && translated.narrative
                ? (0, renderers_1.renderNarrativeMarkdown)(translated.ast)
                : (0, renderers_1.renderMarkdown)(translated.ast, translated.mode, translated.narrative);
        case "tts":
            return translated.mode === "narrative" && translated.narrative
                ? translated.narrative
                : (0, renderers_1.renderTtsPlaintext)(translated.ast);
        case "json":
            return (0, renderers_1.renderJson)(translated);
        case "html-mathjax":
            return (0, renderers_1.renderHtmlMathJax)(translated.ast);
        case "word-equation":
            return (0, renderers_1.renderWordEquation)(translated.ast);
        default:
            throw new Error(`Unsupported renderer: ${renderer}`);
    }
}
function renderMath(translated, options) {
    return renderById(translated, options.renderer);
}
function withRenderedOutput(translated, options) {
    return {
        ...translated,
        output: renderMath(translated, options)
    };
}
