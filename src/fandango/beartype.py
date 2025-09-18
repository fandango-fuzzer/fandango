def activate_beartype() -> None:
    from beartype.claw import beartype_this_package
    from beartype import BeartypeConf

    skip_packages = (
        "fandango.converters.antlr.ANTLRv4Parser",  # auto-generated
        "fandango.converters.antlr.ANTLRv4Lexer",  # auto-generated
        "fandango.language.parser",  # broken
    )

    beartype_this_package(conf=BeartypeConf(claw_skip_package_names=skip_packages))
