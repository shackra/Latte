#![crate_type = "dylib"]
#[macro_use]
extern crate cpython;
extern crate x11;

use cpython::{PyResult, Python};
use x11::xss::{XScreenSaverAllocInfo, XScreenSaverQueryInfo};
use x11::xlib::{XDefaultRootWindow, XOpenDisplay};
use std::env;
use std::os::unix::ffi::OsStrExt;

fn get_inactivity_time(_py: Python) -> PyResult<f64> {
    let display = env::var_os("DISPLAY");
    let mut time = 0.0;
    if display.is_some() {
        unsafe {
            let wdisplay = display.unwrap().as_bytes().as_ptr() as *const i8;
            let dpy = XOpenDisplay(wdisplay);
            let root = XDefaultRootWindow(dpy);
            let xss_info = XScreenSaverAllocInfo();
            XScreenSaverQueryInfo(dpy, root, xss_info);
            time = (*xss_info).idle as f64 / 1000.0;
        }
    }
    Ok(time)
}

py_module_initializer!(lattex11, initlattex11, PyInit_lattex11, |py, m| {
    try!(m.add(py, "__doc__", "If available, return the idle time from X11"));
    try!(m.add(py, "get_inactivity_time", py_fn!(py, get_inactivity_time())));
    Ok(())
});
