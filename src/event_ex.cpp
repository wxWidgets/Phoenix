
class wxPyCallback : public wxEvtHandler {
    DECLARE_ABSTRACT_CLASS(wxPyCallback)
public:
    wxPyCallback(PyObject* func);
    wxPyCallback(const wxPyCallback& other);
    ~wxPyCallback();

    void EventThunker(wxEvent& event);

    PyObject*   m_func;
};



IMPLEMENT_ABSTRACT_CLASS(wxPyCallback, wxEvtHandler);

wxPyCallback::wxPyCallback(PyObject* func) {
    m_func = func;
    Py_INCREF(m_func);
}

wxPyCallback::wxPyCallback(const wxPyCallback& other) {
    m_func = other.m_func;
    Py_INCREF(m_func);
}

wxPyCallback::~wxPyCallback() {
    wxPyBlock_t blocked = wxPyBeginBlockThreads();
    Py_DECREF(m_func);
    wxPyEndBlockThreads(blocked);
}


// #define wxPy_PRECALLINIT     "_preCallInit"
// #define wxPy_POSTCALLCLEANUP "_postCallCleanup"

// This function is used for all events destined for Python event handlers.
void wxPyCallback::EventThunker(wxEvent& event) {
    wxPyCallback*   cb = (wxPyCallback*)event.m_callbackUserData;
    PyObject*       func = cb->m_func;
    PyObject*       result;
    PyObject*       arg;
    PyObject*       tuple;
    bool            checkSkip = false;

    wxPyBlock_t blocked = wxPyBeginBlockThreads();
    wxString className = event.GetClassInfo()->GetClassName();

    // // If the event is one of these types then pass the original
    // // event object instead of the one passed to us.
    // if ( className == wxT("wxPyEvent") ) {
    //     arg =       ((wxPyEvent*)&event)->GetSelf();
    //     checkSkip = ((wxPyEvent*)&event)->GetCloned();
    // }
    // else if ( className == wxT("wxPyCommandEvent") ) {
    //     arg =       ((wxPyCommandEvent*)&event)->GetSelf();
    //     checkSkip = ((wxPyCommandEvent*)&event)->GetCloned();
    // }
    // else {
        arg = wxPyConstructObject((void*)&event, className);
    // }

    
    if (!arg) {
        PyErr_Print();
    } else {
        // // "intern" the pre/post method names to speed up the HasAttr
        // static PyObject* s_preName  = NULL;
        // static PyObject* s_postName = NULL;
        // if (s_preName == NULL) {
        //     s_preName  = PyString_FromString(wxPy_PRECALLINIT);
        //     s_postName = PyString_FromString(wxPy_POSTCALLCLEANUP);
        // }

        // // Check if the event object needs some preinitialization
        // if (PyObject_HasAttr(arg, s_preName)) {
        //     result = PyObject_CallMethodObjArgs(arg, s_preName, arg, NULL);
        //     if ( result ) {
        //         Py_DECREF(result);   // result is ignored, but we still need to decref it
        //         PyErr_Clear();       // Just in case...
        //     } else {
        //         PyErr_Print();
        //     }
        // }

        // Call the event handler, passing the event object
        tuple = PyTuple_New(1);
        PyTuple_SET_ITEM(tuple, 0, arg);  // steals ref to arg
        result = PyEval_CallObject(func, tuple);
        if ( result ) {
            Py_DECREF(result);   // result is ignored, but we still need to decref it
            PyErr_Clear();       // Just in case...
        } else {
            PyErr_Print();
        }

        // // Check if the event object needs some post cleanup
        // if (PyObject_HasAttr(arg, s_postName)) {
        //     result = PyObject_CallMethodObjArgs(arg, s_postName, arg, NULL);
        //     if ( result ) {
        //         Py_DECREF(result);   // result is ignored, but we still need to decref it
        //         PyErr_Clear();       // Just in case...
        //     } else {
        //         PyErr_Print();
        //     }
        // }

        // if ( checkSkip ) {
        //     // if the event object was one of our special types and
        //     // it had been cloned, then we need to extract the Skipped
        //     // value from the original and set it in the clone.
        //     result = PyObject_CallMethod(arg, "GetSkipped", "");
        //     if ( result ) {
        //         event.Skip(PyInt_AsLong(result));
        //         Py_DECREF(result);
        //     } else {
        //         PyErr_Print();
        //     }
        // }
        Py_DECREF(tuple);
    }
    wxPyEndBlockThreads(blocked);
}
