import unittest

from fandango import parse
from fandango.constraints.base import (
    ExistsConstraint,
    ForallConstraint,
    ComparisonConstraint,
)
from fandango.constraints.fitness import Comparison
from fandango.language import NonTerminal, DerivationTree, Terminal
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

    @classmethod
    def setUpClass(cls):
        # set parser to python
        # fandango.Fandango.parser = "python"
        cls.grammar, cls.constraints = parse(
            TestStar.EXAMPLE, use_stdlib=False, use_cache=False
        )
        cls.any_constraint = cls.constraints[0]
        cls.all_constraint = cls.constraints[1]
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
        self.assertIsInstance(self.any_constraint, ExistsConstraint)
        self.assertIsInstance(self.any_constraint.statement, ComparisonConstraint)
        self.assertEqual(self.any_constraint.statement.operator, Comparison.EQUAL)
        tmp_var = self.any_constraint.statement.left
        self.assertIn(tmp_var, self.any_constraint.statement.searches)
        self.assertIsInstance(
            self.any_constraint.statement.searches[tmp_var], RuleSearch
        )
        self.assertEqual(
            self.any_constraint.statement.searches[tmp_var].symbol, NonTerminal("<x>")
        )
        self.assertEqual(eval(self.any_constraint.statement.right), "a")
        self.assertEqual(self.any_constraint.bound, NonTerminal("<x>"))
        self.assertIsInstance(self.any_constraint.search, StarSearch)
        self.assertIsInstance(self.any_constraint.search.base, RuleSearch)
        self.assertEqual(self.any_constraint.search.base.symbol, NonTerminal("<a>"))

        # Check forall constraint
        self.assertIsInstance(self.all_constraint, ForallConstraint)
        self.assertIsInstance(self.all_constraint.statement, ComparisonConstraint)
        self.assertEqual(self.all_constraint.statement.operator, Comparison.EQUAL)
        tmp_var = self.all_constraint.statement.left
        self.assertIn(tmp_var, self.all_constraint.statement.searches)
        self.assertIsInstance(
            self.all_constraint.statement.searches[tmp_var], RuleSearch
        )
        self.assertEqual(
            self.all_constraint.statement.searches[tmp_var].symbol, NonTerminal("<x>")
        )
        self.assertEqual(eval(self.all_constraint.statement.right), "c")
        self.assertEqual(self.all_constraint.bound, NonTerminal("<x>"))
        self.assertIsInstance(self.all_constraint.search, StarSearch)
        self.assertIsInstance(self.all_constraint.search.base, RuleSearch)
        self.assertEqual(self.all_constraint.search.base.symbol, NonTerminal("<b>"))

        # Check expression constraint
        self.assertIsInstance(self.expression_constraint, ComparisonConstraint)
        self.assertEqual(self.expression_constraint.operator, Comparison.EQUAL)
        tmp_var = self.expression_constraint.left
        self.assertTrue(tmp_var.startswith("{str(x) for x in "))
        self.assertTrue(tmp_var.endswith("}"))
        tmp_var = tmp_var[17:-1]  # Remove the prefix and suffix
        self.assertIn(tmp_var, self.expression_constraint.searches)
        search = self.expression_constraint.searches[tmp_var]
        self.assertIsInstance(search, StarSearch)
        self.assertIsInstance(search.base, RuleSearch)
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

    @classmethod
    def setUpClass(cls):
        cls.grammar, cls.constraints = parse(
            TestPopulation.EXAMPLE, use_stdlib=False, use_cache=False
        )
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
        self.assertIsInstance(self.any_constraint, ExistsConstraint)
        self.assertIsInstance(self.any_constraint.statement, ComparisonConstraint)
        self.assertEqual(self.any_constraint.statement.operator, Comparison.EQUAL)
        tmp_var = self.any_constraint.statement.left
        self.assertIn(tmp_var, self.any_constraint.statement.searches)
        self.assertIsInstance(
            self.any_constraint.statement.searches[tmp_var], RuleSearch
        )
        self.assertEqual(
            self.any_constraint.statement.searches[tmp_var].symbol, NonTerminal("<x>")
        )
        self.assertEqual(eval(self.any_constraint.statement.right), "a")
        self.assertEqual(self.any_constraint.bound, NonTerminal("<x>"))
        self.assertIsInstance(self.any_constraint.search, PopulationSearch)
        self.assertIsInstance(self.any_constraint.search.base, RuleSearch)
        self.assertEqual(self.any_constraint.search.base.symbol, NonTerminal("<a>"))

        # Check forall constraint
        self.assertIsInstance(self.all_constraint, ForallConstraint)
        self.assertIsInstance(self.all_constraint.statement, ComparisonConstraint)
        self.assertEqual(self.all_constraint.statement.operator, Comparison.EQUAL)
        tmp_var = self.all_constraint.statement.left
        self.assertIn(tmp_var, self.all_constraint.statement.searches)
        self.assertIsInstance(
            self.all_constraint.statement.searches[tmp_var], RuleSearch
        )
        self.assertEqual(
            self.all_constraint.statement.searches[tmp_var].symbol, NonTerminal("<x>")
        )
        self.assertEqual(eval(self.all_constraint.statement.right), "c")
        self.assertEqual(self.all_constraint.bound, NonTerminal("<x>"))
        self.assertIsInstance(self.all_constraint.search, PopulationSearch)
        self.assertIsInstance(self.all_constraint.search.base, RuleSearch)
        self.assertEqual(self.all_constraint.search.base.symbol, NonTerminal("<b>"))

        # Check expression constraint
        self.assertIsInstance(self.expression_constraint, ComparisonConstraint)
        self.assertEqual(self.expression_constraint.operator, Comparison.EQUAL)
        tmp_var = self.expression_constraint.left
        self.assertTrue(tmp_var.startswith("{str(x) for x in "))
        self.assertTrue(tmp_var.endswith("}"))
        tmp_var = tmp_var[17:-1]  # Remove the prefix and suffix
        self.assertIn(tmp_var, self.expression_constraint.searches)
        search = self.expression_constraint.searches[tmp_var]
        self.assertIsInstance(search, PopulationSearch)
        self.assertIsInstance(search.base, RuleSearch)
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

    @classmethod
    def setUpClass(cls):
        # set parser to python
        # fandango.Fandango.parser = "python"
        cls.grammar, cls.constraints = parse(
            TestStarIdentifier.EXAMPLE, use_stdlib=False, use_cache=False
        )
        cls.any_constraint = cls.constraints[0]
        cls.all_constraint = cls.constraints[1]
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
        self.assertIsInstance(self.any_constraint, ExistsConstraint)
        self.assertIsInstance(self.any_constraint.statement, ComparisonConstraint)
        self.assertEqual(self.any_constraint.statement.operator, Comparison.EQUAL)
        tmp_var = self.any_constraint.statement.left
        self.assertNotIn(tmp_var, self.any_constraint.statement.searches)
        self.assertEqual(eval(self.any_constraint.statement.right), "a")
        self.assertEqual(self.any_constraint.bound, "x")
        self.assertEqual(tmp_var, self.any_constraint.bound)
        self.assertIsInstance(self.any_constraint.search, StarSearch)
        self.assertIsInstance(self.any_constraint.search.base, RuleSearch)
        self.assertEqual(self.any_constraint.search.base.symbol, NonTerminal("<a>"))

        # Check forall constraint
        self.assertIsInstance(self.all_constraint, ForallConstraint)
        self.assertIsInstance(self.all_constraint.statement, ComparisonConstraint)
        self.assertEqual(self.all_constraint.statement.operator, Comparison.EQUAL)
        tmp_var = self.all_constraint.statement.left
        self.assertNotIn(tmp_var, self.all_constraint.statement.searches)
        self.assertEqual(eval(self.all_constraint.statement.right), "c")
        self.assertEqual(self.all_constraint.bound, "x")
        self.assertEqual(tmp_var, self.all_constraint.bound)
        self.assertIsInstance(self.all_constraint.search, StarSearch)
        self.assertIsInstance(self.all_constraint.search.base, RuleSearch)
        self.assertEqual(self.all_constraint.search.base.symbol, NonTerminal("<b>"))

        # Check expression constraint
        self.assertIsInstance(self.expression_constraint, ComparisonConstraint)
        self.assertEqual(self.expression_constraint.operator, Comparison.EQUAL)
        tmp_var = self.expression_constraint.left
        self.assertTrue(tmp_var.startswith("{str(x) for x in "))
        self.assertTrue(tmp_var.endswith("}"))
        tmp_var = tmp_var[17:-1]  # Remove the prefix and suffix
        self.assertIn(tmp_var, self.expression_constraint.searches)
        search = self.expression_constraint.searches[tmp_var]
        self.assertIsInstance(search, StarSearch)
        self.assertIsInstance(search.base, RuleSearch)
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

    @classmethod
    def setUpClass(cls):
        cls.grammar, cls.constraints = parse(
            cls.EXAMPLE, use_stdlib=False, use_cache=False
        )
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
        self.assertIsInstance(self.any_constraint, ExistsConstraint)
        self.assertIsInstance(self.any_constraint.statement, ComparisonConstraint)
        self.assertEqual(self.any_constraint.statement.operator, Comparison.EQUAL)
        tmp_var = self.any_constraint.statement.left
        self.assertNotIn(tmp_var, self.any_constraint.statement.searches)
        self.assertEqual(eval(self.any_constraint.statement.right), "a")
        self.assertEqual(self.any_constraint.bound, "x")
        self.assertEqual(tmp_var, self.any_constraint.bound)
        self.assertIsInstance(self.any_constraint.search, PopulationSearch)
        self.assertIsInstance(self.any_constraint.search.base, RuleSearch)
        self.assertEqual(self.any_constraint.search.base.symbol, NonTerminal("<a>"))

        # Check forall constraint
        self.assertIsInstance(self.all_constraint, ForallConstraint)
        self.assertIsInstance(self.all_constraint.statement, ComparisonConstraint)
        self.assertEqual(self.all_constraint.statement.operator, Comparison.EQUAL)
        tmp_var = self.all_constraint.statement.left
        self.assertNotIn(tmp_var, self.all_constraint.statement.searches)
        self.assertEqual(eval(self.all_constraint.statement.right), "c")
        self.assertEqual(self.all_constraint.bound, "x")
        self.assertEqual(tmp_var, self.all_constraint.bound)
        self.assertIsInstance(self.all_constraint.search, PopulationSearch)
        self.assertIsInstance(self.all_constraint.search.base, RuleSearch)
        self.assertEqual(self.all_constraint.search.base.symbol, NonTerminal("<b>"))

        # Check expression constraint
        self.assertIsInstance(self.expression_constraint, ComparisonConstraint)
        self.assertEqual(self.expression_constraint.operator, Comparison.EQUAL)
        tmp_var = self.expression_constraint.left
        self.assertTrue(tmp_var.startswith("{str(x) for x in "))
        self.assertTrue(tmp_var.endswith("}"))
        tmp_var = tmp_var[17:-1]  # Remove the prefix and suffix
        self.assertIn(tmp_var, self.expression_constraint.searches)
        search = self.expression_constraint.searches[tmp_var]
        self.assertIsInstance(search, PopulationSearch)
        self.assertIsInstance(search.base, RuleSearch)
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

    @classmethod
    def setUpClass(cls):
        cls.grammar, _ = parse(cls.EXAMPLE, use_cache=False, use_stdlib=False)

    def test_dot(self):
        _, constraints = parse(self.CONSTRAINT_DOT, use_cache=False, use_stdlib=False)
        self.assertEqual(len(constraints), 1)
        constraint = constraints[0]
        self.assertIsInstance(constraint, ForallConstraint)
        self.assertEqual(constraint.bound, "x")
        statement = constraint.statement
        self.assertIsInstance(statement, ComparisonConstraint)
        self.assertEqual(statement.left, "str(x)")
        self.assertEqual(eval(statement.right), "d")
        star = constraint.search
        self.assertIsInstance(star, StarSearch)
        base = star.base
        self.assertIsInstance(base, AttributeSearch)
        parent = base.base
        self.assertIsInstance(parent, RuleSearch)
        self.assertEqual(parent.symbol, NonTerminal("<a>"))
        attribute = base.attribute
        self.assertIsInstance(attribute, RuleSearch)
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
        self.assertIsInstance(constraint, ForallConstraint)
        self.assertEqual(constraint.bound, "x")
        statement = constraint.statement
        self.assertIsInstance(statement, ComparisonConstraint)
        self.assertEqual(statement.left, "str(x)")
        self.assertEqual(eval(statement.right), "d")
        star = constraint.search
        self.assertIsInstance(star, StarSearch)
        base = star.base
        self.assertIsInstance(base, DescendantAttributeSearch)
        parent = base.base
        self.assertIsInstance(parent, RuleSearch)
        self.assertEqual(parent.symbol, NonTerminal("<start>"))
        attribute = base.attribute
        self.assertIsInstance(attribute, RuleSearch)
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
        self.assertIsInstance(constraint, ForallConstraint)
        self.assertEqual(constraint.bound, "x")
        statement = constraint.statement
        self.assertIsInstance(statement, ComparisonConstraint)
        self.assertEqual(statement.left, "str(x)")
        self.assertEqual(eval(statement.right), "d")
        star = constraint.search
        self.assertIsInstance(star, PopulationSearch)
        base = star.base
        self.assertIsInstance(base, AttributeSearch)
        parent = base.base
        self.assertIsInstance(parent, RuleSearch)
        self.assertEqual(parent.symbol, NonTerminal("<a>"))
        attribute = base.attribute
        self.assertIsInstance(attribute, RuleSearch)
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
        self.assertIsInstance(constraint, ForallConstraint)
        self.assertEqual(constraint.bound, "x")
        statement = constraint.statement
        self.assertIsInstance(statement, ComparisonConstraint)
        self.assertEqual(statement.left, "str(x)")
        self.assertEqual(eval(statement.right), "d")
        star = constraint.search
        self.assertIsInstance(star, PopulationSearch)
        base = star.base
        self.assertIsInstance(base, DescendantAttributeSearch)
        parent = base.base
        self.assertIsInstance(parent, RuleSearch)
        self.assertEqual(parent.symbol, NonTerminal("<start>"))
        attribute = base.attribute
        self.assertIsInstance(attribute, RuleSearch)
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
