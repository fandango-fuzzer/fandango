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

The Fandango project includes a simple language server that makes writing Fandango grammars significantly easier. Currently, it supports the following:
- Autocomplete of nonterminals
- Jump to definition of nonterminal
- Find all references of nonterminal
- Rename nonterminal
- Create a definition for an undefined nonterminal
- Initial Semantic Token support

```{admonition} Under Construction
:class: attention
The language server is experimental.
```

Download or clone the [Fandango source repository](https://github.com/fandango-fuzzer/fandango).

Start the language server by running

```shell
$ python3 src/fandango/language/server/language_server.py
```

## Visual Studio Code Extension

A simple extension for Visual Studio Code (based on the one provided by the `pygls` project) is provided in the source repository in `.vscode/extensions/fandango-language-server`. To use it, clone the source repository, and compile it by running the following:

```shell
$ cd .vscode/extensions/fandango-language-server
$ npm install --no-save
$ npm run compile
```

You can then install it from the workspace-recommended extension section in the extension manager. The extension will automatically start the language server and interface with it once you start editing `.fan` files in this workspace. For additional documentation, refer to `.vscode/extensions/fandango-language-server/README.md`.


## IntelliJ / Pycharm Code Extension

To integrate the Fandango language server into IntelliJ or PyCharm, follow these steps:

1. Download and install the [LSP4IJ plugin](https://plugins.jetbrains.com/plugin/23257-lsp4ij) for IntelliJ / Pycharm.
2. Download the [Fandango LSP4J Language Server configuration](lsp4ij-fandangospec.zip).
3. In your IDE, navigate to the `Language Servers` tab.
4. Click the `+` button or right-click an empty area in the list to add a new language server.
5. In the `Add New Language Server` popup:
   1. For `Template`, select `Import from custom template...`
   2. A file browser will appear. Select the previously downloaded language server configuration.
   3. If necessary, adjust the command in the Server tab to ensure the correct Python executable is used (matching your desired Python version and virtual environment).

The extension will automatically start and interface with the language server.


## Running the Language Server Manually

To manually run the language server, run the following Python script:

```shell
$ python3 [fandango-source-repository]/src/fandango/language/server/language_server.py
```