import json
import sys
import os
import subprocess
import argparse
import tempfile
from cachetools import LRUCache
from pathlib import Path
from fandango.logger import LOGGER


def valid_directory(d):
    if not os.path.isdir(d):
        raise argparse.ArgumentTypeError(f"'{d}' is not an existing directory.")
    return d


def valid_file(f):
    if not os.path.isfile(f):
        raise argparse.ArgumentTypeError(f"'{f}' is not an existing file.")
    return f


class StaticAnalysis:
    def __init__(self, cfg_directory: str, bb_to_dbg_json: str):
        self.cfg_directory = cfg_directory
        self.bb_to_dbg_json = bb_to_dbg_json

        self.cg = {}
        self.cfgs = {}
        self.module_bb_to_f = {}
        self.module_f_to_first_bb = {}
        self.goal_bbid = None
        self.goal_module = None
        self.module_bbid_to_dbg = {}
        self.call_dist_to_target = (
            {}
        )  # maps target (m,f) to the distances from each function to it
        self.bb_dist_to_target = (
            {}
        )  # maps target (m,bb) to the distances from each bb to it
        self.total_bb_count = None
        self.setup()
        self.resolved = {}

    def setup(self):
        self.read_cg_cfgs()
        self.read_bb_dbg_info()

    def resolve(self, module_suffix: str):
        """
        This function resolves the module name suffix to the full path.
        The purpose is to make it easier to specify constraints.
        E.g., the user can specify "f9.c" or "src/f9" in the constraints,
        instead of the full path. This also makes it easier to write
        tests as we do not need to hardcode the full path.
        """
        if module_suffix not in self.resolved:
            for module in self.cfgs:
                if module.endswith(module_suffix):
                    if module_suffix in self.resolved:
                        print(
                            f"Error: multiple matches for {module_suffix}: {self.resolved[module_suffix]} and {module}"
                        )
                        sys.exit(1)
                    else:
                        self.resolved[module_suffix] = module
        return self.resolved[module_suffix]

    def get_total_bb_count(self):
        if self.total_bb_count is None:
            self.total_bb_count = sum(
                len(self.cfgs[m][f]) for m in self.cfgs for f in self.cfgs[m]
            )
        return self.total_bb_count

    def read_cg_cfgs(self):
        print("[*] Reading control-flow graphs")
        for json_file in Path(self.cfg_directory).glob("*.json"):
            print(f"Processing file: {json_file}")
            # function = json_file.stem
            module = json_file.stem
            module = module.replace("@", "/")

            with open(json_file, "r") as f:
                module_cfg = json.load(f)
                self.cfgs[module] = (
                    module_cfg if module_cfg is not None else {}
                )  # e.g., not statically linked, CFG is empty

            self.cg[module] = {}
            for function in self.cfgs[module]:
                self.cg[module][function] = set()
                for bbid in self.cfgs[module][function]:
                    for callee_module, callee_function in self.cfgs[module][function][
                        bbid
                    ]["callees"]:
                        self.cg[module][function].add((callee_module, callee_function))
                    if module not in self.module_bb_to_f:
                        self.module_bb_to_f[module] = {}
                    self.module_bb_to_f[module][bbid] = function
                self.cg[module][function] = list(self.cg[module][function])

                self.module_f_to_first_bb[(module, function)] = str(
                    min(int(k) for k in self.cfgs[module][function].keys())
                )

    def read_goal(self):
        print("[*] Reading goal")
        with open(self.goal_json, "r") as f:
            j = json.load(f)
            self.goal_module = j["module_id"]
            self.goal_bbid = j["bb_id"]

    def read_bb_dbg_info(self):
        print("[*] Reading BB debug information")
        with open(self.bb_to_dbg_json, "r") as f:
            self.module_bbid_to_dbg = json.load(f)

    def _module_bbid_to_dbg(self, module: str, bbid: str):
        return (
            self.module_bbid_to_dbg[module][bbid][-1]
            if (
                module in self.module_bbid_to_dbg
                and bbid in self.module_bbid_to_dbg[module]
            )
            else "N/A"
        )

    def compute_call_distance_to_target_function(
        self, target_module: str, target_function: str
    ):
        self.call_dist_to_target[(target_module, target_function)] = {}
        for _m in self.cg:
            for _f in self.cg[_m]:
                q = [(_m, _f, 0)]
                visited = set()
                while q != []:
                    m, f, dist = q.pop(0)

                    if (m, f) in visited:
                        continue
                    visited.add((m, f))

                    if m == target_module and f == target_function:
                        self.call_dist_to_target[(target_module, target_function)][
                            (_m, _f)
                        ] = dist  # _m, _f !
                        break

                    if m == "__external__":
                        continue  # declaration only
                    for callee_module, callee_function in self.cg[m][f]:
                        if (callee_module, callee_function) not in visited:
                            q.append((callee_module, callee_function, dist + 1))
                if (_m, _f) not in self.call_dist_to_target[
                    (target_module, target_function)
                ]:
                    self.call_dist_to_target[(target_module, target_function)][
                        (_m, _f)
                    ] = float("inf")

    def intraprocedural_distances(self, target_module: str, target_bb: str):
        """
        This function computes the intraprocedural BB distance from each basic block in
        the target function to the target basic block using BFS, storing
        the result in self.bb_dist_to_target[(target_module, target_bb)].
        """
        target_function = self.module_bb_to_f[target_module][target_bb]

        for _bb in self.cfgs[target_module][target_function]:
            q = [(_bb, 0)]
            visited = set()
            while q != []:
                bb, dist = q.pop(0)
                if bb in visited:
                    continue
                visited.add(bb)

                if bb == target_bb:
                    self.bb_dist_to_target[(target_module, target_bb)][
                        (target_module, _bb)
                    ] = dist
                    break

                # Counting conditional, unconditional branches, invoke-branches indifferently
                for _, successor_bbid in self.cfgs[target_module][target_function][bb][
                    "successors"
                ]:
                    if successor_bbid not in visited:
                        q.append((successor_bbid, dist + 1))

    def compute_distance_to_target_bb(self, target_module: str, target_bbid: str):
        """
        This function computes the interprocedural BB distance from
        each basic block in the program to the target basic block, storing
        the result in self.bb_dist_to_target[(target_module, target_bb)].
        Implementation is similar to AFLGo's distance computation.
        It differs in the way that AFLGo adds up BB distance for each BB in seed,
        where as we only care about the minimum distance.
        """

        if target_bbid not in self.module_bb_to_f[target_module]:
            print_reason()
            sys.exit(1)

        # [A] if current_bb in target_function and can_reach_target_bb: distance = intra_procedural_bb_distance(current_bb, target_bb)
        # [B] elif current_bb can reach call into call chain to target function:
        #   -> dist = lowest_bb_distance_to_reaching_call_to_target_function + 10*call_distance_from_that_reaching_point + distBB(Target_functionheaderBB, Target_BB)
        # [C] else: dist = float('inf')

        self.bb_dist_to_target[(target_module, target_bbid)] = {
            (m, bbid): float("inf")
            for m in self.cfgs
            for f in self.cfgs[m]
            for bbid in self.cfgs[m][f]
        }

        self.intraprocedural_distances(target_module, target_bbid)  # Precompute [A]
        target_function_bbs = set(
            int(key)
            for key in self.cfgs[target_module][
                self.module_bb_to_f[target_module][target_bbid]
            ].keys()
        )
        target_function_header_bb = str(min(target_function_bbs))
        bb_dist_target_function_header_to_target_bb = self.bb_dist_to_target[
            (target_module, target_bbid)
        ][(target_module, target_function_header_bb)]

        target_function = self.module_bb_to_f[target_module][target_bbid]
        if (target_module, target_function) not in self.call_dist_to_target:
            # We need to compute this only once to fill
            # `self.sa.call_dist_to_target[(module_name, function_name)]`
            self.compute_call_distance_to_target_function(
                target_module, target_function
            )

        for m in self.cg:
            for f in self.cg[m]:
                if f == target_function:
                    # Computed previously in self.intraprocedural_distances() [A]
                    continue

                for bb in self.cfgs[m][f]:
                    # Get distance for current BB and store it in `self.bb_dist_to_target[(target_module, target_bbid)][(m, bb)]`
                    # Update `self.bb_dist_to_target[(target_module, target_bbid)][(m, bb)]` with min(existing, new),
                    # where new is the distance computed for every shortest path from `bb` to a call that can reach the target function
                    visited = set()
                    q = [(m, bb, 0)]
                    while q != []:
                        _m, _bb, control_flow_dist = q.pop(0)

                        if (_m, _bb) in visited:
                            continue
                        visited.add((_m, _bb))

                        for callee_module, callee_function in self.cfgs[m][f][_bb][
                            "callees"
                        ]:
                            # if callee is not in self.dist_call_to_goal, it's a declaration only
                            if (
                                callee_module,
                                callee_function,
                            ) in self.call_dist_to_target[
                                (target_module, target_function)
                            ]:
                                intraprocedural_distance_to_reach_call = (
                                    control_flow_dist
                                )
                                call_weight = 10  # AFLGo
                                # +1 because we need to call that function first
                                call_distance_to_target_function = call_weight * (
                                    1
                                    + self.call_dist_to_target[
                                        (target_module, target_function)
                                    ][(callee_module, callee_function)]
                                )

                                dist = (
                                    (intraprocedural_distance_to_reach_call)
                                    + (10 * call_distance_to_target_function)
                                    + (bb_dist_target_function_header_to_target_bb)
                                )

                                self.bb_dist_to_target[(target_module, target_bbid)][
                                    (m, bb)
                                ] = min(
                                    dist,
                                    self.bb_dist_to_target[
                                        (target_module, target_bbid)
                                    ][(m, bb)],
                                )

                        for successor_module, successor_bbid in self.cfgs[m][f][_bb][
                            "successors"
                        ]:
                            if (successor_module, successor_bbid) not in visited:
                                q.append(
                                    (
                                        successor_module,
                                        successor_bbid,
                                        control_flow_dist + 1,
                                    )
                                )


