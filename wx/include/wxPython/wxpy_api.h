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
// Copyright:   (c) 2010-2020 by Total Control Software
// Licence:     wxWindows license
//--------------------------------------------------------------------------

#ifndef _WXPY_API_H
#define _WXPY_API_H

#if defined(__APPLE__)
    // When it's possible that we're building universal binaries with both
    // 32-bit and 64-bit architectures then these need to be undef'ed because
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
#define wxPyBlock_t_default PyGILState_UNLOCKED

typedef unsigned char  byte;
typedef unsigned char* buffer;
typedef unsigned long  ulong;


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
    { wxPyThreadBlocker _blocker; stmt; }

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




// Macros to work around some of the differences in the Python 3 API
#if PY_MAJOR_VERSION >= 3
    #define wxPyInt_Check            PyLong_Check
    #define wxPyInt_AsLong           PyLong_AsLong
    #define wxPyInt_AS_LONG          PyLong_AS_LONG
    #define wxPyInt_AsSize_t         PyLong_AsSize_t
    #define wxPyInt_AsSsize_t        PyLong_AsSsize_t
    #define wxPyInt_AsUnsignedLong   PyLong_AsUnsignedLong
    #define wxPyInt_FromLong         PyLong_FromLong
    #define wxPyInt_FromSize_t       PyLong_FromSize_t
    #define wxPyInt_FromSsize_t      PyLong_FromSsize_t
    #define wxPyInt_FromUnsignedLong PyLong_FromUnsignedLong
    #define wxPyNumber_Int           PyNumber_Long
#else
    #define wxPyInt_Check            PyInt_Check
    #define wxPyInt_AsLong           PyInt_AsLong
    #define wxPyInt_AS_LONG          PyInt_AS_LONG
    #define wxPyInt_AsLong           PyInt_AsLong
    #define wxPyInt_AsSize_t(x)      static_cast<size_t>(PyInt_AsUnsignedLongLongMask(x))
    #define wxPyInt_AsSsize_t        PyInt_AsSsize_t
    #define wxPyInt_AsUnsignedLong   PyInt_AsUnsignedLongMask
    #define wxPyInt_FromLong         PyInt_FromLong
    #define wxPyInt_FromSize_t       PyInt_FromSize_t
    #define wxPyInt_FromSsize_t      PyInt_FromSsize_t
    #define wxPyInt_FromUnsignedLong PyInt_FromSize_t
    #define wxPyNumber_Int           PyNumber_Int
#endif

inline
Py_ssize_t wxPyUnicode_AsWideChar(PyObject* unicode, wchar_t* w, Py_ssize_t size)
{
    // GIL should already be held
#if PY_MAJOR_VERSION >= 3
    return PyUnicode_AsWideChar(unicode, w, size);
#else
    return PyUnicode_AsWideChar((PyUnicodeObject*)unicode, w, size);
#endif
}



//--------------------------------------------------------------------------
// These are the API items whose implementation can not or should not be
// inline functions or macros. The implementations will instead be accessed
// via a structure of function pointers that is exported from the wx._core
// extension module. See wxpy_api.sip for the implementations.
//--------------------------------------------------------------------------

struct wxPyAPI {
    wxString      (*p_Py2wxString)(PyObject* source);
    PyObject*     (*p_wxPyConstructObject)(void* ptr, const wxString& className, bool setThisOwn);
    wxPyBlock_t   (*p_wxPyBeginBlockThreads)();
    void          (*p_wxPyEndBlockThreads)(wxPyBlock_t blocked);
    bool          (*p_wxPyWrappedPtr_Check)(PyObject* obj);
    bool          (*p_wxPyConvertWrappedPtr)(PyObject* obj, void **ptr, const wxString& className);
    bool          (*p_wxPy2int_seq_helper)(PyObject* source, int* i1, int* i2);
    bool          (*p_wxPy4int_seq_helper)(PyObject* source, int* i1, int* i2, int* i3, int* i4);
    bool          (*p_wxPyWrappedPtr_TypeCheck)(PyObject* obj, const wxString& className);
    wxVariant     (*p_wxVariant_in_helper)(PyObject* obj);
    PyObject*     (*p_wxVariant_out_helper)(const wxVariant& value);
    bool          (*p_wxPyCheckForApp)(bool raiseException);
    PyObject*     (*p_wxPyMakeBuffer)(void* ptr, Py_ssize_t len, bool readOnly);
    bool          (*p_wxPyNumberSequenceCheck)(PyObject* obj, int reqLength);
    void*         (*p_wxPyGetCppPtr)(sipSimpleWrapper* sipPyObj);
    PyObject*     (*p_wxPyMethod_Self)(PyObject* method);
    void          (*p_wxPyReinitializeModules)();

