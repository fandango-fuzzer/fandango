# from https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#semanticTokenTypes

import enum

from antlr4 import Token


class SemanticTokenTypes(enum.Enum):
    namespace = "namespace"
    # /**
    #  * Represents a generic type. Acts as a fallback for types which
    #  * can't be mapped to a specific type like class or enum.
    #  */
    type = "type"
    _class = "class"
    enum = "enum"
    interface = "interface"
    struct = "struct"
    typeParameter = "typeParameter"
    parameter = "parameter"
    variable = "variable"
    property = "property"
    enumMember = "enumMember"
    event = "event"
    function = "function"
    method = "method"
    macro = "macro"
    keyword = "keyword"
    modifier = "modifier"
    comment = "comment"
    string = "string"
    number = "number"
    regexp = "regexp"
    operator = "operator"
    decorator = "decorator"

    @classmethod
    def values(cls) -> list[str]:
        """Get the values of the semantic token types.

        :return: The values of the semantic token types
        """
        return [e.value for e in cls]

    @classmethod
    def from_token(cls, token: Token) -> "SemanticTokenTypes":
        """Get the semantic token type for a given token.

        :param token: The token to get the semantic token type for
        :return: The semantic token type
        """
        match token.type:
            case "NAME":
                return SemanticTokenTypes.variable
            case "STRING_LITERAL" | "BYTES_LITERAL":
                return SemanticTokenTypes.string
            case (
                "DECIMAL_INTEGER"
                | "OCT_INTEGER"
                | "HEX_INTEGER"
                | "BIN_INTEGER"
                | "FLOAT_NUMBER"
                | "IMAG_NUMBER"
            ):
                return SemanticTokenTypes.number
            case "GRAMMAR_ASSIGN" | "EXPR_ASSIGN" | "OR_OP":
                return SemanticTokenTypes.operator
            case "SKIP_":
                return SemanticTokenTypes.comment
            case _:
                return SemanticTokenTypes.type

    @classmethod
    def from_token_as_number(cls, token: Token) -> int:
        """Get the zero-based index of an enum member in its enum class.

        :param token: The token to get the index for
        :return: The zero-based index of the enum member
        """
        return get_enum_index(cls.from_token(token))


class SemanticTokenModifiers(enum.Enum):
    declaration = "declaration"
    definition = "definition"
    readonly = "readonly"
    static = "static"
    deprecated = "deprecated"
    abstract = "abstract"
    _async = "async"
    modification = "modification"
    documentation = "documentation"
    defaultLibrary = "defaultLibrary"

    @classmethod
    def values(cls) -> list[str]:
        """Get the values of the semantic token modifiers.

        :return: The values of the semantic token modifiers
        """
        return [e.value for e in cls]

    @classmethod
    def from_token(cls, token: Token) -> list["SemanticTokenModifiers"]:
        """Get the semantic token modifiers for a given token.

        :param token: The token to get the semantic token modifiers for
        :return: The semantic token modifiers
        """
        return []  # not currently implemented

    @classmethod
    def from_token_as_number(cls, token: Token) -> int:
        """
        Get the bitmask of the semantic token modifiers for a given token.

        The bitmask is the result of XORing together the indices of the enum members in the enum class.

        :param token: The token to get the index for
        :return: The zero-based index of the enum member
        """
        ints = [get_enum_index(m) for m in cls.from_token(token)]
        res = 0
        for i in ints:
            res |= 1 << i
        return res


def get_enum_index(enum_member: enum.Enum) -> int:
    """Get the zero-based index of an enum member in its enum class.

    :param enum_member: The enum member to get the index for
    :return: The zero-based index of the enum member
    """
    return list(type(enum_member)).index(enum_member)