class DynamicAnalysis:
    def __init__(
        self, sa: StaticAnalysis, root_dir: str, put: str, put_args: list[str] = None
    ):
        self.sa = sa
        self.root_dir = root_dir
        self.put = put
        self.put_args = put_args if put_args is not None else []
        self.cache: dict[str, Trace] = LRUCache(maxsize=1000)

    # TODO: Implement this similarly to the Fandango "run with cmd" feature.
    def trace_input(self, inp: str):
        if inp in self.cache:
            return self.cache[inp]
        env = os.environ.copy()
        with tempfile.NamedTemporaryFile(
            mode="w", prefix="fandango-", suffix=".txt"
        ) as inp_fd:
            inp_fd.write(inp)
            inp_fd.flush()

            with tempfile.NamedTemporaryFile(
                mode="w", prefix="execution-trace-", suffix=".json"
            ) as trace_fd:
                execution_trace_json = trace_fd.name
                env["EXECUTION_TRACE_JSON"] = execution_trace_json
                LOGGER.info(f"Running input: (len: {len(inp)})")
                LOGGER.info(inp)
                result = subprocess.run(
                    [self.put] + self.put_args + [inp_fd.name],
                    cwd=self.root_dir,
                    env=env,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=10,  # kill after 10 seconds
                )

                with open(execution_trace_json, mode="r", encoding="utf-8") as jsonf:
                    trace = Trace(self.sa, json.load(jsonf))
                    self.cache[inp] = trace
                    return trace


