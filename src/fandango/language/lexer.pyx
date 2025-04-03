from fandango.language.utils.stream import InputStream
from fandango.language.utils.token import CommonToken

cdef int INDENT = 1
cdef int DEDENT = 2
cdef int SPACES = 3
cdef int TAB = 4
cdef int NEWLINE = 5
cdef int STRING = 6
cdef int NUMBER = 7
cdef int INTEGER = 8
cdef int NONTERMINAL = 9
cdef int AND = 10
cdef int OR = 11
cdef int ANY = 12
cdef int ALL = 13
cdef int NOT = 14
cdef int FOR = 15
cdef int IF_ = 16
cdef int ELSE_ = 17
cdef int IS = 18
cdef int PASS = 19
cdef int TRUE = 20
cdef int FALSE = 21

cdef int RULE = 22
cdef int CONSTRAINT = 23
cdef int FITNESS = 24

cdef int STRING_LITERAL = 25
cdef int BYTES_LITERAL = 26

cdef int DECIMAL_INTEGER = 27
cdef int OCT_INTEGER = 28
cdef int HEX_INTEGER = 29
cdef int BIN_INTEGER = 30

cdef int GRAMMAR_ASSIGN = 31
cdef int EXPR_ASSIGN = 32
cdef int COLON = 33
cdef int STAR = 34
cdef int DOUBLE_STAR = 35
cdef int DOT = 36
cdef int LPAREN = 37
cdef int RPAREN = 38
cdef int EQ = 39
cdef int LT = 40
cdef int GT = 41
cdef int LE = 42
cdef int GE = 43
cdef int NE = 44

cdef int UNKNOWN_WORD = 45

cdef class FandangoLexer:
    cdef InputStream _input
    cdef int pos = 0
    cdef list tokens = []
    cdef tuple source

    def __init__(self, InputStream input):
        self._input = input
        self.source = (self, input)

    cdef reset(self):
        self.pos = 0
        self.tokens = []

    cdef start(self):
        """
        The start state for the lexer DFA.
        """
        cdef char c = self._input.LA(self.pos)
        if c == ' ':
            self.spaces()

    cdef spaces(self):
        """
        Consume spaces and return a token.
        """
        cdef int start = self.pos
        while self._input.LA(self.pos) == ' ':
            self.pos += 1
        self.tokens.append(CommonToken(self.source, SPACES, start, self.pos))

    cdef tab(self):
        """
        Consume a tab and return a token.
        """
        cdef int start = self.pos
        self.pos += 1
        self.tokens.append(CommonToken(self.source, TAB, start, self.pos))

    cdef newline(self):
        """
        Consume a newline and return a token.
        """
        cdef int start = self.pos
        self.pos += 1
        self.tokens.append(CommonToken(self.source, NEWLINE, start, self.pos))

    cdef string(self):
        """
        Consume a string and return a token.
        """


