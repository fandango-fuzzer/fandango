from collections.abc import Callable
from typing import Optional

from fandango.io import FandangoIO
from fandango.io.navigation.packetforecaster import (
    ForecastingPacket,
    ForecastingResult,
    PacketForecaster,
)
from fandango.language.grammar.grammar import Grammar
from fandango.language.tree import DerivationTree


class ForecastView:
    """
    A wrapper for the forecaster's prediction, the io instance and for the current history tree.
    """

    def __init__(
        self,
        grammar: Grammar,
        io_instance: FandangoIO,
        history_provider: Callable[[], DerivationTree],
    ):
        self._forecaster = PacketForecaster(grammar)
        self._io_instance = io_instance
        self._history = history_provider
        self._cached_tree: Optional[DerivationTree] = None
        self._result: Optional[ForecastingResult] = None

    @property
    def result(self) -> ForecastingResult:
        tree = self._history()
        if self._result is None or self._cached_tree is not tree:
            self._result = self._forecaster.predict(tree)
            self._cached_tree = tree
        return self._result

    def is_complete(self) -> bool:
        return len(self.result.complete_trees) != 0

    def next_fuzzer_parties(
        self,
        show_fuzzer_controlled: bool = True,
        show_external_controlled: bool = False,
    ) -> list[str]:
        return list(
            filter(
                lambda x: (
                    (
                        self._io_instance.parties[x].is_fuzzer_controlled()
                        and show_fuzzer_controlled
                    )
                    or (
                        not self._io_instance.parties[x].is_fuzzer_controlled()
                        and show_external_controlled
                    )
                ),
                self.result.get_msg_parties(),
            )
        )

    def get_fuzzer_packets(self) -> list[ForecastingPacket]:
        return [
            packet
            for sender in self.next_fuzzer_parties()
            for packet in self.result.parties_to_packets[sender].nt_to_packet.values()
        ]

    def next_external_parties(self) -> list[str]:
        return list(
            filter(
                lambda x: not self._io_instance.parties[x].is_fuzzer_controlled(),
                self.result.get_msg_parties(),
            )
        )

    def get_next_parties(self) -> list[str]:
        return list(self.result.get_msg_parties())
