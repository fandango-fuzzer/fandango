def _is_fandango_editable_redirect_finder(finder: object) -> bool:
    """True for this package's scikit-build-core redirect editable finder only."""
    if type(finder).__name__ != "ScikitBuildRedirectingFinder":
        return False
    return "fandango" in getattr(finder, "pkgs", ())


def activate_beartype() -> None:
    import sys

    from beartype import BeartypeConf
    from beartype.claw import beartype_this_package

    # scikit-build-core's redirect editable finder loads modules in a way that
    # bypasses beartype.claw; drop ours so normal imports from src/ work (#556).
    sys.meta_path[:] = [
        finder
        for finder in sys.meta_path
        if not _is_fandango_editable_redirect_finder(finder)
    ]

    skip_packages = (
        "fandango.language.grammar.grammar",  # GrammarProcessor sometimes passes searches instead of NonTerminalNodes to Grammar.set_generator
        "fandango.language.grammar.literal_generator",  # The above is then passed to the constructor of LiteralGenerator
        "fandango.converters.dtd.DTDFandangoConverter",  # the type seems wrong
        "fandango.converters.antlr.ANTLRv4Parser",  # auto-generated
        "fandango.converters.antlr.ANTLRv4Lexer",  # auto-generated
        "fandango.language.parser.FandangoLexer",  # auto-generated
        "fandango.language.parser.FandangoParser",  # auto-generated
        "fandango.language.parser.FandangoParserVisitor",  # auto-generated
        "fandango.language.parser.sa_fandango",  # auto-generated
    )

    beartype_this_package(conf=BeartypeConf(claw_skip_package_names=skip_packages))
