from typing import cast
import unittest

from fandango import parse
from fandango.constraints.constraint import Constraint
from fandango.constraints.comparison import ComparisonConstraint
from fandango.constraints.exists import ExistsConstraint
from fandango.constraints.forall import ForallConstraint
from fandango.constraints.failing_tree import Comparison
from fandango.language.symbols import NonTerminal, Terminal
from fandango.language.tree import DerivationTree
from fandango.language.grammar.grammar import Grammar
from fandango.language.search import (
    StarSearch,
    RuleSearch,
    PopulationSearch,
    AttributeSearch,
    DescendantAttributeSearch,
)


class TestStar(unittest.TestCase):
    EXAMPLE = """
<start> ::= <a> <b> <c> <c>
<a> ::= "a" | "b"
<b> ::= "c" | "d"
<c> ::= "e" | "f" | "g" | "h"

where any(<x> == "a" for <x> in *<a>)
where all(<x> == "c" for <x> in *<b>)
where {str(x) for x in *<c>} == {"e", "f"}
"""

    VALID = DerivationTree(
        NonTerminal("<start>"),
        [
            DerivationTree(NonTerminal("<a>"), [DerivationTree(Terminal("a"))]),
            DerivationTree(NonTerminal("<b>"), [DerivationTree(Terminal("c"))]),
            DerivationTree(NonTerminal("<c>"), [DerivationTree(Terminal("f"))]),
            DerivationTree(NonTerminal("<c>"), [DerivationTree(Terminal("e"))]),
        ],
    )

    INVALID_A = DerivationTree(
        NonTerminal("<start>"),
        [
            DerivationTree(NonTerminal("<a>"), [DerivationTree(Terminal("b"))]),
            DerivationTree(NonTerminal("<b>"), [DerivationTree(Terminal("c"))]),
            DerivationTree(NonTerminal("<c>"), [DerivationTree(Terminal("f"))]),
            DerivationTree(NonTerminal("<c>"), [DerivationTree(Terminal("e"))]),
        ],
    )
    INVALID_B = DerivationTree(
        NonTerminal("<start>"),
        [
            DerivationTree(NonTerminal("<a>"), [DerivationTree(Terminal("a"))]),
            DerivationTree(NonTerminal("<b>"), [DerivationTree(Terminal("d"))]),
            DerivationTree(NonTerminal("<c>"), [DerivationTree(Terminal("f"))]),
            DerivationTree(NonTerminal("<c>"), [DerivationTree(Terminal("e"))]),
        ],
    )
    INVALID_C = DerivationTree(
        NonTerminal("<start>"),
        [
            DerivationTree(NonTerminal("<a>"), [DerivationTree(Terminal("a"))]),
            DerivationTree(NonTerminal("<b>"), [DerivationTree(Terminal("c"))]),
            DerivationTree(NonTerminal("<c>"), [DerivationTree(Terminal("e"))]),
            DerivationTree(NonTerminal("<c>"), [DerivationTree(Terminal("e"))]),
        ],
    )

    grammar: Grammar
    constraints: list[Constraint]
    any_constraint: ExistsConstraint
    all_constraint: ForallConstraint
    expression_constraint: ComparisonConstraint

    @classmethod
    def setUpClass(cls):
        # set parser to python
        # fandango.Fandango.parser = "python"
        grammar, constraints = parse(
            TestStar.EXAMPLE, use_stdlib=False, use_cache=False
        )
        for e in constraints:
            assert isinstance(e, Constraint)
        cls.constraints = cast(list[Constraint], constraints)
        assert grammar is not None
        cls.grammar = grammar
        assert isinstance(cls.constraints[0], ExistsConstraint)
        cls.any_constraint = cls.constraints[0]
        assert isinstance(cls.constraints[1], ForallConstraint)
        cls.all_constraint = cls.constraints[1]
        assert isinstance(cls.constraints[2], ComparisonConstraint)
        cls.expression_constraint = cls.constraints[2]

    def test_parse_star(self):
        self.assertIsNotNone(self.grammar)
        self.assertIsNotNone(self.constraints)
        self.assertEqual(len(self.grammar.rules), 4)
        self.assertEqual(len(self.constraints), 3)
        self.assertIn("<start>", self.grammar)
        self.assertIn("<a>", self.grammar)
        self.assertIn("<b>", self.grammar)
        self.assertIn("<c>", self.grammar)
        # Check constraints
        # Check exists constraint
        assert isinstance(self.any_constraint, ExistsConstraint)
        assert isinstance(self.any_constraint.statement, ComparisonConstraint)
        self.assertEqual(self.any_constraint.statement.operator, Comparison.EQUAL)
        tmp_var = self.any_constraint.statement.left
        self.assertIn(tmp_var, self.any_constraint.statement.searches)
        rule_search = self.any_constraint.statement.searches[tmp_var]
        assert isinstance(rule_search, RuleSearch)
        self.assertEqual(rule_search.symbol, NonTerminal("<x>"))
        self.assertEqual(eval(self.any_constraint.statement.right), "a")
        self.assertEqual(self.any_constraint.bound, NonTerminal("<x>"))
        assert isinstance(self.any_constraint.search, StarSearch)
        assert isinstance(self.any_constraint.search.base, RuleSearch)
        self.assertEqual(self.any_constraint.search.base.symbol, NonTerminal("<a>"))

        # Check forall constraint
        assert isinstance(self.all_constraint, ForallConstraint)
        assert isinstance(self.all_constraint.statement, ComparisonConstraint)
        self.assertEqual(self.all_constraint.statement.operator, Comparison.EQUAL)
        tmp_var = self.all_constraint.statement.left
        self.assertIn(tmp_var, self.all_constraint.statement.searches)
        rule_search = self.all_constraint.statement.searches[tmp_var]
        assert isinstance(rule_search, RuleSearch)
        self.assertEqual(rule_search.symbol, NonTerminal("<x>"))
        self.assertEqual(eval(self.all_constraint.statement.right), "c")
        self.assertEqual(self.all_constraint.bound, NonTerminal("<x>"))
        assert isinstance(self.all_constraint.search, StarSearch)
        assert isinstance(self.all_constraint.search.base, RuleSearch)
        self.assertEqual(self.all_constraint.search.base.symbol, NonTerminal("<b>"))

        # Check expression constraint
        assert isinstance(self.expression_constraint, ComparisonConstraint)
        self.assertEqual(self.expression_constraint.operator, Comparison.EQUAL)
        tmp_var = self.expression_constraint.left
        self.assertTrue(tmp_var.startswith("{str(x) for x in "))
        self.assertTrue(tmp_var.endswith("}"))
        tmp_var = tmp_var[17:-1]  # Remove the prefix and suffix
        self.assertIn(tmp_var, self.expression_constraint.searches)
        search = self.expression_constraint.searches[tmp_var]
        assert isinstance(search, StarSearch)
        assert isinstance(search.base, RuleSearch)
        self.assertEqual(search.base.symbol, NonTerminal("<c>"))
        self.assertEqual(eval(self.expression_constraint.right), {"e", "f"})

    def test_star_constraint_valid(self):
        for constraint in self.constraints:
            self.assertTrue(constraint.check(self.VALID), constraint)

    def test_invalid_a(self):
        self.assertFalse(
            self.any_constraint.check(self.INVALID_A),
            "Invalid <a> should not satisfy the exists constraint",
        )
        self.assertTrue(
            self.all_constraint.check(self.INVALID_A),
            "Invalid <a> should satisfy the forall constraint",
        )
        self.assertTrue(
            self.expression_constraint.check(self.INVALID_A),
            "Invalid <a> should satisfy the expression constraint",
        )

    def test_invalid_b(self):
        self.assertTrue(
            self.any_constraint.check(self.INVALID_B),
            "Invalid <b> should satisfy the exists constraint",
        )
        self.assertFalse(
            self.all_constraint.check(self.INVALID_B),
            "Invalid <b> should not satisfy the forall constraint",
        )
        self.assertTrue(
            self.expression_constraint.check(self.INVALID_B),
            "Invalid <b> should satisfy the expression constraint",
        )

    def test_invalid_c(self):
        self.assertTrue(
            self.any_constraint.check(self.INVALID_C),
            "Invalid <c> should satisfy the exists constraint",
        )
        self.assertTrue(
            self.all_constraint.check(self.INVALID_C),
            "Invalid <c> should satisfy the forall constraint",
        )
        self.assertFalse(
            self.expression_constraint.check(self.INVALID_C),
            "Invalid <c> should not satisfy the expression constraint",
        )


