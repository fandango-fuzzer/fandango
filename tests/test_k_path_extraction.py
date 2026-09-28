from fandango.io.navigation.coverage.coverage_goal import CoverageGoal
from fandango.language.parse.parse import parse
from fandango.language.symbols import NonTerminal

from .utils import RESOURCES_ROOT


def test_extract_k_paths():
    with open(RESOURCES_ROOT / "k_path_io.fan") as f:
        grammar, _ = parse(f, use_stdlib=False, use_cache=False)
    assert grammar is not None
    tree = grammar.parse("GET1200")
    assert tree is not None

    def k_paths(tree, k, overlap_to_root, coverage_goal):
        return {
            " ".join(symbol.format_as_spec() for symbol in path)
            for path in grammar._extract_k_paths_from_tree(
                tree, k, overlap_to_root, coverage_goal, {"Fuzzer"}
            )
        }

    # The whole tree, k=2.
    expected = {
        CoverageGoal.STATE_INPUTS_OUTPUTS: {
            "<start>",
            "<start> <state>",
            "<state>",
            "<state> <exchange>",
            "<exchange>",
            "<exchange> <cmd>",
            "<exchange> <reply>",
            "<cmd>",
            "<cmd> <verb>",
            "<cmd> <arg>",
            "<verb>",
            "<verb> 'GET'",
            "'GET'",
            "<arg>",
            "<arg> <digit>",
            "<digit>",
            "<digit> r'[01]'",
            "r'[01]'",
            "<reply>",
            "<reply> <code>",
            "<code>",
            "<code> '200'",
            "'200'",
        },
        CoverageGoal.STATE_INPUTS: {
            "<start>",
            "<start> <state>",
            "<state>",
            "<state> <exchange>",
            "<exchange>",
            "<exchange> <cmd>",
            "<cmd>",
            "<cmd> <verb>",
            "<cmd> <arg>",
            "<verb>",
            "<verb> 'GET'",
            "'GET'",
            "<arg>",
            "<arg> <digit>",
            "<digit>",
            "<digit> r'[01]'",
            "r'[01]'",
        },
        CoverageGoal.INPUTS: {
            "<cmd>",
            "<cmd> <verb>",
            "<cmd> <arg>",
            "<verb>",
            "<verb> 'GET'",
            "'GET'",
            "<arg>",
            "<arg> <digit>",
            "<digit>",
            "<digit> r'[01]'",
            "r'[01]'",
        },
    }
    for coverage_goal, paths in expected.items():
        assert k_paths(tree, 2, False, coverage_goal) == paths, coverage_goal

    # <arg> inside the input message, with the paths running into it from above, k=3.
    arg = next(tree.find_subtrees(NonTerminal("<arg>")))
    expected = {
        CoverageGoal.STATE_INPUTS_OUTPUTS: {
            "<arg>",
            "<arg> <digit>",
            "<arg> <digit> r'[01]'",
            "<digit>",
            "<digit> r'[01]'",
            "r'[01]'",
            "<cmd> <arg>",
            "<cmd> <arg> <digit>",
            "<exchange> <cmd> <arg>",
        },
        CoverageGoal.STATE_INPUTS: {
            "<arg>",
            "<arg> <digit>",
            "<arg> <digit> r'[01]'",
            "<digit>",
            "<digit> r'[01]'",
            "r'[01]'",
            "<cmd> <arg>",
            "<cmd> <arg> <digit>",
            "<exchange> <cmd> <arg>",
        },
        CoverageGoal.INPUTS: {
            "<arg>",
            "<arg> <digit>",
            "<arg> <digit> r'[01]'",
            "<digit>",
            "<digit> r'[01]'",
            "r'[01]'",
            "<cmd> <arg>",
            "<cmd> <arg> <digit>",
        },
    }
    for coverage_goal, paths in expected.items():
        assert k_paths(arg, 3, True, coverage_goal) == paths, coverage_goal
