//--------------------------------------------------------------------------
// Name:        wxpy_api.sip
// Purpose:     Some utility functions and such that can be used in other 
//              snippets of C++ code to help reduce complexity, etc.
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
// Various wxPython helper/utility functions


// Create a PyObject of the requested type from a void* and a class name.
PyObject* wxPyConstructObject(void* ptr,
                              const wxString& className,
                              int setThisOwn)
{
    const sipTypeDef* td = sipFindType(className);
    if (!td)
        return NULL;
    PyObject* transferObj = setThisOwn ? Py_None : NULL;
    return sipConvertFromType(ptr, td, transferObj);     
}


// See also the wxString MappedType.  This code is similar, but doesn't 
// allocate a new wxString instance on the heap, is able to convert 
// non-string/unicode objects to unicode, and won't raise exceptions
wxString Py2wxString(PyObject* source)
{
    PyObject* uni = source;
    if (PyString_Check(source)) {
        // if it's a string object convert it to unicode first, assumes utf-8
        uni = PyUnicode_FromEncodedObject(source, "utf-8", "strict");
        if (PyErr_Occurred()) {
            PyErr_Clear();
            return wxEmptyString;
        }
    }            
    else if (!PyUnicode_Check(source)) {
        uni = PyObject_Unicode(source); 
        if (PyErr_Occurred()) {
            PyErr_Clear();
            return wxEmptyString;
        }
    }
    wxString target;
    size_t len = PyUnicode_GET_SIZE(uni);
    if (len) {
        PyUnicode_AsWideChar((PyUnicodeObject*)uni,
                             wxStringBuffer(target, len), len);
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
//    if (PyString_Check(obj)) {
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
//        PyUnicode_AsWideChar((PyUnicodeObject*)uni, wxStringBuffer(str, len), len);
//    }
//    if (obj != uni)
//        Py_DECREF(uni) // release the temporary Unicode object we may have created
//    return str;
//}
    
    
%End


//--------------------------------------------------------------------------
