use glob::glob;
use std::env;
use std::path::{Path, PathBuf};
use std::process::Command;

fn run_python(code: &str) -> String {
    let python = env::var_os("PYO3_PYTHON")
        .or_else(|| env::var_os("PYTHON_SYS_EXECUTABLE"))
        .map(PathBuf::from)
        .unwrap_or_else(|| PathBuf::from("python3"));

    let output = Command::new(&python)
        .args(["-c", code])
        .output()
        .unwrap_or_else(|err| panic!("failed to run {}: {err}", python.display()));

    assert!(
        output.status.success(),
        "failed to run {} -c {code:?}: {}",
        python.display(),
        String::from_utf8_lossy(&output.stderr)
    );

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
    let config = pyo3_build_config::get();

    let cpp_parser_dir = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .expect("rust crate has no parent directory")
        .join("src/fandango/language/cpp_parser");

    let mut build = cc::Build::new();
    build.cpp(true).std("c++17");

    // Follow PyO3's resolved ABI (abi3 feature may be off, e.g. free-threaded).
    let target_abi = config.target_abi();
    if matches!(
        target_abi.kind(),
        pyo3_build_config::PythonAbiKind::Stable(pyo3_build_config::StableAbi::Abi3)
    ) {
        let version = target_abi.version();
        let limited_api = format!("0x{:02X}{:02X}0000", version.major, version.minor);
        build.define("Py_LIMITED_API", Some(limited_api.as_str()));
    }

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
    pyo3_build_config::add_extension_module_link_args();

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
