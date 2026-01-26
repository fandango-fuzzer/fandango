#!/usr/bin/env python

import json
import time
import urllib.request
from pathlib import Path
import sys
import os

from importlib.metadata import version, PackageNotFoundError
from packaging.version import Version, InvalidVersion

from fandango.language.parse.cache import get_cache_dir
from fandango.cli.parser import terminal_link
from fandango import DISTRIBUTION_NAME
from fandango.logger import LOGGER

# How often to check for updates (in seconds)
CHECK_INTERVAL_SECONDS = 7 * 24 * 60 * 60  # one week

# Network timeout for PyPI requests
TIMEOUT = 5  # seconds


def check_package_for_update(
    package_name: str, *, cache_dir: Path | None = None, check_now: bool = False
) -> bool:
    """
    If `package` has an update available on PyPI, print a notification to stderr.

    :param package_name: package name
    :param cache_dir: Where to store the cache file (default: ~/.cache)
    :param check_now: Whether to check for updates immediately, bypassing the rate limit
    :return: True if an update notification was printed, False otherwise
    """
    if not cache_dir:
        cache_dir = Path.home() / ".cache"
    cache_file = cache_dir / f"{package_name}_pypi_update_check.json"

    cache_file.parent.mkdir(parents=True, exist_ok=True)
    now = time.time()

    # Rate limiting
    if not check_now and cache_file.exists():
        try:
            last_check = json.loads(cache_file.read_text()).get("last_check", 0)
            if now - last_check < CHECK_INTERVAL_SECONDS:
                return False
        except Exception:
            return False  # ignore broken cache

    LOGGER.debug(f"Checking for updates for package '{package_name}'")

    # Get installed version
    try:
        installed_version = Version(version(package_name))
    except (PackageNotFoundError, InvalidVersion):
        return False  # package not installed or invalid version

    # Get latest version from PyPI
    try:
        with urllib.request.urlopen(
            f"https://pypi.org/pypi/{package_name}/json",
            timeout=TIMEOUT,
        ) as response:
            data = json.load(response)
            latest_version = Version(data["info"]["version"])
    except Exception:
        return False  # network error, bad response, etc.

    # Compare
    notified = False
    if latest_version > installed_version:
        print(
            f"""
📦 Update available for '{package_name}': {installed_version} → {latest_version}. See {terminal_link(f"https://pypi.org/project/{package_name}/{latest_version}/")}
""".strip(),
            file=sys.stderr,
        )
        notified = True

    # Update cache file
    cache_file.write_text(json.dumps({"last_check": now}))

    return notified


NOTIFIED_IN_THIS_SESSION = False


def check_for_fandango_update(check_now: bool = False) -> None:
    """Check for Fandango updates and notify the user if an update is available."""
    global NOTIFIED_IN_THIS_SESSION

    if os.environ.get("CI"):
        return  # skip checks in CI environments
    if os.environ.get("FANDANGO_DISABLE_UPDATE_CHECK"):
        return  # user disabled update checks
    if not sys.stdout.isatty():
        return  # only check in interactive sessions
    if NOTIFIED_IN_THIS_SESSION:
        return  # only notify once per session

    notified = check_package_for_update(
        DISTRIBUTION_NAME, cache_dir=get_cache_dir(), check_now=check_now
    )

    if notified:
        NOTIFIED_IN_THIS_SESSION = True


if __name__ == "__main__":
    check_for_fandango_update()
    for package in sys.argv[1:]:
        check_package_for_update(package, cache_dir=get_cache_dir())
