"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.renderHtmlMathJax = renderHtmlMathJax;
const latex_structural_1 = require("./latex-structural");
function renderHtmlMathJax(ast) {
    const latex = (0, latex_structural_1.renderLatexStructural)(ast);
    const wrapper = ast.meta.displayMode ? ["\\[", "\\]"] : ["\\(", "\\)"];
    return `${wrapper[0]}${latex}${wrapper[1]}`;
}
