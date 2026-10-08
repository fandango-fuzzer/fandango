import random
from collections.abc import Iterator

import pytest

from fandango.api import Fandango
from fandango.constraints.constraint import Constraint
from fandango.constraints.repetition_bounds import RepetitionBoundsConstraint
from fandango.evolution import GeneratorWithReturn
from fandango.evolution.crossover import SimpleSubtreeCrossover
from fandango.evolution.mutation import SimpleMutation
from fandango.io.constraints.constraint_scope import (
    ConstraintScope,
    ConstraintScopeAnalyzer,
)
from fandango.io.navigation.forecasting.forecasting_result import (
    ForecastingPacket,
    MountingPath,
)
from fandango.io.packet_evolution.decorators.mounting_crossover import MountingCrossover
from fandango.io.packet_evolution.decorators.mounting_mutation import MountingMutation
from fandango.io.packet_evolution.io_evaluator import IoEvaluator
from fandango.io.packet_evolution.io_population_manager import IoPopulationManager
from fandango.io.packet_evolution.packet_mounter import PacketMounter
from fandango.language.grammar.nodes.concatenation import Concatenation
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.parse.parse import parse
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
    manager = IoPopulationManager(
        PacketMounter(fandango.grammar, START), fandango.grammar, str(START)
    )
    with manager.packet_mounter.history_context(history):
        yield manager


