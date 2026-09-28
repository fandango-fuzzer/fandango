import random
from collections.abc import Iterator

import pytest

from fandango.api import Fandango
from fandango.evolution import GeneratorWithReturn
from fandango.evolution.algorithm.simple import SimpleGeneticAlgorithm
from fandango.evolution.crossover import SimpleSubtreeCrossover
from fandango.evolution.mutation import SimpleMutation
from fandango.io.navigation.forecasting.forecasting_result import (
    ForecastingPacket,
    MountingPath,
)
from fandango.io.packet_evolution.decorators.io_population_manager import (
    IoPopulationManager,
)
from fandango.io.packet_evolution.decorators.mounting_crossover import MountingCrossover
from fandango.io.packet_evolution.decorators.mounting_evaluator import MountingEvaluator
from fandango.io.packet_evolution.decorators.mounting_mutation import MountingMutation
from fandango.io.packet_evolution.packet_mounter import PacketMounter
from fandango.language.grammar.nodes.concatenation import Concatenation
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.symbols import NonTerminal, Terminal
from fandango.language.tree import DerivationTree

from .utils import RESOURCES_ROOT

START = NonTerminal("<start>")
EXCHANGE = NonTerminal("<exchange>")
NOTE = NonTerminal("<note>")


def note_tree(sender: str, recipient: str, text: str) -> DerivationTree:
    return DerivationTree(
        NOTE, [DerivationTree(Terminal(text))], sender=sender, recipient=recipient
    )


def attached_note(
    manager: IoPopulationManager, text: str, mounting_path: MountingPath
) -> DerivationTree:
    packet = note_tree("Fuzzer", "Extern", text)
    manager.packet_mounter.attach(packet, mounting_path)
    return packet


def is_attached(packet: DerivationTree) -> bool:
    return packet.parent is not None and all(
        child is not packet for child in packet.parent.children
    )


@pytest.fixture(autouse=True)
def seed() -> None:
    random.seed(0)


@pytest.fixture
def fandango() -> Fandango:
    return Fandango(
        (RESOURCES_ROOT / "echo_io_constrained.fan").read_text(),
        use_stdlib=False,
        use_cache=False,
    )


@pytest.fixture
def history() -> DerivationTree:
    return DerivationTree(
        START,
        [
            DerivationTree(
                EXCHANGE,
                [
                    note_tree("Fuzzer", "Extern", "A\n"),
                    note_tree("Extern", "Fuzzer", "A\n"),
                ],
            )
        ],
    )


@pytest.fixture
def new_exchange(history: DerivationTree) -> MountingPath:
    return MountingPath(history, ((START, False), (EXCHANGE, True), (NOTE, False)))


@pytest.fixture
def last_exchange(history: DerivationTree) -> MountingPath:
    return MountingPath(history, ((START, False), (EXCHANGE, False), (NOTE, False)))


@pytest.fixture
def manager(
    fandango: Fandango, history: DerivationTree
) -> Iterator[IoPopulationManager]:
    manager = IoPopulationManager(fandango.grammar, str(START))
    with manager.packet_mounter.history_context(history):
        yield manager


@pytest.fixture
def evaluator(fandango: Fandango, manager: IoPopulationManager) -> MountingEvaluator:
    return MountingEvaluator(
        SimpleGeneticAlgorithm(fandango.grammar, fandango.constraints).evaluator,
        manager.packet_mounter,
    )


def test_history_context_hangs_messages_back_into_history(
    fandango, history, new_exchange
):
    mounter = PacketMounter(fandango.grammar, START)
    messages = [msg.msg for msg in history.protocol_msgs()]
    with mounter.history_context(history):
        mounter.attach(note_tree("Fuzzer", "Extern", "A\n"), new_exchange)
        assert all(message.get_root() is not history for message in messages)
    assert all(message.get_root() is history for message in messages)


def test_commit_returns_history_with_packet(fandango, history, new_exchange):
    mounter = PacketMounter(fandango.grammar, START)
    packet = note_tree("Fuzzer", "Extern", "A\n")
    with mounter.history_context(history):
        mounter.attach(packet, new_exchange)
    next_history = mounter.commit(packet)
    assert str(next_history) == "A\nA\nA\n"
    assert all(
        msg.msg.get_root() is next_history for msg in next_history.protocol_msgs()
    )


