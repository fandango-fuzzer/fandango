import os
import subprocess
import tempfile
import json
from typing import Any, Optional, Union, cast
from cachetools import LRUCache

from fandango.execution.trace_types import (
    ModuleName,
    BasicBlockID,
    ModuleBBID,
    ModuleFunction,
)
from fandango.execution.static_analysis import StaticAnalysis
from fandango.logger import LOGGER


class Trace:
    def __init__(
        self,
        sa: Optional[StaticAnalysis],
        trace: dict[str, Union[int, dict[ModuleName, dict[BasicBlockID, int]]]],
    ):
        self.sa = sa
        self.trace = trace

    ###############################################
    ## Helpers functions for objective functions ##
    ###############################################

    def CoveredBasicBlocks(self) -> set[ModuleBBID]:
        covered = set()
        assert isinstance(self.trace["trace"], dict)
        for module in self.trace["trace"]:
            for bb_id in self.trace["trace"][module]:
                hit_count = self.trace["trace"][module][bb_id]
                if hit_count != 0:
                    covered.add((module, bb_id))
        return covered

    def CoveredFunctions(self) -> set[ModuleFunction]:
        assert self.sa
        functions = set()
        assert isinstance(self.trace["trace"], dict)
        for module in self.trace["trace"]:
            for bb_id in self.trace["trace"][module]:
                hit_count = self.trace["trace"][module][bb_id]
                if hit_count != 0:
                    if bb_id in self.sa.module_bb_to_f[module]:
                        mf = (module, self.sa.module_bb_to_f[module][bb_id])
                        functions.add(mf)
        return functions

    def CoveredBasicBlocksInFunction(
        self, module_name: str, function_name: str
    ) -> set[BasicBlockID]:
        assert self.sa
        module_name = self.sa.resolve(module_name)
        covered = set()
        assert isinstance(self.trace["trace"], dict)
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
    def ExecutionPathLength(self) -> int:
        total = 0
        assert isinstance(self.trace["trace"], dict)
        for module in self.trace["trace"]:
            for bb_id in self.trace["trace"][module]:
                hit_count = self.trace["trace"][module][bb_id]
                total += hit_count
        LOGGER.info("Execution path length: %d", total)
        return total

    # a.k.a. "PerfFuzz"
    def HottestBasicBlock(self) -> int:
        hottest = 0
        assert isinstance(self.trace["trace"], dict)
        for module in self.trace["trace"]:
            for bb_id in self.trace["trace"][module]:
                hit_count = self.trace["trace"][module][bb_id]
                hottest = max(hottest, hit_count)
        return hottest

    # a.k.a. "mem"
    def HeapAllocatedBytes(self) -> int:
        LOGGER.info("Heap allocated bytes: %d", self.trace["allocated_bytes"])
        assert isinstance(self.trace["allocated_bytes"], int)
        return self.trace["allocated_bytes"]

    def CodeCoverage(self) -> int:
        return len(self.CoveredBasicBlocks())

    def FunctionCoverage(self) -> int:
        return len(self.CoveredFunctions())

    def CodeCoverageInFunction(self, module_name: str, function_name: str) -> int:
        assert self.sa
        module_name = self.sa.resolve(module_name)
        return len(self.CoveredBasicBlocksInFunction(module_name, function_name))

    def DistanceToFunction(self, module_name: str, function_name: str) -> float:
        assert self.sa
        module_name = self.sa.resolve(module_name)
        first_bb = self.sa.module_f_to_first_bb[(module_name, function_name)]
        return self.DistanceToBB(module_name, first_bb)

    def DistanceToBB(self, module_name: str, bb_id: str) -> float:
        assert self.sa
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
        return float(dist)


class DynamicAnalysis:
    def __init__(
        self,
        sa: Optional[StaticAnalysis],
        root_dir: str,
        put: str,
        put_args: Optional[list[str]] = None,
    ):
        self.sa = sa
        self.root_dir = root_dir
        self.put = put
        self.put_args = put_args if put_args is not None else []
        self.cache = LRUCache(maxsize=1000)  # type: ignore[no-untyped-call] # LRUCache is not typed

    # TODO: Implement this similarly to the Fandango "run with cmd" feature.
    def trace_input(self, inp: str) -> Trace:
        if inp in self.cache:
            return cast(Trace, self.cache[inp])
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
