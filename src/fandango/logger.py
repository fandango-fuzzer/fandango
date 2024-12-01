import logging
import traceback
import sys

LOGGER = logging.getLogger("fandango")
logging.basicConfig(
    level=logging.INFO,
    format="%(name)s:%(levelname)s: %(message)s",
)
def print_exception(e):
    LOGGER.info(traceback.format_exc().rstrip())
    if not LOGGER.isEnabledFor(logging.INFO):
        print(type(e).__name__ + ":", e, file=sys.stderr)