def test_mounted_context_mounts_packet_itself_when_equal_packet_moved_away(
    manager, evaluator, new_exchange, last_exchange
):
    moved_packet = attached_note(manager, "B\n", new_exchange)
    list(evaluator.evaluate_individual(moved_packet))
    manager.packet_mounter.attach(moved_packet, last_exchange)
    packet = attached_note(manager, "B\n", new_exchange)
    with manager.packet_mounter.mounted_context(packet) as mounted_packet:
        assert mounted_packet is packet
        assert str(mounted_packet.get_root()) == "A\nA\nB\n"


def test_fix_uses_failing_trees_cached_from_equal_packet(
    history, manager, evaluator, new_exchange
):
    evaluated_packet = attached_note(manager, "B\n", new_exchange)
    list(evaluator.evaluate_individual(evaluated_packet))
    equal_packet = attached_note(manager, "B\n", new_exchange)
    _solutions, (_fitness, failing_trees, suggestion) = GeneratorWithReturn(
        evaluator.evaluate_individual(equal_packet)
    ).collect()
    _solutions, (fixed_packet, _fixes_made) = GeneratorWithReturn(
        manager.fix_individual(
            equal_packet, failing_trees, suggestion, evaluator.evaluate_individual
        )
    ).collect()
    assert str(fixed_packet) == "A\n"
    assert is_attached(fixed_packet)
    assert str(fixed_packet.get_root()) == str(history)


def test_mutation_uses_failing_trees_cached_from_equal_packet(
    fandango, history, manager, evaluator, new_exchange
):
    evaluated_packet = attached_note(manager, "B\n", new_exchange)
    list(evaluator.evaluate_individual(evaluated_packet))
    equal_packet = attached_note(manager, "B\n", new_exchange)
    mutation = MountingMutation(SimpleMutation(), manager.packet_mounter)
    _solutions, mutated_packet = GeneratorWithReturn(
        mutation.mutate(equal_packet, fandango.grammar, evaluator.evaluate_individual)
    ).collect()
    assert is_attached(mutated_packet)
    assert str(mutated_packet.get_root()) == str(history)


def test_crossover_children_keep_mount_points_of_their_parents(
    fandango, manager, new_exchange, last_exchange
):
    parent1 = attached_note(manager, "B\n", new_exchange)
    parent2 = attached_note(manager, "C\n", last_exchange)
    crossover = MountingCrossover(SimpleSubtreeCrossover(), manager.packet_mounter)
    children = crossover.crossover(fandango.grammar, parent1, parent2)
    assert children is not None
    child1, child2 = children
    assert {str(child1), str(child2)} == {"B\n", "C\n"}
    assert child1.parent is parent1.parent
    assert child2.parent is parent2.parent
    assert all(is_attached(packet) for packet in (parent1, parent2, child1, child2))


def test_equal_packets_at_different_mount_points_are_unique(
    manager, new_exchange, last_exchange
):
    new_exchange_packet = attached_note(manager, "A\n", new_exchange)
    last_exchange_packet = attached_note(manager, "A\n", last_exchange)
    unique_packets = manager.unique([new_exchange_packet, last_exchange_packet])
    assert len(unique_packets) == 2


def test_equal_packets_at_the_same_mount_point_are_duplicates(manager, new_exchange):
    first_packet = attached_note(manager, "A\n", new_exchange)
    equal_packet = attached_note(manager, "A\n", new_exchange)
    unique_packets = manager.unique([first_packet, equal_packet])
    assert len(unique_packets) == 1
    assert unique_packets[0] is first_packet


def test_refill_keeps_equal_packets_at_every_mount_point(
    fandango, manager, evaluator, new_exchange, last_exchange
):
    exchange_rule = fandango.grammar.rules[EXCHANGE]
    assert isinstance(exchange_rule, Concatenation)
    fuzzer_note = exchange_rule.nodes[0]
    assert isinstance(fuzzer_note, NonTerminalNode)
    fuzzer_note_packet = ForecastingPacket(fuzzer_note)
    fuzzer_note_packet.add_path(new_exchange)
    fuzzer_note_packet.add_path(last_exchange)
    manager.fuzzable_packets = [fuzzer_note_packet]
    population: list[DerivationTree] = []
    list(manager.refill_population(population, evaluator.evaluate_individual, 10, 2))
    assert [str(packet) for packet in population] == ["A\n", "A\n"]
    assert population[0].parent is not population[1].parent
