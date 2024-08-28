//--------------------------------------------------------------------------
// Name:        wxpy_api.sip
// Purpose:     The implementation of the API functions that are exported
//              from the core extension module.
//
// Author:      Robin Dunn
//
// Created:     19-Nov-2010
// Copyright:   (c) 2010-2020 by Total Control Software
// Licence:     wxWindows license
//--------------------------------------------------------------------------


%ModuleHeaderCode
#include <wxPython/wxpy_api.h>
%End

//--------------------------------------------------------------------------


%ModuleCode
// wxPython's API helper and utility functions

//--------------------------------------------------------------------------
// wxString conversion

// See also the wxString MappedType.  This code is similar, but doesn't
// allocate a new wxString instance on the heap, is able to convert
// non-string/unicode objects to unicode, and won't raise exceptions
static wxString i_Py2wxString(PyObject* source)
{
#if wxUSE_UNICODE_WCHAR == 0
#error wxString conversion can only handle WCHAR wxStrings currently
#endif
    PyErr_Clear();
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
    size_t len = PyUnicode_AsWideChar(uni, NULL, 0);
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
//    size_t len = PyUnicode_AsWideChar(uni, NULL, 0);
//    if (len) {
//        wxPyUnicode_AsWideChar(uni, wxStringBuffer(str, len), len);
//    }
//    if (obj != uni)
//        Py_DECREF(uni) // release the temporary Unicode object we may have created
//    return str;
//}

//--------------------------------------------------------------------------
// Wrapped object checks and converters
//
// TODO: Add some versions of these helpers that take a sipTypeDef
// instead of a name? They're accessible everywhere we need them, and
// it may be enough of an efficiency boost to make it worth it.

// Create a PyObject of the requested type from a void* and a class name.
static PyObject* i_wxPyConstructObject(void* ptr,
                                       const wxString& className,
                                       bool setThisOwn)
{
    wxString name = className;
    wxString nsDelimiter = "::";
    int pos = name.Find(nsDelimiter);
    if (pos != wxNOT_FOUND)
        name = name.Mid(pos + nsDelimiter.Len());

    const sipTypeDef* td = sipFindType(name.c_str());
    if (!td)
        return NULL;
    PyObject* transferObj = setThisOwn ? Py_None : NULL;
    return sipConvertFromType(ptr, td, transferObj);
}


// Check if a PyObject is a wrapped type
static bool i_wxPyWrappedPtr_Check(PyObject* obj)
{
    return PyObject_TypeCheck(obj, sipWrapper_Type);
}


// Check if a PyObject is a specific wrapped class or subclass
static bool i_wxPyWrappedPtr_TypeCheck(PyObject* obj, const wxString& className)
{
    const sipTypeDef* td = sipFindType(className.c_str());
    if (!td)
        return false;
    return sipCanConvertToType(obj, td, SIP_NO_CONVERTORS);
}


// Convert a wrapped SIP object to its C++ pointer, ensuring that it is of the expected type
static bool i_wxPyConvertWrappedPtr(PyObject* obj, void **ptr, const wxString& className)
{
    const sipTypeDef* td = sipFindType(className.c_str());
    if (!td)
        return false;
    if (! sipCanConvertToType(obj, td, SIP_NO_CONVERTORS))
        return false;
    int sipIsErr = 0;
    *ptr = sipConvertToType(obj, td, NULL, SIP_NO_CONVERTORS, 0, &sipIsErr);
    return true;
}


//--------------------------------------------------------------------------
// Deal with the GIL

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

//--------------------------------------------------------------------------
// Commonly used helpers for converting small sequences of numbers
// TODO: Are these still needed?

// A helper for converting a 2 element sequence to a pair of integers
static bool i_wxPy2int_seq_helper(PyObject* source, int* i1, int* i2)
{
    bool isFast = PyList_Check(source) || PyTuple_Check(source);
    PyObject *o1, *o2;

    if (!PySequence_Check(source) || PySequence_Length(source) != 2)
        return false;

    if (isFast) {
        o1 = PySequence_Fast_GET_ITEM(source, 0);
        o2 = PySequence_Fast_GET_ITEM(source, 1);
    }
    else {
        o1 = PySequence_GetItem(source, 0);
        o2 = PySequence_GetItem(source, 1);
    }

    *i1 = wxPyInt_AsLong(o1);
    *i2 = wxPyInt_AsLong(o2);

    if (! isFast) {
        Py_DECREF(o1);
        Py_DECREF(o2);
    }
    return true;
}

// A helper for converting a 4 element sequence to a set of integers
static bool i_wxPy4int_seq_helper(PyObject* source, int* i1, int* i2, int* i3, int* i4)
{
    bool isFast = PyList_Check(source) || PyTuple_Check(source);
    PyObject *o1, *o2, *o3, *o4;

    if (!PySequence_Check(source) || PySequence_Length(source) != 4)
        return false;

    if (isFast) {
        o1 = PySequence_Fast_GET_ITEM(source, 0);
        o2 = PySequence_Fast_GET_ITEM(source, 1);
        o3 = PySequence_Fast_GET_ITEM(source, 2);
        o4 = PySequence_Fast_GET_ITEM(source, 3);
    }
    else {
        o1 = PySequence_GetItem(source, 0);
        o2 = PySequence_GetItem(source, 1);
        o3 = PySequence_GetItem(source, 2);
        o4 = PySequence_GetItem(source, 3);
    }

    *i1 = wxPyInt_AsLong(o1);
    *i2 = wxPyInt_AsLong(o2);
    *i3 = wxPyInt_AsLong(o3);
    *i4 = wxPyInt_AsLong(o4);

    if (! isFast) {
        Py_DECREF(o1);
        Py_DECREF(o2);
        Py_DECREF(o3);
        Py_DECREF(o4);
    }
    return true;
}


//--------------------------------------------------------------------------
// wxVariant helpers


// A wxVariantData class that can hold a PyObject
class wxVariantDataPyObject : public wxPyUserDataHelper<wxVariantData>
{
public:
    explicit wxVariantDataPyObject(PyObject* obj = 0)
        : wxPyUserDataHelper<wxVariantData>(obj) {}

    virtual bool Eq(wxVariantData& data) const;

    virtual wxString GetType() const { return wxT("PyObject"); }
    wxVariantData* Clone() const { return new wxVariantDataPyObject(BorrowData()); }
};

bool wxVariantDataPyObject::Eq(wxVariantData& data) const
{
    wxASSERT_MSG( (data.GetType() == wxT("PyObject")),
                  wxT("wxVariantDataPyObject::Eq: argument mismatch") );
    wxVariantDataPyObject& otherData = (wxVariantDataPyObject&) data;

    wxPyThreadBlocker blocker;
    return PyObject_RichCompareBool(BorrowData(), otherData.BorrowData(), Py_EQ);
}




// Helper functions for the wxVariant mapped type. For the basic types that
// wxVariant knows about we will try to store/fetch natively, otherwise we'll
// just carry the PyObject through.
//
// These functions are here in the API so they can be used by both the
// wxVariant MappedType and by other classes or types that want to add support
// for additional kinds of natively supported types (see dataview for example.)

// PyObject --> wxVariant
wxVariant i_wxVariant_in_helper(PyObject* obj)
{
    wxVariant value;

    PyErr_Clear();

    if (PyBytes_Check(obj) || PyUnicode_Check(obj))
        value = Py2wxString(obj);

    else if (PyBool_Check(obj))
        value = (obj == Py_True);

    else if (wxPyInt_Check(obj))
        value = (long)wxPyInt_AS_LONG(obj);

    else if (PyLong_Check(obj))
        value = (long)PyLong_AsLong(obj);

    else if (PyFloat_Check(obj))
        value = PyFloat_AS_DOUBLE(obj);

    else if (obj == Py_None)
        value.MakeNull();

    else if (sipCanConvertToType(obj, sipType_wxDateTime, 0)) {
        wxDateTime* ptr;
        int state = 0;
        int isErr = 0;
        ptr = (wxDateTime*)sipConvertToType(obj, sipType_wxDateTime, NULL, 0, &state, &isErr);
        if (!isErr) {
            value = *ptr;
            sipReleaseType(ptr, sipType_wxDateTime, state);
        }
    }

    else if (wxPyWrappedPtr_TypeCheck(obj, wxT("wxBitmap"))) {
        wxBitmap* ptr;
        wxPyConvertWrappedPtr(obj, (void**)&ptr, wxT("wxBitmap"));
        value << *ptr;
    }

    else if (wxPyWrappedPtr_TypeCheck(obj, wxT("wxImage"))) {
        wxImage* ptr;
        wxPyConvertWrappedPtr(obj, (void**)&ptr, wxT("wxImage"));
        value << *ptr;
    }

    else if (wxPyWrappedPtr_TypeCheck(obj, wxT("wxIcon"))) {
        wxIcon* ptr;
        wxPyConvertWrappedPtr(obj, (void**)&ptr, wxT("wxIcon"));
        value << *ptr;
    }

    else if (wxPyWrappedPtr_TypeCheck(obj, wxT("wxColour"))) {
        wxColour* ptr;
        wxPyConvertWrappedPtr(obj, (void**)&ptr, wxT("wxColour"));
        value << *ptr;
    }

    else if (wxPyCheckStringSequence(obj)) {
        wxArrayString* ptr;
        int state = 0;
        int isErr = 0;
        ptr = (wxArrayString*)sipConvertToType(obj, sipType_wxArrayString, NULL, 0, &state, &isErr);
        if (!isErr) {
            value = *ptr;
            sipReleaseType(ptr, sipType_wxArrayString, state);
        }
    }

    else {
        // Just use the PyObject itself
        PyErr_Clear();
        value = new wxVariantDataPyObject(obj);
    }

    return value;
}


// wxVariant --> PyObject
PyObject* i_wxVariant_out_helper(const wxVariant& value)
{
    PyObject* obj;

    if (value.IsNull()) {
        obj = Py_None;
        Py_INCREF(obj);
    }

    else if (value.IsType("string"))
        obj = wx2PyString(value.GetString());

    else if (value.IsType("bool"))
        obj = PyBool_FromLong((long)value.GetBool());

    else if (value.IsType("long"))
        obj = PyLong_FromLong(value.GetLong());

    else if (value.IsType("longlong"))
        obj = PyLong_FromLongLong(value.GetLongLong().GetValue());

    else if (value.IsType("ulonglong"))
        obj = PyLong_FromUnsignedLongLong(value.GetULongLong().GetValue());

    else if (value.IsType("double"))
        obj = PyFloat_FromDouble(value.GetDouble());

    else if ( value.IsType("datetime") ) {
        wxDateTime val = value.GetDateTime();
        obj = wxPyConstructObject(new wxDateTime(val), "wxDateTime", true);
    }

    else if ( value.IsType("wxBitmap") ) {
        wxBitmap val;
        val << value;
        obj = wxPyConstructObject(new wxBitmap(val), "wxBitmap", true);
    }

    else if ( value.IsType("wxImage") ) {
        wxImage val;
        val << value;
        obj = wxPyConstructObject(new wxImage(val), "wxImage", true);
    }

    else if ( value.IsType("wxIcon") ) {
        wxIcon val;
        val << value;
        obj = wxPyConstructObject(new wxIcon(val), "wxIcon", true);
    }

    else if ( value.IsType("wxColour") ) {
        wxColour val;
        val << value;
        obj = wxPyConstructObject(new wxColour(val), "wxColour", true);
    }

    else if ( value.IsType("arrstring") ) {
        wxArrayString arr = value.GetArrayString();
        obj = sipConvertFromType(&arr, sipType_wxArrayString, NULL);
    }

    else if ( value.IsType("PyObject") ) {
        wxVariantDataPyObject* data = (wxVariantDataPyObject*)value.GetData();
        obj = data->GetData();
    }

    else {
        wxString msg = "Unexpected type (\"" + value.GetType() + "\") in wxVariant.";
        wxPyErr_SetString(PyExc_TypeError, msg.mb_str());
        obj = NULL;
    }

    return obj;
}


//--------------------------------------------------------------------------
// Check if the app object has been created. Raises an exception if not.

// Exception for when the wx.App hasn't been created yet
// (Initialized in wxPyCoreModuleInject)
PyObject* wxPyNoAppError = NULL;

bool i_wxPyCheckForApp(bool raiseException) {
    if (wxApp::GetInstance() != NULL)
        return true;
    else {
        if (raiseException)
            PyErr_SetString(wxPyNoAppError, "The wx.App object must be created first!");
        return false;
    }
}

//--------------------------------------------------------------------------
// Make a memory view object from a C buffer and size.

PyObject* i_wxPyMakeBuffer(void* ptr, Py_ssize_t len, bool readOnly=false) {
    wxPyThreadBlocker blocker;
    if (ptr && len) {
        Py_buffer view;
        int flags = PyBUF_FORMAT|PyBUF_ND;
        if (!readOnly)
            flags |= PyBUF_WRITABLE;
        PyBuffer_FillInfo(&view, NULL, ptr, len, readOnly ? 1:0, flags);
        return PyMemoryView_FromBuffer(&view);
    } else {
        Py_INCREF(Py_None); return Py_None;
        // return PyBytes_FromString("");    TODO: None or an empty string?
    }

//    // TODO: Consider using a sip.array object instead, like this:
//    // Create a sip.array of bytes, and then convert to a memoryview which is
//    // basically the same thing but is a documented built-in Python type
//    int flags = 0;
//    if (readOnly)
//        flags |= SIP_READ_ONLY;
//    PyObject* array = sipConvertToArray(ptr, "B", len, flags);
//    return array;
}


//--------------------------------------------------------------------------
// Check if an object is suitable for conversion to various "value" types that
// can be created from a sequence of numbers, such as wx.Point, wx.Colour,
// wx.Rect, etc.

bool i_wxPyNumberSequenceCheck(PyObject* obj, int reqLength=-1) {
    // Used in the various places where a sequence of numbers can be converted
    // to a wx type, like wxPoint, wxSize, wxColour, etc. Returns true if the
    // object is a Tuple, List or numpy Array of the proper length.

    // See also i_wxPyCheckNumberSequence below which can be used in more
    // general purpose situations and for sequences of any length.

    // tuples or lists are easy
    bool isFast = (PyTuple_Check(obj) || PyList_Check(obj));

    if (!isFast ) {
        // If it's not one of those, then check for an array.
        // It's probably not a good idea to do it this way, but this allows us
        // to check if the object is a numpy array without requiring that
        // numpy be imported even for those applications that are not using it.
        if (strcmp(obj->ob_type->tp_name, "numpy.ndarray") != 0)
            return false;
    }

    // Bail out here if the length isn't given
    if (reqLength == -1)
        return true;

    // Now check that the length matches the expected length
    if (PySequence_Length(obj) != reqLength)
        return false;

    // Check that each item is a number
    for (int i=0; i<reqLength; i+=1) {
        PyObject* item;
        if (isFast)
            item = PySequence_Fast_GET_ITEM(obj, i);
        else
            item = PySequence_ITEM(obj, i);
        bool isNum = PyNumber_Check(item);
        if (!isFast)
            Py_DECREF(item);
        if (!isNum)
            return false;
    }
    return true;
}


//--------------------------------------------------------------------------
// Get the pointer to the C++ object out of the sipSimpleWrapper structure.
// Yes, it's super unsafe and probably stupid, but here it is...

void* i_wxPyGetCppPtr(sipSimpleWrapper* sipPyObj) {
    return sipPyObj->data;
}

//--------------------------------------------------------------------------
// Call the PyMethod_Self API, which is not available when the Python
// limited API is activated.

inline PyObject* i_wxPyMethod_Self(PyObject* method) {
    return PyMethod_Self(method);
}



//--------------------------------------------------------------------------
// Cleanup and reinitialize the wxModules. This is needed because sometimes an
// Extension module will first be imported *after* the wx.App has been
// created, so the wxModules in that extension will not have been registered
// and initialized because they were not yet in memory.

void i_wxPyReinitializeModules() {
    if (i_wxPyCheckForApp(false)) {
        // NOTE: We are intentionally NOT calling wxModule::CleanUpModules
        // here because that could clear some things that will not be reset
        // when used again, leading to crashes. For example, in
        // wxMSWDCImpl::DoGradientFillLinear it is saving a pointer to an API
        // function in a dyn-loaded DLL. When modules are cleaned up then that
        // DLL will be unloaded, leaving a dangling function pointer.  We'll
        // likely end up with multiple instances of some things, but that is
        // better than the alternative currently.
        //wxModule::CleanUpModules();

        wxModule::RegisterModules();
        wxModule::InitializeModules();

        // And since we're not calling CleanUpModules there is no longer any
        // need to re-init the image handlers.
        //wxInitAllImageHandlers();
    }
}

//--------------------------------------------------------------------------
// Route the various usages of the PyDate_ APIs through our API, so we only
// have to worry about PyDateTime_IMPORT being needed in one compilation unit.

int i_wxPyDateTime_Check(PyObject *obj) {
    return PyDateTime_Check(obj);
}

int i_wxPyDate_Check(PyObject *obj) {
    return PyDate_Check(obj);
}

wxDateTime* i_wxPyDateTime_ToWxDateTime(PyObject *obj) {
    return new wxDateTime(PyDateTime_GET_DAY(obj),
                          (wxDateTime::Month)(PyDateTime_GET_MONTH(obj)-1),
                          PyDateTime_GET_YEAR(obj),
                          PyDateTime_DATE_GET_HOUR(obj),
                          PyDateTime_DATE_GET_MINUTE(obj),
                          PyDateTime_DATE_GET_SECOND(obj),
                          PyDateTime_DATE_GET_MICROSECOND(obj)/1000); // micro to milli
}

wxDateTime* i_wxPyDate_ToWxDateTime(PyObject *obj) {
    return new wxDateTime(PyDateTime_GET_DAY(obj),
                          (wxDateTime::Month)(PyDateTime_GET_MONTH(obj)-1),
                          PyDateTime_GET_YEAR(obj));
}

//--------------------------------------------------------------------------

bool i_wxPyCheckNumberSequence(PyObject *obj)
{
    if (PySequence_Check(obj) &&
            !(PyBytes_Check(obj) || PyUnicode_Check(obj))) {

        Py_ssize_t i, len = PySequence_Length(obj);
        bool failed;
        for (i=0; i<len; i++) {
            PyObject* item = PySequence_GetItem(obj, i);
            failed = !PyNumber_Check(item);
            Py_DECREF(item);
            if (failed)
                return false;
        }
        return true;
    }
    return false;
}

bool i_wxPyCheckStringSequence(PyObject *obj)
{
    if (PySequence_Check(obj) &&
            !(PyBytes_Check(obj) || PyUnicode_Check(obj))) {

        Py_ssize_t i, len = PySequence_Length(obj);
        bool failed;
        for (i=0; i<len; i++) {
            PyObject* item = PySequence_GetItem(obj, i);
            failed = !PyBytes_Check(item) && !PyUnicode_Check(item);
            Py_DECREF(item);
            if (failed)
                return false;
        }
        return true;
    }
    return false;
}

//--------------------------------------------------------------------------
// An instance of the API structure
static wxPyAPI  API = {
    i_Py2wxString,
    i_wxPyConstructObject,
    i_wxPyBeginBlockThreads,
    i_wxPyEndBlockThreads,
    i_wxPyWrappedPtr_Check,
    i_wxPyConvertWrappedPtr,
    i_wxPy2int_seq_helper,
    i_wxPy4int_seq_helper,
    i_wxPyWrappedPtr_TypeCheck,
    i_wxVariant_in_helper,
    i_wxVariant_out_helper,
    i_wxPyCheckForApp,
    i_wxPyMakeBuffer,
    i_wxPyNumberSequenceCheck,
    i_wxPyGetCppPtr,
    i_wxPyMethod_Self,
    i_wxPyReinitializeModules,
    i_wxPyDateTime_Check,
    i_wxPyDate_Check,
    i_wxPyDateTime_ToWxDateTime,
    i_wxPyDate_ToWxDateTime,
    i_wxPyCheckNumberSequence,
    i_wxPyCheckStringSequence
};
%End


%ModuleHeaderCode
    #include <datetime.h>
%End

%InitialisationCode
    PyDateTime_IMPORT;
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
