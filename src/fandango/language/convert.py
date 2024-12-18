import ast
from fandango.logger import LOGGER
from io import UnsupportedOperation
from typing import List, Tuple, Dict, Optional, Any

from fandango.constraints.base import (
    ConjunctionConstraint,
    DisjunctionConstraint,
    ImplicationConstraint,
    ExpressionConstraint,
    ComparisonConstraint,
    ExistsConstraint,
    ForallConstraint,
    Constraint,
    Value,
)
from fandango.constraints.fitness import Comparison
from fandango.language.grammar import (
    Grammar,
    Alternative,
    Concatenation,
    Star,
    NonTerminalNode,
    CharSet,
    TerminalNode,
    Plus,
    Option,
    Repetition,
)
from fandango.language.parser.FandangoParser import FandangoParser
from fandango.language.parser.FandangoParserVisitor import FandangoParserVisitor
from fandango.language.search import (
    AttributeSearch,
    RuleSearch,
    LengthSearch,
    DescendantAttributeSearch,
    ItemSearch,
    SelectiveSearch,
)
from fandango.language.symbol import Terminal, NonTerminal


class FandangoSplitter(FandangoParserVisitor):
    def __init__(self):
        self.productions = []
        self.constraints = []
        self.python_code = []

    def visitFandango(self, ctx: FandangoParser.FandangoContext):
        self.productions = []
        self.constraints = []
        self.python_code = []
        self.visitChildren(ctx)

    def visitProduction(self, ctx: FandangoParser.ProductionContext):
        self.productions.append(ctx)

    def visitConstraint(self, ctx: FandangoParser.ConstraintContext):
        self.constraints.append(ctx)

    def visitPython(self, ctx: FandangoParser.PythonContext):
        self.python_code.append(ctx)


class GrammarProcessor(FandangoParserVisitor):
    def __init__(
        self,
        local_variables: Optional[Dict[str, Any]] = None,
        global_variables: Optional[Dict[str, Any]] = None,
    ):
        self.local_variables = local_variables
        self.global_variables = global_variables
        self.searches = SearchProcessor(Grammar.dummy())

    def get_grammar(self, productions: List[FandangoParser.ProductionContext]):
        grammar = Grammar(
            local_variables=self.local_variables,
            global_variables=self.global_variables,
        )
        for production in productions:
            symbol = NonTerminal(production.NONTERMINAL().getText())
            grammar[symbol] = self.visit(production.alternative())
            if production.expression():
                expr, searches, _ = self.searches.visit(production.expression())
                if searches:
                    raise UnsupportedOperation(
                        "Searches in expressions are currently not supported"
                    )
                grammar.set_generator(symbol, ast.unparse(expr))

                if not production.EXPR_ASSIGN():
                    LOGGER.warning(
                        "Using '=' and '::' for generators is deprecated. Use ':=' instead."
                    )

        grammar.update_parser()
        grammar.prime()
        return grammar

    def visitAlternative(self, ctx: FandangoParser.AlternativeContext):
        nodes = [self.visit(child) for child in ctx.concatenation()]
        if len(nodes) == 1:
            return nodes[0]
        return Alternative(nodes)

    def visitConcatenation(self, ctx: FandangoParser.ConcatenationContext):
        nodes = [self.visit(child) for child in ctx.operator()]
        if len(nodes) == 1:
            return nodes[0]
        return Concatenation(nodes)

    def visitKleene(self, ctx: FandangoParser.KleeneContext):
        return Star(self.visit(ctx.symbol()))

    def visitPlus(self, ctx: FandangoParser.PlusContext):
        return Plus(self.visit(ctx.symbol()))

    def visitOption(self, ctx: FandangoParser.OptionContext):
        return Option(self.visit(ctx.symbol()))

    def visitRepeat(self, ctx: FandangoParser.RepeatContext):
        node = self.visit(ctx.symbol())
        if ctx.COMMA():
            bounds = [None, None]
            bounds_index = 0
            started = False
            for child in ctx.getChildren():
                if child.getText() == "{":
                    started = True
                elif child.getText() == "}":
                    break
                elif started:
                    if child.getText() == ",":
                        bounds_index += 1
                    else:
                        bounds[bounds_index] = int(child.getText())
            min_, max_ = bounds
            if min_ is None and max_ is None:
                return Repetition(node)
            elif min_ is None:
                return Repetition(node, max_=max_)
            elif max_ is None:
                return Repetition(node, min_=min_)
            return Repetition(node, min_, max_)
        reps = int(ctx.NUMBER(0).getText())
        return Repetition(node, reps, reps)

    def visitSymbol(self, ctx: FandangoParser.SymbolContext):
        if ctx.NONTERMINAL():
            return NonTerminalNode(NonTerminal(ctx.NONTERMINAL().getText()))
        elif ctx.STRING():
            return TerminalNode(Terminal.from_symbol(ctx.STRING().getText()))
        elif ctx.char_set():
            return CharSet(ctx.char_set().getText())
        elif ctx.alternative():
            return self.visit(ctx.alternative())
        else:
            raise ValueError(f"Unknown symbol: {ctx.getText()}")


