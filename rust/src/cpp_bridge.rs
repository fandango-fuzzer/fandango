use std::sync::Mutex;

use pyo3::prelude::*;

unsafe extern "C" {
    fn PyInit_sa_fandango_cpp_parser() -> *mut pyo3::ffi::PyObject;
}

static CPP_MODULE: Mutex<Option<Py<PyAny>>> = Mutex::new(None);

fn cpp_module(py: Python<'_>) -> PyResult<Py<PyAny>> {
    let mut guard = CPP_MODULE.lock().expect("C++ parser module lock poisoned");
    if let Some(module) = guard.as_ref() {
        return Ok(module.clone_ref(py));
    }
    let ptr = unsafe { PyInit_sa_fandango_cpp_parser() };
    if ptr.is_null() {
        return Err(PyErr::take(py).unwrap_or_else(|| {
            PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
                "failed to initialize C++ parser module",
            )
        }));
    }
    let module = unsafe { Bound::from_owned_ptr(py, ptr).unbind() };
    *guard = Some(module.clone_ref(py));
    Ok(module)
}

pub fn call_cpp_do_parse<'py>(
    py: Python<'py>,
    parser_cls: &Bound<'py, PyAny>,
    stream: &Bound<'py, PyAny>,
    entry_rule_name: &str,
    sa_err_listener: Option<Bound<'py, PyAny>>,
) -> PyResult<Bound<'py, PyAny>> {
    cpp_module(py)?
        .bind(py)
        .getattr("do_parse")?
        .call1((parser_cls, stream, entry_rule_name, sa_err_listener))
}
