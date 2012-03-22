//--------------------------------------------------------------------------
// Name:        wxpy_api.h
// Purpose:     Some utility functions and such that can be used in other 
//              snippets of C++ code to help reduce complexity, etc.
//
// Author:      Robin Dunn
//
// Created:     19-Nov-2010
// Copyright:   (c) 2011 by Total Control Software
// Licence:     wxWindows license
//--------------------------------------------------------------------------

#ifndef _WXPY_API_H
#define _WXPY_API_H

#if defined(__APPLE__)
    // When it's possible that we're building universal binaries with both
    // 32-bit and 64-bit architectures then these need to be undefed because
    // otherwise the values set by configure could conflict with those set
    // based on runtime flags in Python's headers.  We also do something
    // similar in wx/platform.h so it's okay to undef them now because they
    // will be defined again soon.
    #undef SIZEOF_VOID_P
    #undef SIZEOF_LONG
    #undef SIZEOF_SIZE_T

    // Turn off the warning about converting string literals to char*
    // TODO: fix these the right way...
    #pragma GCC diagnostic ignored "-Wwrite-strings"
#endif
#ifdef _MSC_VER
    #pragma warning(disable:4800)
    #pragma warning(disable:4190)
#endif

#include <wx/wx.h>


// Convert a wxString to a Python string (actually a PyUnicode object).
// Assumes that the GIL has already been acquired.
inline PyObject* wx2PyString(const wxString& str) {
    return PyUnicode_FromWideChar(str.wc_str(), str.length());
}

// Convert a PyObject to a wxString
// Assumes that the GIL has already been acquired.
wxString Py2wxString(PyObject* source);
   

typedef PyGILState_STATE wxPyBlock_t;

// Calls from Python to wxWindows code are wrapped in calls to these
// functions:
inline PyThreadState* wxPyBeginAllowThreads() {
    PyThreadState* saved = PyEval_SaveThread();  // Like Py_BEGIN_ALLOW_THREADS;
    return saved;
}

inline void wxPyEndAllowThreads(PyThreadState* saved) {
    PyEval_RestoreThread(saved);   // Like Py_END_ALLOW_THREADS;
}


// Calls from wxWindows back to Python code, or even any PyObject
// manipulations, PyDECREF's and etc. are wrapped in calls to these functions:
inline wxPyBlock_t wxPyBeginBlockThreads() {
    if (! Py_IsInitialized()) {
        return (wxPyBlock_t)0;
    }
    PyGILState_STATE state = PyGILState_Ensure();
    return state;
}

inline void wxPyEndBlockThreads(wxPyBlock_t blocked) {
    if (! Py_IsInitialized()) {
        return;
    }            
    PyGILState_Release(blocked);
}


// A macro that will help to execute simple statments wrapped in
// StartBlock/EndBlockThreads calls
#define wxPyBLOCK_THREADS(stmt) \
    { wxPyBlock_t blocked = wxPyBeginBlockThreads(); stmt; wxPyEndBlockThreads(blocked); }

// Raise any exception with a string value  (blocking threads)
#define wxPyErr_SetString(err, str) \
    wxPyBLOCK_THREADS(PyErr_SetString(err, str))

   
// Raise NotImplemented exceptions
inline void wxPyRaiseNotImplemented() {
    wxPyBLOCK_THREADS( PyErr_SetNone(PyExc_NotImplementedError) );
}

inline void wxPyRaiseNotImplementedMsg(const char* msg) {
    wxPyBLOCK_THREADS( PyErr_SetString(PyExc_NotImplementedError, msg) );
}


// Create a PyObject of the requested type from a void* and a class name.
// Assumes that the GIL has already been acquired.
PyObject* wxPyConstructObject(void* ptr,
                              const wxString& className,
                              int setThisOwn=0);


    
#endif