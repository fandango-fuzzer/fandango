# from https://github.com/amykyta3/speedy-antlr-example/blob/master/setup.py

import sys
import os
import platform
import fnmatch
import setuptools

target = platform.system().lower()
PLATFORMS = {"windows", "linux", "darwin", "cygwin"}
for known in PLATFORMS:
    if target.startswith(known):
        target = known


def run_setup(with_binary):
    if with_binary:
        extra_compile_args = {
            "windows": [
                "/DANTLR4CPP_STATIC",
                "/Zc:__cplusplus",
                "/std:c++17",
                "/EHsc",
                "/D_CRT_SECURE_NO_WARNINGS",
                "/D_WIN32_WINNT=0x0601",  # Windows 7 or later
                "/D_USE_32BIT_TIME_T=0",  # Use 64-bit time_t
                "/D_HAS_STD_BYTE=0",  # Disable std::byte
                "/D_SILENCE_CXX17_CODECVT_HEADER_DEPRECATION_WARNING",  # Silence codecvt deprecation
                "/D_SILENCE_CXX17_ITERATOR_BASE_CLASS_DEPRECATION_WARNING",  # Silence iterator deprecation
            ],
            "linux": ["-std=c++17"],
            "darwin": ["-std=c++17"],
            "cygwin": ["-std=c++17"],
        }

        # Define an Extension object that describes the Antlr accelerator
        cpp_parser_dir = "src/fandango/language/cpp_parser"
        parser_ext = setuptools.Extension(
            # Extension name shall be at the same level as the sa_fandango_parser.py module
            name="fandango.language.parser.sa_fandango_cpp_parser",
            # Add the Antlr runtime source directory to the include search path
            include_dirs=[cpp_parser_dir + "/antlr4-cpp-runtime"],
            # Rather than listing each C++ file (Antlr has a lot!), discover them automatically
            sources=get_files(cpp_parser_dir, "*.cpp"),
            depends=get_files(cpp_parser_dir, "*.h"),
            extra_compile_args=extra_compile_args.get(target, []),
        )
        ext_modules = [parser_ext]
    else:
        ext_modules = []

    # Define a package
    setuptools.setup(
        # TODO: This should come from pyproject.toml
        name="fandango-fuzzer",
        version="0.9.0",
        description="Fandango produces myriads of high-quality random inputs to test programs, giving users unprecedented control over format and shape of the inputs.",
        packages=setuptools.find_packages("src"),
        package_dir={"": "src"},
        include_package_data=True,
        # python_requires='>=3.6.0',
        # install_requires=[
        #     "antlr4-python3-runtime >= 4.11, < 4.12",
        # ],
        ext_modules=ext_modules,
        cmdclass={"build_ext": ve_build_ext},
    )


# ===============================================================================
from setuptools.command.build_ext import build_ext
from distutils.errors import CCompilerError, DistutilsExecError, DistutilsPlatformError


def get_files(path, pattern):
    """
    Recursive file search that is compatible with python3.4 and older
    """
    matches = []
    for root, _, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, pattern):
            matches.append(os.path.join(root, filename))
    return matches


class BuildFailed(Exception):
    pass


class ve_build_ext(build_ext):
    """
    This class extends setuptools to fail with a common BuildFailed exception
    if a build fails
    """

    def run(self):
        try:
            build_ext.run(self)
        except DistutilsPlatformError:
            raise BuildFailed()

    def build_extension(self, ext):
        try:
            build_ext.build_extension(self, ext)
        except (CCompilerError, DistutilsExecError, DistutilsPlatformError) as e:
            print(f"Build failed with error: {str(e)}")
            if hasattr(e, "output"):
                print(f"Compiler output: {e.output}")
            # Print environment information for debugging
            raise BuildFailed()
        except ValueError as e:
            # this can happen on Windows 64 bit, see Python issue 7511
            if "'path'" in str(e):
                print(f"Build failed with path error: {str(e)}")
                raise BuildFailed()
            raise


# Detect if an alternate interpreter is being used
is_jython = "java" in sys.platform
is_pypy = hasattr(sys, "pypy_version_info")
skip_cpp = os.environ.get("FANDANGO_SKIP_CPP_PARSER", "").lower() in (
    "1",
    "true",
    "yes",
)


# Force using fallback if using an alternate interpreter
using_fallback = is_jython or is_pypy or skip_cpp

if not using_fallback:
    try:
        run_setup(with_binary=True)
    except BuildFailed as e:
        if "FANDANGO_REQUIRE_CI_BINARY_BUILD" in os.environ:
            # Require build to pass if running in travis-ci
            import traceback

            traceback.print_exc()
            raise e
        else:
            using_fallback = True

if using_fallback:
    run_setup(with_binary=False)