class TestPopulation(unittest.TestCase):
    EXAMPLE = """
<start> ::= <a> <b> <c>
<a> ::= "a" | "b"
<b> ::= "c" | "d"
<c> ::= "e" | "f" | "g" | "h"

where any(<x> == "a" for <x> in **<a>)
where all(<x> == "c" for <x> in **<b>)
where {str(x) for x in **<c>} == {"e", "f"}
"""

    VALID_POPULATION = [
        DerivationTree(
            NonTerminal("<start>"),
            [
                DerivationTree(NonTerminal("<a>"), [DerivationTree(Terminal("a"))]),
                DerivationTree(NonTerminal("<b>"), [DerivationTree(Terminal("c"))]),
                DerivationTree(NonTerminal("<c>"), [DerivationTree(Terminal("f"))]),
            ],
        ),
        DerivationTree(
            NonTerminal("<start>"),
            [
                DerivationTree(NonTerminal("<a>"), [DerivationTree(Terminal("b"))]),
                DerivationTree(NonTerminal("<b>"), [DerivationTree(Terminal("c"))]),
                DerivationTree(NonTerminal("<c>"), [DerivationTree(Terminal("e"))]),
            ],
        ),
    ]

    INVALID_POPULATION_A = [
        DerivationTree(
            NonTerminal("<start>"),
            [
                DerivationTree(NonTerminal("<a>"), [DerivationTree(Terminal("b"))]),
                DerivationTree(NonTerminal("<b>"), [DerivationTree(Terminal("c"))]),
                DerivationTree(NonTerminal("<c>"), [DerivationTree(Terminal("f"))]),
            ],
        ),
        DerivationTree(
            NonTerminal("<start>"),
            [
                DerivationTree(NonTerminal("<a>"), [DerivationTree(Terminal("b"))]),
                DerivationTree(NonTerminal("<b>"), [DerivationTree(Terminal("c"))]),
                DerivationTree(NonTerminal("<c>"), [DerivationTree(Terminal("e"))]),
            ],
        ),
    ]

    INVALID_POPULATION_B = [
        DerivationTree(
            NonTerminal("<start>"),
            [
                DerivationTree(NonTerminal("<a>"), [DerivationTree(Terminal("a"))]),
                DerivationTree(NonTerminal("<b>"), [DerivationTree(Terminal("d"))]),
                DerivationTree(NonTerminal("<c>"), [DerivationTree(Terminal("f"))]),
            ],
        ),
        DerivationTree(
            NonTerminal("<start>"),
            [
                DerivationTree(NonTerminal("<a>"), [DerivationTree(Terminal("b"))]),
                DerivationTree(NonTerminal("<b>"), [DerivationTree(Terminal("c"))]),
                DerivationTree(NonTerminal("<c>"), [DerivationTree(Terminal("e"))]),
            ],
        ),
    ]

    INVALID_POPULATION_C = [
        DerivationTree(
            NonTerminal("<start>"),
            [
                DerivationTree(NonTerminal("<a>"), [DerivationTree(Terminal("a"))]),
                DerivationTree(NonTerminal("<b>"), [DerivationTree(Terminal("c"))]),
                DerivationTree(NonTerminal("<c>"), [DerivationTree(Terminal("e"))]),
            ],
        ),
        DerivationTree(
            NonTerminal("<start>"),
            [
                DerivationTree(NonTerminal("<a>"), [DerivationTree(Terminal("b"))]),
                DerivationTree(NonTerminal("<b>"), [DerivationTree(Terminal("c"))]),
                DerivationTree(NonTerminal("<c>"), [DerivationTree(Terminal("g"))]),
            ],
        ),
    ]

    grammar: Grammar
    constraints: list[Constraint]
    any_constraint: ExistsConstraint
    all_constraint: ForallConstraint
    expression_constraint: ComparisonConstraint

    @classmethod
    def setUpClass(cls):
        grammar, constraints = parse(
            TestPopulation.EXAMPLE, use_stdlib=False, use_cache=False
        )
        for e in constraints:
            assert isinstance(e, Constraint)
        cls.constraints = cast(list[Constraint], constraints)

        assert grammar is not None
        cls.grammar = grammar
        assert isinstance(cls.constraints[0], ExistsConstraint)
        cls.any_constraint = cls.constraints[0]
        assert isinstance(cls.constraints[1], ForallConstraint)
        cls.all_constraint = cls.constraints[1]
        assert isinstance(cls.constraints[2], ComparisonConstraint)
        cls.expression_constraint = cls.constraints[2]

    def test_parse_population_star(self):
        self.assertIsNotNone(self.grammar)
        self.assertIsNotNone(self.constraints)
        self.assertEqual(len(self.grammar.rules), 4)
        self.assertEqual(len(self.constraints), 3)
        self.assertIn("<start>", self.grammar)
        self.assertIn("<a>", self.grammar)
        self.assertIn("<b>", self.grammar)
        self.assertIn("<c>", self.grammar)
        # Check constraints
        # Check exists constraint
        assert isinstance(self.any_constraint, ExistsConstraint)
        assert isinstance(self.any_constraint.statement, ComparisonConstraint)
        self.assertEqual(self.any_constraint.statement.operator, Comparison.EQUAL)
        tmp_var = self.any_constraint.statement.left
        self.assertIn(tmp_var, self.any_constraint.statement.searches)
        rule_search = self.any_constraint.statement.searches[tmp_var]
        assert isinstance(rule_search, RuleSearch)
        self.assertEqual(rule_search.symbol, NonTerminal("<x>"))
        self.assertEqual(eval(self.any_constraint.statement.right), "a")
        self.assertEqual(self.any_constraint.bound, NonTerminal("<x>"))
        assert isinstance(self.any_constraint.search, PopulationSearch)
        assert isinstance(self.any_constraint.search.base, RuleSearch)
        self.assertEqual(self.any_constraint.search.base.symbol, NonTerminal("<a>"))

        # Check forall constraint
        assert isinstance(self.all_constraint, ForallConstraint)
        assert isinstance(self.all_constraint.statement, ComparisonConstraint)
        self.assertEqual(self.all_constraint.statement.operator, Comparison.EQUAL)
        tmp_var = self.all_constraint.statement.left
        self.assertIn(tmp_var, self.all_constraint.statement.searches)
        rule_search = self.all_constraint.statement.searches[tmp_var]
        assert isinstance(rule_search, RuleSearch)
        self.assertEqual(rule_search.symbol, NonTerminal("<x>"))
        self.assertEqual(eval(self.all_constraint.statement.right), "c")
        self.assertEqual(self.all_constraint.bound, NonTerminal("<x>"))
        assert isinstance(self.all_constraint.search, PopulationSearch)
        assert isinstance(self.all_constraint.search.base, RuleSearch)
        self.assertEqual(self.all_constraint.search.base.symbol, NonTerminal("<b>"))

        # Check expression constraint
        assert isinstance(self.expression_constraint, ComparisonConstraint)
        self.assertEqual(self.expression_constraint.operator, Comparison.EQUAL)
        tmp_var = self.expression_constraint.left
        self.assertTrue(tmp_var.startswith("{str(x) for x in "))
        self.assertTrue(tmp_var.endswith("}"))
        tmp_var = tmp_var[17:-1]  # Remove the prefix and suffix
        self.assertIn(tmp_var, self.expression_constraint.searches)
        search = self.expression_constraint.searches[tmp_var]
        assert isinstance(search, PopulationSearch)
        assert isinstance(search.base, RuleSearch)
        self.assertEqual(search.base.symbol, NonTerminal("<c>"))
        self.assertEqual(eval(self.expression_constraint.right), {"e", "f"})

    def test_population_star_constraint_valid(self):
        for constraint in self.constraints:
            for tree in self.VALID_POPULATION:
                self.assertTrue(
                    constraint.check(tree, population=self.VALID_POPULATION), constraint
                )

    def test_invalid_population_a(self):
        for tree in self.INVALID_POPULATION_A:
            self.assertFalse(
                self.any_constraint.check(tree, population=self.INVALID_POPULATION_A),
                "Invalid <a> should not satisfy the exists constraint",
            )
            self.assertTrue(
                self.all_constraint.check(tree, population=self.INVALID_POPULATION_A),
                "Invalid <a> should satisfy the forall constraint",
            )
            self.assertTrue(
                self.expression_constraint.check(
                    tree, population=self.INVALID_POPULATION_A
                ),
                "Invalid <a> should satisfy the expression constraint",
            )

    def test_invalid_population_b(self):
        for tree in self.INVALID_POPULATION_B:
            self.assertTrue(
                self.any_constraint.check(tree, population=self.INVALID_POPULATION_B),
                "Invalid <b> should satisfy the exists constraint",
            )
            self.assertFalse(
                self.all_constraint.check(tree, population=self.INVALID_POPULATION_B),
                "Invalid <b> should not satisfy the forall constraint",
            )
            self.assertTrue(
                self.expression_constraint.check(
                    tree, population=self.INVALID_POPULATION_B
                ),
                "Invalid <b> should satisfy the expression constraint",
            )

    def test_invalid_population_c(self):
        for tree in self.INVALID_POPULATION_C:
            self.assertTrue(
                self.any_constraint.check(tree, population=self.INVALID_POPULATION_C),
                "Invalid <c> should satisfy the exists constraint",
            )
            self.assertTrue(
                self.all_constraint.check(tree, population=self.INVALID_POPULATION_C),
                "Invalid <c> should satisfy the forall constraint",
            )
            self.assertFalse(
                self.expression_constraint.check(
                    tree, population=self.INVALID_POPULATION_C
                ),
                "Invalid <c> should not satisfy the expression constraint",
            )


