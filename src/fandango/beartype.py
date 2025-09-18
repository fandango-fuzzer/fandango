def activate_beartype() -> None:
    from beartype.claw import beartype_this_package
    from beartype import BeartypeConf

    skip_packages = (
        "fandango.converters.antlr.ANTLRv4Parser",  # auto-generated
        "fandango.converters.antlr.ANTLRv4Lexer",  # auto-generated
        "fandango.language.parser.FandangoLexer",  # auto-generated
        "fandango.language.parser.FandangoParser",  # auto-generated
        "fandango.language.parser.FandangoParserVisitor",  # auto-generated
        "fandango.language.parser.sa_fandango",  # auto-generated
    )

    beartype_this_package(conf=BeartypeConf(claw_skip_package_names=skip_packages))
