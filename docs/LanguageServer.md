---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

(sec:language-server)=
# Fandango Language Server

The Fandango project includes a simple language server that makes writing Fandango grammars significantly easier. Currently, it supports:
- Autocompletion of nonterminals
- Jump to definition
- Find all references

Start the language server by running

```bash
python3 src/fandango/language/server/language_server.py
```

## Visual Studio Code Extension

A simple extension for Visual Studio Code (based on the one provided by the `pygls` project) is provided in `.vscode/extensions/fandango-language-server`. To compile it, run the following:

```bash
cd .vscode/extensions/fandango-language-server
npm install --no-save
npm run compile
```

You can then install it from the workspace-recommended extension section in the extension manager. For additional documentation, refer to `.vscode/extensions/fandango-language-server/README.md`.