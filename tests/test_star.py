import unittest

from fandango import parse
from fandango.constraints.base import (
    ExistsConstraint,
    ForallConstraint,
    ComparisonConstraint,
)
from fandango.constraints.fitness import Comparison
from fandango.language import NonTerminal
from fandango.language.search import StarSearch, RuleSearch


class TestStar(unittest.TestCase):
    EXAMPLE = """
<start> ::= <a> <b> <c> <c>
<a> ::= "a" | "b"
<b> ::= "c" | "d"
<c> ::= "e" | "f" | "g" | "h"

where any(<x> == "a" for <x> in *<a>)
where all(<x> == "c" for <x> in *<b>)
where *<c> == ["a", "b"]
"""

    @classmethod
    def setUpClass(cls):
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
        self.assertIn(tmp_var, self.expression_constraint.searches)
        search = self.expression_constraint.searches[tmp_var]
        self.assertIsInstance(search, StarSearch)
        self.assertIsInstance(search.base, RuleSearch)
        self.assertEqual(search.base.symbol, NonTerminal("<c>"))
        self.assertEqual(eval(self.expression_constraint.right), ["a", "b"])
