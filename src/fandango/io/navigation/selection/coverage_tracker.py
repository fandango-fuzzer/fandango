from collections.abc import Callable
from typing import Any, Optional

from fandango.io.navigation.coverage.coverage_goal import CoverageGoal
from fandango.io.navigation.selection.protocol_model import ProtocolModel
from fandango.language.grammar.grammar import Grammar, KPath
from fandango.language.symbols import NonTerminal
from fandango.language.tree import DerivationTree


class CoverageTracker:
    """
    Measures reached k-path coverage of the current and past protocol runs.
    """

    def __init__(
        self,
        grammar: Grammar,
        diversity_k: int,
        model: ProtocolModel,
        start_symbol: NonTerminal,
        input_parties: Callable[[], set[str]],
        history: Callable[[], DerivationTree],
        coverage_goal: CoverageGoal,
    ):
        self._grammar = grammar
        self._diversity_k = diversity_k
        self._model = model
        self._start_symbol = start_symbol
        self._input_parties = input_parties
        self._history = history
        self._coverage_goal = coverage_goal
        self._whole_covered: set[KPath] = set()
        self._message_covered: dict[bool, dict[NonTerminal, set[KPath]]] = {
            False: {},
            True: {},
        }
        self._coverage_scores: Optional[list[tuple[NonTerminal, float]]] = None

    def add_completed_tree(self, tree: DerivationTree) -> None:
        """Fold a finished run into the coverage basis."""
        self._whole_covered |= self._covered(
            [tree],
            coverage_goal=self._coverage_goal,
            input_parties=self._input_parties(),
        )
        messages_by_nt = self._model.group_messages_by_nt([tree])
        for overlap_to_root, covered_by_nt in self._message_covered.items():
            for symbol, subtrees in messages_by_nt.items():
                covered_by_nt.setdefault(symbol, set()).update(
                    self._covered(subtrees, overlap_to_root=overlap_to_root)
                )
        self._coverage_scores = None

    def reset(self) -> None:
        self._whole_covered.clear()
        for covered_by_nt in self._message_covered.values():
            covered_by_nt.clear()
        self._coverage_scores = None

    def invalidate(self) -> None:
        self._coverage_scores = None

    def set_coverage_goal(self, goal: CoverageGoal) -> None:
        # coverage_goal feeds whole-tree extraction, so the folded basis is invalid.
        self._coverage_goal = goal
        self._whole_covered.clear()
        self._coverage_scores = None

    def uncovered_paths(self, *, alt_cache: bool = False) -> list[KPath]:
        all_paths = self._all_k_paths(
            self._start_symbol,
            coverage_goal=self._coverage_goal,
            input_parties=self._input_parties(),
            alt_cache=alt_cache,
        )
        return list(all_paths.difference(self._whole_covered_paths(alt_cache=alt_cache)))

    def coverage_scores(self) -> list[tuple[NonTerminal, float]]:
        if self._coverage_scores is None:
            self._coverage_scores = self._compute_coverage_scores()
        return self._coverage_scores

    def coverage_percent(self, *, alt_cache: bool = False) -> float:
        uncovered = self.uncovered_paths(alt_cache=alt_cache)
        if len(uncovered) == 0:
            return 1.0
        all_paths = self._all_k_paths(
            self._start_symbol,
            coverage_goal=self._coverage_goal,
            input_parties=self._input_parties(),
            alt_cache=alt_cache,
        )
        if len(all_paths) == 0:
            return 1.0
        return 1.0 - (len(uncovered) / len(all_paths))

    def coverage_trees(
        self, overlap_to_root: bool, *, alt_cache: bool = True
    ) -> dict[NonTerminal, tuple[int, int]]:
        """Per-NonTerminal and per-role (covered, total) k-path counts, for logging.
        Uses the alt cache so measurement does not warm the guidance cache."""
        history_messages = self._model.group_messages_by_nt([self._history()])
        covered_by_nt = self._message_covered[overlap_to_root]
        paths_by_role: dict[str, Any] = {
            "all_party": {
                "covered": [],
                "covered_unique": set(),
                "all": [],
                "all_unique": set(),
                "symbols": set(),
            }
        }
        roles_by_symbol: dict[NonTerminal, set[str]] = {}
        for pnt in self._grammar.get_protocol_messages(self._start_symbol):
            sender = pnt.sender
            symbol = pnt.symbol
            if sender not in paths_by_role:
                assert sender is not None
                paths_by_role[sender] = {
                    "covered": [],
                    "covered_unique": set(),
                    "all": [],
                    "all_unique": set(),
                    "symbols": set(),
                }
            paths_by_role[sender]["symbols"].add(symbol)
            paths_by_role["all_party"]["symbols"].add(symbol)
            roles_by_symbol.setdefault(symbol, set()).add(sender)
            roles_by_symbol[symbol].add("all_party")

        nt_coverage: dict[NonTerminal, tuple[int, int]] = {}
        for symbol in self._model.state_grammar_symbols:
            all_k_paths = self._all_k_paths(
                symbol, overlap_to_root=overlap_to_root, alt_cache=alt_cache
            )
            covered_k_paths = set(covered_by_nt.get(symbol, ()))
            covered_k_paths |= self._covered(
                history_messages.get(symbol, []),
                overlap_to_root=overlap_to_root,
                alt_cache=alt_cache,
            )
            if symbol in roles_by_symbol:
                for role in roles_by_symbol[symbol]:
                    paths_by_role[role]["all"].extend(all_k_paths)
                    paths_by_role[role]["all_unique"].update(all_k_paths)
                    paths_by_role[role]["covered"].extend(covered_k_paths)
                    paths_by_role[role]["covered_unique"].update(covered_k_paths)
            nt_coverage[symbol] = (len(covered_k_paths), len(all_k_paths))
        for role, paths in paths_by_role.items():
            nt_coverage[NonTerminal("__role_" + role)] = (
                len(paths["covered"]),
                len(paths["all"]),
            )
            nt_coverage[NonTerminal("__role_unique_" + role)] = (
                len(paths["covered_unique"]),
                len(paths["all_unique"]),
            )
        return nt_coverage

    def _covered(
        self,
        trees: list[DerivationTree],
        *,
        overlap_to_root: bool = False,
        coverage_goal: CoverageGoal = CoverageGoal.STATE_INPUTS_OUTPUTS,
        input_parties: Optional[set[str]] = None,
        alt_cache: bool = False,
    ) -> set[KPath]:
        """k-paths covered by the trees (union of the per-tree extraction)."""
        result: set[KPath] = set()
        for tree in trees:
            result |= self._grammar._extract_k_paths_from_tree(
                tree,
                self._diversity_k,
                overlap_to_root,
                coverage_goal,
                input_parties=input_parties,
                alt_cache=alt_cache,
            )
        return result

    def _all_k_paths(
        self,
        non_terminal: NonTerminal,
        *,
        overlap_to_root: bool = False,
        coverage_goal: CoverageGoal = CoverageGoal.STATE_INPUTS_OUTPUTS,
        input_parties: Optional[set[str]] = None,
        alt_cache: bool = False,
    ) -> set[KPath]:
        return self._grammar.generate_all_k_paths(
            k=self._diversity_k,
            non_terminal=non_terminal,
            overlap_to_root=overlap_to_root,
            coverage_goal=coverage_goal,
            input_parties=input_parties,
            alt_cache=alt_cache,
        )

    def _whole_covered_paths(self, *, alt_cache: bool = False) -> set[KPath]:
        """Folded basis plus the in-progress history tree."""
        covered = set(self._whole_covered)
        covered |= self._covered(
            [self._history()],
            coverage_goal=self._coverage_goal,
            input_parties=self._input_parties(),
            alt_cache=alt_cache,
        )
        return covered

    def _compute_coverage_scores(self) -> list[tuple[NonTerminal, float]]:
        """Per-NonTerminal coverage score: covered / total k-paths."""
        history_messages = self._model.group_messages_by_nt([self._history()])
        covered_by_nt = self._message_covered[False]
        nt_coverage: dict[NonTerminal, float] = {}
        for symbol in self._model.state_grammar_symbols:
            if symbol not in covered_by_nt and symbol not in history_messages:
                nt_coverage[symbol] = 0.0
                continue
            covered = set(covered_by_nt.get(symbol, ()))
            covered |= self._covered(history_messages.get(symbol, []))
            all_paths = self._all_k_paths(symbol)
            if len(all_paths) == 0:
                nt_coverage[symbol] = 1.0
            else:
                nt_coverage[symbol] = len(covered) / len(all_paths)
        return list(sorted(nt_coverage.items(), key=lambda x: (x[1], x[0].name())))
