use glob::glob;
use std::env;
use std::path::{Path, PathBuf};
use std::process::Command;

/// Minimum Python version for the stable ABI (matches `abi3-py311` in Cargo.toml).
const PY_LIMITED_API: &str = "0x030B0000";

fn python_executable() -> String {
    pyo3_build_config::get()
        .executable()
        .map(str::to_owned)
        .or_else(|| env::var("PYO3_PYTHON").ok())
        .or_else(|| env::var("PYTHON_SYS_EXECUTABLE").ok())
        .unwrap_or_else(|| "python3".to_string())
}

/// The CPP parser links to `<Python.h>`, so we need to find the Python include directory.
fn python_include_dir() -> String {
    let output = Command::new(python_executable())
        .arg("-c")
        .arg("import sysconfig; print(sysconfig.get_paths()['include'])")
        .output()
        .expect("failed to run Python for include dir");

    assert!(
        output.status.success(),
        "failed to get Python include dir from interpreter"
    );

    String::from_utf8(output.stdout)
        .expect("python include output is not UTF-8")
        .trim()
        .to_owned()
}

/// Collect all C++ sources in the CPP parser directory.
fn cpp_sources(cpp_dir: &Path) -> Vec<PathBuf> {
    let pattern = format!("{}/**/*.cpp", cpp_dir.display());
    let mut files: Vec<_> = glob(&pattern)
        .expect("invalid glob pattern for C++ sources")
        .map(|entry| entry.expect("failed to read C++ source glob entry"))
        .collect();
    files.sort();
    files
}

fn main() {
    let python = pyo3_build_config::get();

    let repo_root = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .expect("rust crate has no parent directory")
        .to_path_buf();
    let cpp_parser_dir = repo_root.join("src/fandango/language/cpp_parser");

    let mut build = cc::Build::new();
    build.cpp(true);
    build.std("c++17");
    // Match abi3-py311: MSVC then links python3.lib instead of pythonXY.lib.
    build.define("Py_LIMITED_API", Some(PY_LIMITED_API));
    // ANTLR paths must come before the Python include directory: on Python
    // 3.11 (and on case-insensitive filesystems), Include/token.h shadows
    // antlr4-cpp-runtime/Token.h and its macros (STRING, INDENT, ...) break
    // the generated parser headers. Python 3.12+ removed token.h.
    build.include(&cpp_parser_dir);
    build.include(cpp_parser_dir.join("antlr4-cpp-runtime"));
    build.include(python_include_dir());

    // MSVC-only settings for the vendored ANTLR4 C++ runtime (see antlr4-common.h).
    if cfg!(target_os = "windows") {
        // We compile ANTLR sources directly into this extension, not a separate DLL.
        // Without this, ANTLR4CPP_PUBLIC becomes __declspec(dllimport), which is wrong
        // for static linkage and can cause Windows link failures.
        build.define("ANTLR4CPP_STATIC", None);
        // MSVC reports __cplusplus as 199711L unless this flag is set. Harmless at
        // C++17 (generated parser still takes the C++17 code paths), but required if
        // we ever bump to C++20 so #if __cplusplus checks see the real standard.
        build.flag("/Zc:__cplusplus");
    }

    for source in cpp_sources(&cpp_parser_dir) {
        println!("cargo:rerun-if-changed={}", source.display());
        build.file(source);
    }

    build.compile("fandango_cpp_parser");

    // C++ calls the Python C API. PyO3 handles Rust-side linking; for C++ on macOS
    // use dynamic_lookup, and on Windows add the import lib search path for the
    // python3.lib pragma injected by pyconfig.h (with Py_LIMITED_API).
    pyo3_build_config::add_extension_module_link_args();
    if cfg!(target_os = "windows") {
        if let Some(lib_dir) = python.lib_dir() {
            println!("cargo:rustc-link-search=native={lib_dir}");
        }
    }
}
