import logging
import os
import sys
import time
import traceback
from typing import Optional, TYPE_CHECKING

from ansi_styles import ansiStyles as styles

if TYPE_CHECKING:
    from fandango.language.tree import DerivationTree
else:
    DerivationTree = object  # needs to be defined for beartype


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
            "  Convert <symbol> to the expected type, say 'str(<symbol>)', 'int(<symbol>)', or 'bytes(<symbol>)'",
            file=sys.stderr,
        )


USE_VISUALIZATION: bool | None = None


def set_visualization(use_visualization: bool | None):
    """Set whether to use visualization while Fandango is running"""
    global USE_VISUALIZATION
    USE_VISUALIZATION = use_visualization


COLUMNS = None
LINES = None


def use_visualization():
    """Return True if we should use visualization while Fandango is running"""
    global COLUMNS, LINES, USE_VISUALIZATION

    if COLUMNS is not None and COLUMNS < 0:
        return False  # We have checked this before

    if USE_VISUALIZATION is not None and not USE_VISUALIZATION:
        return False

    if not USE_VISUALIZATION and LOGGER.isEnabledFor(logging.INFO):
        # Don't want to interfere with logging
        COLUMNS = -1
        return False

    if not USE_VISUALIZATION and "JPY_PARENT_PID" in os.environ:
        # We're within Jupyter Notebook
        COLUMNS = -1
        return False

    if not USE_VISUALIZATION and not sys.stderr.isatty():
        # Output is not a terminal
        COLUMNS = -1
        return False

    if COLUMNS is None:
        try:
            COLUMNS, LINES = os.get_terminal_size()
        except Exception:
            if USE_VISUALIZATION:
                # Assume some reasonable default width
                COLUMNS = 80
            else:
                COLUMNS = -1
                return False

    assert COLUMNS > 0
    return True


LINE_IS_CLEAR = True


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

    global LINE_IS_CLEAR
    LINE_IS_CLEAR = False

    print(f"\r{s}", end="", file=sys.stderr)


def clear_visualization(max_generations: Optional[int] = None):
    """Clear Fandango visualization"""
    if not use_visualization():  # or max_generations is None:
        return

    global LINE_IS_CLEAR
    if LINE_IS_CLEAR:
        return

    time.sleep(0.25)
    assert COLUMNS is not None
    s = " " * (COLUMNS - 1)
    print(f"\r{s}\r", end="", file=sys.stderr)

    LINE_IS_CLEAR = True


def log_message_transfer(
    sender: str,
    receiver: str | None,
    msg: "DerivationTree",
    self_is_sender: bool,
):
    info = sender
    if receiver:
        info += f" -> {receiver}"

    if msg.contains_bits():
        print_msg = str(msg.to_bytes())
    else:
        print_msg = str(msg.value())

    LOGGER.info(f"{info}: {print_msg!r}")
