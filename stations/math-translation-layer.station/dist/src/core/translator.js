"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.translateMath = translateMath;
const dictionaries_1 = require("../dictionaries");
const ast_utils_1 = require("./ast-utils");
function cloneAst(ast) {
    return JSON.parse(JSON.stringify(ast));
}
function applyAliases(value, dictionary) {
    return dictionary.aliases.reduce((current, alias) => {
        const pattern = alias.pattern.replace(/\\\\/g, "\\");
        const replacement = alias.replacement.replace(/\\\\/g, "\\");
        return current.split(pattern).join(replacement);
    }, value);
}
function matchEquation(source, dictionary) {
    for (const rule of dictionary.equations) {
        for (const pattern of rule.patterns) {
            const regex = new RegExp(pattern, "g");
            if (regex.test(source)) {
                return { rule, pattern };
            }
        }
    }
    return {};
}
function matchSymbol(source, rules) {
    return rules.find((rule) => {
        const regex = new RegExp(rule.pattern, "g");
        return regex.test(source);
    });
}
function translateNode(node, dictionary, context) {
    const wholeNodeMatch = matchSymbol((0, ast_utils_1.nodeSource)(node), dictionary.symbols);
    if (wholeNodeMatch && node.kind !== "group" && node.kind !== "operator" && node.kind !== "number") {
        node.translatedText = wholeNodeMatch.label;
        node.spokenText = wholeNodeMatch.spoken ?? wholeNodeMatch.label;
        node.translationStrategy = "replace-node";
        context.resolvedSymbolCount += 1;
        return node;
    }
    switch (node.kind) {
        case "group":
            node.children = node.children.map((child) => translateNode(child, dictionary, context));
            return node;
        case "symbol": {
            const rule = matchSymbol(node.name, dictionary.symbols);
            if (rule) {
                node.translatedText = rule.label;
                node.spokenText = rule.spoken ?? rule.label;
                node.translationStrategy = "replace-node";
                context.resolvedSymbolCount += 1;
            }
            return node;
        }
        case "text":
            if (!node.translatedText) {
                node.translatedText = node.value;
            }
            return node;
        case "function": {
            const rule = matchSymbol(node.name, dictionary.symbols);
            if (rule) {
                node.translatedText = rule.label;
                node.spokenText = rule.spoken ?? rule.label;
                node.translationStrategy = "replace-head";
                context.resolvedSymbolCount += 1;
            }
            node.args = node.args.map((arg) => translateNode(arg, dictionary, context));
            return node;
        }
        case "fraction":
            node.numerator = translateNode(node.numerator, dictionary, context);
            node.denominator = translateNode(node.denominator, dictionary, context);
            return node;
        case "root":
            node.radicand = translateNode(node.radicand, dictionary, context);
            return node;
        case "superscript":
            node.base = translateNode(node.base, dictionary, context);
            node.exponent = translateNode(node.exponent, dictionary, context);
            return node;
        case "subscript":
            node.base = translateNode(node.base, dictionary, context);
            node.subscript = translateNode(node.subscript, dictionary, context);
            return node;
        case "sum":
        case "product":
        case "integral":
            if (node.lower) {
                node.lower = translateNode(node.lower, dictionary, context);
            }
            if (node.upper) {
                node.upper = translateNode(node.upper, dictionary, context);
            }
            return node;
        case "derivative":
            node.subject = translateNode(node.subject, dictionary, context);
            node.variable = translateNode(node.variable, dictionary, context);
            return node;
        case "opaque":
            context.diagnostics.push({
                type: "unsupported",
                message: "Opaque construct preserved during translation.",
                source: node.value
            });
            return node;
        default:
            return node;
    }
}
function translateMath(ast, options) {
    const dictionary = (0, dictionaries_1.loadDictionary)(options.dictionary);
    const normalizedInput = applyAliases(dictionary.hooks.normalizeInput(ast.meta.rawInput), dictionary.data);
    const { rule, pattern } = matchEquation(normalizedInput, dictionary.data);
    const workingAst = cloneAst(ast);
    const diagnostics = [];
    const context = {
        resolvedSymbolCount: 0,
        diagnostics
    };
    translateNode(workingAst, dictionary.data, context);
    let translatedAst = workingAst;
    if (options.mode === "structural") {
        translatedAst = dictionary.hooks.decorateStructuralAst(workingAst, {
            equationId: rule?.equationId
        });
    }
    const translated = {
        dictionaryId: dictionary.data.metadata.id,
        mode: options.mode,
        ast: translatedAst,
        equationId: rule?.equationId,
        summary: rule ? dictionary.data.summaries[rule.equationId] : undefined,
        narrative: options.mode === "narrative" ? rule?.narrative : undefined,
        matchedPattern: pattern,
        diagnostics: dictionary.hooks.buildDiagnostics(translatedAst, diagnostics),
        resolvedSymbolCount: context.resolvedSymbolCount
    };
    if (!translated.summary) {
        translated.summary = dictionary.hooks.fallbackSummary(translated);
    }
    if (!rule && translated.resolvedSymbolCount === 0) {
        translated.diagnostics.push({
            type: "unmapped",
            message: "No dictionary mapping matched this expression.",
            source: ast.meta.rawInput
        });
    }
    return translated;
}
