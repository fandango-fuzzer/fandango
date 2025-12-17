import os
import platform
import shutil
from pathlib import Path

import setuptools
from scikit_build_core.setuptools.build_cmake import BuildCMake as _build_cmake

CXX_PARSER_NAME = "sa_fandango_cpp_parser"
LIB_EXT = "pyd" if platform.system().lower() == "windows" else "so"


class BuildFailed(Exception):
    pass


class BuildCMakeWithCopy(_build_cmake):
    """Custom build_cmake that copies extensions to source tree after CMake build."""

    def run(self):
        # Run the parent build_cmake command first (this does the actual CMake build)
        super().run()
        # After CMake build completes, copy the extension to source tree
        self.copy_extension_to_source()

    def copy_extension_to_source(self):
        """Copy built extensions to the source tree for editable/redirect mode."""
        project_dir = Path(__file__).parent.resolve()
        target_dir = project_dir / "src" / "fandango" / "language" / "parser"

        so_files = list(Path(self.build_lib).rglob(f"{CXX_PARSER_NAME}*.{LIB_EXT}"))

        if os.environ.get("FANDANGO_REQUIRE_BINARY_BUILD", "0") == "1" and not so_files:
            raise BuildFailed()

        target_dir.mkdir(parents=True, exist_ok=True)
        for src_file in so_files:
            target_file = target_dir / src_file.name

            print("Copying C++ parser to source tree:")
            print(f"  From: {src_file}")
            print(f"  To:   {target_file}")

            try:
                shutil.copy2(src_file, target_file)
                print("✓ C++ parser extension successfully installed!")
                return
            except Exception as e:
                print(f"⚠ Warning: Failed to copy extension: {e}")
                return


# Use our custom command
cmdclass = {"build_cmake": BuildCMakeWithCopy}


setuptools.setup(cmake_source_dir=".", cmdclass=cmdclass)
