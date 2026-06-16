"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.renderJson = renderJson;
function renderJson(translated) {
    return JSON.stringify({
        dictionaryId: translated.dictionaryId,
        mode: translated.mode,
        equationId: translated.equationId,
        summary: translated.summary,
        narrative: translated.narrative,
        diagnostics: translated.diagnostics,
        resolvedSymbolCount: translated.resolvedSymbolCount
    }, null, 2);
}
