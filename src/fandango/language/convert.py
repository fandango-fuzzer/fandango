import ast
from io import UnsupportedOperation
from typing import List, Tuple, Dict

from numpy.ma.core import identity

from fandango.constraints.base import (
    ConjunctionConstraint,
    DisjunctionConstraint,
    ImplicationConstraint,
    ExpressionConstraint,
    Comparison,
    ComparisonConstraint,
)
from fandango.language.grammar import (
    Grammar,
    Alternative,
    Concatenation,
    Star,
    NonTerminal,
    CharSet,
    Terminal,
)
from fandango.language.parser.FandangoParser import FandangoParser
from fandango.language.parser.FandangoParserVisitor import FandangoParserVisitor
from fandango.language.search import AttributeSearch, RuleSearch, LengthSearch


class FandangoSplitter(FandangoParserVisitor):
    def __init__(self):
        self.productions = []
        self.constraints = []
        self.python_code = []

    def visitProduction(self, ctx: FandangoParser.ProductionContext):
        self.productions.append(ctx)

    def visitConstraint(self, ctx: FandangoParser.ConstraintContext):
        self.constraints.append(ctx)

    def visitPython(self, ctx: FandangoParser.PythonContext):
        self.visitChildren(ctx.python_tag())


class GrammarProcessor(FandangoParserVisitor):
    def get_grammar(self, productions: List[FandangoParser.ProductionContext]):
        rules = {}
        for production in productions:
            rules[production.RULE_NAME().getText()] = self.visit(
                production.alternative()
            )
        return Grammar(rules)

    def visitAlternative(self, ctx: FandangoParser.AlternativeContext):
        return Alternative([self.visit(child) for child in ctx.concatenation()])

    def visitConcatenation(self, ctx: FandangoParser.ConcatenationContext):
        return Concatenation([self.visit(child) for child in ctx.operator()])

    def visitKleene(self, ctx: FandangoParser.KleeneContext):
        return Star(self.visit(ctx.symbol()))

    def visitSymbol(self, ctx: FandangoParser.SymbolContext):
        if ctx.RULE_NAME():
            return NonTerminal(ctx.RULE_NAME().getText())
        elif ctx.STRING():
            return Terminal.from_symbol(ctx.STRING().getText())
        elif ctx.char_set():
            return CharSet(ctx.char_set().getText())
        elif ctx.alternative():
            return self.visit(ctx.alternative())
        else:
            raise ValueError(f"Unknown symbol: {ctx.getText()}")


class ConstraintProcessor(FandangoParserVisitor):
    def __init__(self, grammar: Grammar):
        self.searches = SearchProcessor(grammar)

    def get_constraints(self, constraints: List[FandangoParser.ConstraintContext]):
        return ConjunctionConstraint(
            [self.visit(constraint) for constraint in constraints]
        )

    def visitConstraint(self, ctx: FandangoParser.ConstraintContext):
        return self.visit(ctx.implies())

    def visitImplies(self, ctx: FandangoParser.ImpliesContext):
        constraint = self.visit(ctx.quantifier())
        if ctx.ARROW():
            return ImplicationConstraint(constraint, self.visit(ctx.implies()))
        return self.visit(ctx.quantifier())

    def visitQuantifier(self, ctx: FandangoParser.QuantifierContext):
        if ctx.formula_disjunction():
            return self.visit(ctx.formula_disjunction())

    def visitFormula_disjunction(self, ctx: FandangoParser.Formula_disjunctionContext):
        constraints = [
            self.visit(constraint) for constraint in ctx.formula_conjunction()
        ]
        if len(constraints) == 1:
            return constraints[0]
        else:
            return DisjunctionConstraint(constraints)

    def visitFormula_conjunction(self, ctx: FandangoParser.Formula_conjunctionContext):
        constraints = [
            self.visit(constraint) for constraint in ctx.formula_conjunction()
        ]
        if len(constraints) == 1:
            return constraints[0]
        else:
            return ConjunctionConstraint(constraints)

    def visitFormula_atom(self, ctx: FandangoParser.Formula_atomContext):
        if ctx.implies():
            return self.visit(ctx.implies())
        elif ctx.expr():
            return self.visit(ctx.expr())
        elif ctx.formula_comparison():
            return self.visit(ctx.formula_comparison())
        else:
            raise ValueError(f"Unknown formula atom: {ctx.getText()}")

    def visitExpr(self, ctx: FandangoParser.ExprContext):
        if ctx.selector_length():
            expr, _, search_map = self.searches.visit(ctx.selector_length())
        elif ctx.expression():
            expr, _, search_map = self.searches.visit(ctx.expression())
        else:
            raise ValueError(f"Unknown expression: {ctx.getText()}")
        expr: ast.AST
        return ExpressionConstraint(ast.unparse(expr), searches=search_map)

    def visitFormula_comparison(self, ctx: FandangoParser.Formula_comparisonContext):
        if ctx.LESS_THAN():
            op = Comparison.LESS
        elif ctx.GREATER_THAN():
            op = Comparison.GREATER
        elif ctx.EQUALS():
            op = Comparison.EQUAL
        elif ctx.GT_EQ():
            op = Comparison.GREATER_EQUAL
        elif ctx.LT_EQ():
            op = Comparison.LESS_EQUAL
        elif ctx.NOT_EQ_1() or ctx.NOT_EQ_2():
            op = Comparison.NOT_EQUAL
        else:
            raise UnsupportedOperation(f"Unknown operator in {ctx}")
        left, _, left_map = self.searches.visit(ctx.expr(0))
        right, _, right_map = self.searches.visit(ctx.expr(1))
        left = ast.unparse(left)
        right = ast.unparse(right)
        return ComparisonConstraint(op, left, right, searches={**left_map, **right_map})