@pytest.fixture
def evaluator(fandango: Fandango, manager: IoPopulationManager) -> IoEvaluator:
    return IoEvaluator(
        packet_mounter=manager.packet_mounter,
        grammar=fandango.grammar,
        constraints=fandango.constraints,
        expected_fitness=1.0,
        diversity_k=5,
        diversity_weight=1.0,
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
    _, (_fitness, failing_trees, suggestion) = GeneratorWithReturn(
        evaluator.evaluate_individual(equal_packet)
    ).collect()
    _, (fixed_packet, _) = GeneratorWithReturn(
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
    _, mutated_packet = GeneratorWithReturn(
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


def test_constraint_inside_message_ignores_earlier_messages(evaluator):
    history = DerivationTree(
        START,
        [
            DerivationTree(
                EXCHANGE,
                [
                    note_tree("Fuzzer", "Extern", "A\n"),
                    # Would fail constraint
                    note_tree("Extern", "Fuzzer", "B\n"),
                ],
            )
        ],
    )
    mounter = evaluator._packet_mounter
    with mounter.history_context(history):
        packet = note_tree("Fuzzer", "Extern", "A\n")
        mounter.attach(
            packet,
            MountingPath(history, ((START, False), (EXCHANGE, True), (NOTE, False))),
        )
        _, (fitness, failing_trees, _) = GeneratorWithReturn(
            evaluator.evaluate_individual(packet)
        ).collect()
    assert fitness == 1.0
    assert failing_trees == []


def test_constraint_inside_message_fails_on_the_packet(
    manager, evaluator, new_exchange
):
    # B not allowed in grammar
    packet = attached_note(manager, "B\n", new_exchange)
    _, (fitness, failing_trees, _) = GeneratorWithReturn(
        evaluator.evaluate_individual(packet)
    ).collect()
    assert fitness < 1.0
    assert [str(failing.tree) for failing in failing_trees] == ["B\n"]


def test_constraint_scopes():
    k_path_io = (RESOURCES_ROOT / "k_path_io.fan").read_text()
    cmd = NonTerminal("<cmd>")
    reply = NonTerminal("<reply>")
    cases = [
        ("str(<verb>) == 'GET'", ConstraintScope.INSIDE, ConstraintScope.UNRELATED),
        (
            "forall <a> in <arg>: len(str(<a>)) < 5",
            ConstraintScope.INSIDE,
            ConstraintScope.UNRELATED,
        ),
        ("str(<code>) == '200'", ConstraintScope.UNRELATED, ConstraintScope.INSIDE),
        (
            "str(<verb>) == 'GET' or str(<code>) == '200'",
            ConstraintScope.CROSSING,
            ConstraintScope.CROSSING,
        ),
        (
            "str(<exchange>.<cmd>) != ''",
            ConstraintScope.CROSSING,
            ConstraintScope.UNRELATED,
        ),
        (
            "forall <d> in <start>..<digit>: str(<d>) == '0'",
            ConstraintScope.CROSSING,
            ConstraintScope.UNRELATED,
        ),
        (
            "forall <e> in <state>.<exchange>: str(<e>.<cmd>) != ''",
            ConstraintScope.CROSSING,
            ConstraintScope.CROSSING,
        ),
        ("len(str(<start>)) > 0", ConstraintScope.CROSSING, ConstraintScope.CROSSING),
    ]
    for constraint_text, cmd_scope, reply_scope in cases:
        grammar, constraints = parse(
            k_path_io + f"\nwhere {constraint_text}\n",
            use_stdlib=False,
            use_cache=False,
        )
        assert grammar is not None
        (constraint,) = constraints
        assert isinstance(constraint, Constraint)
        scopes = ConstraintScopeAnalyzer(grammar)
        assert scopes.analyse_scope(cmd, constraint) == cmd_scope, constraint_text
        assert scopes.analyse_scope(reply, constraint) == reply_scope, constraint_text

    reply_rule = "<reply> ::= <code>\n"
    assert reply_rule in k_path_io
    grammar, constraints = parse(
        k_path_io.replace(
            reply_rule,
            "<reply> ::= <code> ' ' <n> <text>{int(<n>)}\n"
            "<n> ::= '1' | '2'\n"
            "<text> ::= 'a' | 'b'\n",
        ),
        use_stdlib=False,
        use_cache=False,
    )
    assert grammar is not None
    (bounds,) = [c for c in constraints if isinstance(c, RepetitionBoundsConstraint)]
    scopes = ConstraintScopeAnalyzer(grammar)
    assert scopes.analyse_scope(cmd, bounds) == ConstraintScope.UNRELATED
    assert scopes.analyse_scope(reply, bounds) == ConstraintScope.INSIDE


def test_paths_through_a_bound_variable_stay_inside_what_the_quantifier_finds():
    k_path_io = (RESOURCES_ROOT / "k_path_io.fan").read_text()
    reply_rule = "<reply> ::= <code>\n"
    assert reply_rule in k_path_io
    k_path_io = k_path_io.replace(reply_rule, "<reply> ::= <code> <digit>\n")
    cmd = NonTerminal("<cmd>")
    reply = NonTerminal("<reply>")
    cases = [
        (
            "forall <r> in <reply>: str(<r>.<digit>) == '0'",
            ConstraintScope.UNRELATED,
            ConstraintScope.INSIDE,
        ),
        (
            "forall <r> in <reply>: str(<r>.<digit>) == str(<digit>)",
            ConstraintScope.CROSSING,
            ConstraintScope.INSIDE,
        ),
        (
            "forall <e> in <exchange>: str(<e>.<reply>.<digit>) == '0'",
            ConstraintScope.CROSSING,
            ConstraintScope.CROSSING,
        ),
    ]
    for constraint_text, cmd_scope, reply_scope in cases:
        grammar, constraints = parse(
            k_path_io + f"\nwhere {constraint_text}\n",
            use_stdlib=False,
            use_cache=False,
        )
        assert grammar is not None
        (constraint,) = constraints
        assert isinstance(constraint, Constraint)
        scopes = ConstraintScopeAnalyzer(grammar)
        assert scopes.analyse_scope(cmd, constraint) == cmd_scope, constraint_text
        assert scopes.analyse_scope(reply, constraint) == reply_scope, constraint_text


def evaluator_with(constraint_text: str) -> IoEvaluator:
    grammar_text = (RESOURCES_ROOT / "echo_io_constrained.fan").read_text()
    note_constraint = 'where str(<note>) == "A\\n"\n'
    assert note_constraint in grammar_text
    fandango = Fandango(
        grammar_text.replace(note_constraint, f"where {constraint_text}\n"),
        use_stdlib=False,
        use_cache=False,
    )
    return IoEvaluator(
        packet_mounter=PacketMounter(fandango.grammar, START),
        grammar=fandango.grammar,
        constraints=fandango.constraints,
        expected_fitness=1.0,
        diversity_k=5,
        diversity_weight=1.0,
    )


def evaluate_mounted(
    evaluator: IoEvaluator,
    history: DerivationTree,
    path: tuple[tuple[NonTerminal, bool], ...],
    packet: DerivationTree,
) -> tuple[float, list[NonTerminal]]:
    """Fitness of packet mounted along path, and the symbols of the trees that fail."""
    mounter = evaluator._packet_mounter
    with mounter.history_context(history):
        mounter.attach(packet, MountingPath(history, path))
        _, (fitness, failing_trees, _) = GeneratorWithReturn(
            evaluator.evaluate_individual(packet)
        ).collect()
    return fitness, [failing.tree.symbol for failing in failing_trees]


# Fails "an exchange does not start with B" and "both notes of an exchange are equal", but is history
FAILING_EXCHANGE = DerivationTree(
    EXCHANGE,
    [note_tree("Fuzzer", "Extern", "B\n"), note_tree("Extern", "Fuzzer", "A\n")],
)
NEW_EXCHANGE = ((START, False), (EXCHANGE, True), (NOTE, False))
LAST_EXCHANGE = ((START, False), (EXCHANGE, False), (NOTE, False))


def test_forall_through_its_variable_skips_instances_the_packet_is_not_in():
    evaluator = evaluator_with("forall <e> in <exchange>: not str(<e>).startswith('B')")
    history = DerivationTree(START, [FAILING_EXCHANGE.deepcopy()])

    assert evaluate_mounted(
        evaluator, history, NEW_EXCHANGE, note_tree("Fuzzer", "Extern", "A\n")
    ) == (1.0, [])
    fitness, failing = evaluate_mounted(
        evaluator, history, NEW_EXCHANGE, note_tree("Fuzzer", "Extern", "B\n")
    )
    assert fitness < 1.0
    assert failing == [EXCHANGE]


def test_forall_through_its_variable_reads_the_whole_instance_the_packet_is_in():
    # The reply is checked against the earlier request of its own exchange, not against other exchanges
    evaluator = evaluator_with("forall <e> in <exchange>: str(<e>[1]) == str(<e>[0])")
    history = DerivationTree(
        START,
        [
            FAILING_EXCHANGE.deepcopy(),
            DerivationTree(EXCHANGE, [note_tree("Fuzzer", "Extern", "C\n")]),
        ],
    )

    assert evaluate_mounted(
        evaluator, history, LAST_EXCHANGE, note_tree("Extern", "Fuzzer", "C\n")
    ) == (1.0, [])
    fitness, failing = evaluate_mounted(
        evaluator, history, LAST_EXCHANGE, note_tree("Extern", "Fuzzer", "A\n")
    )
    assert fitness < 1.0
    assert set(failing) == {NOTE}


def test_forall_that_also_reads_outside_its_variable_checks_every_instance():
    # <start> is reached without <e>, so the failing history exchange counts again
    evaluator = evaluator_with(
        "forall <e> in <exchange>: not str(<e>).startswith('B') or len(str(<start>)) < 0"
    )
    history = DerivationTree(START, [FAILING_EXCHANGE.deepcopy()])

    fitness, failing = evaluate_mounted(
        evaluator, history, NEW_EXCHANGE, note_tree("Fuzzer", "Extern", "A\n")
    )
    assert fitness < 1.0
    assert EXCHANGE in failing
