"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.listDictionaries = listDictionaries;
exports.loadDictionary = loadDictionary;
const theophysics_json_1 = __importDefault(require("./theophysics.json"));
const theophysics_hooks_1 = require("./theophysics.hooks");
const REGISTRY = {
    theophysics: {
        data: theophysics_json_1.default,
        hooks: theophysics_hooks_1.theophysicsHooks
    }
};
function listDictionaries() {
    return Object.values(REGISTRY).map(({ data }) => ({
        id: data.metadata.id,
        name: data.metadata.name,
        version: data.metadata.version
    }));
}
function loadDictionary(id) {
    const dictionary = REGISTRY[id];
    if (!dictionary) {
        throw new Error(`Unknown dictionary: ${id}`);
    }
    return dictionary;
}
