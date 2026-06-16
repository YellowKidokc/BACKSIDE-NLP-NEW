"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.extractMathBlocks = extractMathBlocks;
function pushMatches(blocks, regex, content, groupIndex, isBlock) {
    let match;
    while ((match = regex.exec(content)) !== null) {
        blocks.push({
            latex: match[groupIndex].trim(),
            start: match.index,
            end: match.index + match[0].length,
            isBlock
        });
    }
}
function extractMathBlocks(content) {
    const blocks = [];
    pushMatches(blocks, /\$\$([\s\S]+?)\$\$/g, content, 1, true);
    pushMatches(blocks, /(?<!\$)\$([^\$\n]+?)\$(?!\$)/g, content, 1, false);
    pushMatches(blocks, /\\\((.+?)\\\)/g, content, 1, false);
    pushMatches(blocks, /\\\[(.+?)\\\]/gs, content, 1, true);
    pushMatches(blocks, /<div[^>]*class=["'][^"']*math[^"']*["'][^>]*>\s*(\$\$[\s\S]+?\$\$|\\\[[\s\S]+?\\\]|\$[^$]+\$|\\\(.+?\\\))\s*<\/div>/gi, content, 1, true);
    return blocks.sort((left, right) => left.start - right.start);
}