class ConstraintProcessor(FandangoParserVisitor):
    def __init__(
        self,
        grammar: Grammar,
        local_variables: Optional[Dict[str, Any]] = None,
        global_variables: Optional[Dict[str, Any]] = None,
        lazy: bool = False,
    ):
        self.searches = SearchProcessor(grammar)
        self.lazy = lazy
        self.local_variables = local_variables
        self.global_variables = global_variables

    def get_constraints(
        self, constraints: List[FandangoParser.ConstraintContext]
    ) -> Constraint:
        return [self.visit(constraint) for constraint in constraints]
        # if len(constraints) == 1:
        #     return constraints[0]
        # else:
        #     return ConjunctionConstraint(
        #         constraints,
        #         local_variables=self.local_variables,
        #         global_variables=self.global_variables,
        #         lazy=self.lazy,
        #    )

    def visitConstraint(self, ctx: FandangoParser.ConstraintContext):
        if ctx.implies():
            return self.visit(ctx.implies())
        elif ctx.FITNESS():
            expression_constraint = self.visitExpr(ctx.expr())
            return Value(
                expression_constraint.expression,
                searches=expression_constraint.searches,
                local_variables=expression_constraint.local_variables,
                global_variables=expression_constraint.global_variables,
            )
        else:
            raise ValueError(f"Unknown constraint: {ctx.getText()}")

    def visitImplies(self, ctx: FandangoParser.ImpliesContext):
        constraint = self.visit(ctx.quantifier())
        if ctx.ARROW():
            return ImplicationConstraint(
                constraint,
                self.visit(ctx.implies()),
                local_variables=self.local_variables,
                global_variables=self.global_variables,
            )
        return self.visit(ctx.quantifier())

    def visitQuantifier(self, ctx: FandangoParser.QuantifierContext):
        if ctx.formula_disjunction():
            return self.visit(ctx.formula_disjunction())
        elif ctx.EXISTS() or ctx.FORALL():
            constraint = self.visit(ctx.quantifier())
            bound = NonTerminal(ctx.NONTERMINAL().getText())
            search = self.searches.visit(ctx.selector())[1][0]
            if ctx.EXISTS():
                return ExistsConstraint(
                    constraint,
                    bound,
                    search,
                    local_variables=self.local_variables,
                    global_variables=self.global_variables,
                    lazy=self.lazy,
                )
            elif ctx.FORALL():
                return ForallConstraint(
                    constraint,
                    bound,
                    search,
                    local_variables=self.local_variables,
                    global_variables=self.global_variables,
                    lazy=self.lazy,
                )
            else:
                raise ValueError(f"Unknown quantifier: {ctx.getText()}")
        else:
            raise ValueError(f"Unknown quantifier: {ctx.getText()}")

    def visitFormula_disjunction(self, ctx: FandangoParser.Formula_disjunctionContext):
        constraints = [
            self.visit(constraint) for constraint in ctx.formula_conjunction()
        ]
        if len(constraints) == 1:
            return constraints[0]
        else:
            return DisjunctionConstraint(
                constraints,
                local_variables=self.local_variables,
                global_variables=self.global_variables,
                lazy=self.lazy,
            )

    def visitFormula_conjunction(self, ctx: FandangoParser.Formula_conjunctionContext):
        constraints = [self.visit(constraint) for constraint in ctx.formula_atom()]
        if len(constraints) == 1:
            return constraints[0]
        else:
            return ConjunctionConstraint(
                constraints,
                local_variables=self.local_variables,
                global_variables=self.global_variables,
                lazy=self.lazy,
            )

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
            expr, _, search_map = self.searches.visitSelector_length(
                ctx.selector_length()
            )
        elif ctx.IF():
            body, _, body_search_map = self.searches.visitInversion(ctx.inversion(0))
            test, _, test_search_map = self.searches.visitInversion(ctx.inversion(1))
            orelse, _, orelse_search_map = self.searches.visitInversion(
                ctx.inversion(2)
            )
            search_map = {**body_search_map, **test_search_map, **orelse_search_map}
            expr = ast.IfExp(test=test, body=body, orelse=orelse)
        elif ctx.inversion():
            expr, _, search_map = self.searches.visitInversion(ctx.inversion(0))
        else:
            raise ValueError(f"Unknown expression: {ctx.getText()}")
        return ExpressionConstraint(
            ast.unparse(expr),
            searches=search_map,
            local_variables=self.local_variables,
            global_variables=self.global_variables,
        )

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
            raise UnsupportedOperation(f"Unknown operator in {ctx.getText()}")
        left, _, left_map = self.searches.visit(ctx.expr(0))
        right, _, right_map = self.searches.visit(ctx.expr(1))
        return ComparisonConstraint(
            op,
            ast.unparse(left),
            ast.unparse(right),
            searches={**left_map, **right_map},
            local_variables=self.local_variables,
            global_variables=self.global_variables,
        )


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

    def visitRs_pairs(self, ctx: FandangoParser.Rs_pairsContext):
        symbols = list()
        slices = list()
        for child in ctx.rs_pair():
            sym, items = self.visitRs_pair(child)
            symbols.append(sym)
            slices.append(items)
        return symbols, slices

    def visitRs_pair(self, ctx: FandangoParser.Rs_pairContext):
        symbol = (
            NonTerminal(ctx.NONTERMINAL().getText()),
            False if ctx.STAR() else True,
        )
        if ctx.rs_slice():
            return symbol, self.visitRs_slice(ctx.rs_slice())
        return symbol, None

    def visitRs_slice(self, ctx: FandangoParser.Rs_sliceContext):
        if ctx.COLON():
            return slice(
                int(ctx.NUMBER(0).getText()) if ctx.NUMBER(0) else None,
                int(ctx.NUMBER(1).getText()) if ctx.NUMBER(1) else None,
                int(ctx.NUMBER(2).getText()) if ctx.NUMBER(2) else None,
            )
        else:
            return int(ctx.NUMBER(0).getText())

    def visitRs_slices(self, ctx: FandangoParser.Rs_slicesContext):
        return [self.visitRs_slice(child) for child in ctx.rs_slice()]

    def visitBase_selection(self, ctx: FandangoParser.Base_selectionContext):
        if ctx.NONTERMINAL():
            return RuleSearch(NonTerminal(ctx.NONTERMINAL().getText()))
        elif ctx.selector():
            return self.get_attribute_searches(ctx.selector())
        else:
            raise ValueError(f"Unknown base selection: {ctx.getText()}")

    def transform_selection(self, ctx: FandangoParser.SelectionContext):
        base = self.visitBase_selection(ctx.base_selection())
        if ctx.rs_pairs():
            symbols, slices = self.visitRs_pairs(ctx.rs_pairs())
            return SelectiveSearch(base, symbols, slices)
        elif ctx.rs_slices():
            return ItemSearch(base, self.visitRs_slices(ctx.rs_slices()))
        return base

    def get_attribute_searches(self, ctx: FandangoParser.SelectorContext):
        search = self.transform_selection(ctx.selection())

        if ctx.DOT():
            return AttributeSearch(self.get_attribute_searches(ctx.selector()), search)
        elif ctx.DOTDOT():
            return DescendantAttributeSearch(
                self.get_attribute_searches(ctx.selector()), search
            )
        else:
            return search

    def visitSelector_length(self, ctx: FandangoParser.Selector_lengthContext):
        tree, searches, search_map = self.visitSelector(ctx.selector())
        if ctx.OR_OP():
            search_map[tree.id] = LengthSearch(searches[0])
        return tree, searches, search_map

    def visitSelector(self, ctx: FandangoParser.SelectorContext):
        identifier = self.get_new_identifier()
        search = self.get_attribute_searches(ctx)
        return ast.Name(id=identifier), [search], {identifier: search}

    def visitExpression(self, ctx: FandangoParser.ExpressionContext):
        if ctx.IF():
            then_ast, then_searches, then_map = self.visit(ctx.disjunction(0))
            test_ast, test_searches, test_map = self.visit(ctx.disjunction(1))
            else_ast, else_searches, else_map = self.visit(ctx.expression())
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
            return self.visit(ctx.disjunction(0))
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
        return self.visit(ctx.conjunction(0))

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
        return self.visit(ctx.inversion(0))

    def _visit_unary_op(self, ctx, op):
        trees, searches, search_map = self.visitChildren(ctx)
        return (
            ast.UnaryOp(
                op=op,
                operand=trees[0],
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
        return ast.Eq(), self.visit(ctx.bitwise_or())

    def visitNoteq_bitwise_or(self, ctx: FandangoParser.Noteq_bitwise_orContext):
        return ast.NotEq(), self.visit(ctx.bitwise_or())

    def visitLte_bitwise_or(self, ctx: FandangoParser.Lte_bitwise_orContext):
        return ast.LtE(), self.visit(ctx.bitwise_or())

    def visitGte_bitwise_or(self, ctx: FandangoParser.Gte_bitwise_orContext):
        return ast.GtE(), self.visit(ctx.bitwise_or())

    def visitLt_bitwise_or(self, ctx: FandangoParser.Lt_bitwise_orContext):
        return ast.Lt(), self.visit(ctx.bitwise_or())

    def visitGt_bitwise_or(self, ctx: FandangoParser.Gt_bitwise_orContext):
        return ast.Gt(), self.visit(ctx.bitwise_or())

    def visitNotin_bitwise_or(self, ctx: FandangoParser.Notin_bitwise_orContext):
        return ast.NotIn(), self.visit(ctx.bitwise_or())

    def visitIn_bitwise_or(self, ctx: FandangoParser.In_bitwise_orContext):
        return ast.In(), self.visit(ctx.bitwise_or())

    def visitIs_bitwise_or(self, ctx: FandangoParser.Is_bitwise_orContext):
        return ast.Is(), self.visit(ctx.bitwise_or())

    def visitIsnot_bitwise_or(self, ctx: FandangoParser.Isnot_bitwise_orContext):
        return ast.IsNot(), self.visit(ctx.bitwise_or())

    def _visit_bin_op(self, ctx, op):
        trees, searches, search_map = self.visitChildren(ctx)
        return (
            ast.BinOp(
                left=trees[0],
                op=op,
                right=trees[1],
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
            return (
                ast.Attribute(value=tree, attr=ctx.NAME().getText()),
                searches,
                search_map,
            )
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
            return self._process_slices(ctx.slices(), tree, searches, search_map)
        elif ctx.atom():
            return self.visit(ctx.atom())
        else:
            raise SyntaxError(f"Unsupported atom {ctx.getText()}")

    def _process_slices(self, slices, tree, searches, search_map):
        slice_trees, slice_searches, slice_search_map = self.visit(slices)
        if isinstance(slice_trees, list):
            if len(slice_trees) == 1:
                slice_trees = slice_trees[0]
            else:
                slice_trees = ast.Tuple(elts=slice_trees)
        return (
            ast.Subscript(value=tree, slice=slice_trees),
            searches + slice_searches,
            {**search_map, **slice_search_map},
        )

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
            return self.visitStrings(ctx.strings())
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
            raise SyntaxError(f"Unsupported atom {ctx.getText()}")

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
            f"Assignment expressions are currently not supported: {ctx.getText()}"
        )

    def visitSlice(self, ctx: FandangoParser.SliceContext):
        if ctx.COLON():
            slices = [None, None, None]
            slice_count = 0
            searches = list()
            search_map = dict()
            for child in ctx.getChildren():
                if child.getText() == ":":
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
                f"Fstrings are currently not supported {ctx.getText()}"
            )
        else:
            string = ""
            for child in ctx.string():
                string += Terminal.clean(child.STRING().getText())
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
            return self._process_slices(ctx.slices(), tree, searches, search_map)
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
            return self._process_slices(ctx.slices(), tree, searches, search_map)
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

    def visitParameters(self, ctx: FandangoParser.ParametersContext):
        posonlyargs, defaults = [], []
        searches = []
        search_map = {}
        if ctx.slash_no_default():
            p = self.visitSlash_no_default(ctx.slash_no_default())
            posonlyargs.extend(p)
        elif ctx.slash_with_default():
            p, d, s, m = self.visitSlash_with_default(ctx.slash_with_default())
            posonlyargs.extend(p)
            defaults.extend(d)
            searches.extend(s)
            search_map.update(m)
        args = []
        for param in ctx.param_no_default():
            arg, s, m = self.visitParam_no_default(param)
            args.append(arg)
            searches.extend(s)
            search_map.update(m)
        kwonlyargs = []
        kw_defaults = []
        for param in ctx.param_with_default():
            arg, d, s, m = self.visitParam_with_default(param)
            if ctx.slash_with_default():
                args.append(arg),
                defaults.append(d)
            else:
                kwonlyargs.append(arg)
                kw_defaults.append(d)
            searches.extend(s)
            search_map.update(m)
        if ctx.star_etc():
            vararg, kw_args, kw_d, kwarg, s, m = self.visitStar_etc(ctx.star_etc())
            kwonlyargs.extend(kw_args)
            kw_defaults.extend(kw_d)
            searches.extend(s)
            search_map.update(m)
        else:
            vararg, kwarg = None, None
        return (
            ast.arguments(
                posonlyargs=posonlyargs,
                args=args,
                vararg=vararg,
                kwonlyargs=kwonlyargs,
                kw_defaults=kw_defaults,
                kwarg=kwarg,
                defaults=defaults,
            ),
            searches,
            search_map,
        )

    def visitStar_etc(self, ctx: FandangoParser.Star_etcContext):
        searches, search_map = [], {}
        vararg = None
        if ctx.STAR():
            if ctx.param_no_default():
                vararg, s, m = self.visitParam_no_default(ctx.param_no_default())
            else:
                vararg, s, m = self.visitParam_no_default_star_annotation(
                    ctx.param_no_default_star_annotation()
                )
            searches.extend(s)
            search_map.update(m)
        kwonlyargs = []
        kw_defaults = []
        for param in ctx.param_maybe_default():
            arg, d, s, m = self.visitParam_maybe_default(param)
            kwonlyargs.append(arg)
            kw_defaults.append(d)
            searches.extend(s)
            search_map.update(m)
        kwarg = None
        if ctx.kwds():
            kwarg, s, m = self.visitParam_no_default(ctx.kwds().param_no_default())
            searches.extend(s)
            search_map.update(m)
        return vararg, kwonlyargs, kw_defaults, kwarg, searches, search_map

    def visitParam_no_default(self, ctx: FandangoParser.Param_no_defaultContext):
        return self.visitParam(ctx.param())

    def visitParam_no_default_star_annotation(
        self, ctx: FandangoParser.Param_no_default_star_annotationContext
    ):
        return self.visitParam_star_annotation(ctx.param_star_annotation())

    def visitParam_with_default(self, ctx: FandangoParser.Param_with_defaultContext):
        arg, searches, search_map = self.visitParam(ctx.param())
        default, default_searches, default_search_map = self.visitExpression(
            ctx.default().expression()
        )
        return (
            arg,
            default,
            searches + default_searches,
            {**search_map, **default_search_map},
        )

    def visitParam_maybe_default(self, ctx: FandangoParser.Param_maybe_defaultContext):
        arg, searches, search_map = self.visitParam(ctx.param())
        if ctx.default():
            default, default_searches, default_search_map = self.visitExpression(
                ctx.default().expression()
            )
            return (
                arg,
                default,
                searches + default_searches,
                {**search_map, **default_search_map},
            )
        else:
            return arg, None, searches, search_map

    def visitParam(self, ctx: FandangoParser.ParamContext):
        if ctx.annotation():
            annotation, searches, search_map = self.visitExpression(
                ctx.annotation().expression()
            )
        else:
            annotation, searches, search_map = None, [], {}
        return (
            ast.arg(
                arg=ctx.NAME().getText(),
                annotation=annotation,
            ),
            searches,
            search_map,
        )

    def visitParam_star_annotation(
        self, ctx: FandangoParser.Param_star_annotationContext
    ):
        if ctx.star_annotation():
            annotation, searches, search_map = self.visitStar_expression(
                ctx.star_annotation().expression()
            )
        else:
            annotation, searches, search_map = None, [], {}
        return (
            ast.arg(
                arg=ctx.NAME().getText(),
                annotation=annotation,
            ),
            searches,
            search_map,
        )

    def visitSingle_target(self, ctx: FandangoParser.Single_targetContext):
        if ctx.NAME():
            return ast.Name(id=ctx.NAME().getText()), [], {}
        elif ctx.single_subscript_attribute_target():
            return self.visitSingle_subscript_attribute_target(
                ctx.single_subscript_attribute_target()
            )
        else:
            return self.visitSingle_target(ctx.single_target())

    def visitSingle_subscript_attribute_target(
        self, ctx: FandangoParser.Single_subscript_attribute_targetContext
    ):
        tree, searches, search_map = self.visit(ctx.t_primary())
        if ctx.DOT():
            return (
                ast.Attribute(value=tree, attr=ctx.NAME().getText()),
                searches,
                search_map,
            )
        else:
            return self._process_slices(ctx.slices(), tree, searches, search_map)

    def visitDel_target(self, ctx: FandangoParser.Del_targetContext):
        if ctx.DOT():
            tree, searches, search_map = self.visit(ctx.t_primary())
            return (
                ast.Attribute(value=tree, attr=ctx.NAME().getText()),
                searches,
                search_map,
            )
        elif ctx.slices():
            tree, searches, search_map = self.visit(ctx.t_primary())
            return self._process_slices(ctx.slices(), tree, searches, search_map)
        else:
            return self.visitDel_t_atom(ctx.del_t_atom())

    def visitDel_t_atom(self, ctx: FandangoParser.Del_t_atomContext):
        if ctx.NAME():
            return ast.Name(id=ctx.NAME().getText()), [], {}
        else:
            if ctx.del_targets():
                trees, searches, search_map = self.visitDel_targets(ctx.del_targets())
            else:
                trees, searches, search_map = self.defaultResult()
            if ctx.OPEN_PAREN():
                return ast.Tuple(elts=trees), searches, search_map
            else:
                return ast.List(elts=trees), searches, search_map

    def visitStar_expressions(self, ctx: FandangoParser.Star_expressionsContext):
        expressions, searches, search_map = self.visitChildren(ctx)
        if isinstance(expressions, list):
            if len(expressions) == 1:
                expression = expressions[0]
            else:
                expression = ast.Tuple(elts=expressions)
        else:
            expression = expressions
        return expression, searches, search_map

    def visitStar_expression(self, ctx: FandangoParser.Star_expressionContext):
        if ctx.STAR():
            tree, searches, search_map = self.visitBitwise_or(ctx.bitwise_or())
            return ast.Starred(value=tree), searches, search_map
        else:
            return self.visitExpression(ctx.expression())


class PythonProcessor(FandangoParserVisitor):
    def __init__(self):
        self.search_processor = SearchProcessor(Grammar.dummy())

    def get_code(self, stmts: List[FandangoParser.PythonContext]):
        return ast.Module(body=[self.visit(stmt) for stmt in stmts], type_ignores=[])

    def get_expression(self, expression):
        if expression:
            tree, searches, _ = self.search_processor.visit(expression)
            if searches:
                raise ValueError(
                    f"Nonterminals can only be used in grammars and constraints, not in regular Python code: {expression.getText()}"
                )
            return tree
        return None

    def visitStatements(self, ctx: FandangoParser.StatementsContext):
        return [tree for stmt in ctx.stmt() for tree in self.visitStmt(stmt)]

    def visitSimple_stmts(self, ctx: FandangoParser.Simple_stmtsContext):
        return [self.visitSimple_stmt(stmt) for stmt in ctx.simple_stmt()]

    def visitStmt(self, ctx: FandangoParser.StmtContext):
        if ctx.compound_stmt():
            return [self.visitCompound_stmt(ctx.compound_stmt())]
        elif ctx.simple_stmts():
            return self.visitSimple_stmts(ctx.simple_stmts())
        else:
            raise ValueError(f"Unknown symbol: {ctx.getText()}")

    def visitSimple_stmt(self, ctx: FandangoParser.Simple_stmtContext):
        if ctx.assignment():
            return self.visitAssignment(ctx.assignment())
        elif ctx.type_alias():
            return self.visitType_alias(ctx.type_alias())
        elif ctx.star_expressions():
            return ast.Expr(value=self.get_expression(ctx.star_expressions()))
        elif ctx.return_stmt():
            return self.visitReturn_stmt(ctx.return_stmt())
        elif ctx.import_stmt():
            return self.visitImport_stmt(ctx.import_stmt())
        elif ctx.raise_stmt():
            return self.visitRaise_stmt(ctx.raise_stmt())
        elif ctx.PASS():
            return ast.Pass()
        elif ctx.del_stmt():
            return self.visitDel_stmt(ctx.del_stmt())
        elif ctx.yield_stmt():
            return self.visitYield_stmt(ctx.yield_stmt())
        elif ctx.assert_stmt():
            return self.visitAssert_stmt(ctx.assert_stmt())
        elif ctx.BREAK():
            return ast.Break()
        elif ctx.CONTINUE():
            return ast.Continue()
        elif ctx.global_stmt():
            return self.visitGlobal_stmt(ctx.global_stmt())
        elif ctx.nonlocal_stmt():
            return self.visitNonlocal_stmt(ctx.nonlocal_stmt())
        else:
            raise ValueError(f"Unknown symbol: {ctx.getText()}")

    def visitAssignment(self, ctx: FandangoParser.AssignmentContext):
        if ctx.COLON():
            right = self.get_expression(ctx.annotated_rhs())
            if ctx.NAME():
                return ast.AnnAssign(
                    target=ast.Name(id=ctx.NAME().getText()),
                    annotation=self.get_expression(ctx.expression()),
                    value=right,
                    simple=1,
                )
            if ctx.single_target():
                left = self.get_expression(ctx.single_target())
            elif ctx.single_subscript_attribute_target():
                left = self.get_expression(ctx.single_subscript_attribute_target())
            else:
                raise ValueError(
                    f"Unsupported left hand side for assignment {ctx.getText()}"
                )
            return ast.AnnAssign(
                target=left,
                annotation=self.get_expression(ctx.expression()),
                value=right,
                simple=0,
                lineno=0,
            )
        else:
            if ctx.yield_expr():
                value = self.get_expression(ctx.yield_expr())
            elif ctx.star_expressions():
                value = self.get_expression(ctx.star_expressions())
            else:
                raise ValueError(
                    f"Unsupported right hand side for assignment {ctx.getText()}"
                )
            if ctx.ASSIGN():
                return ast.Assign(
                    targets=[
                        self.get_expression(target) for target in ctx.star_targets()
                    ],
                    value=value,
                    lineno=0,
                )
            aug: FandangoParser.AugassignContext = ctx.augassign()
            if aug.ADD_ASSIGN():
                op = ast.Add()
            elif aug.SUB_ASSIGN():
                op = ast.Sub()
            elif aug.MULT_ASSIGN():
                op = ast.Mult()
            elif aug.AT_ASSIGN():
                op = ast.MatMult()
            elif aug.DIV_ASSIGN():
                op = ast.Div()
            elif aug.MOD_ASSIGN():
                op = ast.Mod()
            elif aug.AND_ASSIGN():
                op = ast.BitAnd()
            elif aug.OR_ASSIGN():
                op = ast.BitOr()
            elif aug.XOR_ASSIGN():
                op = ast.BitXor()
            elif aug.LEFT_SHIFT_ASSIGN():
                op = ast.LShift()
            elif aug.RIGHT_SHIFT_ASSIGN():
                op = ast.RShift()
            elif aug.POWER_ASSIGN():
                op = ast.Pow()
            elif aug.IDIV_ASSIGN():
                op = ast.FloorDiv()
            else:
                raise ValueError(
                    f"Unsupported operator for augmented assignment: {aug.getText()}"
                )
            return ast.AugAssign(
                target=self.get_expression(ctx.single_target()),
                op=op,
                value=value,
                lineno=0,
            )

    def visitType_alias(self, ctx: FandangoParser.Type_aliasContext):
        raise UnsupportedOperation(
            "Type alias currently not supported: {ctx.getText()}"
        )

    def visitReturn_stmt(self, ctx: FandangoParser.Return_stmtContext):
        return ast.Return(value=self.get_expression(ctx.star_expressions()))

    def visitRaise_stmt(self, ctx: FandangoParser.Raise_stmtContext):
        return ast.Raise(
            exc=self.get_expression(ctx.expression(0)),
            cause=self.get_expression(ctx.expression(1)),
        )

    def visitGlobal_stmt(self, ctx: FandangoParser.Global_stmtContext):
        return ast.Global(names=[name.getText() for name in ctx.NAME()])

    def visitNonlocal_stmt(self, ctx: FandangoParser.Nonlocal_stmtContext):
        return ast.Nonlocal(names=[name.getText() for name in ctx.NAME()])

    def visitDel_stmt(self, ctx: FandangoParser.Del_stmtContext):
        return ast.Delete(targets=self.get_expression(ctx.del_targets()))

    def visitYield_stmt(self, ctx: FandangoParser.Yield_stmtContext):
        return ast.Expr(value=self.get_expression(ctx.yield_expr()))

    def visitAssert_stmt(self, ctx: FandangoParser.Assert_stmtContext):
        return ast.Assert(
            test=self.get_expression(ctx.expression(0)),
            msg=self.get_expression(ctx.expression(1)),
        )

    def visitImport_stmt(self, ctx: FandangoParser.Import_stmtContext):
        if ctx.import_name():
            return self.visitImport_name(ctx.import_name())
        elif ctx.import_from():
            return self.visitImport_from(ctx.import_from())
        else:
            raise ValueError(f"Unknown symbol: {ctx.getText()}")

    def visitImport_name(self, ctx: FandangoParser.Import_nameContext):
        return ast.Import(names=self.visitDotted_as_names(ctx.dotted_as_names()))

    def visitImport_from(self, ctx: FandangoParser.Import_fromContext):
        level = len(ctx.DOT()) + 3 * len(ctx.ELLIPSIS())
        return ast.ImportFrom(
            module=ctx.dotted_name().getText() if ctx.dotted_name() else None,
            names=self.visitImport_from_targets(ctx.import_from_targets()),
            level=level,
        )

    def visitDotted_as_names(self, ctx: FandangoParser.Dotted_as_namesContext):
        return [self.visitDotted_as_name(name) for name in ctx.dotted_as_name()]

    def visitDotted_as_name(self, ctx: FandangoParser.Dotted_as_nameContext):
        return ast.alias(
            name=ctx.dotted_name().getText(),
            asname=ctx.NAME().getText() if ctx.NAME() else None,
        )

    def visitImport_from_targets(self, ctx: FandangoParser.Import_from_targetsContext):
        if ctx.STAR():
            return [ast.alias(name="*", asname=None)]
        else:
            return self.visitImport_from_as_names(ctx.import_from_as_names())

    def visitImport_from_as_names(
        self, ctx: FandangoParser.Import_from_as_namesContext
    ):
        return [
            self.visitImport_from_as_name(name) for name in ctx.import_from_as_name()
        ]

    def visitImport_from_as_name(self, ctx: FandangoParser.Import_from_as_nameContext):
        return ast.alias(
            name=ctx.NAME(0).getText(),
            asname=ctx.NAME(1).getText() if ctx.NAME(1) else None,
        )

    def visitCompound_stmt(self, ctx: FandangoParser.Compound_stmtContext):
        if ctx.function_def():
            return self.visitFunction_def(ctx.function_def())
        elif ctx.if_stmt():
            return self.visitIf_stmt(ctx.if_stmt())
        elif ctx.class_def():
            return self.visitClass_def(ctx.class_def())
        elif ctx.with_stmt():
            return self.visitWith_stmt(ctx.with_stmt())
        elif ctx.for_stmt():
            return self.visitFor_stmt(ctx.for_stmt())
        elif ctx.try_stmt():
            return self.visitTry_stmt(ctx.try_stmt())
        elif ctx.while_stmt():
            return self.visitWhile_stmt(ctx.while_stmt())
        elif ctx.match_stmt():
            return self.visitMatch_stmt(ctx.match_stmt())
        else:
            raise ValueError(f"Unknown symbol: {ctx.getText()}")

    def visitClass_def(self, ctx: FandangoParser.Class_defContext):
        class_def = self.visitClass_def_raw(ctx.class_def_raw())
        if ctx.decorators():
            class_def.decorator_list = self.visitDecorators(ctx.decorators())
        return class_def

    def visitClass_def_raw(self, ctx: FandangoParser.Class_def_rawContext):
        bases = list()
        keywords = list()
        if ctx.type_params():
            raise UnsupportedOperation(
                f"Type params unsupported for class definitions {ctx.getText()}"
            )
        if ctx.arguments():
            base_trees, base_searches, _ = self.search_processor.visitArguments(
                ctx.arguments()
            )
            if base_searches:
                raise ValueError(
                    f"Nonterminals can only be used in grammars and constraints, not in regular Python code: {ctx.getText()}"
                )
            for base in base_trees:
                if isinstance(base, ast.keyword):
                    keywords.append(base)
                else:
                    bases.append(base)
        body = self.visitBlock(ctx.block())
        return ast.ClassDef(
            name=ctx.NAME().getText(),
            bases=bases,
            keywords=keywords,
            body=body,
            decorator_list=[],
        )

    def visitFunction_def(self, ctx: FandangoParser.Function_defContext):
        function_def = self.visitFunction_def_raw(ctx.function_def_raw())
        if ctx.decorators():
            function_def.decorator_list = self.visitDecorators(ctx.decorators())
        return function_def

    def visitFunction_def_raw(self, ctx: FandangoParser.Function_def_rawContext):
        if ctx.type_params():
            raise UnsupportedOperation(
                f"Type params unsupported for class definitions: {ctx.getText()}"
            )
        if ctx.params():
            params = self.visitParams(ctx.params())
        else:
            params = list()
        body = self.visitBlock(ctx.block())
        if ctx.ASYNC():
            class_ = ast.AsyncFunctionDef
        else:
            class_ = ast.FunctionDef
        return class_(
            name=ctx.NAME().getText(),
            args=params,
            body=body,
            decorator_list=[],
            returns=self.get_expression(ctx.expression()),
            type_comment=None,
            lineno=0,
        )

    def visitDecorators(self, ctx: FandangoParser.DecoratorsContext):
        decorators = list()
        for expression in ctx.named_expression():
            tree, searches, _ = self.search_processor.visitNamed_expression(expression)
            if searches:
                raise ValueError(
                    f"Nonterminals can only be used in grammars and constraints, not in regular Python code: {ctx.getText()}"
                )
            decorators.append(expression)
        return decorators

    def visitBlock(self, ctx: FandangoParser.BlockContext):
        if ctx.statements():
            return self.visitStatements(ctx.statements())
        elif ctx.simple_stmts():
            return self.visitSimple_stmts(ctx.simple_stmts())
        else:
            raise ValueError(f"Unknown symbol: {ctx.getText()}")

    def visitParams(self, ctx: FandangoParser.ParamsContext):
        return self.get_expression(ctx.parameters())

    def _process_if(
        self, ctx: FandangoParser.If_stmtContext | FandangoParser.Elif_stmtContext
    ):
        test = self.get_expression(ctx.named_expression())
        body = self.visitBlock(ctx.block())
        if ctx.elif_stmt():
            orelse = [self._process_if(ctx.elif_stmt())]
        elif ctx.else_block():
            orelse = self.visitBlock(ctx.else_block().block())
        else:
            orelse = None
        return ast.If(
            test=test,
            body=body,
            orelse=orelse,
        )

    def visitIf_stmt(self, ctx: FandangoParser.If_stmtContext):
        return self._process_if(ctx)

    def visitElif_stmt(self, ctx: FandangoParser.Elif_stmtContext):
        return self._process_if(ctx)

    def visitWith_stmt(self, ctx: FandangoParser.With_stmtContext):
        items = [self.visitWith_item(item) for item in ctx.with_item()]
        body = self.visitBlock(ctx.block())
        if ctx.ASYNC():
            return ast.AsyncWith(
                items=items,
                body=body,
                lineno=0,
            )
        return ast.With(
            items=items,
            body=body,
            lineno=0,
        )

    def visitWith_item(self, ctx: FandangoParser.With_itemContext):
        return ast.withitem(
            context_expr=self.get_expression(ctx.expression()),
            optional_vars=self.get_expression(ctx.star_target()),
        )

    def visitFor_stmt(self, ctx: FandangoParser.For_stmtContext):
        target = self.get_expression(ctx.star_targets())
        iter_ = self.get_expression(ctx.star_expressions())
        body = self.visitBlock(ctx.block())
        if ctx.else_block():
            orelse = self.visitBlock(ctx.else_block().block())
        else:
            orelse = None
        if ctx.ASYNC():
            return ast.AsyncFor(
                target=target,
                iter=iter_,
                body=body,
                orelse=orelse,
                lineno=0,
            )
        return ast.For(
            target=target,
            iter=iter_,
            body=body,
            orelse=orelse,
            lineno=0,
        )

    def visitWhile_stmt(self, ctx: FandangoParser.While_stmtContext):
        if ctx.else_block():
            orelse = self.visitBlock(ctx.else_block().block())
        else:
            orelse = None
        return ast.While(
            test=self.get_expression(ctx.named_expression()),
            body=self.visitBlock(ctx.block()),
            orelse=orelse,
        )

    def visitTry_stmt(self, ctx: FandangoParser.Try_stmtContext):
        body = self.visitBlock(ctx.block())
        if ctx.else_block():
            orelse = self.visitBlock(ctx.else_block().block())
        else:
            orelse = None
        if ctx.finally_block():
            finalbody = self.visitBlock(ctx.finally_block().block())
        else:
            finalbody = None
        if ctx.except_star_block():
            return ast.TryStar(
                body=body,
                handlers=[
                    self.visitExcept_star_block(handler)
                    for handler in ctx.except_star_block()
                ],
                orelse=orelse,
                finalbody=finalbody,
            )
        return ast.Try(
            body=body,
            handlers=[
                self.visitExcept_block(handler) for handler in ctx.except_block()
            ],
            orelse=orelse,
            finalbody=finalbody,
        )

    def visitExcept_block(self, ctx: FandangoParser.Except_blockContext):
        if ctx.NAME():
            name = ctx.NAME().getText()
        else:
            name = None
        return ast.ExceptHandler(
            type=self.get_expression(ctx.expression()),
            name=name,
            body=self.visitBlock(ctx.block()),
        )

    def visitExcept_star_block(self, ctx: FandangoParser.Except_star_blockContext):
        if ctx.NAME():
            name = ctx.NAME().getText()
        else:
            name = None
        return ast.ExceptHandler(
            type=self.get_expression(ctx.expression()),
            name=name,
            body=self.visitBlock(ctx.block()),
        )

    def visitMatch_stmt(self, ctx: FandangoParser.Match_stmtContext):
        raise UnsupportedOperation(
            f"Match statement currently not supported: {ctx.getText()}"
        )