class TestStarIdentifier(unittest.TestCase):
    EXAMPLE = """
<start> ::= <a> <b> <c> <c>
<a> ::= "a" | "b"
<b> ::= "c" | "d"
<c> ::= "e" | "f" | "g" | "h"

where any(x == "a" for x in *<a>)
where all(x == "c" for x in *<b>)
where {str(x) for x in *<c>} == {"e", "f"}
"""

    grammar: Grammar
    constraints: list[Constraint]
    any_constraint: ExistsConstraint
    all_constraint: ForallConstraint
    expression_constraint: ComparisonConstraint

    @classmethod
    def setUpClass(cls):
        # set parser to python
        # fandango.Fandango.parser = "python"
        grammar, constraints = parse(
            TestStarIdentifier.EXAMPLE, use_stdlib=False, use_cache=False
        )
        for e in constraints:
            assert isinstance(e, Constraint)
        cls.constraints = cast(list[Constraint], constraints)

        assert grammar is not None
        cls.grammar = grammar

        assert isinstance(cls.constraints[0], ExistsConstraint)
        cls.any_constraint = cls.constraints[0]
        assert isinstance(cls.constraints[1], ForallConstraint)
        cls.all_constraint = cls.constraints[1]
        assert isinstance(cls.constraints[2], ComparisonConstraint)
        cls.expression_constraint = cls.constraints[2]

    def test_parse_star(self):
        self.assertIsNotNone(self.grammar)
        self.assertIsNotNone(self.constraints)
        self.assertEqual(len(self.grammar.rules), 4)
        self.assertEqual(len(self.constraints), 3)
        self.assertIn("<start>", self.grammar)
        self.assertIn("<a>", self.grammar)
        self.assertIn("<b>", self.grammar)
        self.assertIn("<c>", self.grammar)
        # Check constraints
        # Check exists constraint
        assert isinstance(self.any_constraint, ExistsConstraint)
        assert isinstance(self.any_constraint.statement, ComparisonConstraint)
        self.assertEqual(self.any_constraint.statement.operator, Comparison.EQUAL)
        tmp_var = self.any_constraint.statement.left
        self.assertNotIn(tmp_var, self.any_constraint.statement.searches)
        self.assertEqual(eval(self.any_constraint.statement.right), "a")
        self.assertEqual(self.any_constraint.bound, "x")
        self.assertEqual(tmp_var, self.any_constraint.bound)
        assert isinstance(self.any_constraint.search, StarSearch)
        assert isinstance(self.any_constraint.search.base, RuleSearch)
        self.assertEqual(self.any_constraint.search.base.symbol, NonTerminal("<a>"))

        # Check forall constraint
        assert isinstance(self.all_constraint, ForallConstraint)
        assert isinstance(self.all_constraint.statement, ComparisonConstraint)
        self.assertEqual(self.all_constraint.statement.operator, Comparison.EQUAL)
        tmp_var = self.all_constraint.statement.left
        self.assertNotIn(tmp_var, self.all_constraint.statement.searches)
        self.assertEqual(eval(self.all_constraint.statement.right), "c")
        self.assertEqual(self.all_constraint.bound, "x")
        self.assertEqual(tmp_var, self.all_constraint.bound)
        assert isinstance(self.all_constraint.search, StarSearch)
        assert isinstance(self.all_constraint.search.base, RuleSearch)
        self.assertEqual(self.all_constraint.search.base.symbol, NonTerminal("<b>"))

        # Check expression constraint
        assert isinstance(self.expression_constraint, ComparisonConstraint)
        self.assertEqual(self.expression_constraint.operator, Comparison.EQUAL)
        tmp_var = self.expression_constraint.left
        self.assertTrue(tmp_var.startswith("{str(x) for x in "))
        self.assertTrue(tmp_var.endswith("}"))
        tmp_var = tmp_var[17:-1]  # Remove the prefix and suffix
        self.assertIn(tmp_var, self.expression_constraint.searches)
        search = self.expression_constraint.searches[tmp_var]
        assert isinstance(search, StarSearch)
        assert isinstance(search.base, RuleSearch)
        self.assertEqual(search.base.symbol, NonTerminal("<c>"))
        self.assertEqual(eval(self.expression_constraint.right), {"e", "f"})

    def test_star_constraint_valid(self):
        for constraint in self.constraints:
            self.assertTrue(constraint.check(TestStar.VALID), constraint)

    def test_invalid_a(self):
        self.assertFalse(
            self.any_constraint.check(TestStar.INVALID_A),
            "Invalid <a> should not satisfy the exists constraint",
        )
        self.assertTrue(
            self.all_constraint.check(TestStar.INVALID_A),
            "Invalid <a> should satisfy the forall constraint",
        )
        self.assertTrue(
            self.expression_constraint.check(TestStar.INVALID_A),
            "Invalid <a> should satisfy the expression constraint",
        )

    def test_invalid_b(self):
        self.assertTrue(
            self.any_constraint.check(TestStar.INVALID_B),
            "Invalid <b> should satisfy the exists constraint",
        )
        self.assertFalse(
            self.all_constraint.check(TestStar.INVALID_B),
            "Invalid <b> should not satisfy the forall constraint",
        )
        self.assertTrue(
            self.expression_constraint.check(TestStar.INVALID_B),
            "Invalid <b> should satisfy the expression constraint",
        )

    def test_invalid_c(self):
        self.assertTrue(
            self.any_constraint.check(TestStar.INVALID_C),
            "Invalid <c> should satisfy the exists constraint",
        )
        self.assertTrue(
            self.all_constraint.check(TestStar.INVALID_C),
            "Invalid <c> should satisfy the forall constraint",
        )
        self.assertFalse(
            self.expression_constraint.check(TestStar.INVALID_C),
            "Invalid <c> should not satisfy the expression constraint",
        )