class Trace:
    def __init__(self, sa: StaticAnalysis, trace: dict):
        self.sa = sa
        self.trace = trace

    ###############################################
    ## Helpers functions for objective functions ##
    ###############################################

    def CoveredBasicBlocks(self) -> set:
        covered = set()
        for module in self.trace["trace"]:
            for bb_id in self.trace["trace"][module]:
                hit_count = self.trace["trace"][module][bb_id]
                if hit_count != 0:
                    covered.add((module, bb_id))
        return covered

    def CoveredFunctions(self) -> set:
        functions = set()
        for module in self.trace["trace"]:
            for bb_id in self.trace["trace"][module]:
                hit_count = self.trace["trace"][module][bb_id]
                if hit_count != 0:
                    if bb_id in self.sa.module_bb_to_f[module]:
                        mf = (module, self.sa.module_bb_to_f[module][bb_id])
                        functions.add(mf)
        return functions

    def CoveredBasicBlocksInFunction(self, module_name: str, function_name: str):
        module_name = self.sa.resolve(module_name)
        covered = set()
        for module in self.trace["trace"]:
            for bb_id in self.trace["trace"][module]:
                hit_count = self.trace["trace"][module][bb_id]
                if hit_count != 0:
                    if module == module_name:
                        if bb_id in self.sa.module_bb_to_f[module]:
                            f = self.sa.module_bb_to_f[module][bb_id]
                            if f == function_name:
                                covered.add(bb_id)
            return covered

    ###################################################################
    ## Objective functions, which can be used in Fadango constraints ##
    ###################################################################

    # a.k.a. "SlowFuzz"
    def ExecutionPathLength(self):
        total = 0
        for module in self.trace["trace"]:
            for bb_id in self.trace["trace"][module]:
                hit_count = self.trace["trace"][module][bb_id]
                total += hit_count
        LOGGER.info("Execution path length: %d", total)
        return total

    # a.k.a. "PerfFuzz"
    def HottestBasicBlock(self):
        hottest = 0
        for module in self.trace["trace"]:
            for bb_id in self.trace["trace"][module]:
                hit_count = self.trace["trace"][module][bb_id]
                hottest = max(hottest, hit_count)
        return hottest

    # a.k.a. "mem"
    def HeapAllocatedBytes(self):
        LOGGER.info("Heap allocated bytes: %d", self.trace["allocated_bytes"])
        return self.trace["allocated_bytes"]

    def CodeCoverage(self):
        return len(self.CoveredBasicBlocks())

    def FunctionCoverage(self):
        return len(self.CoveredFunctions())

    def CodeCoverageInFunction(self, module_name: str, function_name: str):
        module_name = self.sa.resolve(module_name)
        return len(self.CoveredBasicBlocksInFunction(module_name, function_name))

    def DistanceToFunction(self, module_name: str, function_name: str):
        module_name = self.sa.resolve(module_name)
        first_bb = self.sa.module_f_to_first_bb[(module_name, function_name)]
        return self.DistanceToBB(module_name, first_bb)

    def DistanceToBB(self, module_name: str, bb_id: str):
        module_name = self.sa.resolve(module_name)
        if (module_name, bb_id) not in self.sa.bb_dist_to_target:
            # We need to compute this only once to fill
            # `self.sa.bb_dist_to_target[(module_name, bb_id)]`
            self.sa.compute_distance_to_target_bb(module_name, bb_id)

        dist = float("inf")
        for cur_module, cur_bb in self.CoveredBasicBlocks():
            if (cur_module, cur_bb) not in self.sa.bb_dist_to_target[
                (module_name, bb_id)
            ]:
                # Comment: see print_reason().
                continue

            dist = min(
                dist,
                self.sa.bb_dist_to_target[(module_name, bb_id)][(cur_module, cur_bb)],
            )
        return dist


def print_reason():
    print(
        """
    In rare cases, BBIDs may not be in the static analysis info, but dynamic
    analysis can generate them.
    E.g., ('/Users/name/Downloads/lunasvg/source/lunasvg.cpp', '417')
    Reason: BBID is part of an inlined libc++ function,
    which was inlined in more than one translation unit with linkage
    linkonce_odr. After linking, only one implementation is kept, and the others
    are discarded.
    The underlying reason is that static analysis is based on llvm-link'd .bc's,
    while dynamic analysis is based on the binary linked with the default linker,
    it seems like they make different choices w.r.t which implementation is kept.
    So we ignore traces of these functions which are not in the static analysis info,
    which only affected uninteresting inlined libc++ functions so far.
    """
    )
