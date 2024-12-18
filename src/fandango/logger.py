import logging
import traceback
import sys
import os
import time
from ansi_styles import ansiStyles as styles

LOGGER = logging.getLogger("fandango")
logging.basicConfig(
    level=logging.INFO,
    format="%(name)s:%(levelname)s: %(message)s",
)


def print_exception(e: Exception):
    LOGGER.info(traceback.format_exc().rstrip())
    if not LOGGER.isEnabledFor(logging.INFO):
        print(type(e).__name__ + ":", e, file=sys.stderr)
    if "DerivationTree" in str(e):
        print(
            "Convert <symbol> to the expected type, say 'str(<symbol>)', 'int(<symbol>)', or 'float(<symbol>)'"
        )


COLUMNS = None
LINES = None


def use_visualization():
    """Return True if we should use visualization while Fandango is running"""
    global COLUMNS, LINES
    if COLUMNS is not None and COLUMNS < 0:
        return False  # No terminal

    if not sys.stderr.isatty():
        COLUMNS = -1
        return False  # No terminal

    if LOGGER.isEnabledFor(logging.INFO):
        COLUMNS = -1
        return False  # Don't want to interfere with logging

    if COLUMNS is None:
        try:
            COLUMNS, LINES = os.get_terminal_size()
        except Exception:
            COLUMNS = -1
            return False

    assert COLUMNS > 0
    return True


def visualize_evaluation(generation, max_generations, evaluation):
    """Visualize current evolution while Fandango is running"""
    if not use_visualization():
        return

    fitnesses = []
    for _, fitness, _ in evaluation:
        fitnesses.append(fitness)
    fitnesses.sort(reverse=True)

    columns = COLUMNS
    s = f"💃 {styles.color.ansi256(styles.rgbToAnsi256(128, 0, 0))}Fandango {styles.color.close} {generation}/{max_generations} "
    columns -= len(f"   Fandango {generation}/{max_generations} ") + 1
    columns /= 3.0
    for column in range(0, int(columns)):
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


def clear_visualization():
    """Clear Fandango visualization"""
    if not use_visualization():
        return

    time.sleep(0.5)
    s = " " * (COLUMNS - 1)
    print(f"\r{s}\r", end="", file=sys.stderr)
