import subprocess

if __name__ == "__main__":
    subprocess.run(
        [
            "antlr",
            "-Dlanguage=Python3",
            "-o",
            "../src/fandango/language/parser",
            "-visitor",
            "-listener",
            "FandangoLexer.g4",
            "FandangoParser.g4",
        ],
        cwd="language",
    )
    subprocess.run(["black", "src"])