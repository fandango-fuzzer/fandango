use std::env;
use std::path::PathBuf;

fn main() {
    let project_root = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .expect("rust crate has no parent directory")
        .to_path_buf();

    println!(
        "cargo:rerun-if-changed={}",
        project_root.join("CMakeLists.txt").display()
    );
    println!(
        "cargo:rerun-if-changed={}",
        project_root
            .join("src/fandango/language/cpp_parser")
            .display()
    );

    let python = env::var("PYO3_PYTHON")
        .or_else(|_| env::var("PYTHON_SYS_EXECUTABLE"))
        .unwrap_or_else(|_| "python3".into());

    let dst = cmake::Config::new(&project_root)
        .define("SKBUILD_PROJECT_NAME", "fandango")
        .define("SKBUILD_PROJECT_VERSION", env!("CARGO_PKG_VERSION"))
        .define("Python3_EXECUTABLE", &python)
        // STATIC archive must be PIC to link into the cdylib (Linux).
        .define("CMAKE_POSITION_INDEPENDENT_CODE", "ON")
        // Build the archive directly (cmake-rs defaults to an install target).
        .build_target("sa_fandango_cpp_parser")
        .build();

    // cmake-rs builds into $OUT_DIR/build; no install() rules in CMakeLists.txt.
    println!("cargo:rustc-link-search=native={}/build", dst.display());
    println!(
        "cargo:rustc-link-search=native={}/build/Release",
        dst.display()
    );
    println!(
        "cargo:rustc-link-search=native={}/build/Debug",
        dst.display()
    );
    println!("cargo:rustc-link-lib=static=sa_fandango_cpp_parser");

    let target_os = env::var("CARGO_CFG_TARGET_OS").expect("CARGO_CFG_TARGET_OS not set");
    match target_os.as_str() {
        "macos" => {
            println!("cargo:rustc-link-lib=c++");
            // Extension loads into the running interpreter; resolve Python symbols at runtime.
            println!("cargo:rustc-cdylib-link-arg=-Wl,-undefined,dynamic_lookup");
        }
        "linux" => println!("cargo:rustc-link-lib=stdc++"),
        _ => {}
    }

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
