import logging
import os
import sys
import time
import traceback
from typing import Optional

from ansi_styles import ansiStyles as styles

LOGGER = logging.getLogger("fandango")
logging.basicConfig(
    level=logging.WARNING,
    format="%(name)s:%(levelname)s: %(message)s",
)


def print_exception(e: Exception, exception_note: str | None = None):
    if exception_note is not None and getattr(Exception, "add_note", None):
        # Python 3.11+ has add_note() method
        e.add_note(exception_note)
        exception_note = None

    if LOGGER.isEnabledFor(logging.INFO):
        LOGGER.info(traceback.format_exc().rstrip())
    else:
        print(type(e).__name__ + ":", e, file=sys.stderr)
        for note in getattr(e, "__notes__", []):
            print("  " + note, file=sys.stderr)

    if exception_note:
        print("  " + exception_note, file=sys.stderr)

    if "DerivationTree" in str(e):
        print(
            "  Convert <symbol> to the expected type, say 'str(<symbol>)', 'int(<symbol>)', or 'float(<symbol>)'",
            file=sys.stderr,
        )


COLUMNS = None
LINES = None


def use_visualization():
    """Return True if we should use visualization while Fandango is running"""
    global COLUMNS, LINES
    if COLUMNS is not None and COLUMNS < 0:
        return False  # No terminal

    if LOGGER.isEnabledFor(logging.INFO):
        # Don't want to interfere with logging
        COLUMNS = -1
        return False

    if "JPY_PARENT_PID" in os.environ:
        # We're within Jupyter Notebook
        COLUMNS = -1
        return False

    if not sys.stderr.isatty():
        # Output is not a terminal
        COLUMNS = -1
        return False

    if COLUMNS is None:
        try:
            COLUMNS, LINES = os.get_terminal_size()
        except Exception:
            COLUMNS = -1
            return False

    assert COLUMNS > 0
    return True


def visualize_evaluation(
    generation: int,
    max_generations: Optional[int],
    evaluation: list[tuple],
):
    """Visualize current evolution while Fandango is running"""
    if not use_visualization() or max_generations is None:
        return

    fitnesses = [fitness for _ind, fitness, _failing_trees in evaluation]
    fitnesses.sort(reverse=True)
    assert COLUMNS is not None
    columns = COLUMNS
    s = f"💃 {styles.color.ansi256(styles.rgbToAnsi256(128, 0, 0))}Fandango {styles.color.close} {generation}/{max_generations} "
    columns -= len(f"   Fandango {generation}/{max_generations} ") + 1
    columns = int(columns / 3.0)
    for column in range(0, columns):
        individual = int(column / columns * len(fitnesses))
        fitness = fitnesses[individual]

        if fitness <= 0.01:
            red, green, blue = 127, 127, 127
        else:
            red = int((1.0 - fitness) * 255)
            green = int(fitness * 255)
            blue = 0

        s += styles.bgColor.ansi256(styles.rgbToAnsi256(red, green, blue))
        s += "   "
        s += styles.bgColor.close

    print(f"\r{s}", end="", file=sys.stderr)
    return


def clear_visualization(max_generations: Optional[int] = None):
    """Clear Fandango visualization"""
    if not use_visualization() or max_generations is None:
        return

    time.sleep(0.5)
    assert COLUMNS is not None
    s = " " * (COLUMNS - 1)
    print(f"\r{s}\r", end="", file=sys.stderr)


def log_message_transfer(
    sender: str,
    receiver: str | None,
    msg,
    self_is_sender: bool,
):
    info = sender
    if receiver:
        info += f" -> {receiver}"

    LOGGER.info(f"{info}: {msg.value()!r}")