    int           (*p_wxPyDateTime_Check)(PyObject *obj);
    int           (*p_wxPyDate_Check)(PyObject *obj);
    wxDateTime*   (*p_wxPyDateTime_ToWxDateTime)(PyObject *obj);
    wxDateTime*   (*p_wxPyDate_ToWxDateTime)(PyObject *obj);

    bool          (*p_wxPyCheckNumberSequence)(PyObject *obj);
    bool          (*p_wxPyCheckStringSequence)(PyObject *obj);
    // Always add new items here at the end.
};



inline wxPyAPI* wxPyGetAPIPtr()
{
    static wxPyAPI* wxPyAPIPtr = NULL;

    if (wxPyAPIPtr == NULL) {
        PyGILState_STATE state = PyGILState_Ensure();
        wxPyAPIPtr = (wxPyAPI*)PyCapsule_Import("wx._wxPyAPI", 0);
        // uncomment if needed for debugging
        //if (PyErr_Occurred()) { PyErr_Print(); }
        //wxASSERT_MSG(wxPyAPIPtr != NULL, wxT("wxPyAPIPtr is NULL!!!"));
        PyGILState_Release(state);
    }

    return wxPyAPIPtr;
}

//--------------------------------------------------------------------------
// Inline wrappers which call the functions in the API structure

// Convert a PyObject to a wxString
// Assumes that the GIL has already been acquired.
inline wxString Py2wxString(PyObject* source)
    { return wxPyGetAPIPtr()->p_Py2wxString(source); }


// Create a PyObject of the requested type from a void* and a class name.
// Assumes that the GIL has already been acquired.
inline PyObject* wxPyConstructObject(void* ptr, const wxString& className, bool setThisOwn=false)
    { return wxPyGetAPIPtr()->p_wxPyConstructObject(ptr, className, setThisOwn); }


// Check if a PyObject is a wrapped type
inline bool wxPyWrappedPtr_Check(PyObject* obj)
    { return wxPyGetAPIPtr()->p_wxPyWrappedPtr_Check(obj); }

// Check if a PyObject is a specific wrapped type (or a subclass)
inline bool wxPyWrappedPtr_TypeCheck(PyObject* obj, const wxString& className)
    { return wxPyGetAPIPtr()->p_wxPyWrappedPtr_TypeCheck(obj, className); }


// Convert a wrapped SIP object to its C++ pointer, ensuring that it is of the expected type
inline bool wxPyConvertWrappedPtr(PyObject* obj, void **ptr, const wxString& className)
    { return wxPyGetAPIPtr()->p_wxPyConvertWrappedPtr(obj, ptr, className); }


// Calls from wxWindows back to Python code, or even any PyObject
// manipulations, PyDECREF's and etc. should be wrapped in calls to these functions:
inline wxPyBlock_t wxPyBeginBlockThreads()
    { return wxPyGetAPIPtr()->p_wxPyBeginBlockThreads(); }

inline void wxPyEndBlockThreads(wxPyBlock_t blocked)
    { wxPyGetAPIPtr()->p_wxPyEndBlockThreads(blocked); }



// A helper for converting a 2 element sequence to a pair of integers
inline bool wxPy2int_seq_helper(PyObject* source, int* i1, int* i2)
    { return wxPyGetAPIPtr()->p_wxPy2int_seq_helper(source, i1, i2); }

// A helper for converting a 4 element sequence to a set of integers
inline bool wxPy4int_seq_helper(PyObject* source, int* i1, int* i2, int* i3, int* i4)
    { return wxPyGetAPIPtr()->p_wxPy4int_seq_helper(source, i1, i2, i3, i4); }


// Convert a PyObject to a wxVariant
inline wxVariant wxVariant_in_helper(PyObject* obj)
    { return wxPyGetAPIPtr()->p_wxVariant_in_helper(obj); }

// Convert a wxVariant to a PyObject
inline PyObject* wxVariant_out_helper(const wxVariant& value)
    { return wxPyGetAPIPtr()->p_wxVariant_out_helper(value); }


// Check if a wx.App object has been created
inline bool wxPyCheckForApp(bool raiseException=true)
    { return wxPyGetAPIPtr()->p_wxPyCheckForApp(raiseException); }


// Create a buffer object from a pointer and size
inline PyObject* wxPyMakeBuffer(void* ptr, Py_ssize_t len, bool readOnly=false)
    { return wxPyGetAPIPtr()->p_wxPyMakeBuffer(ptr, len, readOnly); }

