#!/usr/bin/env pytest

import unittest

from fandango.language.search import (
    RuleSearch,
    AttributeSearch,
    ItemSearch,
    SelectiveSearch,
    DescendantAttributeSearch,
    PopulationSearch,
    StarSearch,
)
from fandango.language.symbol import NonTerminal, Terminal
from fandango.language.tree import DerivationTree


class TestSearches(unittest.TestCase):
    _0 = DerivationTree(Terminal("0"))
    _1 = DerivationTree(Terminal("1"))
    _C1 = DerivationTree(NonTerminal("<c>"), [_0])
    _C2 = DerivationTree(NonTerminal("<c>"), [_1])
    _B1 = DerivationTree(
        NonTerminal("<b>"),
        [_C1],
    )
    _B2 = DerivationTree(
        NonTerminal("<b>"),
        [_C2],
    )
    _D = DerivationTree(NonTerminal("<d>"), [_B2])

    _A = DerivationTree(NonTerminal("<a>"), [_B1, _D])
    EXAMPLE = _A

    _C3 = DerivationTree(NonTerminal("<c>"), [_0, _1])

    def test_rule_find_a(self):
        search = RuleSearch(NonTerminal("<a>"))
        trees = [c.evaluate() for c in search.find(self.EXAMPLE)]
        self.assertEqual(1, len(trees))
        self.assertEqual(self._A, trees[0])

    def test_rule_find_b(self):
        search = RuleSearch(NonTerminal("<b>"))
        trees = [c.evaluate() for c in search.find(self.EXAMPLE)]
        self.assertEqual(2, len(trees))
        self.assertIn(self._B1, trees)
        self.assertIn(self._B2, trees)

    def test_rule_find_c(self):
        search = RuleSearch(NonTerminal("<c>"))
        trees = [c.evaluate() for c in search.find(self.EXAMPLE)]
        self.assertEqual(2, len(trees))
        self.assertIn(self._C1, trees)
        self.assertIn(self._C2, trees)

    def test_rule_find_d(self):
        search = RuleSearch(NonTerminal("<d>"))
        trees = [c.evaluate() for c in search.find(self.EXAMPLE)]
        self.assertEqual(1, len(trees))
        self.assertEqual(self._D, trees[0])

    def test_rule_find_bc(self):
        search = AttributeSearch(
            RuleSearch(NonTerminal("<b>")), RuleSearch(NonTerminal("<c>"))
        )
        trees = [c.evaluate() for c in search.find(self.EXAMPLE)]
        self.assertEqual(2, len(trees))
        self.assertIn(self._C1, trees)
        self.assertIn(self._C2, trees)

    def test_rule_find_db(self):
        search = AttributeSearch(
            RuleSearch(NonTerminal("<d>")), RuleSearch(NonTerminal("<b>"))
        )
        trees = [c.evaluate() for c in search.find(self.EXAMPLE)]
        self.assertEqual(1, len(trees))
        self.assertIn(self._B2, trees)

    def test_rule_find_ab(self):
        search = AttributeSearch(
            RuleSearch(NonTerminal("<a>")), RuleSearch(NonTerminal("<b>"))
        )
        trees = [c.evaluate() for c in search.find(self.EXAMPLE)]
        self.assertEqual(1, len(trees))
        self.assertIn(self._B1, trees)

    def test_rule_find_ad(self):
        search = AttributeSearch(
            RuleSearch(NonTerminal("<a>")), RuleSearch(NonTerminal("<d>"))
        )
        trees = [c.evaluate() for c in search.find(self.EXAMPLE)]
        self.assertEqual(1, len(trees))
        self.assertIn(self._D, trees)

    def test_rule_find_abc(self):
        search = AttributeSearch(
            AttributeSearch(
                RuleSearch(NonTerminal("<a>")), RuleSearch(NonTerminal("<b>"))
            ),
            RuleSearch(NonTerminal("<c>")),
        )
        trees = [c.evaluate() for c in search.find(self.EXAMPLE)]
        self.assertEqual(1, len(trees))
        self.assertIn(self._C1, trees)

    def test_rule_find_adb(self):
        search = AttributeSearch(
            AttributeSearch(
                RuleSearch(NonTerminal("<a>")), RuleSearch(NonTerminal("<d>"))
            ),
            RuleSearch(NonTerminal("<b>")),
        )
        trees = [c.evaluate() for c in search.find(self.EXAMPLE)]
        self.assertEqual(1, len(trees))
        self.assertIn(self._B2, trees)

    def test_rule_find_adbc(self):
        search = AttributeSearch(
            AttributeSearch(
                AttributeSearch(
                    RuleSearch(NonTerminal("<a>")), RuleSearch(NonTerminal("<d>"))
                ),
                RuleSearch(NonTerminal("<b>")),
            ),
            RuleSearch(NonTerminal("<c>")),
        )
        trees = [c.evaluate() for c in search.find(self.EXAMPLE)]
        self.assertEqual(1, len(trees))
        self.assertIn(self._C2, trees)

    def test_descendant_attribute_search(self):
        search = DescendantAttributeSearch(
            RuleSearch(NonTerminal("<a>")), RuleSearch(NonTerminal("<b>"))
        )
        trees = [c.evaluate() for c in search.find(self.EXAMPLE)]
        self.assertEqual(2, len(trees))
        self.assertIn(self._B1, trees)
        self.assertIn(self._B2, trees)

    def test_descendant_attribute_search_complex(self):
        search = DescendantAttributeSearch(
            AttributeSearch(
                RuleSearch(NonTerminal("<a>")), RuleSearch(NonTerminal("<d>"))
            ),
            RuleSearch(NonTerminal("<c>")),
        )
        trees = [c.evaluate() for c in search.find(self.EXAMPLE)]
        self.assertEqual(1, len(trees))
        self.assertIn(self._C2, trees)

    def test_item_search(self):
        search = ItemSearch(RuleSearch(NonTerminal("<c>")), 0)
        trees = [c.evaluate() for c in search.find(self.EXAMPLE)]
        self.assertEqual(2, len(trees))
        self.assertIn(self._0, trees)
        self.assertIn(self._1, trees)

    def test_item_search_complex(self):
        search = AttributeSearch(
            ItemSearch(RuleSearch(NonTerminal("<a>")), slice(0, 1)),
            RuleSearch(NonTerminal("<b>")),
        )
        trees = [c.evaluate() for c in search.find(self.EXAMPLE)]
        self.assertEqual(1, len(trees))
        self.assertIn(self._B1, trees)

    def test_selective_search(self):
        search = SelectiveSearch(
            RuleSearch(NonTerminal("<a>")), [(NonTerminal("<d>"), True)], [None]
        )
        trees = [c.evaluate() for c in search.find(self.EXAMPLE)]
        self.assertEqual(1, len(trees))
        self.assertIn(self._D, trees)

    def test_selective_search_complex(self):
        search = AttributeSearch(
            SelectiveSearch(
                RuleSearch(NonTerminal("<a>")), [(NonTerminal("<d>"), True)], [0]
            ),
            SelectiveSearch(
                RuleSearch(NonTerminal("<b>")), [(NonTerminal("<c>"), True)], [0]
            ),
        )
        trees = [c.evaluate() for c in search.find(self.EXAMPLE)]
        self.assertEqual(1, len(trees))
        self.assertIn(self._C2, trees)

    def test_selective_search_more_complex(self):
        search = AttributeSearch(
            SelectiveSearch(
                RuleSearch(NonTerminal("<a>")), [(NonTerminal("<b>"), False)], [None]
            ),
            RuleSearch(NonTerminal("<c>")),
        )
        trees = [c.evaluate() for c in search.find(self.EXAMPLE)]
        self.assertEqual(2, len(trees))
        self.assertIn(self._C1, trees)
        self.assertIn(self._C2, trees)

    def test_star_search(self):
        search = StarSearch(RuleSearch(NonTerminal("<c>")))
        trees = [c.evaluate() for c in search.find(self.EXAMPLE)]
        self.assertEqual(1, len(trees))
        self.assertIsInstance(trees[0], list)
        self.assertEqual(2, len(trees[0]))
        self.assertIn(self._C1, trees[0])
        self.assertIn(self._C2, trees[0])

    def test_population_search(self):
        search = PopulationSearch(RuleSearch(NonTerminal("<c>")))
        trees = [
            c.evaluate()
            for c in search.find(
                self.EXAMPLE,
                population=[self.EXAMPLE, self.EXAMPLE, self._C2, self._C1, self._C3],
            )
        ]
        self.assertEqual(1, len(trees))
        self.assertIsInstance(trees[0], list)
        self.assertEqual(7, len(trees[0]))
        self.assertEqual(
            [self._C1, self._C2, self._C1, self._C2, self._C2, self._C1, self._C3],
            trees[0],
        )
