class FandangoError(ValueError):
    """Generic Error"""

    pass


class FandangoParseError(FandangoError, SyntaxError):
    """Error during parsing inputs"""

    def __init__(self, message: str | None = None, position: int | None = None):
        if message is None:
            if position is not None:
                message = f"Parse error at position {position}"
            else:
                message = "Parse error"

        # Call the parent class constructors
        FandangoError.__init__(self, message)
        SyntaxError.__init__(self, message)
        self.position = position


class FandangoSyntaxError(FandangoError, SyntaxError):
    """Error during parsing a Fandango spec"""

    def __init__(self, message: str):
        FandangoError.__init__(self, message)
        SyntaxError.__init__(self, message)


class FandangoValueError(FandangoError, ValueError):
    """Error during evaluating a Fandango spec"""

    def __init__(self, message: str):
        FandangoError.__init__(self, message)
        ValueError.__init__(self, message)


class FandangoFailedError(FandangoError):
    """Error during the Fandango algorithm"""

    def __init__(self, message: str):
        super().__init__(self, message)
