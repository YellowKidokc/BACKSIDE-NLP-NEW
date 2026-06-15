"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.renderMarkdown = renderMarkdown;
exports.renderNarrativeMarkdown = renderNarrativeMarkdown;
const latex_structural_1 = require("./latex-structural");
const plaintext_1 = require("./plaintext");
function renderMarkdown(ast, mode, narrative) {
    if (mode === "narrative" && narrative) {
        return narrative;
    }
    return `$${(0, latex_structural_1.renderLatexStructural)(ast)}$`;
}
function renderNarrativeMarkdown(ast) {
    return (0, plaintext_1.renderPlaintext)(ast);
}
