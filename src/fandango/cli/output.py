import argparse
import ctypes
from io import UnsupportedOperation
import os
import subprocess
import sys
import tempfile
from typing import IO, Any
from fandango.language.tree import DerivationTree
from fandango.logger import LOGGER, clear_visualization


def output(
    tree: DerivationTree, args: argparse.Namespace, file_mode: str
) -> str | bytes:
    assert file_mode == "binary" or file_mode == "text"

    if args.format == "string":
        if file_mode == "binary":
            LOGGER.debug("Output as bytes")
            return tree.to_bytes()
        elif file_mode == "text":
            LOGGER.debug("Output as text")
            return tree.to_string()

    def convert(s: str) -> str | bytes:
        if file_mode == "binary":
            return s.encode("utf-8")
        else:
            return s

    LOGGER.debug(f"Output as {args.format}")

    if args.format == "tree":
        return convert(tree.to_tree())
    if args.format == "repr":
        return convert(tree.to_repr())
    if args.format == "bits":
        return convert(tree.to_bits())
    if args.format == "grammar":
        return convert(tree.to_grammar())
    if args.format == "value":
        return convert(tree.to_value())
    if args.format == "none":
        return convert("")

    raise NotImplementedError("Unsupported output format")


def open_file(filename: str, file_mode: str, *, mode: str = "r") -> IO[Any]:
    assert file_mode == "binary" or file_mode == "text"

    if file_mode == "binary":
        mode += "b"

    LOGGER.debug(f"Opening {filename!r}; mode={mode!r}")

    if filename == "-":
        if "b" in mode:
            return sys.stdin.buffer if "r" in mode else sys.stdout.buffer
        else:
            return sys.stdin if "r" in mode else sys.stdout

    return open(filename, mode)


def output_population(
    population: list[DerivationTree],
    args: argparse.Namespace,
    file_mode: str,
    *,
    output_on_stdout: bool = True,
) -> None:
    if args.format == "none":
        return

    for i, solution in enumerate(population):
        output_solution(solution, args, i, file_mode, output_on_stdout=output_on_stdout)


def output_solution_to_directory(
    solution: DerivationTree,
    args: argparse.Namespace,
    solution_index: int,
    file_mode: str,
) -> None:
    LOGGER.debug(f"Storing solution in directory {args.directory!r}")
    os.makedirs(args.directory, exist_ok=True)

    basename = f"fandango-{solution_index:04d}{args.filename_extension}"
    filename = os.path.join(args.directory, basename)
    with open_file(filename, file_mode, mode="w") as fd:
        fd.write(output(solution, args, file_mode))


def output_solution_to_file(
    solution: DerivationTree,
    args: argparse.Namespace,
    file_mode: str,
) -> None:
    LOGGER.debug(f"Storing solution in file {args.output!r}")
    with open_file(args.output, file_mode, mode="a") as fd:
        try:
            position = fd.tell()
        except (UnsupportedOperation, OSError):
            # If we're writing to stdout, tell() may not be supported
            position = 0

        if position > 0:
            fd.write(
                args.separator.encode("utf-8")
                if file_mode == "binary"
                else args.separator
            )
        fd.write(output(solution, args, file_mode))


def output_solution_with_test_command(
    solution: DerivationTree, args: argparse.Namespace, file_mode: str
) -> None:
    LOGGER.info(f"Running {args.test_command}")
    base_cmd = [args.test_command] + args.test_args

    if args.input_method == "filename":
        prefix = "fandango-"
        suffix = args.filename_extension
        mode = "wb" if file_mode == "binary" else "w"

        # The return type is private, so we need to use Any
        def named_temp_file(*, mode: str, prefix: str, suffix: str) -> Any:
            try:
                # Windows needs delete_on_close=False, so the subprocess can access the file by name
                return tempfile.NamedTemporaryFile(  # type: ignore [call-overload] # the mode type is not available from the library
                    mode=mode,
                    prefix=prefix,
                    suffix=suffix,
                    delete_on_close=False,
                )
            except Exception:
                # Python 3.11 and earlier have no 'delete_on_close'
                return tempfile.NamedTemporaryFile(
                    mode=mode, prefix=prefix, suffix=suffix
                )

        with named_temp_file(mode=mode, prefix=prefix, suffix=suffix) as fd:
            fd.write(output(solution, args, file_mode))
            fd.flush()
            cmd = base_cmd + [fd.name]
            LOGGER.debug(f"Running {cmd}")
            subprocess.run(cmd, text=True)
    elif args.input_method == "stdin":
        cmd = base_cmd
        LOGGER.debug(f"Running {cmd} with individual as stdin")
        subprocess.run(
            cmd,
            input=output(solution, args, file_mode),
            text=(None if file_mode == "binary" else True),
        )
    elif args.input_method == "libfuzzer":
        if args.file_mode != "binary" or file_mode != "binary":
            raise NotImplementedError("LibFuzzer harnesses only support binary input")
        harness = ctypes.CDLL(args.test_command).LLVMFuzzerTestOneInput

        bytes = output(solution, args, file_mode)
        harness(bytes, len(bytes))
    else:
        raise NotImplementedError("Unsupported input method")


def output_solution_to_stdout(
    solution: DerivationTree,
    args: argparse.Namespace,
    file_mode: str,
) -> None:
    LOGGER.debug("Printing solution on stdout")
    out = output(solution, args, file_mode)
    if not isinstance(out, str):
        out = out.decode("iso8859-1")
    print(out, end="")
    print(args.separator, end="")


def output_solution(
    solution: DerivationTree,
    args: argparse.Namespace,
    solution_index: int,
    file_mode: str,
    *,
    output_on_stdout: bool = True,
) -> None:
    assert file_mode == "binary" or file_mode == "text"

    if args.format == "none":
        return
    if "output" not in args:
        return

    if args.directory:
        output_solution_to_directory(solution, args, solution_index, file_mode)
        output_on_stdout = False

    if args.output:
        output_solution_to_file(solution, args, file_mode)
        output_on_stdout = False

    if "test_command" in args and args.test_command:
        output_solution_with_test_command(solution, args, file_mode)
        output_on_stdout = False

    # Default
    if output_on_stdout:
        clear_visualization()
        output_solution_to_stdout(solution, args, file_mode)