class SearchProcessor(FandangoParserVisitor):
    def __init__(self, grammar: Grammar):
        self.identifier_id = 0
        self.grammar = grammar

    def defaultResult(
        self,
    ) -> Tuple[
        ast.AST | List[ast.AST], List[AttributeSearch], Dict[str, AttributeSearch]
    ]:
        return [], [], {}

    # noinspection PyPep8Naming
    def aggregateResult(self, aggregate, nextResult):
        tree_aggregate, searches_aggregate, search_map_aggregate = aggregate
        tree_next, searches_next, search_map_next = nextResult
        searches = searches_aggregate + searches_next
        search_map = {**search_map_aggregate, **search_map_next}
        if isinstance(tree_aggregate, list):
            if isinstance(tree_next, list):
                tree = tree_aggregate + tree_next
            else:
                tree = tree_aggregate + [tree_next]
        elif isinstance(tree_next, list):
            tree = [tree_aggregate] + tree_next
        else:
            tree = [tree_aggregate, tree_next]
        return tree, searches, search_map

    def get_new_identifier(self):
        identifier = f"___fandango_{id(self)}_{self.identifier_id}___"
        self.identifier_id += 1
        return identifier

    def transform_selection(self, ctx: FandangoParser.SelectionContext):
        return RuleSearch(NonTerminal(ctx.RULE_NAME().getText()), self.grammar)

    def get_attribute_searches(self, ctx: FandangoParser.SelectorContext):
        search = self.transform_selection(ctx.selection())
        if ctx.selector():
            return AttributeSearch(
                self.get_attribute_searches(ctx.selector()), search, self.grammar
            )
        else:
            return search

    def visitSelector_length(self, ctx: FandangoParser.Selector_lengthContext):
        tree, searches, search_map = self.visit(ctx.selector())
        if ctx.OR_OP():
            search = [LengthSearch(searches[0], grammar=self.grammar)]
            search_map[tree.id] = search[0]
        return tree, searches, search_map

    def visitSelector(self, ctx: FandangoParser.SelectorContext):
        identifier = self.get_new_identifier()
        search = self.get_attribute_searches(ctx)
        return ast.Name(id=identifier), [search], {identifier: search}

    def visitExpression(self, ctx: FandangoParser.ExpressionContext):
        if ctx.IF():
            then_ast, then_searches, then_map = self.visit(ctx.disjunction(0))
            test_ast, test_searches, test_map = self.visit(ctx.disjunction(1))
            else_ast, else_searches, else_map = self.visit(ctx.disjunction(2))
            return (
                ast.IfExp(
                    test=test_ast,
                    body=then_ast,
                    orelse=else_ast,
                ),
                then_searches + test_searches + else_searches,
                {**then_map, **test_map, **else_map},
            )
        elif ctx.disjunction():
            return self.visit(ctx.disjunction())
        else:
            return self.visit(ctx.lambdef())

    def visitDisjunction(self, ctx: FandangoParser.DisjunctionContext):
        if ctx.OR():
            trees, searches, search_map = self.visitChildren(ctx)
            return (
                ast.BoolOp(
                    op=ast.Or(),
                    values=trees,
                ),
                searches,
                search_map,
            )
        return self.visit(ctx.conjunction())

    def visitConjunction(self, ctx: FandangoParser.ConjunctionContext):
        if ctx.AND():
            trees, searches, search_map = self.visitChildren(ctx)
            return (
                ast.BoolOp(
                    op=ast.And(),
                    values=trees,
                ),
                searches,
                search_map,
            )
        return self.visit(ctx.inversion())

    def _visit_unary_op(self, ctx, op):
        trees, searches, search_map = self.visitChildren(ctx)
        return (
            ast.UnaryOp(
                op=op,
                operand=trees[1],
            ),
            searches,
            search_map,
        )

    def visitInversion(self, ctx: FandangoParser.InversionContext):
        if ctx.NOT():
            return self._visit_unary_op(ctx, ast.Not())
        return self.visit(ctx.comparison())

    def visitComparison(self, ctx: FandangoParser.ComparisonContext):
        if ctx.compare_op_bitwise_or_pair():
            left, searches, search_map = self.visit(ctx.bitwise_or())
            operators = list()
            trees = list()
            for comparison in ctx.compare_op_bitwise_or_pair():
                operator, result = self.visit(comparison)
                r_tree, r_searches, r_search_map = result
                operators.append(operator)
                trees.append(r_tree)
                searches.extend(r_searches)
                search_map.update(r_search_map)
            return (
                ast.Compare(
                    left=left,
                    ops=operators,
                    comparators=trees,
                ),
                searches,
                search_map,
            )
        return self.visit(ctx.bitwise_or())

    def visitCompare_op_bitwise_or_pair(
        self, ctx: FandangoParser.Compare_op_bitwise_or_pairContext
    ):
        return self.visit(ctx.children[0])

    def visitEq_bitwise_or(self, ctx: FandangoParser.Eq_bitwise_orContext):
        return ast.Eq, self.visit(ctx.bitwise_or())

    def visitNoteq_bitwise_or(self, ctx: FandangoParser.Noteq_bitwise_orContext):
        return ast.NotEq, self.visit(ctx.bitwise_or())

    def visitLte_bitwise_or(self, ctx: FandangoParser.Lte_bitwise_orContext):
        return ast.LtE, self.visit(ctx.bitwise_or())

    def visitGte_bitwise_or(self, ctx: FandangoParser.Gte_bitwise_orContext):
        return ast.GtE, self.visit(ctx.bitwise_or())

    def visitLt_bitwise_or(self, ctx: FandangoParser.Lt_bitwise_orContext):
        return ast.Lt, self.visit(ctx.bitwise_or())

    def visitGt_bitwise_or(self, ctx: FandangoParser.Gt_bitwise_orContext):
        return ast.Gt, self.visit(ctx.bitwise_or())

    def visitNotin_bitwise_or(self, ctx: FandangoParser.Notin_bitwise_orContext):
        return ast.NotIn, self.visit(ctx.bitwise_or())

    def visitIn_bitwise_or(self, ctx: FandangoParser.In_bitwise_orContext):
        return ast.In, self.visit(ctx.bitwise_or())

    def visitIs_bitwise_or(self, ctx: FandangoParser.Is_bitwise_orContext):
        return ast.Is, self.visit(ctx.bitwise_or())

    def visitIsnot_bitwise_or(self, ctx: FandangoParser.Isnot_bitwise_orContext):
        return ast.IsNot, self.visit(ctx.bitwise_or())

    def _visit_bin_op(self, ctx, op):
        trees, searches, search_map = self.visitChildren(ctx)
        return (
            ast.BinOp(
                left=trees[0],
                op=op,
                right=trees[2],
            ),
            searches,
            search_map,
        )

    def visitBitwise_or(self, ctx: FandangoParser.Bitwise_orContext):
        if ctx.bitwise_or():
            return self._visit_bin_op(ctx, ast.BitOr())
        return self.visit(ctx.bitwise_xor())

    def visitBitwise_xor(self, ctx: FandangoParser.Bitwise_xorContext):
        if ctx.bitwise_xor():
            return self._visit_bin_op(ctx, ast.BitXor())
        return self.visit(ctx.bitwise_and())

    def visitBitwise_and(self, ctx: FandangoParser.Bitwise_andContext):
        if ctx.bitwise_and():
            return self._visit_bin_op(ctx, ast.BitAnd())
        return self.visit(ctx.shift_expr())

    def visitShift_expr(self, ctx: FandangoParser.Shift_exprContext):
        if ctx.LEFT_SHIFT():
            return self._visit_bin_op(ctx, ast.LShift())
        elif ctx.RIGHT_SHIFT():
            return self._visit_bin_op(ctx, ast.RShift())
        return self.visit(ctx.sum_())

    def visitSum(self, ctx: FandangoParser.SumContext):
        if ctx.ADD():
            return self._visit_bin_op(ctx, ast.Add())
        elif ctx.MINUS():
            return self._visit_bin_op(ctx, ast.Sub())
        return self.visit(ctx.term())

    def visitTerm(self, ctx: FandangoParser.TermContext):
        if ctx.STAR():
            return self._visit_bin_op(ctx, ast.Mult())
        elif ctx.DIV():
            return self._visit_bin_op(ctx, ast.Div())
        elif ctx.IDIV():
            return self._visit_bin_op(ctx, ast.FloorDiv())
        elif ctx.MOD():
            return self._visit_bin_op(ctx, ast.Mod())
        elif ctx.AT():
            return self._visit_bin_op(ctx, ast.MatMult())
        return self.visit(ctx.factor())

    def visitFactor(self, ctx: FandangoParser.FactorContext):
        if ctx.ADD():
            return self._visit_unary_op(ctx, ast.UAdd())
        elif ctx.MINUS():
            return self._visit_unary_op(ctx, ast.USub())
        elif ctx.NOT_OP():
            return self._visit_unary_op(ctx, ast.Invert())
        return self.visit(ctx.power())

    def visitPower(self, ctx: FandangoParser.PowerContext):
        if ctx.factor():
            return self._visit_bin_op(ctx, ast.Pow())
        return self.visit(ctx.await_primary())

    def visitAwait_primary(self, ctx: FandangoParser.Await_primaryContext):
        if ctx.AWAIT():
            tree, searches, search_map = self.visit(ctx.primary())
            return ast.Await(value=tree), searches, search_map
        return self.visit(ctx.primary())

    def visitPrimary(self, ctx: FandangoParser.PrimaryContext):
        if ctx.NAME():
            tree, searches, search_map = self.visit(ctx.primary())
            return ast.Attribute(value=tree, attr=ctx.NAME().getText())
        elif ctx.genexp():
            tree, searches, search_map = self.visit(ctx.primary())
            gen_tree, gen_searches, gen_search_map = self.visit(ctx.genexp())
            return (
                ast.Call(func=tree, args=[gen_tree], keywords=[]),
                searches + gen_searches,
                {**search_map, **gen_search_map},
            )
        elif ctx.OPEN_PAREN():
            tree, searches, search_map = self.visit(ctx.primary())
            args, keywords = list(), list()
            if ctx.arguments():
                args_trees, args_searches, args_search_map = self.visit(ctx.arguments())
                searches.extend(args_searches)
                search_map.update(args_search_map)
                for arg in args_trees:
                    if isinstance(arg, ast.keyword):
                        keywords.append(arg)
                    else:
                        args.append(arg)
            return (
                ast.Call(func=tree, args=args, keywords=keywords),
                searches,
                search_map,
            )
        elif ctx.slices():
            tree, searches, search_map = self.visit(ctx.primary())
            slice_trees, slice_searches, slice_search_map = self.visit(ctx.slices())
            if isinstance(slice_trees, list):
                slice_trees = ast.Tuple(elts=slice_trees)
            return (
                ast.Subscript(value=tree, slice=slice_trees),
                searches + slice_searches,
                {**search_map, **slice_search_map},
            )
        elif ctx.atom():
            return self.visit(ctx.atom())
        else:
            raise SyntaxError(f"Unsupported atom {ctx}")

    def visitAtom(self, ctx: FandangoParser.AtomContext):
        if ctx.NAME():
            return ast.Name(id=ctx.NAME().getText()), [], {}
        elif ctx.TRUE():
            return ast.Constant(value=True), [], {}
        elif ctx.FALSE():
            return ast.Constant(value=False), [], {}
        elif ctx.NONE():
            return ast.Constant(value=None), [], {}
        elif ctx.strings():
            return self.visit(ctx.strings())
        elif ctx.NUMBER():
            return ast.parse(ctx.NUMBER().getText(), mode="eval").body, [], {}
        elif ctx.tuple_():
            return self.visit(ctx.tuple_())
        elif ctx.group():
            return self.visit(ctx.group())
        elif ctx.genexp():
            return self.visit(ctx.genexp())
        elif ctx.list_():
            return self.visit(ctx.list_())
        elif ctx.listcomp():
            return self.visit(ctx.listcomp())
        elif ctx.dict_():
            return self.visit(ctx.dict_())
        elif ctx.dictcomp():
            return self.visit(ctx.dictcomp())
        elif ctx.set_():
            return self.visit(ctx.set_())
        elif ctx.setcomp():
            return self.visit(ctx.setcomp())
        elif ctx.ELLIPSIS():
            return ast.Constant(value=Ellipsis), [], {}
        elif ctx.selector_length():
            return self.visit(ctx.selector_length())
        else:
            raise SyntaxError(f"Unsupported atom {ctx}")

    def visitKwarg_or_starred(self, ctx: FandangoParser.Kwarg_or_starredContext):
        if ctx.ASSIGN():
            tree, searches, search_map = self.visit(ctx.expression())
            return (
                ast.keyword(arg=ctx.NAME().getText(), value=tree),
                searches,
                search_map,
            )
        else:
            return self.visit(ctx.starred_expression())

    def visitKwarg_or_double_starred(
        self, ctx: FandangoParser.Kwarg_or_double_starredContext
    ):
        tree, searches, search_map = self.visit(ctx.expression())
        arg = None
        if ctx.ASSIGN():
            arg = ctx.NAME().getText()
        return (
            ast.keyword(arg=arg, value=tree),
            searches,
            search_map,
        )

    def visitStarred_expression(self, ctx: FandangoParser.Starred_expressionContext):
        tree, searches, search_map = self.visit(ctx.expression())
        return ast.Starred(value=tree), searches, search_map

    def visitAssignment_expression(
        self, ctx: FandangoParser.Assignment_expressionContext
    ):
        raise UnsupportedOperation(
            "Assignment expressions are currently not supported."
        )

    def visitSlice(self, ctx: FandangoParser.SliceContext):
        if ctx.COLON():
            slices = [None, None, None]
            slice_count = 0
            searches = list()
            search_map = dict()
            for child in ctx.getChildren():
                if child == FandangoParser.COLON:
                    slice_count += 1
                else:
                    slice_tree, slice_searches, slice_search_map = self.visit(child)
                    slices[slice_count] = slice_tree
                    searches.extend(slice_searches)
                    search_map.update(slice_search_map)
            lower, upper, step = slices
            return (
                ast.Slice(
                    lower=lower,
                    upper=upper,
                    step=step,
                ),
                searches,
                search_map,
            )
        else:
            return self.visit(ctx.named_expression())

    def visitStrings(self, ctx: FandangoParser.StringsContext):
        if ctx.fstring():
            raise UnsupportedOperation(
                "JoinedStr with formats are currently not supported"
            )
        else:
            string = ""
            for child in ctx.string():
                string += child.STRING().getText()
            return ast.Constant(value=string), [], {}

    def visitTuple(self, ctx: FandangoParser.TupleContext):
        trees, searches, search_map = self.visitChildren(ctx)
        return ast.Tuple(elts=trees), searches, search_map

    def visitList(self, ctx: FandangoParser.ListContext):
        trees, searches, search_map = self.visitChildren(ctx)
        return ast.List(elts=trees), searches, search_map

    def visitSet(self, ctx: FandangoParser.SetContext):
        trees, searches, search_map = self.visitChildren(ctx)
        return ast.Set(elts=trees), searches, search_map

    def visitDict(self, ctx: FandangoParser.DictContext):
        keys = list()
        values = list()
        if ctx.double_starred_kvpairs():
            kvpairs, searches, search_map = self.visit(ctx.double_starred_kvpairs())
            keys, values = zip(*kvpairs)
        else:
            searches, search_map = [], {}
        return ast.Dict(keys=keys, values=values), searches, search_map

    def visitDouble_starred_kvpair(
        self, ctx: FandangoParser.Double_starred_kvpairContext
    ):
        if ctx.POWER():
            tree, searches, search_map = self.visit(ctx.bitwise_or())
            return (None, tree), searches, search_map
        else:
            return self.visit(ctx.kvpair())

    def visitKvpair(self, ctx: FandangoParser.KvpairContext):
        key, key_searches, key_search_map = self.visit(ctx.expression(0))
        value, value_searches, value_search_map = self.visit(ctx.expression(1))
        return (
            (key, value),
            key_searches + value_searches,
            {**key_search_map, **value_search_map},
        )

    def visitGroup(self, ctx: FandangoParser.GroupContext):
        if ctx.yield_expr():
            return self.visit(ctx.yield_expr())
        else:
            return self.visit(ctx.named_expression())

    def visitYield_expr(self, ctx: FandangoParser.Yield_exprContext):
        if ctx.FROM():
            tree, searches, search_map = self.visit(ctx.expression())
            return ast.YieldFrom(value=tree), searches, search_map
        else:
            if ctx.star_expressions():
                tree, searches, search_map = self.visit(ctx.star_expressions())
                return ast.Yield(value=tree), searches, search_map
            else:
                return ast.Yield(value=None), [], {}

    def visitNamed_expression(self, ctx: FandangoParser.Named_expressionContext):
        if ctx.expression():
            return self.visit(ctx.expression())
        else:
            return self.visit(ctx.assignment_expression())

    def visitGenexp(self, ctx: FandangoParser.GenexpContext):
        if ctx.expression():
            tree, searches, search_map = self.visit(ctx.expression())
        else:
            tree, searches, search_map = self.visit(ctx.assignment_expression())
        generators, gen_searches, gen_search_map = self.visit(ctx.for_if_clauses())
        return (
            ast.GeneratorExp(elt=tree, generators=generators),
            searches + gen_searches,
            {**search_map, **gen_search_map},
        )

    def visitListcomp(self, ctx: FandangoParser.ListcompContext):
        tree, searches, search_map = self.visit(ctx.named_expression())
        generators, gen_searches, gen_search_map = self.visit(ctx.for_if_clauses())
        return (
            ast.ListComp(elt=tree, generators=generators),
            searches + gen_searches,
            {**search_map, **gen_search_map},
        )

    def visitSetcomp(self, ctx: FandangoParser.SetcompContext):
        tree, searches, search_map = self.visit(ctx.named_expression())
        generators, gen_searches, gen_search_map = self.visit(ctx.for_if_clauses())
        return (
            ast.SetComp(elt=tree, generators=generators),
            searches + gen_searches,
            {**search_map, **gen_search_map},
        )

    def visitDictcomp(self, ctx: FandangoParser.DictcompContext):
        tree, searches, search_map = self.visit(ctx.kvpair())
        key, value = tree
        generators, gen_searches, gen_search_map = self.visit(ctx.for_if_clauses())
        return (
            ast.DictComp(key=key, value=value, generators=generators),
            searches + gen_searches,
            {**search_map, **gen_search_map},
        )

    def visitFor_if_clauses(self, ctx: FandangoParser.For_if_clausesContext):
        result = list(), list(), dict()
        for clause in ctx.for_if_clause():
            result = self.aggregateResult(result, self.visit(clause))
        return result

    def visitFor_if_clause(self, ctx: FandangoParser.For_if_clauseContext):
        is_async = True if ctx.ASYNC() else False  # needed for None check
        target, target_searches, target_search_map = self.visit(ctx.star_targets())
        iter_, iter_searches, iter_search_map = self.visit(ctx.disjunction(0))
        searches = target_searches + iter_searches
        search_map = {**target_search_map, **iter_search_map}
        ifs = list()
        for disjunction in ctx.disjunction()[1:]:
            if_, if_searches, if_search_map = self.visit(disjunction)
            ifs.append(if_)
            searches.extend(if_searches)
            search_map.update(if_search_map)
        return (
            ast.comprehension(
                target=target,
                iter=iter_,
                ifs=ifs,
                is_async=is_async,
            ),
            searches,
            search_map,
        )

    def visitStar_targets(self, ctx: FandangoParser.Star_targetsContext):
        targets, searches, search_map = self.visitChildren(ctx)
        if isinstance(targets, list):
            if len(targets) == 1:
                target = targets[0]
            else:
                target = ast.Tuple(elts=targets)
        else:
            target = targets
        return target, searches, search_map

    def visitStar_targets_list_seq(
        self, ctx: FandangoParser.Star_targets_list_seqContext
    ):
        targets, searches, search_map = self.visitChildren(ctx)
        if not isinstance(targets, list):
            targets = [targets]
        return ast.List(
            elts=targets,
        )

    def visitStar_targets_tuple_seq(
        self, ctx: FandangoParser.Star_targets_tuple_seqContext
    ):
        targets, searches, search_map = self.visitChildren(ctx)
        if not isinstance(targets, list):
            targets = [targets]
        return ast.Tuple(
            elts=targets,
        )

    def visitStar_target(self, ctx: FandangoParser.Star_targetContext):
        if ctx.STAR():
            target, searches, search_map = self.visit(ctx.star_target())
            return ast.Starred(value=target), searches, search_map
        return self.visit(ctx.target_with_star_atom())

    def visitTarget_with_star_atom(
        self, ctx: FandangoParser.Target_with_star_atomContext
    ):
        if ctx.DOT():
            target, searches, search_map = self.visit(ctx.t_primary())
            return (
                ast.Attribute(value=target, attr=ctx.NAME().getText()),
                searches,
                search_map,
            )
        elif ctx.slices():
            tree, searches, search_map = self.visit(ctx.t_primary())
            slice_trees, slice_searches, slice_search_map = self.visit(ctx.slices())
            if isinstance(slice_trees, list):
                slice_trees = ast.Tuple(elts=slice_trees)
            return (
                ast.Subscript(value=tree, slice=slice_trees),
                searches + slice_searches,
                {**search_map, **slice_search_map},
            )
        return self.visit(ctx.star_atom())

    def visitStar_atom(self, ctx: FandangoParser.Star_atomContext):
        if ctx.NAME():
            return ast.Name(id=ctx.NAME().getText()), [], {}
        elif ctx.target_with_star_atom():
            return self.visit(ctx.target_with_star_atom())
        elif ctx.OPEN_PAREN():
            if ctx.star_targets_tuple_seq():
                return self.visit(ctx.star_targets_tuple_seq())
            return ast.Tuple(elts=[]), [], {}
        elif ctx.OPEN_BRACK():
            if ctx.star_targets_list_seq():
                return self.visit(ctx.star_targets_list_seq())
            return ast.List(elts=[]), [], {}
        else:
            raise ValueError(f"Unknown symbol: {ctx.getText()}")

    def visitT_primary(self, ctx: FandangoParser.T_primaryContext):
        if ctx.DOT():
            target, searches, search_map = self.visit(ctx.t_primary())
            return (
                ast.Attribute(value=target, attr=ctx.NAME().getText()),
                searches,
                search_map,
            )
        elif ctx.slices():
            tree, searches, search_map = self.visit(ctx.t_primary())
            slice_trees, slice_searches, slice_search_map = self.visit(ctx.slices())
            if isinstance(slice_trees, list):
                slice_trees = ast.Tuple(elts=slice_trees)
            return (
                ast.Subscript(value=tree, slice=slice_trees),
                searches + slice_searches,
                {**search_map, **slice_search_map},
            )
        elif ctx.genexp():
            tree, searches, search_map = self.visit(ctx.t_primary())
            gen_tree, gen_searches, gen_search_map = self.visit(ctx.genexp())
            return (
                ast.Call(func=tree, args=[gen_tree], keywords=[]),
                searches + gen_searches,
                {**search_map, **gen_search_map},
            )
        elif ctx.OPEN_PAREN():
            tree, searches, search_map = self.visit(ctx.t_primary())
            args, keywords = list(), list()
            if ctx.arguments():
                args_trees, args_searches, args_search_map = self.visit(ctx.arguments())
                searches.extend(args_searches)
                search_map.update(args_search_map)
                for arg in args_trees:
                    if isinstance(arg, ast.keyword):
                        keywords.append(arg)
                    else:
                        args.append(arg)
            return (
                ast.Call(func=tree, args=args, keywords=keywords),
                searches,
                search_map,
            )
        return self.visit(ctx.atom())
