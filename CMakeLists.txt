cmake_minimum_required(VERSION 3.18)

project(fandango
    VERSION ${FANDANGO_VERSION}
    LANGUAGES CXX
)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_INTERPROCEDURAL_OPTIMIZATION TRUE)

# Python3_INCLUDE_DIR is set by rust/build.rs via sysconfig (avoids FindPython
# Development.Module, which fails in cibuildwheel macOS venvs).
set(CPP_PARSER_DIR "src/fandango/language/cpp_parser")
file(GLOB_RECURSE CPP_SOURCES "${CPP_PARSER_DIR}/*.cpp")

add_library(sa_fandango_cpp_parser STATIC ${CPP_SOURCES})

target_include_directories(sa_fandango_cpp_parser PRIVATE
    ${Python3_INCLUDE_DIR}
    ${CPP_PARSER_DIR}
    ${CPP_PARSER_DIR}/antlr4-cpp-runtime
)

target_compile_definitions(sa_fandango_cpp_parser PRIVATE
    VERSION_INFO=${PROJECT_VERSION}
)

if(WIN32)
    target_compile_definitions(sa_fandango_cpp_parser PRIVATE ANTLR4CPP_STATIC)
    target_compile_options(sa_fandango_cpp_parser PRIVATE /Zc:__cplusplus)
elseif(APPLE)
    target_compile_options(sa_fandango_cpp_parser PRIVATE -mmacosx-version-min=10.13)
endif()
