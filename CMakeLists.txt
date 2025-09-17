cmake_minimum_required(VERSION 3.18)

project(fandango-fuzzer VERSION 1.0.6 LANGUAGES CXX)

# Handle the case where C++ build is disabled
# Check environment variable first, then CMake option
if(DEFINED ENV{FANDANGO_SKIP_CPP_PARSER} AND "$ENV{FANDANGO_SKIP_CPP_PARSER}" STREQUAL "1")
    set(FANDANGO_SKIP_CPP_PARSER ON)
endif()

# Check if binary build is required
if(DEFINED ENV{FANDANGO_REQUIRE_BINARY_BUILD} AND "$ENV{FANDANGO_REQUIRE_BINARY_BUILD}" STREQUAL "1")
    set(FANDANGO_REQUIRE_BINARY_BUILD ON)
    message(STATUS "Binary build is required - C++ parser must be built successfully")
else()
    set(FANDANGO_REQUIRE_BINARY_BUILD OFF)
endif()

option(FANDANGO_SKIP_CPP_PARSER "Skip building the C++ parser" OFF)
if(FANDANGO_SKIP_CPP_PARSER)
    if(FANDANGO_REQUIRE_BINARY_BUILD)
        message(FATAL_ERROR "FANDANGO_REQUIRE_BINARY_BUILD is set but C++ parser build is disabled")
    endif()
    message(STATUS "Skipping C++ parser build as requested")
    # Create a dummy target to satisfy scikit-build
    add_custom_target(sa_fandango_cpp_parser ALL
        COMMENT "Skipping C++ parser build"
    )
    return()
endif()

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find Python (use Module development to avoid requiring libpython on manylinux)
find_package(Python3 COMPONENTS Interpreter Development.Module REQUIRED)

# Set the C++ parser directory
set(CPP_PARSER_DIR "src/fandango/language/cpp_parser")

# Get all C++ source files
file(GLOB_RECURSE CPP_SOURCES "${CPP_PARSER_DIR}/*.cpp")

# Create the Python extension module
Python3_add_library(sa_fandango_cpp_parser MODULE ${CPP_SOURCES})

# Link against the Python module target (provides include dirs and compile defs)
target_link_libraries(sa_fandango_cpp_parser PRIVATE Python3::Module)

# If binary build is required, ensure the target is properly configured
if(FANDANGO_REQUIRE_BINARY_BUILD)
    # Add a custom property to track if this is a required build
    set_target_properties(sa_fandango_cpp_parser PROPERTIES
        FANDANGO_REQUIRED_BUILD TRUE
    )
    message(STATUS "C++ parser build is required - any build failure will cause the entire build to fail")
endif()

# Set include directories
target_include_directories(sa_fandango_cpp_parser PRIVATE
    ${CPP_PARSER_DIR}
    ${CPP_PARSER_DIR}/antlr4-cpp-runtime
    ${Python3_INCLUDE_DIRS}
)

# Set compile definitions
target_compile_definitions(sa_fandango_cpp_parser PRIVATE
    VERSION_INFO=${PROJECT_VERSION}
)

# Platform-specific compile flags
if(WIN32)
    target_compile_definitions(sa_fandango_cpp_parser PRIVATE ANTLR4CPP_STATIC)
    target_compile_options(sa_fandango_cpp_parser PRIVATE /Zc:__cplusplus /std:c++17)
elseif(APPLE)
    target_compile_options(sa_fandango_cpp_parser PRIVATE -std=c++17 -mmacosx-version-min=10.13)
else()
    target_compile_options(sa_fandango_cpp_parser PRIVATE -std=c++17)
endif()

# Install the module using scikit-build's approach
install(TARGETS sa_fandango_cpp_parser
    DESTINATION fandango/language/parser
)

# Set build type if not specified
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()

