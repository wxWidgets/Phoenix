//--------------------------------------------------------------------------
// Name:        wxpy_utils.sip
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

%End


//--------------------------------------------------------------------------



%ModuleCode
// Various wxPython helper/utility functions


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
%End

//--------------------------------------------------------------------------
// Sometimes we need to hold on to a C array and keep it alive, but typical
// SIP code will treat it as a temporary and delete it as soon as the ctor or
// method call is done. This class can hold a pointer to the array and will
// delete the array in its dtor, and by making this class be wrappable we can
// make a PyObject for it that is then owned by some other object, and
// Python's GC will take care of the delaying the cleanup until it's no longer
// needed.
template <Type>
class wxCArrayHolder
{
%TypeHeaderCode
#include "arrayholder.h"
%End
    
public:
    wxCArrayHolder();
    ~wxCArrayHolder();
    
private:
    wxCArrayHolder(const wxCArrayHolder<Type>&);  // no copies    
    wxCArrayHolder& operator=(wxCArrayHolder<Type>); // no assignment
};

typedef wxCArrayHolder<int>      wxIntCArrayHolder;
typedef wxCArrayHolder<wxString> wxStringCArrayHolder;
typedef wxCArrayHolder<wxDash>   wxDashCArrayHolder;

//--------------------------------------------------------------------------
