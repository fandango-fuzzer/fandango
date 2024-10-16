import logging

LOGGER = logging.getLogger("fandango")
logging.basicConfig(
    level=logging.INFO,
    format="%(name)s :: %(levelname)-8s :: %(message)s",
)
