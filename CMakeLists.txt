cmake_minimum_required(VERSION 3.18)

project(${SKBUILD_PROJECT_NAME}
    VERSION ${SKBUILD_PROJECT_VERSION}
    LANGUAGES CXX
)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Enable Link Time Optimization
set(CMAKE_INTERPROCEDURAL_OPTIMIZATION TRUE)

# Find Python (use Module development to avoid requiring libpython on manylinux)
find_package(Python3 COMPONENTS Interpreter Development.Module REQUIRED)

# Set the C++ parser directory
set(CPP_PARSER_DIR "src/fandango/language/cpp_parser")

# Get all C++ source files
file(GLOB_RECURSE CPP_SOURCES "${CPP_PARSER_DIR}/*.cpp")

# Create the Python extension module
Python3_add_library(sa_fandango_cpp_parser MODULE ${CPP_SOURCES})

# Link and configure the module
target_link_libraries(sa_fandango_cpp_parser PRIVATE Python3::Module)

target_include_directories(sa_fandango_cpp_parser PRIVATE
    ${CPP_PARSER_DIR}
    ${CPP_PARSER_DIR}/antlr4-cpp-runtime
)

target_compile_definitions(sa_fandango_cpp_parser PRIVATE
    VERSION_INFO=${PROJECT_VERSION}
)

# Platform-specific settings
if(WIN32)
    target_compile_definitions(sa_fandango_cpp_parser PRIVATE ANTLR4CPP_STATIC)
    target_compile_options(sa_fandango_cpp_parser PRIVATE /Zc:__cplusplus)
elseif(APPLE)
    target_compile_options(sa_fandango_cpp_parser PRIVATE -mmacosx-version-min=10.13)
endif()

# Install the module
install(TARGETS sa_fandango_cpp_parser
    DESTINATION fandango/language/parser
)
