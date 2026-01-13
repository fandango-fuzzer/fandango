import os
from typing import Optional

from fandango.execution.static_analysis import StaticAnalysis
from fandango.execution.dynamic_analysis import DynamicAnalysis


class FCC:
    def __init__(self, put: Optional[str], put_args: Optional[list[str]]):
        assert put
        self.put = put
        root_directory: str = os.path.dirname(self.put)
        cfg_directory: str = os.path.join(root_directory, ".cfg/")
        bb_to_dbg_json: str = os.path.join(root_directory, ".bb_to_dbg.json")

        self.static_analysis = StaticAnalysis(cfg_directory, bb_to_dbg_json)
        self.dynamic_analysis = DynamicAnalysis(
            self.static_analysis, root_directory, put, put_args
        )
