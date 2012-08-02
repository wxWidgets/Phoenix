//--------------------------------------------------------------------------
// Name:        wxpy_api.sip
// Purpose:     The implementation of the API functions that are exported 
//              from the core extension module.
//
// Author:      Robin Dunn
//
// Created:     19-Nov-2010
// Copyright:   (c) 2011 by Total Control Software
// Licence:     wxWindows license
//--------------------------------------------------------------------------


%ModuleHeaderCode
#include "wxpy_api.h"
%End

//--------------------------------------------------------------------------


%ModuleCode
// wxPython's API helper and utility functions


// See also the wxString MappedType.  This code is similar, but doesn't 
// allocate a new wxString instance on the heap, is able to convert 
// non-string/unicode objects to unicode, and won't raise exceptions
static wxString i_Py2wxString(PyObject* source)
{
#if wxUSE_UNICODE_WCHAR == 0
#error wxString converison can only handle WCHAR wxStrings currently
#endif
    PyObject* uni = source;
    if (PyBytes_Check(source)) {
        // if it's a string object convert it to unicode first, assumes utf-8
        uni = PyUnicode_FromEncodedObject(source, "utf-8", "strict");
        if (PyErr_Occurred()) {
            PyErr_Clear();
            return wxEmptyString;
        }
    }            
    else if (!PyUnicode_Check(source)) {
#if PY_MAJOR_VERSION >= 3
        uni = PyObject_Str(source);
#else
        uni = PyObject_Unicode(source); 
#endif
        if (PyErr_Occurred()) {
            PyErr_Clear();
            return wxEmptyString;
        }
    }
    wxString target;
    size_t len = PyUnicode_GET_SIZE(uni);
    if (len) {
        wxPyUnicode_AsWideChar(uni, wxStringBuffer(target, len), len);
    }
    if (!PyUnicode_Check(source))
        Py_DECREF(uni);  // release the temporary Unicode object we created
    return target;
}

    
// TODO:  This might be a good way to share the string conversion code here and in string.sip...    
// A function to convert a Python string or unicode object to a wxString
// NOTE that it is inline so it should go in the header section
//inline wxString Py2wxString(PyObject* obj, bool setException=false, int& isErr=0) {
//    wxString str;
//    PyObject* uni = obj;
//    if (PyBytes_Check(obj)) {
//        // if it's a string object convert it to unicode first, assuming utf-8
//        uni = PyUnicode_FromEncodedObject(sipPy, "utf-8", "strict");
//        if (PyErr_Occurred()) {
//            if (setException) {
//                isErr = 1;
//            }
//            else {
//                PyErr_Clear();
//            }
//            return wxEmptyString;
//        }
//    }
//    // TODO: Coerce non-unicode types to unicode here?  (Classic does)
//    size_t len = PyUnicode_GET_SIZE(uni);
//    if (len) {
//        wxPyUnicode_AsWideChar(uni, wxStringBuffer(str, len), len);
//    }
//    if (obj != uni)
//        Py_DECREF(uni) // release the temporary Unicode object we may have created
//    return str;
//}
    

// Create a PyObject of the requested type from a void* and a class name.
static PyObject* i_wxPyConstructObject(void* ptr,
                                       const wxString& className,
                                       bool setThisOwn)
{
    const sipTypeDef* td = sipFindType(className);
    if (!td)
        return NULL;
    PyObject* transferObj = setThisOwn ? Py_None : NULL;
    return sipConvertFromType(ptr, td, transferObj);     
}




// Calls from wxWindows back to Python code, or even any PyObject
// manipulations, PyDECREF's and etc. should be wrapped in calls to these functions:
static wxPyBlock_t i_wxPyBeginBlockThreads() 
{
    if (! Py_IsInitialized()) {
        return (wxPyBlock_t)0;
    }
    PyGILState_STATE state = PyGILState_Ensure();
    return state;
}

static void i_wxPyEndBlockThreads(wxPyBlock_t blocked) 
{
    if (! Py_IsInitialized()) {
        return;
    }            
    PyGILState_Release(blocked);
}


// An instance of the API structure
static wxPyAPI  API = {
    i_Py2wxString,
    i_wxPyConstructObject,
    i_wxPyBeginBlockThreads,
    i_wxPyEndBlockThreads
};
%End


%PostInitialisationCode
    // Code that will run when _core is imported that will stash away a
    // pointer to the API structure.
    PyObject* wxmod = PyImport_ImportModule("wx");
    PyObject* wxmodDict = PyModule_GetDict(wxmod);
    PyObject* apiObj = PyCapsule_New(&API, "wx._wxPyAPI", NULL);
    PyDict_SetItemString(wxmodDict, "_wxPyAPI", apiObj);
    Py_XDECREF(apiObj);
    Py_DECREF(wxmod);
    wxPyGetAPIPtr();
%End

//--------------------------------------------------------------------------
