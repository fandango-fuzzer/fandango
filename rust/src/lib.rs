mod cpp_bridge;

use pyo3::prelude::*;

use cpp_bridge::call_cpp_do_parse;

/// Example Rust function callable from Python via `fandango.native.greet`.
#[pyfunction]
fn greet(name: &str) -> String {
    format!("Hello from Rust, {name}!")
}

/// C++ speedy-antlr parser exposed as `fandango.native.cpp_parse`.
#[pyfunction]
#[pyo3(signature = (parser_cls: "type[fandango.language.parser.FandangoParser.FandangoParser]", stream: "antlr4.InputStream", entry_rule_name, sa_err_listener: "fandango.language.parser.sa_fandango.SA_ErrorListener | None" = None) -> "antlr4.tree.Tree.ParseTree")]
fn cpp_parse(
    parser_cls: Bound<'_, PyAny>,
    stream: Bound<'_, PyAny>,
    entry_rule_name: &str,
    sa_err_listener: Option<Bound<'_, PyAny>>,
) -> PyResult<Py<PyAny>> {
    let py = parser_cls.py();
    call_cpp_do_parse(py, &parser_cls, &stream, entry_rule_name, sa_err_listener)
        .map(|value| value.unbind())
}

#[pymodule]
mod native {
    #[pymodule_export]
    use super::{cpp_parse, greet};
}
