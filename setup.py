import os
import platform
import shutil
from pathlib import Path

import setuptools
from scikit_build_core.setuptools.build_cmake import BuildCMake

CXX_PARSER_NAME = "sa_fandango_cpp_parser"
LIB_EXT = "pyd" if platform.system().lower() == "windows" else "so"


class BuildFailed(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message


def get_boolish_env_flag(name: str) -> bool:
    return bool(os.environ.get(name, ""))


class BuildCMakeWithCopy(BuildCMake):
    """Custom build_cmake that copies extensions to source tree after CMake build."""

    def run(self):
        should_compile_cxx_parser: bool = get_boolish_env_flag(
            "FANDANGO_REQUIRE_BINARY_BUILD"
        ) or not get_boolish_env_flag("FANDANGO_SKIP_CPP_PARSER")

        if should_compile_cxx_parser:
            # Run the parent build_cmake command first (this does the actual CMake build)
            super().run()
            # After CMake build completes, copy the extension to source tree
            self.copy_extension_to_source()
        else:
            print("Skipping C++ parser compilation")

    def copy_extension_to_source(self):
        """Copy built extensions to the source tree for editable/redirect mode."""
        project_dir = Path(__file__).parent.resolve()
        target_dir = project_dir / "src" / "fandango" / "language" / "parser"

        so_files = (
            list(Path(self.build_lib).rglob(f"{CXX_PARSER_NAME}*.{LIB_EXT}"))
            if self.build_lib
            else []
        )

        if not so_files:
            raise BuildFailed("Cannot find the C++ parser produced by CMake")

        target_dir.mkdir(parents=True, exist_ok=True)
        for src_file in so_files:
            target_file = target_dir / src_file.name
            print(f"Copying C++ parser to source tree: {src_file} -> {target_file}")
            try:
                shutil.copy2(src_file, target_file)
                print("C++ parser extension successfully installed")
                return
            except Exception as e:
                raise BuildFailed(f"Failed to copy extension: {e}")


setuptools.setup(cmake_source_dir=".", cmdclass={"build_cmake": BuildCMakeWithCopy})