class TestPopulationIdentifier(unittest.TestCase):
    EXAMPLE = """
<start> ::= <a> <b> <c>
<a> ::= "a" | "b"
<b> ::= "c" | "d"
<c> ::= "e" | "f" | "g" | "h"

where any(x == "a" for x in **<a>)
where all(x == "c" for x in **<b>)
where {str(x) for x in **<c>} == {"e", "f"}
"""
    any_constraint: ExistsConstraint
    all_constraint: ForallConstraint
    expression_constraint: ComparisonConstraint
    grammar: Grammar
    constraints: list[Constraint]

    @classmethod
    def setUpClass(cls):
        grammar, constraints = parse(cls.EXAMPLE, use_stdlib=False, use_cache=False)
        for e in constraints:
            assert isinstance(e, Constraint)
        cls.constraints = cast(list[Constraint], constraints)
        assert grammar is not None
        cls.grammar = grammar

        assert len(cls.constraints) == 3
        assert isinstance(cls.constraints[0], ExistsConstraint)
        assert isinstance(cls.constraints[1], ForallConstraint)
        assert isinstance(cls.constraints[2], ComparisonConstraint)
        cls.any_constraint = cls.constraints[0]
        cls.all_constraint = cls.constraints[1]
        cls.expression_constraint = cls.constraints[2]

    def test_parse_population_star(self):
        self.assertIsNotNone(self.grammar)
        self.assertIsNotNone(self.constraints)
        self.assertEqual(len(self.grammar.rules), 4)
        self.assertEqual(len(self.constraints), 3)
        self.assertIn("<start>", self.grammar)
        self.assertIn("<a>", self.grammar)
        self.assertIn("<b>", self.grammar)
        self.assertIn("<c>", self.grammar)
        # Check constraints
        # Check exists constraint
        assert isinstance(self.any_constraint, ExistsConstraint)
        assert isinstance(self.any_constraint.statement, ComparisonConstraint)
        self.assertEqual(self.any_constraint.statement.operator, Comparison.EQUAL)
        tmp_var = self.any_constraint.statement.left
        self.assertNotIn(tmp_var, self.any_constraint.statement.searches)
        self.assertEqual(eval(self.any_constraint.statement.right), "a")
        self.assertEqual(self.any_constraint.bound, "x")
        self.assertEqual(tmp_var, self.any_constraint.bound)
        assert isinstance(self.any_constraint.search, PopulationSearch)
        assert isinstance(self.any_constraint.search.base, RuleSearch)
        self.assertEqual(self.any_constraint.search.base.symbol, NonTerminal("<a>"))

        # Check forall constraint
        assert isinstance(self.all_constraint, ForallConstraint)
        assert isinstance(self.all_constraint.statement, ComparisonConstraint)
        self.assertEqual(self.all_constraint.statement.operator, Comparison.EQUAL)
        tmp_var = self.all_constraint.statement.left
        self.assertNotIn(tmp_var, self.all_constraint.statement.searches)
        self.assertEqual(eval(self.all_constraint.statement.right), "c")
        self.assertEqual(self.all_constraint.bound, "x")
        self.assertEqual(tmp_var, self.all_constraint.bound)
        assert isinstance(self.all_constraint.search, PopulationSearch)
        assert isinstance(self.all_constraint.search.base, RuleSearch)
        self.assertEqual(self.all_constraint.search.base.symbol, NonTerminal("<b>"))

        # Check expression constraint
        assert isinstance(self.expression_constraint, ComparisonConstraint)
        self.assertEqual(self.expression_constraint.operator, Comparison.EQUAL)
        tmp_var = self.expression_constraint.left
        self.assertTrue(tmp_var.startswith("{str(x) for x in "))
        self.assertTrue(tmp_var.endswith("}"))
        tmp_var = tmp_var[17:-1]  # Remove the prefix and suffix
        self.assertIn(tmp_var, self.expression_constraint.searches)
        search = self.expression_constraint.searches[tmp_var]
        assert isinstance(search, PopulationSearch)
        assert isinstance(search.base, RuleSearch)
        self.assertEqual(search.base.symbol, NonTerminal("<c>"))
        self.assertEqual(eval(self.expression_constraint.right), {"e", "f"})

    def test_population_star_constraint_valid(self):
        for constraint in self.constraints:
            for tree in TestPopulation.VALID_POPULATION:
                self.assertTrue(
                    constraint.check(tree, population=TestPopulation.VALID_POPULATION),
                    constraint,
                )

    def test_invalid_population_a(self):
        for tree in TestPopulation.INVALID_POPULATION_A:
            self.assertFalse(
                self.any_constraint.check(
                    tree, population=TestPopulation.INVALID_POPULATION_A
                ),
                "Invalid <a> should not satisfy the exists constraint",
            )
            self.assertTrue(
                self.all_constraint.check(
                    tree, population=TestPopulation.INVALID_POPULATION_A
                ),
                "Invalid <a> should satisfy the forall constraint",
            )
            self.assertTrue(
                self.expression_constraint.check(
                    tree, population=TestPopulation.INVALID_POPULATION_A
                ),
                "Invalid <a> should satisfy the expression constraint",
            )

    def test_invalid_population_b(self):
        for tree in TestPopulation.INVALID_POPULATION_B:
            self.assertTrue(
                self.any_constraint.check(
                    tree, population=TestPopulation.INVALID_POPULATION_B
                ),
                "Invalid <b> should satisfy the exists constraint",
            )
            self.assertFalse(
                self.all_constraint.check(
                    tree, population=TestPopulation.INVALID_POPULATION_B
                ),
                "Invalid <b> should not satisfy the forall constraint",
            )
            self.assertTrue(
                self.expression_constraint.check(
                    tree, population=TestPopulation.INVALID_POPULATION_B
                ),
                "Invalid <b> should satisfy the expression constraint",
            )

    def test_invalid_population_c(self):
        for tree in TestPopulation.INVALID_POPULATION_C:
            self.assertTrue(
                self.any_constraint.check(
                    tree, population=TestPopulation.INVALID_POPULATION_C
                ),
                "Invalid <c> should satisfy the exists constraint",
            )
            self.assertTrue(
                self.all_constraint.check(
                    tree, population=TestPopulation.INVALID_POPULATION_C
                ),
                "Invalid <c> should satisfy the forall constraint",
            )
            self.assertFalse(
                self.expression_constraint.check(
                    tree, population=TestPopulation.INVALID_POPULATION_C
                ),
                "Invalid <c> should not satisfy the expression constraint",
            )


