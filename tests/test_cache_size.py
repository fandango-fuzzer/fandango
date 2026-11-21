import pytest

from fandango.utils import cache_size


def test_default_cache_size_keeps_long_runs_small(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Every constraint, the fitness evaluation, the parser and the k-path
    extraction each keep this many entries, and an entry can keep a whole
    derivation tree alive."""
    monkeypatch.delenv("FANDANGO_CACHE_SIZE", raising=False)
    assert cache_size() == 10_000


def test_cache_size_can_be_set(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FANDANGO_CACHE_SIZE", "500")
    assert cache_size() == 500
