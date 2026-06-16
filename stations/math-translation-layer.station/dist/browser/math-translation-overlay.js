"use strict";
var MathTranslationOverlay = (() => {
  var __defProp = Object.defineProperty;
  var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
  var __getOwnPropNames = Object.getOwnPropertyNames;
  var __hasOwnProp = Object.prototype.hasOwnProperty;
  var __export = (target, all) => {
    for (var name in all)
      __defProp(target, name, { get: all[name], enumerable: true });
  };
  var __copyProps = (to, from, except, desc) => {
    if (from && typeof from === "object" || typeof from === "function") {
      for (let key of __getOwnPropNames(from))
        if (!__hasOwnProp.call(to, key) && key !== except)
          __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
    }
    return to;
  };
  var __toCommonJS = (mod) => __copyProps(__defProp({}, "__esModule", { value: true }), mod);

  // src/browser/overlay.ts
  var overlay_exports = {};
  __export(overlay_exports, {
    enhanceDocument: () => enhanceDocument,
    enhanceMathElement: () => enhanceMathElement
  });

  // src/core/ast-utils.ts
  function nodeSource(node) {
    switch (node.kind) {
      case "group":
        return node.children.map(nodeSource).join(" ").trim();
      case "symbol":
        return node.name;
      case "number":
        return node.value;
      case "operator":
        return node.value;
      case "fraction":
        return `\\frac{${nodeSource(node.numerator)}}{${nodeSource(node.denominator)}}`;
      case "root":
        return `\\sqrt{${nodeSource(node.radicand)}}`;
      case "superscript":
        return `${nodeSource(node.base)}^${nodeSource(node.exponent)}`;
      case "subscript":
        return `${nodeSource(node.base)}_${nodeSource(node.subscript)}`;
      case "function":
        return `${node.name}${node.args.map((arg) => `(${nodeSource(arg)})`).join("")}`;
      case "integral":
        return node.command;
      case "sum":
        return "\\sum";
      case "product":
        return "\\prod";
      case "derivative":
        return `\\frac{${node.operator}${nodeSource(node.subject)}}{${node.operator}${nodeSource(node.variable)}}`;
      case "text":
        return node.value;
      case "opaque":
        return node.value;
      default:
        return "";
    }
  }

  // src/core/parser.ts
  var INTEGRAL_COMMANDS = /* @__PURE__ */ new Set(["\\int", "\\iint", "\\iiint", "\\oint"]);
  var FLATTENED_STRUCTURAL_COMMANDS = /* @__PURE__ */ new Set([
    "\\mathrm",
    "\\mathbf",
    "\\operatorname"
  ]);
  var PRESERVED_STRUCTURAL_COMMANDS = /* @__PURE__ */ new Set([
    "\\mathcal",
    "\\mathbb",
    "\\vec",
    "\\dot",
    "\\ddot",
    "\\bar",
    "\\hat",
    "\\tilde"
  ]);
  var OPERATOR_COMMANDS = /* @__PURE__ */ new Set([
    "\\cdot",
    "\\times",
    "\\approx",
    "\\ge",
    "\\le",
    "\\gg",
    "\\ll",
    "\\equiv",
    "\\rightarrow",
    "\\Rightarrow",
    "\\Leftrightarrow",
    "\\sim",
    "\\propto",
    "\\neq",
    "\\in",
    "\\notin"
  ]);
  function tokenize(input) {
    const tokens = [];
    let index = 0;
    while (index < input.length) {
      const char = input[index];
      if (/\s/.test(char)) {
        index += 1;
        continue;
      }
      if (char === "\\") {
        let value = "\\";
        let lookahead = index + 1;
        if (lookahead < input.length && /[A-Za-z]/.test(input[lookahead])) {
          while (lookahead < input.length && /[A-Za-z]/.test(input[lookahead])) {
            value += input[lookahead];
            lookahead += 1;
          }
        } else if (lookahead < input.length) {
          value += input[lookahead];
          lookahead += 1;
        }
        tokens.push({ type: "command", value });
        index = lookahead;
        continue;
      }
      if (char === "{") {
        tokens.push({ type: "braceOpen", value: char });
        index += 1;
        continue;
      }
      if (char === "}") {
        tokens.push({ type: "braceClose", value: char });
        index += 1;
        continue;
      }
      if (char === "(") {
        tokens.push({ type: "parenOpen", value: char });
        index += 1;
        continue;
      }
      if (char === ")") {
        tokens.push({ type: "parenClose", value: char });
        index += 1;
        continue;
      }
      if (char === "[") {
        tokens.push({ type: "bracketOpen", value: char });
        index += 1;
        continue;
      }
      if (char === "]") {
        tokens.push({ type: "bracketClose", value: char });
        index += 1;
        continue;
      }
      if (char === "^") {
        tokens.push({ type: "superscript", value: char });
        index += 1;
        continue;
      }
      if (char === "_") {
        tokens.push({ type: "subscript", value: char });
        index += 1;
        continue;
      }
      if (char === ",") {
        tokens.push({ type: "comma", value: char });
        index += 1;
        continue;
      }
      if (/[0-9]/.test(char)) {
        let value = char;
        let lookahead = index + 1;
        while (lookahead < input.length && /[0-9.]/.test(input[lookahead])) {
          value += input[lookahead];
          lookahead += 1;
        }
        tokens.push({ type: "number", value });
        index = lookahead;
        continue;
      }
      if (/[=+\-*/·<>|:]/.test(char)) {
        tokens.push({ type: "operator", value: char });
        index += 1;
        continue;
      }
      if (/[A-Za-z\u00C0-\u024F\u0370-\u03FF0-9']/u.test(char)) {
        let value = char;
        let lookahead = index + 1;
        while (lookahead < input.length && /[A-Za-z\u00C0-\u024F\u0370-\u03FF0-9']/u.test(input[lookahead])) {
          value += input[lookahead];
          lookahead += 1;
        }
        tokens.push({ type: "identifier", value });
        index = lookahead;
        continue;
      }
      tokens.push({ type: "operator", value: char });
      index += 1;
    }
    tokens.push({ type: "eof", value: "" });
    return tokens;
  }
  function createGroup(delimiter, children, source, options) {
    return {
      kind: "group",
      delimiter,
      children,
      source,
      ...options
    };
  }
  function canStartPrimary(token) {
    if (token.type === "command") {
      return !OPERATOR_COMMANDS.has(token.value) && token.value !== "\\left" && token.value !== "\\right";
    }
    return [
      "identifier",
      "number",
      "braceOpen",
      "parenOpen",
      "bracketOpen"
    ].includes(token.type);
  }
  function canImplicitMultiply(node) {
    return !(node.kind === "operator" || node.kind === "integral" || node.kind === "sum" || node.kind === "product" || node.kind === "derivative" || node.kind === "group" && node.children.length === 0);
  }
  var Parser = class _Parser {
    constructor(input) {
      this.input = input;
      this.position = 0;
      this.issues = [];
      this.tokens = tokenize(input);
    }
    parse(format, displayMode) {
      const children = this.parseChildren((token) => token.type === "eof");
      return {
        kind: "group",
        delimiter: "none",
        children,
        source: this.input,
        meta: {
          format,
          rawInput: this.input,
          displayMode,
          parseIssues: [...this.issues]
        }
      };
    }
    current() {
      return this.tokens[this.position];
    }
    advance() {
      const token = this.tokens[this.position];
      this.position += 1;
      return token;
    }
    addIssue(issue) {
      this.issues.push(issue);
    }
    parseChildren(stop) {
      const children = [];
      while (!stop(this.current())) {
        if (children.length > 0 && canImplicitMultiply(children[children.length - 1]) && canStartPrimary(this.current())) {
          children.push({ kind: "operator", value: "\xB7", implicit: true });
        }
        const node = this.parseNode();
        if (!node) {
          break;
        }
        children.push(node);
      }
      return children;
    }
    parseNode() {
      const token = this.current();
      switch (token.type) {
        case "identifier":
          return this.parsePostfix({ kind: "symbol", name: this.advance().value });
        case "number":
          return { kind: "number", value: this.advance().value };
        case "operator":
          return { kind: "operator", value: this.advance().value };
        case "command":
          return this.parseCommand();
        case "braceOpen":
          return this.parseGroup("brace", "braceClose");
        case "parenOpen":
          return this.parseGroup("paren", "parenClose");
        case "bracketOpen":
          return this.parseGroup("bracket", "bracketClose");
        case "comma":
          return { kind: "operator", value: this.advance().value };
        default:
          return null;
      }
    }
    parseCommand() {
      const token = this.advance();
      if (token.value === "\\left") {
        return this.parseLeftRightGroup();
      }
      if (token.value === "\\right") {
        const delimiter = this.consumeDelimiterToken();
        this.addIssue({
          code: "unexpected-right",
          message: "Encountered \\right without a matching \\left.",
          source: delimiter.raw ? `\\right${delimiter.raw}` : "\\right"
        });
        return {
          kind: "opaque",
          value: delimiter.raw ? `\\right${delimiter.raw}` : "\\right"
        };
      }
      if (token.value === "\\frac") {
        const numerator = this.consumeScriptArgument();
        const denominator = this.consumeScriptArgument();
        return this.maybeDerivative(numerator, denominator);
      }
      if (token.value === "\\sqrt") {
        return {
          kind: "root",
          radicand: this.consumeScriptArgument(),
          source: token.value
        };
      }
      if (token.value === "\\text") {
        const group = this.consumeScriptArgument();
        return {
          kind: "text",
          value: nodeSource(group)
        };
      }
      if (INTEGRAL_COMMANDS.has(token.value)) {
        return this.parseIntegral(token.value);
      }
      if (token.value === "\\sum") {
        return this.parseSummation("sum");
      }
      if (token.value === "\\prod") {
        return this.parseSummation("product");
      }
      if (OPERATOR_COMMANDS.has(token.value)) {
        return { kind: "operator", value: token.value };
      }
      if (FLATTENED_STRUCTURAL_COMMANDS.has(token.value) || PRESERVED_STRUCTURAL_COMMANDS.has(token.value)) {
        const argument = this.consumeScriptArgument();
        const argumentSource = nodeSource(argument).replace(/\s+/g, "");
        const name = FLATTENED_STRUCTURAL_COMMANDS.has(token.value) ? argumentSource : `${token.value}{${argumentSource}}`;
        return this.parsePostfix({ kind: "symbol", name });
      }
      if (this.current().type === "parenOpen") {
        const call = {
          kind: "function",
          name: token.value,
          args: [this.parseGroup("paren", "parenClose")]
        };
        return this.parseScripts(call);
      }
      return this.parsePostfix({ kind: "symbol", name: token.value });
    }
    parseIntegral(command) {
      const node = {
        kind: "integral",
        command
      };
      this.applyLimits(node);
      return node;
    }
    parseSummation(kind) {
      const node = kind === "sum" ? { kind: "sum" } : { kind: "product" };
      this.applyLimits(node);
      return node;
    }
    applyLimits(node) {
      while (this.current().type === "subscript" || this.current().type === "superscript") {
        const token = this.advance();
        if (token.type === "subscript") {
          node.lower = this.consumeScriptArgument();
        } else {
          node.upper = this.consumeScriptArgument();
        }
      }
    }
    parseGroup(delimiter, closingToken) {
      this.advance();
      const children = this.parseChildren((token) => token.type === closingToken || token.type === "eof");
      if (this.current().type === closingToken) {
        this.advance();
      } else {
        this.addIssue({
          code: "missing-group-close",
          message: `Missing closing token for ${delimiter} group.`,
          source: this.input
        });
      }
      return this.parsePostfix(createGroup(delimiter, children));
    }
    parsePostfix(node) {
      const withScripts = this.parseScripts(node);
      if ((withScripts.kind === "symbol" || withScripts.kind === "text") && this.current().type === "parenOpen") {
        return {
          kind: "function",
          name: withScripts.kind === "symbol" ? withScripts.name : withScripts.value,
          args: [this.parseGroup("paren", "parenClose")]
        };
      }
      return withScripts;
    }
    parseScripts(node) {
      let currentNode = node;
      while (this.current().type === "subscript" || this.current().type === "superscript") {
        const token = this.advance();
        if (token.type === "subscript") {
          currentNode = {
            kind: "subscript",
            base: currentNode,
            subscript: this.consumeScriptArgument()
          };
        } else {
          currentNode = {
            kind: "superscript",
            base: currentNode,
            exponent: this.consumeScriptArgument()
          };
        }
      }
      return currentNode;
    }
    consumeScriptArgument() {
      const token = this.current();
      if (token.type === "braceOpen") {
        return this.parseGroup("brace", "braceClose");
      }
      if (token.type === "parenOpen") {
        return this.parseGroup("paren", "parenClose");
      }
      if (token.type === "bracketOpen") {
        return this.parseGroup("bracket", "bracketClose");
      }
      if (token.type === "eof") {
        this.addIssue({
          code: "missing-argument",
          message: "Expected an argument but reached the end of input.",
          source: this.input
        });
        return createGroup("none", []);
      }
      const node = this.parseNode();
      return createGroup("none", node ? [node] : []);
    }
    parseLeftRightGroup() {
      const left = this.consumeDelimiterToken();
      const children = this.parseChildren(
        (token) => token.type === "eof" || token.type === "command" && token.value === "\\right"
      );
      let right = { raw: left.raw, delimiter: left.delimiter };
      if (this.current().type === "command" && this.current().value === "\\right") {
        this.advance();
        right = this.consumeDelimiterToken();
      } else {
        this.addIssue({
          code: "unmatched-left-right",
          message: "Encountered \\left without a matching \\right.",
          source: `\\left${left.raw}`
        });
      }
      return this.parsePostfix(createGroup(
        left.delimiter === "none" ? right.delimiter : left.delimiter,
        children,
        void 0,
        {
          leftDelimiter: left.raw,
          rightDelimiter: right.raw,
          scalable: true
        }
      ));
    }
    consumeDelimiterToken() {
      const token = this.current();
      if (token.type === "parenOpen" || token.type === "parenClose") {
        this.advance();
        return { raw: token.value, delimiter: "paren" };
      }
      if (token.type === "bracketOpen" || token.type === "bracketClose") {
        this.advance();
        return { raw: token.value, delimiter: "bracket" };
      }
      if (token.type === "braceOpen" || token.type === "braceClose") {
        this.advance();
        return { raw: token.value, delimiter: "brace" };
      }
      if (token.type === "operator" || token.type === "command") {
        this.advance();
        return {
          raw: token.value,
          delimiter: token.value === "(" || token.value === ")" ? "paren" : token.value === "[" || token.value === "]" ? "bracket" : token.value === "{" || token.value === "}" || token.value === "\\{" || token.value === "\\}" ? "brace" : "none"
        };
      }
      this.addIssue({
        code: "missing-argument",
        message: "Expected a delimiter after \\left or \\right.",
        source: this.input
      });
      return { raw: ".", delimiter: "none" };
    }
    maybeDerivative(numerator, denominator) {
      const numeratorSource = nodeSource(numerator).replace(/\s+/g, "");
      const denominatorSource = nodeSource(denominator).replace(/\s+/g, "");
      const totalPattern = numeratorSource.startsWith("\\partial") && denominatorSource.startsWith("\\partial");
      const plainPattern = numeratorSource.startsWith("d") && denominatorSource.startsWith("d");
      if (!totalPattern && !plainPattern) {
        return {
          kind: "fraction",
          numerator,
          denominator
        };
      }
      const operator = totalPattern ? "partial" : "d";
      const subjectSource = totalPattern ? numeratorSource.replace(/^\\partial/, "") : numeratorSource.slice(1);
      const variableSource = totalPattern ? denominatorSource.replace(/^\\partial/, "") : denominatorSource.slice(1);
      return {
        kind: "derivative",
        operator,
        subject: this.parseSubExpression(subjectSource),
        variable: this.parseSubExpression(variableSource)
      };
    }
    parseSubExpression(source) {
      const nested = new _Parser(source);
      return createGroup("none", nested.parseChildren((token) => token.type === "eof"), source);
    }
  };
  function parseMath(input, options) {
    if (options.format !== "tex" && options.format !== "unicode" && options.format !== "mathml") {
      return {
        kind: "group",
        delimiter: "none",
        children: [{ kind: "opaque", value: input }],
        source: input,
        meta: {
          format: options.format,
          rawInput: input,
          displayMode: options.displayMode,
          parseIssues: []
        }
      };
    }
    const parser = new Parser(input);
    return parser.parse(options.format, options.displayMode);
  }

  // src/renderers/latex-structural.ts
  function escapeText(value) {
    return value.replace(/\\/g, "\\textbackslash ").replace(/[{}]/g, "");
  }
  function renderChildren(children) {
    return children.map(renderNode).join(" ").replace(/\s+/g, " ").trim();
  }
  function renderScriptValue(node) {
    if (node.kind === "group" && node.delimiter === "none") {
      return renderChildren(node.children);
    }
    return renderNode(node);
  }
  function renderFunctionArgument(node) {
    if (node.kind === "group") {
      return renderChildren(node.children);
    }
    return renderNode(node);
  }
  function groupDelimiters(node) {
    if (node.leftDelimiter && node.rightDelimiter) {
      return [node.leftDelimiter, node.rightDelimiter];
    }
    if (node.delimiter === "none") {
      return null;
    }
    const delimiters = {
      brace: ["{", "}"],
      paren: ["(", ")"],
      bracket: ["[", "]"]
    };
    return [...delimiters[node.delimiter]];
  }
  function renderNode(node) {
    if (node.translatedText && node.translationStrategy !== "replace-head" && node.kind !== "group" && node.kind !== "operator" && node.kind !== "number") {
      return `\\text{${escapeText(node.translatedText)}}`;
    }
    switch (node.kind) {
      case "group": {
        const content = renderChildren(node.children);
        const delimiters = groupDelimiters(node);
        if (!delimiters) {
          return content;
        }
        const [left, right] = delimiters;
        if (node.scalable) {
          return `\\left${left}${content}\\right${right}`;
        }
        return `${left}${content}${right}`;
      }
      case "symbol":
        return node.name;
      case "number":
        return node.value;
      case "operator":
        return node.value === "\xB7" ? "\\cdot" : node.value;
      case "fraction":
        return `\\frac{${renderScriptValue(node.numerator)}}{${renderScriptValue(node.denominator)}}`;
      case "root":
        return `\\sqrt{${renderScriptValue(node.radicand)}}`;
      case "superscript":
        return `${renderNode(node.base)}^{${renderScriptValue(node.exponent)}}`;
      case "subscript":
        return `${renderNode(node.base)}_{${renderScriptValue(node.subscript)}}`;
      case "function":
        return `${node.translationStrategy === "replace-head" && node.translatedText ? `\\text{${escapeText(node.translatedText)}}` : node.name}${node.args.map((arg) => `(${renderFunctionArgument(arg)})`).join("")}`;
      case "sum": {
        let value = "\\sum";
        if (node.lower) {
          value += `_{${renderScriptValue(node.lower)}}`;
        }
        if (node.upper) {
          value += `^{${renderScriptValue(node.upper)}}`;
        }
        return value;
      }
      case "product": {
        let value = "\\prod";
        if (node.lower) {
          value += `_{${renderScriptValue(node.lower)}}`;
        }
        if (node.upper) {
          value += `^{${renderScriptValue(node.upper)}}`;
        }
        return value;
      }
      case "integral": {
        let value = node.command;
        if (node.lower) {
          value += `_{${renderScriptValue(node.lower)}}`;
        }
        if (node.upper) {
          value += `^{${renderScriptValue(node.upper)}}`;
        }
        return value;
      }
      case "derivative": {
        const symbol = node.operator === "partial" ? "\\partial" : "d";
        return `\\frac{${symbol}${renderScriptValue(node.subject)}}{${symbol}${renderScriptValue(node.variable)}}`;
      }
      case "text":
        return `\\text{${escapeText(node.value)}}`;
      case "opaque":
        return node.value;
      default:
        return "";
    }
  }
  function renderLatexStructural(ast) {
    return renderChildren(ast.children);
  }

  // src/renderers/html-mathjax.ts
  function renderHtmlMathJax(ast) {
    const latex = renderLatexStructural(ast);
    const wrapper = ast.meta.displayMode ? ["\\[", "\\]"] : ["\\(", "\\)"];
    return `${wrapper[0]}${latex}${wrapper[1]}`;
  }

  // src/renderers/json.ts
  function renderJson(translated) {
    return JSON.stringify(
      {
        dictionaryId: translated.dictionaryId,
        mode: translated.mode,
        equationId: translated.equationId,
        summary: translated.summary,
        narrative: translated.narrative,
        diagnostics: translated.diagnostics,
        resolvedSymbolCount: translated.resolvedSymbolCount
      },
      null,
      2
    );
  }

  // src/renderers/plaintext.ts
  function renderChildren2(children, spoken = false) {
    return children.map((child) => renderNode2(child, spoken)).join(" ").replace(/\s+/g, " ").trim();
  }
  function operatorText(value, spoken) {
    if (!spoken) {
      return value === "\\cdot" ? "\xB7" : value;
    }
    switch (value) {
      case "=":
        return "equals";
      case "+":
        return "plus";
      case "-":
        return "minus";
      case "\xB7":
      case "\\cdot":
        return "times";
      case "/":
        return "divided by";
      case "\\ge":
        return "is greater than or equal to";
      case "\\le":
        return "is less than or equal to";
      case "\\rightarrow":
        return "leads to";
      default:
        return value;
    }
  }
  function groupDelimiters2(node) {
    if (node.leftDelimiter && node.rightDelimiter) {
      const left = node.leftDelimiter === "\\{" ? "{" : node.leftDelimiter;
      const right = node.rightDelimiter === "\\}" ? "}" : node.rightDelimiter;
      return [left, right];
    }
    if (node.delimiter === "none") {
      return null;
    }
    const delimiters = {
      brace: ["{", "}"],
      paren: ["(", ")"],
      bracket: ["[", "]"]
    };
    return [...delimiters[node.delimiter]];
  }
  function renderFunctionArgument2(node) {
    if (node.kind === "group") {
      return renderChildren2(node.children, false);
    }
    return renderNode2(node, false);
  }
  function renderSpokenFunctionArgument(node) {
    if (node.kind === "group") {
      return renderChildren2(node.children, true);
    }
    return renderNode2(node, true);
  }
  function renderNode2(node, spoken) {
    if (node.translatedText && node.translationStrategy !== "replace-head" && node.kind !== "group" && node.kind !== "operator" && node.kind !== "number") {
      return spoken ? node.spokenText ?? node.translatedText : node.translatedText;
    }
    switch (node.kind) {
      case "group": {
        const content = renderChildren2(node.children, spoken);
        const delimiters = groupDelimiters2(node);
        if (!delimiters) {
          return content;
        }
        return `${delimiters[0]}${content}${delimiters[1]}`;
      }
      case "symbol":
        return node.name;
      case "number":
        return node.value;
      case "operator":
        return operatorText(node.value, spoken);
      case "fraction":
        return spoken ? `the ratio of ${renderNode2(node.numerator, spoken)} to ${renderNode2(node.denominator, spoken)}` : `${renderNode2(node.numerator, spoken)} / ${renderNode2(node.denominator, spoken)}`;
      case "root":
        return spoken ? `the square root of ${renderNode2(node.radicand, spoken)}` : `sqrt(${renderNode2(node.radicand, spoken)})`;
      case "superscript":
        return spoken ? `${renderNode2(node.base, spoken)} to the power of ${renderNode2(node.exponent, spoken)}` : `${renderNode2(node.base, spoken)}^${renderNode2(node.exponent, spoken)}`;
      case "subscript":
        return spoken ? `${renderNode2(node.base, spoken)} sub ${renderNode2(node.subscript, spoken)}` : `${renderNode2(node.base, spoken)}_${renderNode2(node.subscript, spoken)}`;
      case "function":
        return `${node.translationStrategy === "replace-head" && node.translatedText ? spoken ? node.spokenText ?? node.translatedText : node.translatedText : node.name}(${node.args.map((arg) => spoken ? renderSpokenFunctionArgument(arg) : renderFunctionArgument2(arg)).join(", ")})`;
      case "sum":
        return spoken ? "sum" : "sum";
      case "product":
        return spoken ? "product" : "prod";
      case "integral":
        return spoken ? "integral" : node.command;
      case "derivative":
        return spoken ? `${node.operator === "partial" ? "partial" : "d"} ${renderNode2(node.subject, spoken)} over ${node.operator === "partial" ? "partial" : "d"} ${renderNode2(node.variable, spoken)}` : `${node.operator === "partial" ? "\u2202" : "d"}(${renderNode2(node.subject, spoken)})/${node.operator === "partial" ? "\u2202" : "d"}(${renderNode2(node.variable, spoken)})`;
      case "text":
        return node.value;
      case "opaque":
        return node.value;
      default:
        return "";
    }
  }
  function renderPlaintext(ast) {
    return renderChildren2(ast.children, false);
  }
  function renderTtsPlaintext(ast) {
    return renderChildren2(ast.children, true);
  }

  // src/renderers/markdown.ts
  function renderMarkdown(ast, mode, narrative) {
    if (mode === "narrative" && narrative) {
      return narrative;
    }
    return `$${renderLatexStructural(ast)}$`;
  }
  function renderNarrativeMarkdown(ast) {
    return renderPlaintext(ast);
  }

  // src/renderers/word-equation.ts
  function cleanDelimiter(value) {
    return value.replace(/^\\left/, "").replace(/^\\right/, "").replace(/^\\/, "");
  }
  function groupDelimiters3(node) {
    if (node.leftDelimiter && node.rightDelimiter) {
      return [cleanDelimiter(node.leftDelimiter), cleanDelimiter(node.rightDelimiter)];
    }
    if (node.delimiter === "none") {
      return null;
    }
    const delimiters = {
      brace: ["{", "}"],
      paren: ["(", ")"],
      bracket: ["[", "]"]
    };
    return [...delimiters[node.delimiter]];
  }
  function joinChildren(children) {
    return children.map(renderNode3).join(" ").replace(/\s+/g, " ").trim();
  }
  function renderFunctionArgument3(node) {
    if (node.kind === "group") {
      return joinChildren(node.children);
    }
    return renderNode3(node);
  }
  function operatorText2(value) {
    switch (value) {
      case "\xB7":
      case "\\cdot":
      case "\\times":
        return "\xD7";
      case "-":
        return "\u2212";
      default:
        return value;
    }
  }
  function renderFunctionName(node) {
    if (node.translationStrategy === "replace-head" && node.translatedText) {
      return node.translatedText;
    }
    if (node.translatedText) {
      return node.translatedText;
    }
    return node.name;
  }
  function renderNode3(node) {
    if (node.translatedText && node.translationStrategy !== "replace-head" && node.kind !== "group" && node.kind !== "operator" && node.kind !== "number") {
      return node.translatedText;
    }
    switch (node.kind) {
      case "group": {
        const content = joinChildren(node.children);
        const delimiters = groupDelimiters3(node);
        if (!delimiters) {
          return content;
        }
        return `${delimiters[0]}${content}${delimiters[1]}`;
      }
      case "symbol":
        return node.name;
      case "number":
        return node.value;
      case "operator":
        return operatorText2(node.value);
      case "fraction":
        return `(${renderNode3(node.numerator)}) / (${renderNode3(node.denominator)})`;
      case "root":
        return `sqrt(${renderNode3(node.radicand)})`;
      case "superscript": {
        const base = renderNode3(node.base);
        const exponent = renderNode3(node.exponent);
        if (exponent === "2") {
          return `${base} squared`;
        }
        if (exponent === "3") {
          return `${base} cubed`;
        }
        return `${base}^${exponent}`;
      }
      case "subscript":
        return `${renderNode3(node.base)}_${renderNode3(node.subscript)}`;
      case "function":
        return `${renderFunctionName(node)}(${node.args.map(renderFunctionArgument3).join(", ")})`;
      case "sum": {
        let value = "sum";
        if (node.lower) {
          value += `_${renderNode3(node.lower)}`;
        }
        if (node.upper) {
          value += `^${renderNode3(node.upper)}`;
        }
        return value;
      }
      case "product": {
        let value = "product";
        if (node.lower) {
          value += `_${renderNode3(node.lower)}`;
        }
        if (node.upper) {
          value += `^${renderNode3(node.upper)}`;
        }
        return value;
      }
      case "integral": {
        let value = "integral";
        if (node.lower) {
          value += `_${renderNode3(node.lower)}`;
        }
        if (node.upper) {
          value += `^${renderNode3(node.upper)}`;
        }
        return value;
      }
      case "derivative": {
        const symbol = node.operator === "partial" ? "partial" : "d";
        return `${symbol}(${renderNode3(node.subject)}) / ${symbol}(${renderNode3(node.variable)})`;
      }
      case "text":
        return node.value;
      case "opaque":
        return node.value;
      default:
        return "";
    }
  }
  function renderWordEquation(ast) {
    return joinChildren(ast.children);
  }

  // src/core/renderer.ts
  function renderById(translated, renderer) {
    switch (renderer) {
      case "latex-structural":
        return renderLatexStructural(translated.ast);
      case "plaintext":
        return translated.mode === "narrative" && translated.narrative ? translated.narrative : renderPlaintext(translated.ast);
      case "markdown":
        return translated.mode === "narrative" && translated.narrative ? renderNarrativeMarkdown(translated.ast) : renderMarkdown(translated.ast, translated.mode, translated.narrative);
      case "tts":
        return translated.mode === "narrative" && translated.narrative ? translated.narrative : renderTtsPlaintext(translated.ast);
      case "json":
        return renderJson(translated);
      case "html-mathjax":
        return renderHtmlMathJax(translated.ast);
      case "word-equation":
        return renderWordEquation(translated.ast);
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

  // src/dictionaries/theophysics.json
  var theophysics_default = {
    metadata: {
      id: "theophysics",
      name: "Theophysics Canon Dictionary",
      version: "2026.05.02",
      description: "Machine-readable canon translation layer for Theophysics equations, factors, summaries, and law-bridge mappings.",
      factorOrder: [
        "G",
        "M",
        "E",
        "S_eff",
        "T",
        "K",
        "R",
        "Q",
        "F",
        "C"
      ],
      canonicalInputs: [
        "public-release:README.md",
        "public-release:IDENTIFIER_POLICY.md",
        "public-release:NLP_REVIEW_EVENTS.md",
        "private-canon:not-included"
      ]
    },
    aliases: [
      {
        pattern: "\\\\iiint",
        replacement: "\\\\int"
      },
      {
        pattern: "\\\\iint",
        replacement: "\\\\int"
      },
      {
        pattern: "\xB7",
        replacement: "\\\\cdot"
      }
    ],
    symbols: [
      {
        id: "chi",
        pattern: "^\\\\chi$",
        label: "Coherence Output",
        spoken: "chi",
        canonicalName: "Integrated coherence output",
        spiritualReading: "Christic coherence result"
      },
      {
        id: "factor.G",
        pattern: "^G$",
        label: "Grace",
        spoken: "G",
        canonicalName: "External negentropy influx rate",
        spiritualReading: "Grace"
      },
      {
        id: "factor.M",
        pattern: "^M$",
        label: "Alignment",
        spoken: "M",
        canonicalName: "Alignment cosine",
        spiritualReading: "Moral alignment"
      },
      {
        id: "factor.E",
        pattern: "^E$",
        label: "Truth",
        spoken: "E",
        canonicalName: "Signal propagation fidelity",
        spiritualReading: "Truth transmission"
      },
      {
        id: "factor.S",
        pattern: "^S$",
        label: "Entropy",
        spoken: "S",
        canonicalName: "Entropy placeholder",
        spiritualReading: "Moral entropy"
      },
      {
        id: "factor.S_eff",
        pattern: "^S_eff$",
        label: "Effective Entropy Factor",
        spoken: "S effective",
        canonicalName: "Effective entropy factor",
        spiritualReading: "Entropy inverted through grace"
      },
      {
        id: "factor.S_prod",
        pattern: "^S_prod$",
        label: "Raw Entropy Production",
        spoken: "S prod",
        canonicalName: "Entropy production rate",
        spiritualReading: "Raw disorder accumulation"
      },
      {
        id: "factor.T",
        pattern: "^T$",
        label: "Time",
        spoken: "T",
        canonicalName: "Temporal integration parameter",
        spiritualReading: "Consequence over time"
      },
      {
        id: "factor.K",
        pattern: "^K$",
        label: "Logos",
        spoken: "K",
        canonicalName: "Information compression ratio",
        spiritualReading: "Logos"
      },
      {
        id: "factor.R",
        pattern: "^R$",
        label: "Phase Lock",
        spoken: "R",
        canonicalName: "Phase transition indicator",
        spiritualReading: "Conversion or consequence lock"
      },
      {
        id: "factor.Q",
        pattern: "^Q$",
        label: "Faith Potential",
        spoken: "Q",
        canonicalName: "Superposition measure",
        spiritualReading: "Unresolved faith-choice space"
      },
      {
        id: "factor.F",
        pattern: "^F$",
        label: "Faith Bond",
        spoken: "F",
        canonicalName: "Non-local correlation strength",
        spiritualReading: "Covenant bond"
      },
      {
        id: "factor.C",
        pattern: "^C$",
        label: "Christ Factor",
        spoken: "C",
        canonicalName: "Total integration measure",
        spiritualReading: "Christ or coherence factor"
      },
      {
        id: "moral-entropy",
        pattern: "^S_m$",
        label: "Moral Entropy",
        spoken: "moral entropy"
      },
      {
        id: "grace-work",
        pattern: "^W_grace$",
        label: "Grace Work",
        spoken: "grace work"
      },
      {
        id: "initial-grace",
        pattern: "^G_0$",
        label: "Initial Grace",
        spoken: "G zero"
      },
      {
        id: "grace-resistance",
        pattern: "^R\\(t\\)$",
        label: "Grace Resistance",
        spoken: "resistance at time t"
      },
      {
        id: "grace-receptivity",
        pattern: "^r\\(t'\\)$",
        label: "Grace Receptivity",
        spoken: "receptivity at time t prime"
      },
      {
        id: "moral-dissipation",
        pattern: "^D\\(t\\)$",
        label: "Moral Dissipation",
        spoken: "moral dissipation at time t"
      },
      {
        id: "correction-term",
        pattern: "^C\\(\\\\Psi,\\s*\\\\chi\\)$",
        label: "Christ Alignment Correction",
        spoken: "Christ alignment correction"
      },
      {
        id: "theta-c",
        pattern: "^\\\\Theta_c$",
        label: "Actualization Threshold",
        spoken: "theta c"
      },
      {
        id: "psi",
        pattern: "^\\\\psi$",
        label: "Wavefunction",
        spoken: "psi"
      },
      {
        id: "Psi",
        pattern: "^\\\\Psi$",
        label: "Quantum State",
        spoken: "capital psi"
      },
      {
        id: "Psi-soul",
        pattern: "^\\\\Psi_S$",
        label: "Soul Field",
        spoken: "soul field"
      },
      {
        id: "phi-love",
        pattern: "^\\\\Phi_L$",
        label: "Love Phase Function",
        spoken: "Phi L"
      },
      {
        id: "phi-justice",
        pattern: "^\\\\Phi_J$",
        label: "Justice Phase Function",
        spoken: "Phi J"
      },
      {
        id: "phi-mercy",
        pattern: "^\\\\Phi_M$",
        label: "Mercy Phase Function",
        spoken: "Phi M"
      },
      {
        id: "rho",
        pattern: "^\\\\rho$",
        label: "Density Matrix",
        spoken: "rho"
      },
      {
        id: "hbar",
        pattern: "^\\\\hbar$",
        label: "Reduced Planck Constant",
        spoken: "h bar"
      },
      {
        id: "lambda",
        pattern: "^\\\\Lambda$",
        label: "Cosmological Constant",
        spoken: "lambda"
      },
      {
        id: "ell-p",
        pattern: "^\\\\ell_P$",
        label: "Planck Length",
        spoken: "ell p"
      },
      {
        id: "hubble",
        pattern: "^H_0$",
        label: "Hubble Constant",
        spoken: "H zero"
      },
      {
        id: "k-b",
        pattern: "^k_B$",
        label: "Boltzmann Constant",
        spoken: "k b"
      },
      {
        id: "sigma",
        pattern: "^\\\\sigma$",
        label: "Entropy Generation",
        spoken: "sigma"
      },
      {
        id: "delta",
        pattern: "^\\\\delta$",
        label: "Moral Damage",
        spoken: "delta"
      },
      {
        id: "nu-loss",
        pattern: "^\\\\nu_loss$",
        label: "Invisible Moral Displacement",
        spoken: "nu loss"
      },
      {
        id: "chi-critical",
        pattern: "^\\\\chi_c$",
        label: "Critical Coherence Threshold",
        spoken: "chi c"
      },
      {
        id: "beta-love",
        pattern: "^\\\\beta_L$",
        label: "Love Steepness Parameter",
        spoken: "beta L"
      },
      {
        id: "alpha-s",
        pattern: "^\\\\alpha_s$",
        label: "Strong Coupling Constant",
        spoken: "alpha s"
      },
      {
        id: "alpha",
        pattern: "^\\\\alpha$",
        label: "Coupling Parameter",
        spoken: "alpha"
      },
      {
        id: "beta",
        pattern: "^\\\\beta$",
        label: "Grace Coupling",
        spoken: "beta"
      },
      {
        id: "mu-zero",
        pattern: "^\\\\mu_0$",
        label: "Vacuum Permeability",
        spoken: "mu zero"
      },
      {
        id: "epsilon-zero",
        pattern: "^\\\\epsilon_0$",
        label: "Vacuum Permittivity",
        spoken: "epsilon zero"
      },
      {
        id: "tau-d",
        pattern: "^\\\\tau_D$",
        label: "Decoherence Timescale",
        spoken: "tau d"
      },
      {
        id: "lagrangian",
        pattern: "^\\\\mathcal\\{L\\}$",
        label: "Lagrangian",
        spoken: "Lagrangian"
      },
      {
        id: "hamiltonian",
        pattern: "^\\\\hat\\{H\\}$",
        label: "Hamiltonian Operator",
        spoken: "Hamiltonian"
      },
      {
        id: "z-three",
        pattern: "^\\\\mathbb\\{Z\\}_3$",
        label: "Cyclic Group of Order Three",
        spoken: "Z three"
      },
      {
        id: "tanh",
        pattern: "^\\\\tanh$",
        label: "Sigmoid Transition",
        spoken: "hyperbolic tangent"
      },
      {
        id: "log-two",
        pattern: "^\\\\log_2$",
        label: "Base Two Logarithm",
        spoken: "log base two"
      },
      {
        id: "ln",
        pattern: "^\\\\ln$",
        label: "Natural Logarithm",
        spoken: "natural logarithm"
      },
      {
        id: "exp",
        pattern: "^\\\\exp$",
        label: "Exponential",
        spoken: "exponential"
      },
      {
        id: "law6.B_rel",
        pattern: "^B_\\{\\\\mathrm\\{rel\\}\\}$|^B_rel$",
        label: "Relational bandwidth",
        spoken: "B sub rel",
        canonicalName: "Relational channel bandwidth",
        spiritualReading: "Relation as the carrying capacity of truth"
      },
      {
        id: "law6.S_truth",
        pattern: "^S_\\{\\\\mathrm\\{truth\\}\\}$|^S_truth$",
        label: "Truth signal",
        spoken: "S sub truth",
        canonicalName: "Command-originating truth signal",
        spiritualReading: "Truth signal sourced from Command"
      },
      {
        id: "law6.N_distortion",
        pattern: "^N_\\{\\\\mathrm\\{distortion\\}\\}$|^N_distortion$",
        label: "Distortion noise",
        spoken: "N sub distortion",
        canonicalName: "Misaligned-will distortion noise",
        spiritualReading: "Noise injected by misaligned will"
      },
      {
        id: "law6.R_max",
        pattern: "^R_\\{\\\\max\\}$|^R_max$",
        label: "Maximum revelation capacity",
        spoken: "R max",
        canonicalName: "Maximum revelation capacity",
        spiritualReading: "Maximum truth that can survive the relation channel"
      },
      {
        id: "substrate.Command",
        pattern: "^\\\\mathcal\\{C\\}$",
        label: "Command",
        spoken: "Command",
        canonicalName: "Command primitive",
        spiritualReading: "Generative standard/source"
      },
      {
        id: "substrate.Record",
        pattern: "^\\\\mathcal\\{D\\}$",
        label: "Record",
        spoken: "Record",
        canonicalName: "Record primitive",
        spiritualReading: "Persistent memory and testimony surface"
      }
    ],
    structures: [
      {
        id: "fraction",
        pattern: "^\\\\frac",
        label: "ratio",
        spoken: "the ratio of"
      },
      {
        id: "root",
        pattern: "^\\\\sqrt",
        label: "square root",
        spoken: "the square root of"
      },
      {
        id: "integral",
        pattern: "^\\\\int",
        label: "integral",
        spoken: "the integral of"
      },
      {
        id: "sum",
        pattern: "^\\\\sum",
        label: "sum",
        spoken: "the sum of"
      },
      {
        id: "product",
        pattern: "^\\\\prod",
        label: "product",
        spoken: "the product of"
      },
      {
        id: "derivative",
        pattern: "^(d|\\\\partial)",
        label: "derivative",
        spoken: "the rate of change of"
      },
      {
        id: "gradient",
        pattern: "^\\\\nabla$",
        label: "gradient",
        spoken: "gradient"
      },
      {
        id: "divergence",
        pattern: "^\\\\nabla\\\\cdot",
        label: "divergence",
        spoken: "divergence"
      },
      {
        id: "curl",
        pattern: "^\\\\nabla\\\\times",
        label: "curl",
        spoken: "curl"
      }
    ],
    equations: [
      {
        equationId: "master-equation-local",
        title: "Master Equation Local Form",
        patterns: [
          "\\\\chi_local\\(x,\\s*t\\)\\s*=\\s*G\\(x,\\s*t\\)\\s*\\\\cdot\\s*M\\(x,\\s*t\\)\\s*\\\\cdot\\s*E\\(x,\\s*t\\)\\s*\\\\cdot\\s*S_eff\\(x,\\s*t\\)\\s*\\\\cdot\\s*T\\(x,\\s*t\\)\\s*\\\\cdot\\s*K\\(x,\\s*t\\)\\s*\\\\cdot\\s*R\\(x,\\s*t\\)\\s*\\\\cdot\\s*Q\\(x,\\s*t\\)\\s*\\\\cdot\\s*F\\(x,\\s*t\\)\\s*\\\\cdot\\s*C\\(x,\\s*t\\)",
          "\\\\chi\\s*=\\s*\\\\int\\s*\\(G\\s*\\\\cdot\\s*M\\s*\\\\cdot\\s*E\\s*\\\\cdot\\s*S\\s*\\\\cdot\\s*T\\s*\\\\cdot\\s*K\\s*\\\\cdot\\s*R\\s*\\\\cdot\\s*Q\\s*\\\\cdot\\s*F\\s*\\\\cdot\\s*C\\)\\s*dx\\s*dy\\s*dt",
          "\\\\chi\\s*=\\s*\\\\int.*G\\s*\\\\cdot\\s*M\\s*\\\\cdot\\s*E\\s*\\\\cdot\\s*S\\s*\\\\cdot\\s*T\\s*\\\\cdot\\s*K\\s*\\\\cdot\\s*R\\s*\\\\cdot\\s*Q\\s*\\\\cdot\\s*F\\s*\\\\cdot\\s*C.*dt",
          "\\\\chi\\s*=\\s*G\\s*\\\\cdot\\s*M\\s*\\\\cdot\\s*E\\s*\\\\cdot\\s*S_eff\\s*\\\\cdot\\s*T\\s*\\\\cdot\\s*K\\s*\\\\cdot\\s*R\\s*\\\\cdot\\s*Q\\s*\\\\cdot\\s*F\\s*\\\\cdot\\s*C",
          "\\\\chi\\s*=\\s*G\\s*\\\\cdot\\s*M\\s*\\\\cdot\\s*E\\s*\\\\cdot\\s*S\\s*\\\\cdot\\s*T\\s*\\\\cdot\\s*K\\s*\\\\cdot\\s*R\\s*\\\\cdot\\s*Q\\s*\\\\cdot\\s*F\\s*\\\\cdot\\s*C"
        ],
        narrative: "The local coherence output equals the product of all ten canonical factors, with entropy entering only through the effective entropy factor.",
        summary: "Total coherence is the product of all ten factors, and if any one collapses to zero the output collapses with it."
      },
      {
        equationId: "master-equation-total",
        title: "Master Equation Integral Form",
        patterns: [
          "\\\\chi_total\\s*=\\s*\\\\int",
          "\\\\chi\\s*=\\s*\\\\prod\\s*\\\\eta_i"
        ],
        narrative: "The total coherence output is the integrated product of the ten canonical factors across region and time.",
        summary: "Global coherence is the accumulated integral of the same ten-factor product over space and time."
      },
      {
        equationId: "grace-function",
        title: "Grace Function",
        patterns: [
          "G\\s*=\\s*G_0\\s*\\\\cdot\\s*e\\^\\{\\\\int\\s*r\\(t'\\)\\s*dt'\\}\\s*\\\\cdot\\s*\\(1\\s*-\\s*R\\(t\\)\\)"
        ],
        narrative: "Grace compounds with receptivity over time and is attenuated by resistance.",
        summary: "Grace compounds with receptivity over time and diminishes with resistance."
      },
      {
        equationId: "moral-entropy-equation",
        title: "Moral Entropy Equation",
        patterns: [
          "\\\\frac\\{dS_m\\}\\{dt\\}\\s*=\\s*\\\\sigma\\s*-\\s*\\\\frac\\{W_\\{grace\\}\\}\\{T\\}"
        ],
        narrative: "Moral entropy rises from sin-generated disorder and only decreases when grace performs external work on the system.",
        summary: "Without grace, moral disorder only increases, and grace is the only term that reverses the second law in the moral domain."
      },
      {
        equationId: "yukawa-potential",
        title: "Yukawa Plus Confinement Potential",
        patterns: [
          "V\\(r\\)\\s*=\\s*-\\\\frac\\{\\\\alpha_s\\}\\{r\\}\\s*\\+\\s*k\\s*\\\\cdot\\s*r",
          "V\\(r\\)\\s*=\\s*-\\\\alpha_s\\s*/\\s*r\\s*\\+\\s*k\\s*r"
        ],
        narrative: "Love behaves like a confining potential: attractive at short range and increasingly binding over distance.",
        summary: "Love binds at proximity and the bond strengthens with distance, never releasing."
      },
      {
        equationId: "shannon-capacity-soul",
        title: "Soul Shannon Capacity",
        patterns: [
          "C_i\\s*=\\s*A_i\\s*\\\\cdot\\s*\\\\log_2\\(1\\s*\\+\\s*\\\\frac\\{T_i\\}\\{D_i\\}\\)"
        ],
        narrative: "A soul's truth-carrying capacity grows with receptive bandwidth and with the ratio of truth signal to drift noise.",
        summary: "As sin noise approaches zero, the soul's capacity to receive truth approaches infinity."
      },
      {
        equationId: "shannon-capacity",
        title: "Shannon Channel Capacity",
        patterns: [
          "C\\s*=\\s*B\\s*\\\\log_2\\(1\\s*\\+\\s*\\\\frac\\{S\\}\\{N\\}\\)"
        ],
        narrative: "Channel capacity is set by bandwidth and signal-to-noise ratio, which the spiritual bridge interprets as truth transmission through noise.",
        summary: "Channel capacity rises as signal-to-noise rises."
      },
      {
        equationId: "born-rule",
        title: "Born Rule",
        patterns: [
          "P\\s*=\\s*\\|\\\\langle\\s*\\\\phi\\s*\\|\\s*\\\\psi\\s*\\\\rangle\\|\\^2"
        ],
        narrative: "Faith determines the distribution over possible outcomes by weighting which superposed possibility is realized.",
        summary: "Faith determines the probability distribution of which possibility becomes actual."
      },
      {
        equationId: "faith-threshold",
        title: "Faith Threshold",
        patterns: [
          "FQ\\s*\\\\ge\\s*\\\\Theta_c"
        ],
        narrative: "Possibility actualizes only when faith intensity and quantum potential jointly exceed the collapse threshold.",
        summary: "Faith and possibility must jointly cross threshold before actuality locks in."
      },
      {
        equationId: "moral-beta-decay",
        title: "Three Body Sin Decay",
        patterns: [
          "\\\\psi_\\{whole\\}\\s*\\\\rightarrow\\s*\\\\psi_\\{broken\\}\\s*\\+\\s*\\\\delta\\s*\\+\\s*\\\\nu_\\{loss\\}"
        ],
        narrative: "Sin is modeled as a directional three-body decay where state, damage, and hidden displacement all persist in the ledger.",
        summary: "Sin is a three-body process, and nothing disappears from the moral ledger."
      },
      {
        equationId: "moral-conservation",
        title: "Moral Conservation Equation",
        patterns: [
          "\\\\frac\\{dE\\}\\{dt\\}\\s*=\\s*-\\\\alpha\\s*D\\(t\\)\\s*\\+\\s*\\\\beta\\s*C\\(\\\\Psi,\\s*\\\\chi\\)"
        ],
        narrative: "Moral energy decays under dissipation unless restored by Christ-aligned corrective grace.",
        summary: "Without Christ-aligned correction, moral energy only decays."
      },
      {
        equationId: "einstein-field",
        title: "Einstein Field Equation",
        patterns: [
          "G_\\{\\\\mu\\\\nu\\}\\s*\\+\\s*\\\\Lambda\\s*g_\\{\\\\mu\\\\nu\\}\\s*=\\s*\\\\frac\\{8\\\\pi\\s*G\\}\\{c\\^4\\}\\s*T_\\{\\\\mu\\\\nu\\}"
        ],
        narrative: "Grace and curvature are paired through the geometry of spacetime responding to content and coupling.",
        summary: "Curvature responds to content, which the spiritual bridge reads as grace bending reality around moral mass."
      },
      {
        equationId: "newton-second-law",
        title: "Newton Second Law",
        patterns: [
          "F\\s*=\\s*ma"
        ],
        narrative: "Grace acts as force upon the inertia of nature, pushing motion into a new trajectory.",
        summary: "Force changes motion, which the bridge reads as grace acting on inertia."
      },
      {
        equationId: "faraday-law",
        title: "Faraday Law",
        patterns: [
          "\\\\nabla\\s*\\\\times\\s*E\\s*=\\s*-\\\\frac\\{\\\\partial\\s*B\\}\\{\\\\partial\\s*t\\}"
        ],
        narrative: "Changing field conditions generate revelation the way changing magnetic flux generates electric field.",
        summary: "Changing field conditions generate revelation."
      },
      {
        equationId: "second-law",
        title: "Second Law of Thermodynamics",
        patterns: [
          "\\\\frac\\{dS\\}\\{dt\\}\\s*\\\\ge\\s*0"
        ],
        narrative: "Closed systems accumulate entropy, which the spiritual bridge treats as moral decay without external grace.",
        summary: "Closed systems drift toward disorder unless acted on from outside."
      },
      {
        equationId: "minkowski-metric",
        title: "Minkowski Metric",
        patterns: [
          "ds\\^2\\s*=\\s*-c\\^2\\s*dt\\^2\\s*\\+\\s*dx\\^2\\s*\\+\\s*dy\\^2\\s*\\+\\s*dz\\^2"
        ],
        narrative: "The invariant interval stays fixed even as space and time trade off, which the bridge reads as frame-invariant truth.",
        summary: "Time and space trade off, but the invariant interval remains absolute."
      },
      {
        equationId: "mass-energy-equivalence",
        title: "Mass Energy Equivalence",
        patterns: [
          "E\\s*=\\s*mc\\^2"
        ],
        narrative: "Matter is concentrated energy, which the bridge reads as physical manifestation of deeper substance.",
        summary: "Matter is concentrated energy."
      },
      {
        equationId: "density-matrix",
        title: "Density Matrix",
        patterns: [
          "\\\\rho\\s*=\\s*\\|\\\\psi\\\\rangle\\\\langle\\\\psi\\|"
        ],
        narrative: "The density matrix retains the full state and its coherences, which the bridge pairs with Christ as the coherence that holds all things together.",
        summary: "The full state retains coherence information rather than just outcome probabilities."
      },
      {
        equationId: "noether-theorem",
        title: "Noether Theorem",
        patterns: [
          "\\\\frac\\{\\\\partial\\s*\\\\mathcal\\{L\\}\\}\\{\\\\partial\\s*t\\}\\s*=\\s*0\\s*\\\\Rightarrow\\s*\\\\exists\\s*Q"
        ],
        narrative: "Time-translation symmetry implies a conserved quantity, which the bridge uses to ground moral conservation.",
        summary: "Symmetry generates conservation."
      },
      {
        equationId: "klein-gordon-soul-field",
        title: "Soul Field Klein Gordon Equation",
        patterns: [
          "\\(\\\\Box\\s*\\+\\s*m_S\\^2\\)\\\\Psi_S\\s*=\\s*0"
        ],
        narrative: "The soul field propagates as a massive relativistic wave.",
        summary: "The soul field propagates as a relativistic massive field."
      },
      {
        equationId: "black-hole-entropy",
        title: "Black Hole Entropy",
        patterns: [
          "S_\\{BH\\}\\s*=\\s*\\\\frac\\{k_B\\s*A\\}\\{4\\\\ell_P\\^2\\}"
        ],
        narrative: "Entropy scales with horizon area, showing that information is written on the boundary.",
        summary: "Black hole entropy scales with boundary area rather than volume."
      },
      {
        equationId: "law6-shannon-k-bridge",
        title: "Law 6 Shannon Capacity to Knowledge Bridge",
        patterns: [
          "R_\\{\\\\max\\}\\s*=\\s*B_\\{\\\\mathrm\\{rel\\}\\}\\s*\\\\log_2\\s*\\\\left\\(1\\s*\\+\\s*\\\\frac\\{S_\\{\\\\mathrm\\{truth\\}\\}\\}\\{N_\\{\\\\mathrm\\{distortion\\}\\}\\}\\s*\\\\right\\)",
          "R_\\{\\\\max\\}\\s*=\\s*B_\\{rel\\}\\s*\\\\log_2\\s*\\\\left\\(1\\s*\\+\\s*\\\\frac\\{S_\\{truth\\}\\}\\{N_\\{distortion\\}\\}\\s*\\\\right\\)"
        ],
        narrative: "Law 6 maps Shannon channel capacity into the Logos/Knowledge factor: truth from Command survives only through relational bandwidth against distortion from misaligned Will.",
        summary: "Knowledge is truth that survives transmission, distortion, and recording."
      },
      {
        equationId: "law6-k-compression-ratio",
        title: "K as Logos Compression Ratio",
        patterns: [
          "K\\s*\\(\\\\mathcal\\s*S_\\{\\\\mathrm\\{sys\\}\\}\\)\\s*=\\s*\\\\min\\s*\\\\left\\(\\s*\\\\frac\\{I\\s*\\(\\\\mathcal\\{C\\}\\s*;\\s*\\\\mathcal\\{D\\}\\)\\}\\{H_\\{\\\\mathrm\\{Logos\\}\\}\\s*\\(\\\\mathcal\\{C\\}\\)\\}\\s*,\\s*R_\\{\\\\max\\}\\s*\\\\right\\)",
          "K\\s*=\\s*\\\\min\\s*\\\\left\\(\\s*\\\\frac\\{I\\s*\\(C\\s*;\\s*D\\)\\}\\{H_\\{\\\\mathrm\\{Logos\\}\\}\\}\\s*,\\s*R_\\{\\\\max\\}\\s*\\\\right\\)"
        ],
        narrative: "The Knowledge factor measures how efficiently the Command signal survives into the Record, bounded by the maximum revelation capacity of the relation channel.",
        summary: "K measures Command-to-Record survival, not raw information volume."
      },
      {
        equationId: "law6-k-slot-rejection",
        title: "Law 6 Slot Rejection Control",
        patterns: [
          "B_\\{\\\\mathrm\\{rel\\}\\}\\s*=\\s*0\\s*\\\\Rightarrow\\s*R_\\{\\\\max\\}\\s*=\\s*0\\s*\\\\Rightarrow\\s*K\\s*=\\s*0",
          "B_\\{rel\\}\\s*=\\s*0\\s*->\\s*R_\\{\\\\max\\}\\s*=\\s*0\\s*->\\s*K\\s*=\\s*0"
        ],
        narrative: "If the triadic relation slot collapses, relational bandwidth goes to zero; channel capacity goes to zero; therefore K collapses to zero.",
        summary: "A self-referential system cannot generate Logos from itself."
      },
      {
        equationId: "c-constraint-manifold",
        title: "C as Global Constraint Manifold",
        patterns: [
          "\\\\Phi\\s*\\(\\s*G\\s*,\\s*M\\s*,\\s*E\\s*,\\s*S\\s*,\\s*T\\s*,\\s*K\\s*,\\s*R\\s*,\\s*Q\\s*,\\s*F\\s*\\)\\s*=\\s*0",
          "\\\\Phi\\s*\\(G,M,E,S,T,K,R,Q,F\\)\\s*=\\s*0"
        ],
        narrative: "The C factor is best treated as the global coherence constraint under which the preceding nine factors hold together, while chi remains the output field.",
        summary: "C is the integration condition; chi is the output."
      },
      {
        equationId: "substrate-to-factor-template",
        title: "Substrate to Factor Bridge Template",
        patterns: [
          "SystemState\\s*->\\s*LawConstraint\\s*->\\s*FactorScalar",
          "SystemState\\s*\u2192\\s*LawConstraint\\s*\u2192\\s*Factor"
        ],
        narrative: "Every bridge should pass substrate primitives through a physical law constraint and output one typed Master Equation factor.",
        summary: "Do not just map terms; route SystemState through a real law constraint."
      }
    ],
    summaries: {
      "master-equation-local": "Total coherence is the product of all ten factors, and if any one collapses to zero the output collapses with it.",
      "master-equation-total": "Global coherence is the accumulated integral of the same ten-factor product over space and time.",
      "grace-function": "Grace compounds with receptivity over time and diminishes with resistance.",
      "moral-entropy-equation": "Without grace, moral disorder only increases, and grace is the only term that reverses the second law in the moral domain.",
      "yukawa-potential": "Love binds at proximity and the bond strengthens with distance, never releasing.",
      "shannon-capacity-soul": "As sin noise approaches zero, the soul's capacity to receive truth approaches infinity.",
      "shannon-capacity": "Channel capacity rises as signal-to-noise rises.",
      "born-rule": "Faith determines the probability distribution of which possibility becomes actual.",
      "faith-threshold": "Faith and possibility must jointly cross threshold before actuality locks in.",
      "moral-beta-decay": "Sin is a three-body process, and nothing disappears from the moral ledger.",
      "moral-conservation": "Without Christ-aligned correction, moral energy only decays.",
      "einstein-field": "Curvature responds to content, which the spiritual bridge reads as grace bending reality around moral mass.",
      "newton-second-law": "Force changes motion, which the bridge reads as grace acting on inertia.",
      "faraday-law": "Changing field conditions generate revelation.",
      "second-law": "Closed systems drift toward disorder unless acted on from outside.",
      "minkowski-metric": "Time and space trade off, but the invariant interval remains absolute.",
      "mass-energy-equivalence": "Matter is concentrated energy.",
      "density-matrix": "The full state retains coherence information rather than just outcome probabilities.",
      "noether-theorem": "Symmetry generates conservation.",
      "klein-gordon-soul-field": "The soul field propagates as a relativistic massive field.",
      "black-hole-entropy": "Black hole entropy scales with boundary area rather than volume.",
      "law6-shannon-k-bridge": "Knowledge is truth that survives transmission, distortion, and recording.",
      "law6-k-compression-ratio": "K measures Command-to-Record survival, not raw information volume.",
      "law6-k-slot-rejection": "A self-referential system cannot generate Logos from itself.",
      "c-constraint-manifold": "C is the integration condition; chi is the output.",
      "substrate-to-factor-template": "Do not just map terms; route SystemState through a real law constraint."
    }
  };

  // src/dictionaries/theophysics.hooks.ts
  function cloneNode(node) {
    return JSON.parse(JSON.stringify(node));
  }
  function walk(node, visitor) {
    visitor(node);
    switch (node.kind) {
      case "group":
        node.children.forEach((child) => walk(child, visitor));
        return;
      case "fraction":
        walk(node.numerator, visitor);
        walk(node.denominator, visitor);
        return;
      case "root":
        walk(node.radicand, visitor);
        return;
      case "superscript":
        walk(node.base, visitor);
        walk(node.exponent, visitor);
        return;
      case "subscript":
        walk(node.base, visitor);
        walk(node.subscript, visitor);
        return;
      case "function":
        node.args.forEach((arg) => walk(arg, visitor));
        return;
      case "sum":
      case "product":
      case "integral":
        if (node.lower) {
          walk(node.lower, visitor);
        }
        if (node.upper) {
          walk(node.upper, visitor);
        }
        return;
      case "derivative":
        walk(node.subject, visitor);
        walk(node.variable, visitor);
        return;
      default:
        return;
    }
  }
  function structuralizeMasterEntropy(node) {
    if (node.kind === "symbol" && (node.name === "S" || node.name === "S_prod")) {
      node.translatedText = "Effective Entropy Factor";
      node.spokenText = "S effective";
    }
  }
  var theophysicsHooks = {
    normalizeInput(input) {
      return input.replace(/\$\$/g, "").replace(/\$/g, "").replace(/\\,/g, " ").replace(/\s+/g, " ").trim();
    },
    decorateStructuralAst(ast, context) {
      const clone = cloneNode(ast);
      if (context.equationId === "master-equation-local" || context.equationId === "master-equation-total") {
        walk(clone, structuralizeMasterEntropy);
      }
      return clone;
    },
    buildDiagnostics(ast, diagnostics) {
      const next = [...diagnostics];
      walk(ast, (node) => {
        if (node.kind === "opaque") {
          next.push({
            type: "unsupported",
            message: "Opaque construct preserved during parsing.",
            source: node.value
          });
        }
      });
      return next;
    },
    fallbackSummary(translated) {
      if (translated.equationId) {
        return translated.summary;
      }
      if (translated.resolvedSymbolCount > 0) {
        return "Structural translation applied using the Theophysics dictionary.";
      }
      return void 0;
    }
  };

  // src/dictionaries/index.ts
  var REGISTRY = {
    theophysics: {
      data: theophysics_default,
      hooks: theophysicsHooks
    }
  };
  function loadDictionary(id) {
    const dictionary = REGISTRY[id];
    if (!dictionary) {
      throw new Error(`Unknown dictionary: ${id}`);
    }
    return dictionary;
  }

  // src/core/translator.ts
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
    const wholeNodeMatch = matchSymbol(nodeSource(node), dictionary.symbols);
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
    const dictionary = loadDictionary(options.dictionary);
    const normalizedInput = applyAliases(
      dictionary.hooks.normalizeInput(ast.meta.rawInput),
      dictionary.data
    );
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
      summary: rule ? dictionary.data.summaries[rule.equationId] : void 0,
      narrative: options.mode === "narrative" ? rule?.narrative : void 0,
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

  // src/core/index.ts
  function translate(request) {
    const ast = parseMath(request.input, {
      format: request.format,
      displayMode: request.displayMode
    });
    const translated = translateMath(ast, {
      dictionary: request.dictionary,
      mode: request.mode
    });
    return withRenderedOutput(translated, {
      renderer: request.renderer
    });
  }

  // src/browser/overlay.ts
  var STYLE_ID = "mtl-overlay-style";
  var STATE = /* @__PURE__ */ new WeakMap();
  function ensureStyles(document2) {
    if (document2.getElementById(STYLE_ID)) {
      return;
    }
    const style = document2.createElement("style");
    style.id = STYLE_ID;
    style.textContent = `
        .mtl-shell {
            margin: 0.75rem auto 2rem;
            max-width: min(50rem, calc(100vw - 2rem));
        }
        .mtl-original-equation {
            display: block !important;
            margin: 1.5rem auto !important;
            max-width: 100% !important;
            overflow-x: auto !important;
            text-align: center !important;
            font-size: clamp(1.1rem, 2.4vw, 1.75rem) !important;
            line-height: 1.35 !important;
        }
        .mtl-card {
            display: grid;
            gap: 0.75rem;
            margin-top: 0;
            color: var(--text, #e0e0e0);
            line-height: 1.55;
        }
        .mtl-card[hidden] {
            display: none;
        }

        .mtl-equation-callout {
            border: 1px solid rgba(212, 175, 55, 0.25);
            background: linear-gradient(180deg, rgba(212, 175, 55, 0.06), rgba(0, 0, 0, 0));
            border-radius: 0.7rem;
            padding: 0.8rem 1rem;
            margin-bottom: 0.75rem;
            text-align: center;
        }
        .mtl-structure-label {
            color: var(--text-secondary, #a0a0a0);
            font-size: 0.68rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 0.25rem;
        }
        .mtl-layer {
            border-radius: 0 0.5rem 0.5rem 0;
            padding: 1rem 1.5rem;
            text-align: left;
        }
        .mtl-word-card {
            background: var(--gold-glow, rgba(212, 175, 55, 0.06));
            border: 1px solid var(--gold-dim, rgba(212, 175, 55, 0.15));
            border-left: 3px solid var(--gold, #d4af37);
        }
        .mtl-explanation-card {
            background: var(--green-dim, rgba(34, 197, 94, 0.1));
            border: 1px solid rgba(34, 197, 94, 0.15);
            border-left: 3px solid var(--green, #22c55e);
            margin-bottom: 1.25rem;
        }
        .mtl-label {
            color: var(--gold, #d4af37);
            font-family: var(--mono-font, "JetBrains Mono", monospace);
            font-size: 0.55rem;
            letter-spacing: 0.15em;
            text-transform: uppercase;
            margin-bottom: 0.4rem;
        }
        .mtl-explanation-card .mtl-label {
            color: var(--green, #22c55e);
        }
        .mtl-spoken,
        .mtl-meaning {
            margin: 0.45rem 0 0;
        }
        .mtl-word-equation {
            color: var(--text, #e0e0e0);
            font-family: var(--serif-font, "Crimson Text", Georgia, serif);
            font-size: clamp(1rem, 1.8vw, 1.15rem);
            font-style: italic;
            line-height: 1.6;
            margin: 0;
            overflow-x: auto;
            white-space: normal;
            overflow-wrap: anywhere;
        }
        .mtl-word-equation .mtl-operator {
            color: var(--gold, #d4af37);
            font-weight: 800;
            padding: 0 0.12rem;
        }
        .mtl-word-equation .mtl-grouping {
            color: var(--gold, #d4af37);
        }
        .mtl-word-equation .mtl-number {
            color: var(--blue, #4a9eff);
        }
        .mtl-structure-map {
            display: grid;
            gap: 0.25rem;
            margin: 0.15rem 0 0.8rem;
            overflow-x: auto;
            padding-bottom: 0.2rem;
        }
        .mtl-structure-row {
            display: inline-grid;
            grid-auto-flow: column;
            grid-auto-columns: minmax(3.25rem, max-content);
            align-items: stretch;
            gap: 0.25rem;
            min-width: max-content;
        }
        .mtl-structure-token {
            border: 1px solid rgba(212, 175, 55, 0.16);
            border-radius: 0.35rem;
            padding: 0.32rem 0.45rem;
            text-align: center;
        }
        .mtl-structure-word .mtl-structure-token {
            background: rgba(212, 175, 55, 0.08);
            color: var(--text, #e0e0e0);
            font-family: var(--sans-font, "Inter", sans-serif);
            font-size: 0.72rem;
            line-height: 1.25;
        }
        .mtl-structure-math .mtl-structure-token {
            background: rgba(0, 0, 0, 0.18);
            color: var(--gold, #d4af37);
            font-family: var(--mono-font, "JetBrains Mono", monospace);
            font-size: 0.86rem;
            line-height: 1.35;
            white-space: nowrap;
        }
        .mtl-meaning {
            color: var(--text-dim, #a0a0a0);
            font-family: var(--sans-font, "Inter", sans-serif);
            font-size: 0.9rem;
            line-height: 1.7;
            margin: 0;
            max-width: 100%;
            text-align: left;
        }
        .mtl-key {
            display: grid;
            gap: 0.28rem;
            margin-top: 0.6rem;
        }
        .mtl-key div {
            font-size: 0.92rem;
        }
        .mtl-symbol {
            color: var(--gold, #d4af37);
            font-weight: 700;
        }
        .mtl-summary {
            color: var(--text-secondary, #a0a0a0);
            font-size: 0.92rem;
            font-style: italic;
            margin-top: 0.65rem;
        }
        .mtl-toggle,
        .mtl-master-toggle {
            background: none;
            border: none;
            color: var(--gold, #d4af37);
            cursor: pointer;
            font-family: var(--mono-font, "JetBrains Mono", monospace);
            font-size: 0.76rem;
            padding: 0;
            margin-top: 0.5rem;
            text-decoration: underline;
            text-underline-offset: 0.18rem;
        }
        .mtl-master-toggle {
            position: fixed;
            right: 1rem;
            top: 1rem;
            z-index: 9999;
        }
        .mtl-tts-cue {
            position: absolute;
            width: 1px;
            height: 1px;
            padding: 0;
            margin: -1px;
            overflow: hidden;
            clip: rect(0, 0, 0, 0);
            white-space: nowrap;
            border: 0;
        }
    `;
    document2.head.appendChild(style);
  }
  function stripDelimiters(source) {
    return source.replace(/^\$\$/, "").replace(/\$\$$/, "").replace(/^\$/, "").replace(/\$$/, "").replace(/^\\\[/, "").replace(/\\\]$/, "").replace(/^\\\(/, "").replace(/\\\)$/, "").trim();
  }
  function normalizeForLookup(source) {
    const replacements = [
      [/\\chi|\u03c7|𝜒/g, "chi"],
      [/\\iiint|\u222d|\\iint|\u222b|\\int/g, "int"],
      [/\\cdot|⋅|·|\*/g, ""],
      [/\\,|\\left|\\right|\\text|\\mathrm/g, ""],
      [/\\geq|≥/g, "ge"],
      [/\\leq|≤/g, "le"],
      [/\\neq|≠/g, "ne"],
      [/\\propto|∝/g, "propto"],
      [/\\to|→/g, "to"],
      [/\\Delta|Δ/g, "delta"],
      [/\\Phi|Φ/g, "phi"],
      [/\\Psi|Ψ/g, "psi"],
      [/\\sigma|σ/g, "sigma"],
      [/\\gamma|γ/g, "gamma"],
      [/\\mu|μ/g, "mu"],
      [/\\nu|ν/g, "nu"],
      [/\\rho|ρ/g, "rho"],
      [/\\Lambda|Λ/g, "lambda"],
      [/\\Theta|Θ/g, "theta"],
      [/\\hbar|ℏ/g, "hbar"],
      [/\\pi|π/g, "pi"]
    ];
    let normalized = source;
    for (const [pattern, replacement] of replacements) {
      normalized = normalized.replace(pattern, replacement);
    }
    return normalized.replace(/\\[A-Za-z]+/g, "").replace(/[^A-Za-z0-9]+/g, "").toLowerCase();
  }
  function findReviewedTranslation(source, document2) {
    const win = document2.defaultView;
    if (!win) {
      return void 0;
    }
    const table = win.MATH_TRANSLATION_TABLE_V2;
    if (!table?.length) {
      return void 0;
    }
    const key = normalizeForLookup(source);
    return table.find((entry) => entry.key === key);
  }
  function reviewedVisualIsReadable(visual) {
    return Boolean(visual && !/[\\{}_^]/.test(visual));
  }
  function escapeHtml(value) {
    return value.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }
  function renderWordEquationMarkup(value) {
    return escapeHtml(value).replace(/(\d+(?:\.\d+)?|[=+*/-]|[()])/g, (match) => {
      if (/^\d/.test(match)) {
        return `<span class="mtl-number">${match}</span>`;
      }
      if (/[()]/.test(match)) {
        return `<span class="mtl-grouping">${match}</span>`;
      }
      return `<span class="mtl-operator">${match}</span>`;
    });
  }
  function isLikelyMath(source) {
    return /\\[A-Za-z]+|=|·|\^|_|\$/.test(source);
  }
  function extractSource(element) {
    const dataSource = element.dataset.mtlSource ?? element.dataset.tex;
    if (dataSource) {
      return dataSource;
    }
    const clone = element.cloneNode(true);
    clone.querySelectorAll(".eq-label, .elbl, .lbl, .mlabel, .mnote, .mtl-shell, .mtl-card").forEach((node) => node.remove());
    const text = clone.textContent?.replace(/\s+/g, " ").trim();
    if (text && isLikelyMath(text)) {
      return text;
    }
    return void 0;
  }
  function setMode(state, mode) {
    state.mode = mode;
    state.card.hidden = mode === "hidden";
  }
  var TERMS = {
    "\\chi": "coherence output",
    "\u03C7": "coherence output",
    G: "outside-in restoration force",
    M: "moral alignment",
    E: "truth transmission",
    S: "breakdown pressure",
    S_eff: "effective entropy factor",
    T: "time",
    K: "Logos",
    R: "phase lock",
    Q: "faith potential",
    F: "faith bond",
    C: "inner wholeness",
    O_eff: "effective observer or ordering strength"
  };
  function termLabel(source, symbol) {
    if (symbol === "C" && !/\\frac\{dC\}\{dt\}|dC\/dt|C\^\*/.test(source)) {
      return "Christ factor";
    }
    if (symbol === "G" && /G_\{\\mu\\nu\}/.test(source)) {
      return void 0;
    }
    return TERMS[symbol];
  }
  function sourceHas(source, symbol) {
    const escaped = symbol.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    return new RegExp(`(^|[^A-Za-z])${escaped}([^A-Za-z]|$)`).test(source);
  }
  function stableHash(value) {
    let hash = 2166136261;
    for (let i = 0; i < value.length; i += 1) {
      hash ^= value.charCodeAt(i);
      hash = Math.imul(hash, 16777619);
    }
    return (hash >>> 0).toString(16).padStart(8, "0");
  }
  function browserEventId(source, tokens) {
    const tokenText = tokens.map((token) => `${token.math}:${token.word}`).join("|");
    return `mtl-struct-${stableHash(`${source}${tokenText}`)}`;
  }
  function structureLabel(source, math) {
    const clean = math.replace(/\s+/g, "");
    if (/^\\frac\{dC\}\{dt\}$|^dC\/dt$|^dCdt$/i.test(clean)) {
      return "change in coherence";
    }
    if (/^\(1-C\)$/.test(clean)) {
      return "remaining gap";
    }
    if (clean === "=") {
      return "equals";
    }
    if (clean === "+" || clean === "\\+") {
      return "plus";
    }
    if (clean === "-") {
      return "minus";
    }
    if (clean === "\\cdot" || clean === "\xC2\xB7" || clean === "*" || clean === "\\times") {
      return "times";
    }
    if (clean === "(" || clean === ")") {
      return clean;
    }
    if (/^\d/.test(clean)) {
      return clean;
    }
    const label = termLabel(source, clean);
    if (label) {
      return label;
    }
    if (clean === "\\chi" || clean === "\u03C7") {
      return "coherence output";
    }
    return clean.replace(/^\\/, "");
  }
  function structuralTokens(source) {
    const normalized = source.replace(/\$\$?/g, "").replace(/\\left|\\right/g, "").replace(/\s+/g, " ").trim();
    const derivativeMatch = normalized.match(/\\frac\{dC\}\{dt\}\s*=\s*O\s*(?:\\cdot|Â·|\*)?\s*G\s*\(1-C\)\s*-\s*S\s*(?:\\cdot|Â·|\*)?\s*C/);
    if (derivativeMatch) {
      return [
        { math: "dC/dt", word: "change in coherence" },
        { math: "=", word: "equals" },
        { math: "O", word: "openness" },
        { math: "\xB7", word: "times" },
        { math: "G", word: "outside-in restoration" },
        { math: "(1-C)", word: "remaining gap" },
        { math: "\u2212", word: "minus" },
        { math: "S", word: "breakdown pressure" },
        { math: "\xB7", word: "times" },
        { math: "C", word: "inner wholeness" }
      ];
    }
    const tokenPattern = /\\frac\{dC\}\{dt\}|\\chi|[A-Za-z](?:_\{[^{}]+\}|\^\*|\([^)]+\))?|\(1-C\)|\\cdot|\\times|Â·|[=+\-*/()]|\d+(?:\.\d+)?/g;
    const tokens = normalized.match(tokenPattern) ?? [];
    return tokens.slice(0, 28).map((math) => ({ math: math === "\\cdot" || math === "\\times" ? "\xB7" : math, word: structureLabel(source, math) })).filter((token) => token.math && token.word);
  }
  function renderStructureMapMarkup(source) {
    const tokens = structuralTokens(source);
    if (tokens.length < 3) {
      return "";
    }
    const wordRow = tokens.map((token) => `<span class="mtl-structure-token">${escapeHtml(token.word)}</span>`).join("");
    const mathRow = tokens.map((token) => `<span class="mtl-structure-token">${escapeHtml(token.math)}</span>`).join("");
    const eventId = browserEventId(source, tokens);
    const payload = {
      eventId,
      event: "structural-equation-map",
      source,
      tokens,
      reviewPriority: "high",
      reviewInstruction: "Check whether the common-language row preserves the same logical structure as the math row."
    };
    return [
      `<div class="mtl-structure-map" aria-label="Equation structure translated symbol by symbol" data-mtl-event-id="${eventId}" data-mtl-event="structural-equation-map" data-mtl-review-priority="high" data-mtl-review='${escapeHtml(JSON.stringify(payload))}'>`,
      `<div class="mtl-structure-label">Word structure</div><div class="mtl-structure-row mtl-structure-word">${wordRow}</div>`,
      `<div class="mtl-structure-label">Symbol structure</div><div class="mtl-structure-row mtl-structure-math">${mathRow}</div>`,
      "</div>"
    ].join("");
  }
  function orderedTerms(source) {
    const order = ["\\chi", "\u03C7", "G", "M", "E", "S_eff", "S", "T", "K", "R", "Q", "F", "C", "O_eff"];
    const seen = /* @__PURE__ */ new Set();
    const terms = [];
    for (const symbol of order) {
      if (seen.has(symbol)) {
        continue;
      }
      if (source.includes(symbol) || sourceHas(source, symbol)) {
        const label = termLabel(source, symbol);
        if (label) {
          terms.push([symbol === "\\chi" || symbol === "\u03C7" ? "chi" : symbol, label]);
          seen.add(symbol);
        }
      }
    }
    return terms;
  }
  function buildSpokenStructure(source) {
    const terms = orderedTerms(source);
    const hasIntegral = /\\i{0,3}int|\u222b|\u222d/.test(source);
    const hasDerivative = /\\frac\{d|dCdt|dC\/dt/.test(source);
    const prefix = hasDerivative ? "d C over d t equals the change in coherence over time." : hasIntegral ? "chi equals the total integrated result over the tested domain." : "Read the expression as this structured claim.";
    const key = terms.length > 0 ? `${terms.map(([symbol, label]) => `${symbol} equals ${label}`).join("; ")}.` : "";
    const suffix = hasIntegral ? "Integrated over x, y, and t." : "";
    return [prefix, key, suffix].filter(Boolean).join(" ");
  }
  function buildVisualEquation(source) {
    const hasIntegral = /\\i{0,3}int|\u222b|\u222d/.test(source);
    const hasDerivative = /\\frac\{d|dCdt|dC\/dt/.test(source);
    const terms = orderedTerms(source);
    if (/\\psi\\rangle/.test(source) && /\\alpha/.test(source) && /\\beta/.test(source)) {
      return "quantum state = alpha-weighted state zero + beta-weighted state one; squared amplitudes add to one";
    }
    if (/\\Psi_\{\\text\{Eden\}\}/.test(source) && /Obedience/.test(source) && /Transgression/.test(source)) {
      return "Eden state = obedience-weighted moral state + transgression-weighted moral state before measurement";
    }
    if (/V\(\\phi\)/.test(source) && /\\mu\^2/.test(source) && /\\lambda/.test(source)) {
      return "potential energy = negative mass term times the order parameter squared + self-interaction term times the order parameter to the fourth";
    }
    if (/\\hat\{L\}/.test(source) && /\\hat\{K\}/.test(source)) {
      return "Tree of Life operator sustains coherence; Tree of Knowledge operator collapses superposition into a measured state";
    }
    if (/\\sigma\s*=\s*6\.35/.test(source) && /10\^\{-4\}/.test(source)) {
      return "PEAR-LAB signal = 6.35 sigma statistical significance with an effect size around one part in ten thousand";
    }
    if (/\\chi\s*=\s*\\iiint\s*\(G\s*\\cdot\s*M\s*\\cdot\s*E\s*\\cdot\s*S\s*\\cdot\s*T\s*\\cdot\s*K\s*\\cdot\s*R\s*\\cdot\s*Q\s*\\cdot\s*F\s*\\cdot\s*C\)/.test(source)) {
      return "coherence output = triple integral of (outside-in restoration force * moral alignment * truth transmission * breakdown pressure * time * Logos * phase lock * faith potential * faith bond * Christ factor) over space and time";
    }
    if (/C\(t\)\s*=\s*337\s*\\cdot\s*e\^\{-t\/214\}\s*\+\s*93/.test(source)) {
      return "lifespan coherence over time = 337 * exponential decay over 214 years + 93-year floor";
    }
    if (/C_\{eq\}\s*=\s*\\frac\{O\s*\\cdot\s*G\}\{O\s*\\cdot\s*G\s*\+\s*S\}/.test(source)) {
      return "equilibrium wholeness = (willingness to receive * outside-in restoration force) / (willingness to receive * outside-in restoration force + breakdown pressure)";
    }
    if (/C_1\(t\)\s*=\s*\\bar\{L\}\s*=\s*912\s*\\text\{\s*years\s*\}/.test(source)) {
      return "pre-Flood lifespan pattern = average lifespan = 912 years";
    }
    if (/C_2\(t\)\s*=\s*A\s*\\cdot\s*e\^\{-t\/\\tau_d\}\s*\+\s*L_\{\\text\{floor\}\}/.test(source)) {
      return "post-Flood lifespan pattern = decay amplitude * exponential decay over the decoherence time constant + lifespan floor";
    }
    if (/\\frac\{dC\}\{dt\}\s*=\s*O\s*\\cdot\s*G\(1-C\)\s*-\s*S\s*\\cdot\s*C/.test(source)) {
      return "d(inner wholeness)/dt = willingness to receive * outside-in restoration force * (1 - inner wholeness) - breakdown pressure * inner wholeness";
    }
    if (/C\^\*\s*=\s*\\frac\{O\s*\\cdot\s*G\}\{O\s*\\cdot\s*G\s*\+\s*S\}/.test(source)) {
      return "settled wholeness = (willingness to receive * outside-in restoration force) / (willingness to receive * outside-in restoration force + breakdown pressure)";
    }
    if (/\\frac\{dC\}\{dt\}\s*=\s*\\frac\{\(1\+s\)\}\{2\}\s*\\cdot\s*G\(1-C\)\s*-\s*S\s*\\cdot\s*C/.test(source)) {
      return "d(inner wholeness)/dt = ((1 + direction of the will) / 2) * outside-in restoration force * (1 - inner wholeness) - breakdown pressure * inner wholeness";
    }
    if (/\\frac\{dC\}\{dt\}\s*=\s*0\s*\\cdot\s*G\(1-C\)\s*-\s*S\s*\\cdot\s*C\s*=\s*-S\s*\\cdot\s*C/.test(source)) {
      return "d(inner wholeness)/dt = 0 * outside-in restoration force * (1 - inner wholeness) - breakdown pressure * inner wholeness = -breakdown pressure * inner wholeness";
    }
    if (/\\frac\{dC\}\{dt\}\s*\\approx\s*\\frac\{1\}\{2\}\s*G\(1-C\)\s*-\s*S\s*\\cdot\s*C/.test(source)) {
      return "d(inner wholeness)/dt ~= (1/2) * outside-in restoration force * (1 - inner wholeness) - breakdown pressure * inner wholeness";
    }
    if (/C\^\*_\{perf\}\s*=\s*\\frac\{\\frac\{G\}\{2\}\}\{\\frac\{G\}\{2\}\s*\+\s*S\}\s*=\s*\\frac\{G\}\{G\s*\+\s*2S\}/.test(source)) {
      return "performance-settled wholeness = ((outside-in restoration force / 2) / (outside-in restoration force / 2 + breakdown pressure)) = outside-in restoration force / (outside-in restoration force + 2 * breakdown pressure)";
    }
    if (/\\frac\{dC\}\{dt\}\s*=\s*G\(1-C\)\s*-\s*S\s*\\cdot\s*C/.test(source)) {
      return "d(inner wholeness)/dt = outside-in restoration force * (1 - inner wholeness) - breakdown pressure * inner wholeness";
    }
    if (/C\^\*\s*=\s*\\frac\{G\}\{G\s*\+\s*S\}/.test(source)) {
      return "settled wholeness = outside-in restoration force / (outside-in restoration force + breakdown pressure)";
    }
    if ((/\\chi|\u03c7/.test(source) || terms.some(([symbol]) => symbol === "chi")) && terms.length >= 5) {
      const factorLabels = terms.filter(([symbol]) => symbol !== "chi").map(([, label]) => label);
      const joined = factorLabels.join(" times ");
      return `coherence output = integrated product of (${joined}) across the tested domain`;
    }
    if (/\\int\s*\\chi\s*dV/.test(source)) {
      return "total coherence = coherence output gathered across volume";
    }
    if (hasDerivative) {
      return "rate of change = driving factor times current state";
    }
    if (hasIntegral) {
      const readableTerms = terms.map(([, label]) => label).join(" times ");
      return readableTerms ? `total result = gathered value of (${readableTerms}) across the domain` : "total result = gathered value across the domain";
    }
    if (/\\Delta x/.test(source) && /\\Delta p/.test(source)) {
      return "position uncertainty times momentum uncertainty is at least h bar divided by two";
    }
    if (/G_\{\\mu\\nu\}/.test(source) && /T_\{\\mu\\nu\}/.test(source)) {
      return "spacetime curvature = constant scaling factor times stress energy";
    }
    if (/C\(t\)/.test(source) && /C_\{\\max\}/.test(source)) {
      return "coherence over time = maximum coherence times growth curve times threshold switch";
    }
    return buildSpokenStructure(source);
  }
  function buildEverydayMeaning(source, summary) {
    if (summary && !/Structural translation applied/i.test(summary)) {
      return summary;
    }
    if (/\\chi\s*=/.test(source) && /\\iiint/.test(source)) {
      return "In everyday words: the Master Equation says reality's coherence is built from all ten factors acting together across the whole domain. In this article, the crucial point is that the time term changes when dt appears.";
    }
    if (/C\(t\)\s*=\s*337/.test(source)) {
      return "In everyday words: after the Flood, the lifespan curve falls fast at first, then approaches a floor instead of collapsing to zero.";
    }
    if (/C_\{eq\}|C\^\*/.test(source) && /\\frac/.test(source)) {
      return "In everyday words: the settled level depends on how strongly outside-in restoration outweighs breakdown pressure.";
    }
    if (/C_1\(t\)|C_2\(t\)/.test(source)) {
      return "In everyday words: the article compares a flat pre-Flood pattern with a post-Flood decay curve that approaches a lower floor.";
    }
    if (/\\frac\{dC\}\{dt\}|dCdt|dC\/dt/.test(source)) {
      return "In everyday words: inner wholeness grows when the will is open to outside-in restoration, and decays when breakdown pressure dominates. Grace is not self-generated help; it is the external restoration force that prevents collapse.";
    }
    if (/\\chi|χ/.test(source) && /G/.test(source) && /C/.test(source)) {
      return "In everyday words: the model says total coherence is what results when grace, alignment, truth, entropy accounting, time, Logos, phase lock, faith potential, faith bond, and the Christ factor are considered together across the domain being tested.";
    }
    return "In everyday words: this equation is being restated as a claim about what each symbol contributes to the structure.";
  }
  function attachTranslationCard(state, shell) {
    const document2 = shell.ownerDocument;
    const card = document2.createElement("div");
    card.className = "mtl-card";
    card.dataset.ttsMode = "read-word-equation-and-explanation";
    card.dataset.ttsSpeech = `See the word equation below. ${state.visualEquation}. ${state.everydayMeaning}`;
    const ttsCue = document2.createElement("p");
    ttsCue.className = "mtl-tts-cue";
    ttsCue.textContent = "See the word equation below.";
    card.appendChild(ttsCue);
    const wordCard = document2.createElement("div");
    wordCard.className = "mtl-layer mtl-word-card";
    const label = document2.createElement("div");
    label.className = "mtl-label";
    label.textContent = "Word equation";
    label.setAttribute("aria-hidden", "true");
    wordCard.appendChild(label);
    const structureMarkup = renderStructureMapMarkup(state.source);
    if (structureMarkup) {
      const structure = document2.createElement("div");
      structure.innerHTML = structureMarkup;
      wordCard.appendChild(structure.firstElementChild);
    }
    const wordEquation = document2.createElement("p");
    wordEquation.className = "mtl-word-equation";
    wordEquation.dataset.ttsRole = "word-equation";
    wordEquation.innerHTML = renderWordEquationMarkup(state.visualEquation);
    wordCard.appendChild(wordEquation);
    card.appendChild(wordCard);
    const explanationCard = document2.createElement("div");
    explanationCard.className = "mtl-layer mtl-explanation-card";
    const explanationLabel = document2.createElement("div");
    explanationLabel.className = "mtl-label";
    explanationLabel.textContent = "Everyday translation";
    explanationLabel.setAttribute("aria-hidden", "true");
    explanationCard.appendChild(explanationLabel);
    const meaning = document2.createElement("p");
    meaning.className = "mtl-meaning";
    meaning.dataset.ttsRole = "explanation";
    meaning.textContent = state.everydayMeaning;
    explanationCard.appendChild(meaning);
    if (state.summary && !state.everydayMeaning.includes(state.summary)) {
      const summary = document2.createElement("div");
      summary.className = "mtl-summary";
      summary.textContent = state.summary;
      explanationCard.appendChild(summary);
    }
    card.appendChild(explanationCard);
    shell.appendChild(card);
    state.card = card;
  }
  function enhanceMathElement(element) {
    if (STATE.has(element)) {
      return STATE.get(element);
    }
    const source = extractSource(element);
    if (!source) {
      return void 0;
    }
    const cleanedSource = stripDelimiters(source);
    const document2 = element.ownerDocument;
    const reviewed = findReviewedTranslation(cleanedSource, document2);
    const spoken = translate({
      input: cleanedSource,
      format: "tex",
      dictionary: "theophysics",
      mode: "structural",
      renderer: "tts",
      displayMode: true
    });
    const state = {
      root: element,
      card: element,
      source: cleanedSource,
      spokenStructure: buildSpokenStructure(cleanedSource) || spoken.output,
      visualEquation: reviewedVisualIsReadable(reviewed?.visual) ? reviewed.visual : buildVisualEquation(cleanedSource),
      everydayMeaning: reviewed?.meaning || buildEverydayMeaning(cleanedSource, spoken.summary),
      summary: spoken.summary,
      mode: "translation"
    };
    ensureStyles(document2);
    element.classList.add("mtl-original-equation");
    element.dataset.ttsSkip = "true";
    element.setAttribute("aria-hidden", "true");
    const shell = document2.createElement("div");
    shell.className = "mtl-shell";
    const equationBlock = element.closest(".eq-block, .math-box");
    (equationBlock ?? element).insertAdjacentElement("afterend", shell);
    attachTranslationCard(state, shell);
    setMode(state, "translation");
    element.dataset.mtlSource = cleanedSource;
    STATE.set(element, state);
    return state;
  }
  function enhanceDocument(document2 = window.document) {
    ensureStyles(document2);
    const selected = Array.from(
      document2.querySelectorAll(
        ".eq-block, .equation-block, .equation-block .math, .math-box, .math, .hero-eq, .bx-eq, script[type^='math/tex'], [data-tex], mjx-container"
      )
    ).filter((element, index, array) => array.indexOf(element) === index);
    const elements = selected.filter(
      (element) => !selected.some((candidate) => candidate !== element && candidate.contains(element))
    );
    const states = elements.map((element) => enhanceMathElement(element)).filter((state) => Boolean(state));
    return states;
  }
  if (typeof window !== "undefined" && typeof document !== "undefined") {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", () => {
        enhanceDocument(document);
      });
    } else {
      enhanceDocument(document);
    }
  }
  return __toCommonJS(overlay_exports);
})();
