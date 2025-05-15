from antlr4 import InputStream, Token
from pygls.server import LanguageServer
import lsprotocol.types as lsp
from typing import Dict, Optional, List
import logging
from fandango.language.parser.FandangoLexer import FandangoLexer

logger = logging.getLogger(__name__)


def map_to_locations(references: List[Token], uri: str):
    locations = [
        lsp.Location(
            uri=uri,
            range=lsp.Range(
                start=lsp.Position(line=t.line - 1, character=t.column),
                end=lsp.Position(line=t.line - 1, character=t.column + len(t.text)),
            ),
        )
        for t in references
    ]

    return locations


class FileAssets:
    def __init__(self, lexer: FandangoLexer):
        self.tokens = lexer.getAllTokens()


class FandangoLanguageServer(LanguageServer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.files: Dict[str, FileAssets] = {}

    def get_text_document(self, document: lsp.VersionedTextDocumentIdentifier):
        return self.workspace.get_text_document(document.uri)

    def parse(self, document: lsp.VersionedTextDocumentIdentifier):
        document_text = self.get_text_document(document).source
        lexer = FandangoLexer(InputStream(document_text))
        self.files[document.uri] = FileAssets(lexer)

    def get_file_assets(self, document: lsp.VersionedTextDocumentIdentifier):
        return self.files[document.uri]

    def get_nonterminals(self, document: lsp.VersionedTextDocumentIdentifier):
        tokens = self.get_file_assets(document).tokens
        nonterminals = [t for t in tokens if t.type == FandangoLexer.NONTERMINAL]
        return nonterminals

    def get_references(
        self, document: lsp.VersionedTextDocumentIdentifier, position: lsp.Position
    ):
        non_terminals = self.get_nonterminals(document)
        current_token = [
            t
            for t in non_terminals
            if t.line == position.line + 1
            and t.column <= position.character
            and t.column + len(t.text) >= position.character
        ]

        references = [
            t for t in non_terminals if t.text in [ct.text for ct in current_token]
        ]

        return references


server = FandangoLanguageServer("fandango-language-server", "v0.1")


@server.feature(lsp.TEXT_DOCUMENT_DID_OPEN)
def did_open(ls: FandangoLanguageServer, params: lsp.DidOpenTextDocumentParams):
    """Parse each document when it is opened"""
    ls.parse(params.text_document)


@server.feature(lsp.TEXT_DOCUMENT_DID_CHANGE)
def did_change(ls: FandangoLanguageServer, params: lsp.DidChangeTextDocumentParams):
    """Parse each document when it is changed"""
    ls.parse(params.text_document)


# COMPLETION
@server.feature(
    lsp.TEXT_DOCUMENT_COMPLETION,
    lsp.CompletionOptions(trigger_characters=["<"], all_commit_characters=[">"]),
)
def completions(params: Optional[lsp.CompletionParams] = None) -> lsp.CompletionList:
    """Returns completion items."""

    items = [
        lsp.CompletionItem(label=t.text, insert_text=t.text[1:])
        for t in server.get_nonterminals(params.text_document)
    ]

    return lsp.CompletionList(is_incomplete=False, items=items)


@server.feature(lsp.TEXT_DOCUMENT_REFERENCES)
def find_references(server: FandangoLanguageServer, params: lsp.ReferenceParams):
    """Find references of an object."""

    return map_to_locations(
        server.get_references(params.text_document, params.position),
        params.text_document.uri,
    )


@server.feature(lsp.TEXT_DOCUMENT_DEFINITION)
def goto_definition(server: FandangoLanguageServer, params: lsp.DefinitionParams):
    """Jump to an object's definition."""

    tokens = server.get_file_assets(params.text_document).tokens
    references = server.get_references(params.text_document, params.position)

    for r in references:
        tokens_i = tokens.index(r)

        next_grammar_assign_i = [
            i + tokens_i
            for i, t in enumerate(tokens[tokens_i:])
            if t.type == FandangoLexer.GRAMMAR_ASSIGN
        ]

        if len(next_grammar_assign_i) == 0:  # no definition after the nonterminal
            continue
        next_grammar_assign_i = next_grammar_assign_i[0]

        diff = tokens[tokens_i + 1 : next_grammar_assign_i]

        if all(t.type == FandangoLexer.SKIP_ for t in diff):
            return map_to_locations(
                [r],
                params.text_document.uri,
            )[0]


if __name__ == "__main__":
    server.start_io()
