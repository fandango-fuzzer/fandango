import logging
from typing import Optional

from pygls.lsp.server import LanguageServer
import lsprotocol.types as lsp
from antlr4 import InputStream, Token

from fandango.language.parser.FandangoLexer import FandangoLexer
from fandango.language.server.semantic_tokens import (
    SemanticTokenModifiers,
    SemanticTokenTypes,
)

logger = logging.getLogger(__name__)


def map_to_ranges(references: list[Token], uri: str):
    def mapper(t: Token):
        assert isinstance(t.line, int), f"Token {t} has no line"
        assert isinstance(t.column, int), f"Token {t} has no column"
        return lsp.Range(
            start=lsp.Position(line=t.line - 1, character=t.column),
            end=lsp.Position(line=t.line - 1, character=t.column + len(t.text)),
        )

    return list(map(mapper, references))


def map_to_locations(references: list[Token], uri: str):
    return [lsp.Location(uri, range) for range in map_to_ranges(references, uri)]


class FileAssets:
    def __init__(self, lexer: FandangoLexer):
        self.tokens: list[Token] = lexer.getAllTokens()


class FandangoLanguageServer(LanguageServer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.files: dict[str, FileAssets] = {}

    def parse(self, uri: str):
        document = self.workspace.get_text_document(uri)
        document_text = document.source
        lexer = FandangoLexer(InputStream(document_text))
        self.files[document.uri] = FileAssets(lexer)

    def get_file_assets(self, document: lsp.TextDocumentIdentifier):
        return self.files[document.uri]

    def get_nonterminals(self, document: lsp.TextDocumentIdentifier):
        tokens = self.get_file_assets(document).tokens
        nonterminals = [t for t in tokens if t.type == FandangoLexer.NAME]
        return nonterminals

    def get_references(
        self,
        document: lsp.TextDocumentIdentifier,
        position: lsp.Position,
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
    ls.parse(params.text_document.uri)


@server.feature(lsp.TEXT_DOCUMENT_DID_CHANGE)
def did_change(ls: FandangoLanguageServer, params: lsp.DidChangeTextDocumentParams):
    """Parse each document when it is changed"""
    ls.parse(params.text_document.uri)


# COMPLETION
@server.feature(
    lsp.TEXT_DOCUMENT_COMPLETION,
    lsp.CompletionOptions(trigger_characters=["<"], all_commit_characters=[">"]),
)
def completions(params: Optional[lsp.CompletionParams] = None) -> lsp.CompletionList:
    """Returns completion items."""
    if params is None:
        raise ValueError("params must not be None")

    texts = set(t.text for t in server.get_nonterminals(params.text_document))
    items = [lsp.CompletionItem(label=f"<{t}>", insert_text=f"{t}>") for t in texts]

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
        is_definition = False
        # continue until either newline (is not definition) or grammar assign (is definition)
        for i in range(tokens_i, len(tokens)):
            if tokens[i].type == FandangoLexer.NEWLINE:
                break
            elif tokens[i].type == FandangoLexer.GRAMMAR_ASSIGN:
                is_definition = True
                break

        if is_definition:
            return map_to_locations(
                [tokens[tokens_i]],
                params.text_document.uri,
            )[0]


@server.feature(lsp.TEXT_DOCUMENT_RENAME)
def rename(ls: FandangoLanguageServer, params: lsp.RenameParams):
    """Rename the symbol at the given position."""

    references = ls.get_references(params.text_document, params.position)
    edits = [
        lsp.TextEdit(range=range, new_text=params.new_name)
        for range in map_to_ranges(references, params.text_document.uri)
    ]

    return lsp.WorkspaceEdit(changes={params.text_document.uri: edits})


@server.feature(lsp.TEXT_DOCUMENT_PREPARE_RENAME)
def prepare_rename(ls: FandangoLanguageServer, params: lsp.PrepareRenameParams):
    """Called by the client to determine if renaming the symbol at the given location
    is a valid operation."""

    if len(ls.get_references(params.text_document, params.position)) == 0:
        return None

    return lsp.PrepareRenameDefaultBehavior(default_behavior=True)


@server.feature(
    lsp.TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL,
    lsp.SemanticTokensLegend(
        token_types=SemanticTokenTypes.values(),
        token_modifiers=SemanticTokenModifiers.values(),
    ),
)
def semantic_tokens_full(ls: FandangoLanguageServer, params: lsp.SemanticTokensParams):
    tokens = ls.get_file_assets(params.text_document).tokens

    output = []
    prev_line = 0
    prev_col = 0

    for t in tokens:
        line = t.line - 1
        col = t.column

        delta_line = line - prev_line
        delta_start = col - prev_col if delta_line == 0 else col

        output.extend(
            [
                delta_line,
                delta_start,
                len(t.text),
                SemanticTokenTypes.from_token_as_number(t),
                SemanticTokenModifiers.from_token_as_number(t),
            ]
        )

        prev_line = line
        prev_col = col

    return lsp.SemanticTokens(data=output)


@server.feature(
    lsp.TEXT_DOCUMENT_CODE_ACTION,
    lsp.CodeActionOptions(code_action_kinds=[lsp.CodeActionKind.QuickFix]),
)
def code_actions(params: lsp.CodeActionParams):
    if (
        params.range.start.line != params.range.end.line
        or params.range.start.character != params.range.end.character
    ):
        return []  # ignore selections for now

    line = params.range.start.line
    column = params.range.start.character

    tokens = server.get_file_assets(params.text_document).tokens

    current_token = next(
        (
            t
            for t in tokens
            if t.line - 1 == line
            and t.column <= column
            and t.column + len(t.text) >= column
        ),
        None,
    )

    if current_token is None:
        return []

    defined_tokens = set()
    for i, t in enumerate(tokens):
        if t.type != FandangoLexer.GRAMMAR_ASSIGN:
            continue
        non_terminals = [nt for nt in tokens[i:0:-1] if nt.type == FandangoLexer.NAME]
        if len(non_terminals) == 0:
            continue
        defined_tokens.add(non_terminals[0].text)

    if current_token.text in defined_tokens:
        return []

    position = lsp.Position(line=current_token.line, character=0)
    range = lsp.Range(start=position, end=position)  # start == end means insert
    text_edit = lsp.TextEdit(
        range=range,
        new_text=f"<{current_token.text}> ::= # TODO: Implement\n",
    )

    return [
        lsp.CodeAction(
            title=f"Add definition for '{t.text}'",
            kind=lsp.CodeActionKind.QuickFix,
            edit=lsp.WorkspaceEdit(
                changes={params.text_document.uri: [text_edit]},
            ),
        )
    ]


if __name__ == "__main__":
    server.start_io()
