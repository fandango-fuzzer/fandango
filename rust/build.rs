use glob::glob;
use std::env;
use std::path::{Path, PathBuf};
use std::process::Command;

fn run_python(code: &str) -> String {
    let python = env::var("PYO3_PYTHON")
        .or_else(|_| env::var("PYTHON_SYS_EXECUTABLE"))
        .unwrap_or_else(|_| "python3".into());
    let output = Command::new(python)
        .args(["-c", code])
        .output()
        .expect("failed to run Python");
    assert!(output.status.success(), "failed to run Python: {code}");
    String::from_utf8(output.stdout)
        .expect("python output is not UTF-8")
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
    // C++ uses the CPython API (auto-generated speedy-antlr sources). Match PyO3's abi3.
    build.define("Py_LIMITED_API", Some("0x030B0000"));
    // ANTLR before Python headers: on case-insensitive FS, Python's token.h shadows Token.h.
    build.include(&cpp_parser_dir);
    build.include(cpp_parser_dir.join("antlr4-cpp-runtime"));
    build.include(run_python(
        "import sysconfig; print(sysconfig.get_paths()['include'])",
    ));

    // MSVC settings for the vendored ANTLR C++ runtime.
    #[cfg(windows)]
    {
        // Statically link ANTLR into fandango_cpp_parser.lib (no separate antlr4 DLL).
        build.define("ANTLR4CPP_STATIC", None);
        // Without this MSVC leaves __cplusplus at 199711L; ANTLR and our code use C++17.
        build.flag("/Zc:__cplusplus");
    }

    for source in cpp_sources(&cpp_parser_dir) {
        println!("cargo:rerun-if-changed={}", source.display());
        build.file(source);
    }
    build.compile("fandango_cpp_parser");

    // Extension loads into the running interpreter; resolve Python symbols at runtime.
    #[cfg(target_os = "macos")]
    println!("cargo:rustc-cdylib-link-arg=-Wl,-undefined,dynamic_lookup");

    // Import library for C++ code that #include <Python.h> (auto-generated speedy-antlr).
    #[cfg(windows)]
    {
        // pyconfig.h emits #pragma comment(lib, "python3.lib"); uv's Windows Python ships none.
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
