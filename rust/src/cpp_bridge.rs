use pyo3::prelude::*;

unsafe extern "C" {
    fn PyInit_sa_fandango_cpp_parser() -> *mut pyo3::ffi::PyObject;
}

pub fn call_cpp_do_parse<'py>(
    py: Python<'py>,
    parser_cls: &Bound<'py, PyAny>,
    stream: &Bound<'py, PyAny>,
    entry_rule_name: &str,
    sa_err_listener: Option<Bound<'py, PyAny>>,
) -> PyResult<Bound<'py, PyAny>> {
    unsafe {
        let cpp_module_ptr = PyInit_sa_fandango_cpp_parser();
        if cpp_module_ptr.is_null() {
            return Err(PyErr::take(py).unwrap_or_else(|| {
                PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
                    "failed to initialize C++ parser module",
                )
            }));
        }
        Bound::from_owned_ptr(py, cpp_module_ptr)
            .getattr("do_parse")?
            .call1((parser_cls, stream, entry_rule_name, sa_err_listener))
    }
}
