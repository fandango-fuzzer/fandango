from typing import Optional, Any
from itertools import zip_longest
import random
from fandango.constraints.constraint import Constraint
from fandango.constraints.constraint_visitor import ConstraintVisitor
from fandango.constraints.fitness import ConstraintFitness, FailingTree
from fandango.constraints.failing_tree import (
    BoundsFailingTree,
    Comparison,
    ComparisonSide,
)
from fandango.errors import FandangoValueError
from fandango.language.grammar.grammar import Grammar
from fandango.language.grammar.nodes.repetition import Repetition
from fandango.language.search import NonTerminalSearch
from fandango.language.symbols.non_terminal import NonTerminal
from fandango.language.tree import DerivationTree, index_by_reference


class RepetitionBoundsConstraint(Constraint):
    """
    Represents a constraint that checks the number of repetitions of a certain pattern in a tree.
    This is useful for ensuring that certain patterns do not occur too frequently or too infrequently.
    """

    def __init__(
        self,
        repetition_id: str,
        expr_data_min: tuple[str, list, dict],
        expr_data_max: tuple[str, list, dict],
        repetition_node: Repetition,
        *args,
        **kwargs,
    ):
        """
        Initializes the repetition bounds constraint with the given pattern and repetition bounds.
        :param NonTerminalSearch pattern: The pattern to check for repetitions.
        :param int min_reps: The minimum number of repetitions allowed.
        :param int max_reps: The maximum number of repetitions allowed.
        :param args: Additional arguments.
        :param kwargs: Additional keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.repetition_id = repetition_id
        self.expr_data_min = expr_data_min
        self.expr_data_max = expr_data_max
        self.search_min: Optional[NonTerminalSearch] = None
        self.search_max: Optional[NonTerminalSearch] = None
        if len(expr_data_min[1]) == 0:
            self.search_min = None
        elif len(expr_data_min[1]) == 1:
            self.search_min = expr_data_min[1][0]
        else:
            raise FandangoValueError(
                "RepetitionBoundsConstraint requires exactly one or zero searches for expr_data_max bound"
            )

        if len(expr_data_max[1]) == 0:
            self.search_max = None
        elif len(expr_data_max[1]) == 1:
            self.search_max = expr_data_max[1][0]
        else:
            raise FandangoValueError(
                "RepetitionBoundsConstraint requires exactly one or zero searches for expr_data_max bound"
            )
        self.repetition_node = repetition_node

    def _compute_rep_bound(
        self, tree_rightmost_relevant_node: "DerivationTree", expr_data
    ):
        expr, _, searches = expr_data
        local_cpy = self.local_variables.copy()

        if len(searches) == 0:
            return eval(expr, self.global_variables, local_cpy)

        nodes = []
        if len(searches) != 1:
            raise FandangoValueError(
                "Computed repetition requires exactly one or zero searches"
            )

        search_name, search = next(iter(searches.items()))
        max_path = tree_rightmost_relevant_node.get_choices_path()
        for container in search.find(tree_rightmost_relevant_node.get_root()):
            container_tree: DerivationTree = container.evaluate()
            search_in_bounds = True
            zip_var = list(zip_longest(max_path, container_tree.get_choices_path()))
            for i, (max_step, search_step) in enumerate(zip_var):
                if max_step is None:
                    break
                if search_step is None:
                    break
                if max_step.index > search_step.index:
                    break
                if max_step.index < search_step.index:
                    search_in_bounds = False
                    break
            if not search_in_bounds:
                continue
            nodes.append(container_tree)

        if len(nodes) == 0:
            raise FandangoValueError(
                f"Couldn't find search target ({search}) in prefixed DerivationTree for computed repetition"
            )

        target = nodes[-1]
        local_cpy[search_name] = target
        return eval(expr, self.global_variables, local_cpy), target

    def min(self, tree_stop_before: DerivationTree):
        return self._compute_rep_bound(tree_stop_before, self.expr_data_min)

    def max(self, tree_stop_before: DerivationTree):
        return self._compute_rep_bound(tree_stop_before, self.expr_data_max)

    def group_by_repetition_id(
        self, id_trees: list[DerivationTree]
    ) -> dict[tuple[str, int], dict[int, list[DerivationTree]]]:
        reference_trees: dict[tuple[str, int], dict[int, list[DerivationTree]]] = {}
        for id_tree in id_trees:
            iteration_ids: list[tuple[str, int, int]] = list(
                filter(lambda x: x[0] == self.repetition_id, id_tree.origin_repetitions)
            )
            for i_id in iteration_ids:
                call_id = tuple[str, int](i_id[:2])
                rep_round = i_id[2]
                # Group by id and repetition round

                if call_id not in reference_trees:
                    reference_trees[call_id] = dict()
                iter_list = reference_trees[call_id]
                if rep_round not in iter_list:
                    iter_list[rep_round] = []
                iter_list[rep_round].append(id_tree)
        return reference_trees

    def fitness(
        self,
        tree: DerivationTree,
        scope: Optional[dict[NonTerminal, DerivationTree]] = None,
        population: Optional[list[DerivationTree]] = None,
        local_variables: Optional[dict[str, Any]] = None,
    ) -> ConstraintFitness:
        """
        Calculate the fitness of the tree based on the number of repetitions of the pattern.
        :param DerivationTree tree: The tree to evaluate.
        :param Optional[dict[NonTerminal, DerivationTree]] scope: The scope of the tree.
        :param Optional[list[DerivationTree]] population: The population of trees.
        :param Optional[dict[str, Any]] local_variables: Local variables to use in the evaluation.
        :return ConstraintFitness: The fitness of the tree.
        """
        id_trees = tree.find_by_origin(self.repetition_id)
        if len(id_trees) == 0:
            # Assume that the field containing the nr of repetitions is zero.
            # This is the case where we might have deleted all repetitions from the tree.
            return ConstraintFitness(1, 1, True)

        reference_trees = self.group_by_repetition_id(id_trees)
        failing_trees: list[FailingTree] = []
        solved = 0
        total = len(reference_trees.keys())

        for call_id in reference_trees.keys():
            iter_list = reference_trees[call_id]
            smallest_rep = min(iter_list.keys())
            highest_rep = max(iter_list.keys())
            first_iteration = iter_list[smallest_rep][0]
            last_iteration = iter_list[highest_rep][-1]

            max_bounds_search = first_iteration
            assert max_bounds_search.parent is not None
            while (
                index_by_reference(max_bounds_search.parent.children, max_bounds_search)
                == 0
            ):
                max_bounds_search = max_bounds_search.parent
                assert max_bounds_search.parent is not None

            parent = max_bounds_search.parent
            assert parent is not None
            index = index_by_reference(parent.children, max_bounds_search)
            assert (
                index is not None and index > 0
            ), "Invalid child index for bounds search"
            max_bounds_search = parent.children[index - 1]

            bound_min, min_ref_tree = self.min(max_bounds_search)
            bound_max, max_ref_tree = self.max(max_bounds_search)
            bound_len = len(iter_list)

            if bound_min <= bound_len <= bound_max:
                solved += 1
            else:
                iter_id = call_id[1]
                suggestions: list[tuple[Comparison, Any, ComparisonSide]] = []
                goal_len = random.randint(bound_min, bound_max)
                suggestions.append(
                    (
                        Comparison.EQUAL,
                        (iter_id, bound_len, goal_len),
                        ComparisonSide.RIGHT,
                    )
                )
                suggestions.append(
                    (
                        Comparison.EQUAL,
                        (iter_id, bound_len, goal_len),
                        ComparisonSide.LEFT,
                    )
                )
                assert first_iteration.parent is not None
                failing_trees.append(
                    BoundsFailingTree(
                        first_iteration.parent,
                        first_iteration,
                        last_iteration,
                        min_ref_tree,
                        max_ref_tree,
                        self,
                        suggestions=suggestions,
                    )
                )

        return ConstraintFitness(
            solved, total, solved == total, failing_trees=failing_trees
        )

    def get_first_common_node(
        self, tree_a: DerivationTree, tree_b: DerivationTree
    ) -> DerivationTree:
        common_node = tree_a.get_root(True)
        for a_path, b_path in zip(tree_a.get_choices_path(), tree_b.get_choices_path()):
            if a_path.index == b_path.index:
                common_node = common_node.children[a_path.index]
            else:
                break
        return common_node

    def fix_individual(
        self,
        grammar: Grammar,
        failing_tree: BoundsFailingTree,
        allow_repetition_full_delete: bool,
    ) -> list[tuple[DerivationTree, DerivationTree]]:
        if failing_tree.tree.read_only:
            return []
        replacements: list[tuple[DerivationTree, DerivationTree]] = list()
        for operator, value, side in failing_tree.suggestions:
            if operator == Comparison.EQUAL and side == ComparisonSide.LEFT:
                iter_id, bound_len, goal_len = value
                if goal_len > bound_len:
                    replacements.append(
                        self.insert_repetitions(
                            nr_to_insert=goal_len - bound_len,
                            rep_iteration=iter_id,
                            grammar=grammar,
                            tree=failing_tree.tree,
                            end_rep=failing_tree.ending_rep_tree,
                        )
                    )
                else:
                    if goal_len == 0 and not allow_repetition_full_delete:
                        if not allow_repetition_full_delete:
                            goal_len = 1
                    if goal_len == bound_len:
                        continue
                    delete_replace_pair = self.delete_repetitions(
                        nr_to_delete=bound_len - goal_len,
                        rep_iteration=iter_id,
                        tree=failing_tree.tree,
                    )
                    if goal_len == 0:
                        delete_replacement: DerivationTree = delete_replace_pair[1]
                        node_a = self.get_first_common_node(
                            failing_tree.tree, failing_tree.starting_rep_value
                        )
                        node_b = self.get_first_common_node(
                            failing_tree.tree, failing_tree.ending_rep_value
                        )
                        node_c = self.get_first_common_node(
                            failing_tree.starting_rep_value,
                            failing_tree.ending_rep_value,
                        )
                        # Get the node that is closest to root
                        first_node = sorted(
                            [node_a, node_b, node_c], key=lambda x: len(x.get_path())
                        )[0]
                        replacement = first_node.deepcopy(
                            copy_children=True, copy_params=False, copy_parent=False
                        )
                        replacement = replacement.replace_multiple(
                            grammar=grammar,
                            replacements=[(failing_tree.tree, delete_replacement)],
                            current_path=first_node.get_choices_path(),
                        )

                        read_only_start_idx = len(first_node.get_path()) - 1
                        current_node = replacement
                        for path_node in failing_tree.tree.get_choices_path()[
                            read_only_start_idx:
                        ]:
                            current_node = current_node.children[path_node.index]
                            current_node.read_only = True
                        current_node = replacement
                        for (
                            path_node
                        ) in failing_tree.starting_rep_value.get_choices_path()[
                            read_only_start_idx:
                        ]:
                            current_node = current_node.children[path_node.index]
                            current_node.read_only = True
                        current_node.set_all_read_only(True)
                        current_node = replacement
                        for (
                            path_node
                        ) in failing_tree.ending_rep_value.get_choices_path()[
                            read_only_start_idx:
                        ]:
                            current_node = current_node.children[path_node.index]
                            current_node.read_only = True
                        current_node.set_all_read_only(True)
                        replacements.append((first_node, replacement))
                    else:
                        replacements.append(delete_replace_pair)
                continue
        return replacements

    def insert_repetitions(
        self,
        *,
        nr_to_insert: int,
        rep_iteration: int,
        grammar: "Grammar",
        tree: DerivationTree,
        end_rep: DerivationTree,
    ) -> tuple[DerivationTree, DerivationTree]:
        assert end_rep.parent is not None, "end_rep must have a parent"
        index = index_by_reference(end_rep.parent, end_rep)
        if index is None:
            raise ValueError("end_rep not found in its parent's children")
        insertion_index = index + 1

        starting_rep = 0
        for ref in end_rep.origin_repetitions:
            if ref[0] == self.repetition_id and ref[1] == rep_iteration:
                assert ref[2] is not None, "repetition index (ref[2]) must not be None"
                starting_rep = ref[2] + 1

        old_tree_children = tree.children
        tree.set_children([])

        self.repetition_node.fuzz(
            tree,
            grammar,
            override_starting_repetition=starting_rep,
            override_current_iteration=rep_iteration,
            override_iterations_to_perform=starting_rep + nr_to_insert,
        )

        insert_children = tree.children
        tree.set_children(old_tree_children)

        copy_parent = tree.deepcopy(
            copy_children=True,
            copy_parent=False,
            copy_params=False,
        )
        copy_parent.set_children(
            copy_parent.children[:insertion_index]
            + insert_children
            + copy_parent.children[insertion_index:]
        )

        return tree, copy_parent

    def delete_repetitions(
        self, *, nr_to_delete: int, rep_iteration: int, tree: DerivationTree
    ) -> tuple[DerivationTree, DerivationTree]:
        copy_parent = tree.deepcopy(
            copy_children=True, copy_parent=False, copy_params=False
        )
        curr_rep_id = None
        reps_deleted = 0
        new_children: list[DerivationTree] = []
        for child in copy_parent.children[::-1]:
            repetition_node_id = self.repetition_id
            matching_o_nodes = list(
                filter(
                    lambda x: x[0] == repetition_node_id and x[1] == rep_iteration,
                    child.origin_repetitions,
                )
            )
            if len(matching_o_nodes) == 0:
                new_children.insert(0, child)
                continue
            matching_o_node = matching_o_nodes[0]
            rep_id = matching_o_node[2]
            if curr_rep_id != rep_id and reps_deleted >= nr_to_delete:
                # We have deleted enough repetitions iteratively add all remaining children
                new_children.insert(0, child)
                continue
            curr_rep_id = rep_id
            reps_deleted += 1
        copy_parent.set_children(new_children)
        return tree, copy_parent

    def format_as_spec(self) -> str:
        if self.search_min is None:
            print_min, _, _ = self.expr_data_min
        else:
            print_min = self.search_min.format_as_spec()
        if self.search_max is None:
            print_max, _, _ = self.expr_data_max
        else:
            print_max = self.search_max.format_as_spec()
        return f"RepetitionBounds({print_min} <= |{self.repetition_node.node.format_as_spec()}| <= {print_max})"

    def accept(self, visitor: "ConstraintVisitor"):
        """Accepts a visitor to traverse the constraint structure."""
        visitor.visit_repetition_bounds_constraint(self)

    def invert(self):
        """
        RepetitionBoundsConstraint are not inverted.
        """
        raise NotImplementedError("RepetitionBoundsConstraints should not be inverted.")