// Check if an object is a sequence of numbers
inline bool wxPyNumberSequenceCheck(PyObject* obj, int reqLength=-1)
    { return wxPyGetAPIPtr()->p_wxPyNumberSequenceCheck(obj, reqLength); }


inline void* wxPyGetCppPtr(sipSimpleWrapper* sipPyObj)
    { return wxPyGetAPIPtr()->p_wxPyGetCppPtr(sipPyObj); }

inline PyObject* wxPyMethod_Self(PyObject* method)
    { return wxPyGetAPIPtr()->p_wxPyMethod_Self(method); }


inline void wxPyReinitializeModules()
    { return wxPyGetAPIPtr()->p_wxPyReinitializeModules(); }



inline int wxPyDateTime_Check(PyObject *obj)
    { return wxPyGetAPIPtr()->p_wxPyDateTime_Check(obj); }

inline int wxPyDate_Check(PyObject *obj)
    { return wxPyGetAPIPtr()->p_wxPyDate_Check(obj); }

inline wxDateTime* wxPyDateTime_ToWxDateTime(PyObject *obj)
    { return wxPyGetAPIPtr()->p_wxPyDateTime_ToWxDateTime(obj); }

inline wxDateTime* wxPyDate_ToWxDateTime(PyObject *obj)
    { return wxPyGetAPIPtr()->p_wxPyDate_ToWxDateTime(obj); }


inline bool wxPyCheckNumberSequence(PyObject *obj)
{
    return wxPyGetAPIPtr()->p_wxPyCheckNumberSequence(obj);
}

inline bool wxPyCheckStringSequence(PyObject *obj)
{
    return wxPyGetAPIPtr()->p_wxPyCheckStringSequence(obj);
}

//--------------------------------------------------------------------------
// Convenience helper for RAII-style thread blocking

class wxPyThreadBlocker {
public:
    explicit wxPyThreadBlocker(bool block=true)
        :   m_oldstate(block ?  wxPyBeginBlockThreads() : wxPyBlock_t_default),
            m_block(block)
    { }

    ~wxPyThreadBlocker() {
        if (m_block) {
            wxPyEndBlockThreads(m_oldstate);
        }
    }

private:
    void operator=(const wxPyThreadBlocker&);
    explicit wxPyThreadBlocker(const wxPyThreadBlocker&);
    wxPyBlock_t m_oldstate;
    bool        m_block;
};


//--------------------------------------------------------------------------
// helper template to make common code for all of the various user data owners

template<typename Base>
class wxPyUserDataHelper : public Base {
public:
    explicit wxPyUserDataHelper(PyObject* obj = NULL)
        : m_obj(obj ? obj : Py_None)
    {
        wxPyThreadBlocker blocker;
        Py_INCREF(m_obj);
    }

    ~wxPyUserDataHelper()
    {   // normally the derived class does the clean up, or deliberately leaks
        // by setting m_obj to 0, but if not then do it here.
        if (m_obj) {
            wxPyThreadBlocker blocker;
            Py_DECREF(m_obj);
            m_obj = 0;
        }
    }

    // Return Value: New reference
    PyObject* GetData() const {
        wxPyThreadBlocker blocker;
        Py_INCREF(m_obj);
        return m_obj;
    }

    // Return Value: Borrowed reference
    PyObject* BorrowData() const {
        return m_obj;
    }

    void SetData(PyObject* obj) {
        if (obj != m_obj) {
            wxPyThreadBlocker blocker;
            Py_DECREF(m_obj);
            m_obj = obj ? obj : Py_None;
            Py_INCREF(m_obj);
        }
    }

    // Return the object in udata or None if udata is null
    // Return Value: New reference
    static PyObject* SafeGetData(wxPyUserDataHelper<Base>* udata) {
        wxPyThreadBlocker blocker;
        PyObject* obj = udata ? udata->BorrowData() : Py_None;
        Py_INCREF(obj);
        return obj;
    }

    // Set the m_obj to null, this should only be used during clean up, when
    // the object should be leaked.
    // Calling any other methods on this object is then undefined behaviour
    void ReleaseDataDuringCleanup()
    {
        m_obj = 0;
    }

private:
    PyObject* m_obj;
};



// A wxClientData that holds a reference to a Python object
class wxPyClientData : public wxPyUserDataHelper<wxClientData>
{
public:
    wxPyClientData(PyObject* obj = NULL)
        : wxPyUserDataHelper<wxClientData>(obj)
    { }
};




// A wxObject object that holds a reference to a Python object
class wxPyUserData : public wxPyUserDataHelper<wxObject>
{
public:
    wxPyUserData(PyObject* obj = NULL)
        : wxPyUserDataHelper<wxObject>(obj)
    { }
};


//--------------------------------------------------------------------------
#endif