class TestStarInCombination(unittest.TestCase):
    EXAMPLE = "\n".join(
        [
            "<start> ::= <a>",
            "<a> ::= <b> | <c>",
            "<b> ::= <d> | <e>",
            "<c> ::= <e> <d>",
            '<d> ::= "d"',
            '<e> ::= "e"',
        ]
    )

    CONSTRAINT_DOT = "where all(str(x) == 'd' for x in *<a>.<b>)"
    CONSTRAINT_DOT_DOT = "where all(str(x) == 'd' for x in *<start>..<b>)"
    CONSTRAINT_POPULATION_DOT = "where all(str(x) == 'd' for x in **<a>.<b>)"
    CONSTRAINT_POPULATION_DOT_DOT = "where all(str(x) == 'd' for x in **<start>..<b>)"

    EXAMPLE_1 = DerivationTree(
        NonTerminal("<start>"),
        [
            DerivationTree(
                NonTerminal("<a>"),
                [
                    DerivationTree(
                        NonTerminal("<b>"),
                        [
                            DerivationTree(
                                NonTerminal("<d>"),
                                [
                                    DerivationTree(Terminal("d")),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )

    EXAMPLE_2 = DerivationTree(
        NonTerminal("<start>"),
        [
            DerivationTree(
                NonTerminal("<a>"),
                [
                    DerivationTree(
                        NonTerminal("<b>"),
                        [
                            DerivationTree(
                                NonTerminal("<e>"),
                                [
                                    DerivationTree(
                                        Terminal("e"),
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )

    EXAMPLE_3 = DerivationTree(
        NonTerminal("<start>"),
        [
            DerivationTree(
                NonTerminal("<a>"),
                [
                    DerivationTree(
                        NonTerminal("<c>"),
                        [
                            DerivationTree(
                                NonTerminal("<e>"),
                                [
                                    DerivationTree(
                                        Terminal("e"),
                                    )
                                ],
                            ),
                            DerivationTree(
                                NonTerminal("<d>"),
                                [
                                    DerivationTree(
                                        Terminal("d"),
                                    )
                                ],
                            ),
                        ],
                    )
                ],
            )
        ],
    )

    grammar: Grammar

    @classmethod
    def setUpClass(cls):
        grammar, _ = parse(cls.EXAMPLE, use_cache=False, use_stdlib=False)
        assert grammar is not None
        cls.grammar = grammar

    def test_dot(self):
        _, constraints = parse(self.CONSTRAINT_DOT, use_cache=False, use_stdlib=False)
        self.assertEqual(len(constraints), 1)
        constraint = constraints[0]
        assert isinstance(constraint, ForallConstraint)
        self.assertEqual(constraint.bound, "x")
        statement = constraint.statement
        assert isinstance(statement, ComparisonConstraint)
        self.assertEqual(statement.left, "str(x)")
        self.assertEqual(eval(statement.right), "d")
        star = constraint.search
        assert isinstance(star, StarSearch)
        base = star.base
        assert isinstance(base, AttributeSearch)
        parent = base.base
        assert isinstance(parent, RuleSearch)
        self.assertEqual(parent.symbol, NonTerminal("<a>"))
        attribute = base.attribute
        assert isinstance(attribute, RuleSearch)
        self.assertEqual(attribute.symbol, NonTerminal("<b>"))

        self.assertTrue(constraint.check(self.EXAMPLE_1))
        self.assertFalse(constraint.check(self.EXAMPLE_2))
        self.assertTrue(constraint.check(self.EXAMPLE_3))

    def test_dot_dot(self):
        _, constraints = parse(
            self.CONSTRAINT_DOT_DOT, use_cache=False, use_stdlib=False
        )
        self.assertEqual(len(constraints), 1)
        constraint = constraints[0]
        assert isinstance(constraint, ForallConstraint)
        self.assertEqual(constraint.bound, "x")
        statement = constraint.statement
        assert isinstance(statement, ComparisonConstraint)
        self.assertEqual(statement.left, "str(x)")
        self.assertEqual(eval(statement.right), "d")
        star = constraint.search
        assert isinstance(star, StarSearch)
        base = star.base
        assert isinstance(base, DescendantAttributeSearch)
        parent = base.base
        assert isinstance(parent, RuleSearch)
        self.assertEqual(parent.symbol, NonTerminal("<start>"))
        attribute = base.attribute
        assert isinstance(attribute, RuleSearch)
        self.assertEqual(attribute.symbol, NonTerminal("<b>"))

        self.assertTrue(constraint.check(self.EXAMPLE_1))
        self.assertFalse(constraint.check(self.EXAMPLE_2))
        self.assertTrue(constraint.check(self.EXAMPLE_3))

    def test_population_dot(self):
        _, constraints = parse(
            self.CONSTRAINT_POPULATION_DOT, use_cache=False, use_stdlib=False
        )
        self.assertEqual(len(constraints), 1)
        constraint = constraints[0]
        assert isinstance(constraint, ForallConstraint)
        self.assertEqual(constraint.bound, "x")
        statement = constraint.statement
        assert isinstance(statement, ComparisonConstraint)
        self.assertEqual(statement.left, "str(x)")
        self.assertEqual(eval(statement.right), "d")
        star = constraint.search
        assert isinstance(star, PopulationSearch)
        base = star.base
        assert isinstance(base, AttributeSearch)
        parent = base.base
        assert isinstance(parent, RuleSearch)
        self.assertEqual(parent.symbol, NonTerminal("<a>"))
        attribute = base.attribute
        assert isinstance(attribute, RuleSearch)
        self.assertEqual(attribute.symbol, NonTerminal("<b>"))

        self.assertFalse(
            constraint.check(
                self.EXAMPLE_1,
                population=[self.EXAMPLE_1, self.EXAMPLE_2, self.EXAMPLE_3],
            )
        )
        self.assertTrue(
            constraint.check(
                self.EXAMPLE_1,
                population=[self.EXAMPLE_1, self.EXAMPLE_1, self.EXAMPLE_3],
            )
        )

    def test_population_dot_dot(self):
        _, constraints = parse(
            self.CONSTRAINT_POPULATION_DOT_DOT, use_cache=False, use_stdlib=False
        )
        self.assertEqual(len(constraints), 1)
        constraint = constraints[0]
        assert isinstance(constraint, ForallConstraint)
        self.assertEqual(constraint.bound, "x")
        statement = constraint.statement
        assert isinstance(statement, ComparisonConstraint)
        self.assertEqual(statement.left, "str(x)")
        self.assertEqual(eval(statement.right), "d")
        star = constraint.search
        assert isinstance(star, PopulationSearch)
        base = star.base
        assert isinstance(base, DescendantAttributeSearch)
        parent = base.base
        assert isinstance(parent, RuleSearch)
        self.assertEqual(parent.symbol, NonTerminal("<start>"))
        attribute = base.attribute
        assert isinstance(attribute, RuleSearch)
        self.assertEqual(attribute.symbol, NonTerminal("<b>"))

        self.assertFalse(
            constraint.check(
                self.EXAMPLE_1,
                population=[self.EXAMPLE_1, self.EXAMPLE_2, self.EXAMPLE_3],
            )
        )
        self.assertTrue(
            constraint.check(
                self.EXAMPLE_1, population=[self.EXAMPLE_1, self.EXAMPLE_3]
            )
        )
