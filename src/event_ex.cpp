
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
    wxPyBLOCK_THREADS( Py_INCREF(m_func) );
}

wxPyCallback::wxPyCallback(const wxPyCallback& other) {
    m_func = other.m_func;
    wxPyBLOCK_THREADS( Py_INCREF(m_func) );
}

wxPyCallback::~wxPyCallback() {
    wxPyBLOCK_THREADS( Py_DECREF(m_func) );
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

    wxPyThreadBlocker blocker;
    wxString className = event.GetClassInfo()->GetClassName();
    // A wrapper that already exists belongs to Python code (for example an
    // event created in Python and passed to ProcessEvent), so it must not be
    // invalidated below.
    bool existed = false;
    const sipTypeDef* td = sipFindType(className.c_str());
    if (td) {
        existed = sipGetPyObject(&event, td) != NULL;
        arg = sipConvertFromType(&event, td, NULL);
    }
    else {
        arg = wxPyConstructObject((void*)&event, className);
    }

    if (!arg) {
        PyErr_Print();
    } else {
        // Call the event handler, passing the event object
        tuple = PyTuple_New(1);
        PyTuple_SET_ITEM(tuple, 0, arg);  // steals ref to arg
        result = PyObject_CallObject(func, tuple);
        if ( result ) {
            Py_DECREF(result);   // result is ignored, but we still need to decref it
            PyErr_Clear();       // Just in case...
        } else {
            PyErr_Print();
        }
        // The C++ event usually goes away right after this, so if the handler
        // kept a reference to the wrapper, disconnect it. Using it later then
        // raises an exception instead of reading a dead object, and SIP won't
        // hand it out again for another event created at the same address.
        if (!existed && Py_REFCNT(arg) > 1) {
            sipSimpleWrapper* sw = reinterpret_cast<sipSimpleWrapper*>(arg);
            sipInstanceDestroyedEx(&sw);
        }
        Py_DECREF(tuple);
    }
}
