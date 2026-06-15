#!/usr/bin/env node
"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.runCli = runCli;
const fs_1 = __importDefault(require("fs"));
const path_1 = __importDefault(require("path"));
const core_1 = require("../core");
const dictionaries_1 = require("../dictionaries");
function normalizeLatex(source) {
    return source
        .replace(/^\$\$/, "")
        .replace(/\$\$$/, "")
        .replace(/^\$/, "")
        .replace(/\$$/, "")
        .replace(/^\\\[/, "")
        .replace(/\\\]$/, "")
        .replace(/^\\\(/, "")
        .replace(/\\\)$/, "")
        .trim();
}
function readOption(args, name) {
    const index = args.indexOf(name);
    if (index === -1 || index === args.length - 1) {
        return undefined;
    }
    return args[index + 1];
}
function hasFlag(args, name) {
    return args.includes(name);
}
function collectFiles(targetPath) {
    const stat = fs_1.default.statSync(targetPath);
    if (stat.isFile()) {
        return [targetPath];
    }
    const files = [];
    for (const entry of fs_1.default.readdirSync(targetPath)) {
        const fullPath = path_1.default.join(targetPath, entry);
        const entryStat = fs_1.default.statSync(fullPath);
        if (entryStat.isDirectory()) {
            files.push(...collectFiles(fullPath));
            continue;
        }
        if (/\.(html|md|markdown|tex|txt)$/i.test(fullPath)) {
            files.push(fullPath);
        }
    }
    return files;
}
function renderReport(report, format) {
    if (format === "json") {
        return JSON.stringify(report, null, 2);
    }
    const lines = [];
    for (const item of report) {
        lines.push(`${item.file}`);
        lines.push(`  Found: ${item.found}`);
        lines.push(`  Translated: ${item.translated}`);
        lines.push(`  Unmapped: ${item.unmapped.length}`);
        if (item.unmapped.length > 0) {
            lines.push(`  Missing: ${item.unmapped.join(" | ")}`);
        }
    }
    return lines.join("\n");
}
async function handleTranslate(args, io) {
    const inline = readOption(args, "--input");
    const file = readOption(args, "--file");
    const format = (readOption(args, "--input-format") ?? "tex");
    const dictionary = readOption(args, "--dictionary") ?? "theophysics";
    const mode = (readOption(args, "--mode") ?? "structural");
    const outputFormat = readOption(args, "--output-format");
    const renderer = (readOption(args, "--renderer") ?? (mode === "narrative" ? "plaintext" : "latex-structural"));
    const outputPath = readOption(args, "--output");
    const input = inline ?? (file ? fs_1.default.readFileSync(file, "utf8") : "");
    if (!input) {
        io.stderr("No input provided. Use --input or --file.");
        return 1;
    }
    const normalizedInput = normalizeLatex(input);
    if (outputFormat === "full") {
        const result = await (0, core_1.translateEquation)(normalizedInput, {
            format,
            dictionary,
            enableFallback: true,
            displayMode: hasFlag(args, "--display")
        });
        const rendered = [
            "=== ORIGINAL ===",
            result.original,
            "",
            "=== WORD EQUATION ===",
            result.wordEquation,
            "",
            "=== EXPLANATION ===",
            result.spokenExplanation,
            "",
            "=== METADATA ===",
            `Confidence: ${result.confidence.toFixed(2)}`,
            `Used Fallback: ${result.usedFallback}`,
            result.diagnostics.length > 0 ? `Diagnostics: ${result.diagnostics.join(" | ")}` : "Diagnostics: none"
        ].join("\n");
        if (outputPath) {
            fs_1.default.writeFileSync(outputPath, rendered, "utf8");
        }
        else {
            io.stdout(rendered);
        }
        return 0;
    }
    const result = (0, core_1.translate)({
        input: normalizedInput,
        format,
        dictionary,
        mode,
        renderer,
        displayMode: hasFlag(args, "--display")
    });
    if (outputPath) {
        fs_1.default.writeFileSync(outputPath, result.output, "utf8");
    }
    else {
        io.stdout(result.output);
    }
    return 0;
}
async function handleDictionary(args, io) {
    const subcommand = args[1] ?? "list";
    if (subcommand === "list") {
        io.stdout(JSON.stringify((0, dictionaries_1.listDictionaries)(), null, 2));
        return 0;
    }
    if (subcommand === "inspect") {
        const dictionary = readOption(args, "--dictionary") ?? "theophysics";
        io.stdout(JSON.stringify((0, dictionaries_1.loadDictionary)(dictionary).data, null, 2));
        return 0;
    }
    io.stderr(`Unknown dictionary subcommand: ${subcommand}`);
    return 1;
}
async function handleScan(args, io) {
    const targetPath = readOption(args, "--path");
    if (!targetPath) {
        io.stderr("Missing --path for scan command.");
        return 1;
    }
    const dictionary = readOption(args, "--dictionary") ?? "theophysics";
    const mode = (readOption(args, "--mode") ?? "structural");
    const renderer = (readOption(args, "--renderer") ?? "latex-structural");
    const reportFormat = (readOption(args, "--report") ?? "text");
    const outputPath = readOption(args, "--output");
    const report = [];
    for (const file of collectFiles(targetPath)) {
        const content = fs_1.default.readFileSync(file, "utf8");
        const blocks = (0, core_1.extractMathBlocks)(content);
        const fileReport = {
            file,
            found: blocks.length,
            translated: 0,
            unmapped: []
        };
        for (const block of blocks) {
            const result = (0, core_1.translate)({
                input: normalizeLatex(block.latex),
                format: "tex",
                dictionary,
                mode,
                renderer,
                displayMode: block.isBlock
            });
            const isUnmapped = result.diagnostics.some((diagnostic) => diagnostic.type === "unmapped");
            if (!isUnmapped) {
                fileReport.translated += 1;
            }
            else {
                fileReport.unmapped.push(block.latex);
            }
        }
        report.push(fileReport);
    }
    const rendered = renderReport(report, reportFormat);
    if (outputPath) {
        fs_1.default.writeFileSync(outputPath, rendered, "utf8");
    }
    else {
        io.stdout(rendered);
    }
    return 0;
}
async function runCli(argv, io) {
    const sink = io ?? {
        stdout(message) {
            process.stdout.write(`${message}\n`);
        },
        stderr(message) {
            process.stderr.write(`${message}\n`);
        }
    };
    const [command = "translate"] = argv;
    if (command === "translate") {
        return handleTranslate(argv.slice(1), sink);
    }
    if (command === "scan") {
        return handleScan(argv.slice(1), sink);
    }
    if (command === "dictionary") {
        return handleDictionary(argv.slice(1), sink);
    }
    sink.stderr(`Unknown command: ${command}`);
    return 1;
}
if (require.main === module) {
    runCli(process.argv.slice(2)).then((code) => {
        process.exitCode = code;
    });
}
