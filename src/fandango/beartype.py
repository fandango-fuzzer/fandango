def activate_beartype() -> None:
    from beartype.claw import beartype_this_package  # type: ignore [import-not-found]
    from beartype import BeartypeConf  # type: ignore [import-not-found]

    skip_packages = (
        "fandango.converters.antlr.ANTLRv4Parser",  # auto-generated
        "fandango.converters.antlr.ANTLRv4Lexer",  # auto-generated
        "fandango.language.grammar",  # broken
        "fandango.language.symbol",  # broken
        "fandango.language.parser",  # broken
        "fandango.language.search",  # broken, at least test_item_search and test_searches call ItemSearch with non-lists
        "fandango.constraints.fitness",  # ValueFitness sometimes receives a list of ints in the constructor
        "fandango.api",  # at least `parse` is broken
        "fandango.io.packetforecaster",  # broken
    )

    beartype_this_package(conf=BeartypeConf(claw_skip_package_names=skip_packages))
