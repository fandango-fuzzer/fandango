from collections import OrderedDict
from typing import Generic, Iterator, Optional, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class LRUCache(Generic[K, V]):
    """LRU cache with a configurable maximum number of entries.

    When the cache is full, the entry that has gone the longest without a cache
    hit is evicted before inserting the new entry.  Pass ``max_size=None`` for
    an unbounded cache.
    """

    def __init__(self, max_size: Optional[int] = None) -> None:
        if max_size is not None and max_size < 0:
            raise ValueError("max_size must be non-negative or None")
        self._max_size = max_size
        self._cache: OrderedDict[K, V] = OrderedDict()

    @property
    def max_size(self) -> Optional[int]:
        return self._max_size

    def __contains__(self, key: object) -> bool:
        return key in self._cache

    def __getitem__(self, key: K) -> V:
        self._cache.move_to_end(key)
        return self._cache[key]

    def __setitem__(self, key: K, value: V) -> None:
        if key in self._cache:
            self._cache.move_to_end(key)
        self._cache[key] = value
        if self._max_size is not None and len(self._cache) > self._max_size:
            self._cache.popitem(last=False)

    def __len__(self) -> int:
        return len(self._cache)

    def __iter__(self) -> Iterator[K]:
        return iter(self._cache)

    def clear(self) -> None:
        self._cache.clear()


TreeCache = LRUCache
