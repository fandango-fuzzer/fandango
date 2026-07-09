use glob::glob;
use std::env;
use std::path::{Path, PathBuf};
use std::process::Command;

/// Minimum Python version for the stable ABI (matches `abi3-py311` in Cargo.toml).
const PY_LIMITED_API: &str = "0x030B0000";

fn python_executable() -> String {
    env::var("PYO3_PYTHON")
        .or_else(|_| env::var("PYTHON_SYS_EXECUTABLE"))
        .unwrap_or_else(|_| "python3".to_string())
}

fn run_python(code: &str) -> String {
    let output = Command::new(python_executable())
        .arg("-c")
        .arg(code)
        .output()
        .expect("failed to run Python");

    assert!(output.status.success(), "failed to run Python: {code}");

    String::from_utf8(output.stdout)
        .expect("python output is not UTF-8")
        .trim()
        .to_owned()
}

/// The CPP parser links to `<Python.h>`, so we need to find the Python include directory.
fn python_include_dir() -> String {
    run_python("import sysconfig; print(sysconfig.get_paths()['include'])")
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

    // C++ calls the Python C API; symbols resolve when the extension is loaded.
    if cfg!(target_os = "macos") {
        println!("cargo:rustc-cdylib-link-arg=-Wl,-undefined,dynamic_lookup");
    }
    #[cfg(target_os = "windows")]
    link_windows_cpp_python();
}

/// MSVC needs python3.lib for the pragma from pyconfig.h (with Py_LIMITED_API).
/// Maturin's PYO3_CONFIG_FILE omits lib_dir, and uv's Python may not ship import
/// libs, so generate a stable-ABI import library into OUT_DIR.
#[cfg(target_os = "windows")]
fn link_windows_cpp_python() {
    let out_dir = PathBuf::from(env::var("OUT_DIR").unwrap()).join("python3-lib");
    std::fs::create_dir_all(&out_dir).expect("failed to create python3-lib directory");
    let arch = env::var("CARGO_CFG_TARGET_ARCH").expect("CARGO_CFG_TARGET_ARCH not set");
    let env_name = env::var("CARGO_CFG_TARGET_ENV").expect("CARGO_CFG_TARGET_ENV not set");
    python3_dll_a::generate_implib_for_target(&out_dir, &arch, &env_name)
        .expect("failed to generate python3.lib");
    println!("cargo:rustc-link-search=native={}", out_dir.display());
}
