//--------------------------------------------------------------------------
// Name:        wxpy_api.h
// Purpose:     Some utility functions and such that can be used in other 
//              snippets of C++ code to help reduce complexity, etc.  They 
//              are all either macros, inline functions, or functions that
//              are exported from the core extension module.
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
#endif

#if defined(__GNUC__)
    // Turn off the warning about converting string literals to char*
    // TODO: fix these the right way...
    #pragma GCC diagnostic ignored "-Wwrite-strings"
#endif

#ifdef _MSC_VER
    #pragma warning(disable:4800)
    #pragma warning(disable:4190)
#endif

#include <wx/wx.h>

//--------------------------------------------------------------------------
// The API items that can be inline functions or macros.  
// These are made available simply by #including this header file.
//--------------------------------------------------------------------------

typedef PyGILState_STATE wxPyBlock_t;


// Convert a wxString to a Python string (actually a PyUnicode object).
// Assumes that the GIL has already been acquired.
inline PyObject* wx2PyString(const wxString& str) {
    return PyUnicode_FromWideChar(str.wc_str(), str.length());
}


// Calls from Python to wxWidgets code should be wrapped in calls to these
// functions:
inline PyThreadState* wxPyBeginAllowThreads() {
    PyThreadState* saved = PyEval_SaveThread();  // Like Py_BEGIN_ALLOW_THREADS;
    return saved;
}

inline void wxPyEndAllowThreads(PyThreadState* saved) {
    PyEval_RestoreThread(saved);   // Like Py_END_ALLOW_THREADS;
}




// A macro that will help to execute simple statments wrapped in
// StartBlock/EndBlockThreads calls
#define wxPyBLOCK_THREADS(stmt) \
    { wxPyBlock_t blocked = wxPyBeginBlockThreads(); stmt; wxPyEndBlockThreads(blocked); }

// Raise any exception with a string value  (blocking threads)
#define wxPyErr_SetString(err, str) \
    wxPyBLOCK_THREADS(PyErr_SetString(err, str))

   
// Raise NotImplemented exceptions
#define wxPyRaiseNotImplemented() \
    wxPyBLOCK_THREADS( PyErr_SetNone(PyExc_NotImplementedError) )


#define wxPyRaiseNotImplementedMsg(msg) \
    wxPyBLOCK_THREADS( PyErr_SetString(PyExc_NotImplementedError, msg) );


// A convenience macro for properly returning Py_None
//#define RETURN_NONE()    { Py_INCREF(Py_None); return Py_None; }
#define RETURN_NONE()    { wxPyBLOCK_THREADS(Py_INCREF(Py_None)); return Py_None; }

//--------------------------------------------------------------------------
// The API items whose implementation can not or should not be inline 
// functions or macros.  The implementations will instead be accessed via 
// a structure of function pointers that is exported from the wx._core 
// extension module.  See wxpy_api.sip for the implementations.
//--------------------------------------------------------------------------


struct wxPyAPI {
    wxString      (*p_Py2wxString)(PyObject* source);
    PyObject*     (*p_wxPyConstructObject)(void* ptr, const wxString& className, bool setThisOwn);
    wxPyBlock_t   (*p_wxPyBeginBlockThreads)();
    void          (*p_wxPyEndBlockThreads)(wxPyBlock_t blocked);
    // Always add new items here at the end.
};

inline wxPyAPI* wxPyGetAPIPtr()
{
    static wxPyAPI* wxPyAPIPtr = NULL;
    
    if (wxPyAPIPtr == NULL) {
        wxPyAPIPtr = (wxPyAPI*)PyCObject_Import("wx._core", "_wxPyAPI");
    }
    // wxASSERT_MSG(wxPyAPIPtr != NULL, wxT("wxPyAPIPtr is NULL!!!"));  // uncomment when needed for debugging
    return wxPyAPIPtr;
}

//--------------------------------------------------------------------------
// Inline wrappers to call the API functions

// Convert a PyObject to a wxString
// Assumes that the GIL has already been acquired.
inline wxString Py2wxString(PyObject* source) 
    { return wxPyGetAPIPtr()->p_Py2wxString(source); }


// Create a PyObject of the requested type from a void* and a class name.
// Assumes that the GIL has already been acquired.
inline PyObject* wxPyConstructObject(void* ptr, const wxString& className, bool setThisOwn=false) 
    { return wxPyGetAPIPtr()->p_wxPyConstructObject(ptr, className, setThisOwn); }

    
// Calls from wxWindows back to Python code, or even any PyObject
// manipulations, PyDECREF's and etc. should be wrapped in calls to these functions:
inline wxPyBlock_t wxPyBeginBlockThreads() 
    { return wxPyGetAPIPtr()->p_wxPyBeginBlockThreads(); }
inline void wxPyEndBlockThreads(wxPyBlock_t blocked) 
    { wxPyGetAPIPtr()->p_wxPyEndBlockThreads(blocked); }
    
#endif
