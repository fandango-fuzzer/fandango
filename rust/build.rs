use glob::glob;
use std::env;
use std::path::{Path, PathBuf};
use std::process::Command;

/// Matches `abi3-py311` in Cargo.toml.
const PY_LIMITED_API: &str = "0x030B0000";

fn python_include_dir() -> String {
    let python = env::var("PYO3_PYTHON")
        .or_else(|_| env::var("PYTHON_SYS_EXECUTABLE"))
        .unwrap_or_else(|_| "python3".into());
    let output = Command::new(python)
        .args([
            "-c",
            "import sysconfig; print(sysconfig.get_paths()['include'])",
        ])
        .output()
        .expect("failed to run Python for include dir");
    assert!(output.status.success());
    String::from_utf8(output.stdout)
        .expect("python include output is not UTF-8")
        .trim()
        .to_owned()
}

fn cpp_sources(dir: &Path) -> Vec<PathBuf> {
    let mut files: Vec<_> = glob(&format!("{}/**/*.cpp", dir.display()))
        .expect("invalid glob pattern for C++ sources")
        .map(|entry| entry.expect("failed to read C++ source glob entry"))
        .collect();
    files.sort();
    files
}

fn main() {
    let cpp_parser_dir = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .expect("rust crate has no parent directory")
        .join("src/fandango/language/cpp_parser");

    let mut build = cc::Build::new();
    build.cpp(true).std("c++17");
    build.define("Py_LIMITED_API", Some(PY_LIMITED_API));
    // ANTLR before Python includes: on 3.11 / case-insensitive FS, token.h shadows Token.h.
    build.include(&cpp_parser_dir);
    build.include(cpp_parser_dir.join("antlr4-cpp-runtime"));
    build.include(python_include_dir());

    if cfg!(windows) {
        build.define("ANTLR4CPP_STATIC", None);
        build.flag("/Zc:__cplusplus");
    }

    for source in cpp_sources(&cpp_parser_dir) {
        println!("cargo:rerun-if-changed={}", source.display());
        build.file(source);
    }
    build.compile("fandango_cpp_parser");

    if cfg!(target_os = "macos") {
        println!("cargo:rustc-cdylib-link-arg=-Wl,-undefined,dynamic_lookup");
    }

    // C++ uses Python.h's python3.lib pragma; generate it (uv/maturin don't provide lib_dir).
    #[cfg(windows)]
    {
        let lib_dir = PathBuf::from(env::var("OUT_DIR").unwrap()).join("python3-lib");
        std::fs::create_dir_all(&lib_dir).expect("failed to create python3-lib directory");
        python3_dll_a::generate_implib_for_target(
            &lib_dir,
            &env::var("CARGO_CFG_TARGET_ARCH").expect("CARGO_CFG_TARGET_ARCH not set"),
            &env::var("CARGO_CFG_TARGET_ENV").expect("CARGO_CFG_TARGET_ENV not set"),
        )
        .expect("failed to generate python3.lib");
        println!("cargo:rustc-link-search=native={}", lib_dir.display());
    }
}
