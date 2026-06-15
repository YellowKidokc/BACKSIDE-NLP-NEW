"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.MathTranslator = void 0;
const core_1 = require("./src/core");
class MathTranslator {
    static translate(latex) {
        return (0, core_1.translate)({
            input: latex,
            format: "tex",
            dictionary: "theophysics",
            mode: "narrative",
            renderer: "plaintext"
        }).output;
    }
    static extractMathBlocks(content) {
        return (0, core_1.extractMathBlocks)(content);
    }
    static translateDocument(content) {
        return (0, core_1.translateDocument)(content, {
            dictionary: "theophysics",
            mode: "narrative",
            renderer: "plaintext"
        }).map((item) => ({
            original: item.original,
            translation: item.translation,
            position: item.position
        }));
    }
}
exports.MathTranslator = MathTranslator;
