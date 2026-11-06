//--------------------------------------------------------------------------
// Name:        string.sip
// Purpose:     Implements a %MappedType for wxString
//
// Author:      Robin Dunn
//
// Created:     9-Nov-2010
// Copyright:   (c) 2010-2020 by Total Control Software
// Licence:     wxWindows license
//--------------------------------------------------------------------------


// We don't want the Python user to ever need to deal directly with wxString
// at all, so it will be mapped to and from Python Unicode objects using the
// code snippets below.
// NOTE: Currently we assume that string objects are encoded in utf-8.

%MappedType wxString
{

    // TODO: It is still possible to have a wx build that uses utf-8 inside
    // wxString, so we should probably be checking wxUSE_UNICODE_WCHAR or
    // wxUSE_UNICODE_UTF8 for this conversion.

    %ConvertToTypeCode
        #if wxUSE_UNICODE_WCHAR == 0
        #error wxString conversion can only handle WCHAR wxStrings currently
        #endif

        // Code to test a PyObject for compatibility with wxString
        if (!sipIsErr) {
            if (PyBytes_Check(sipPy) || PyUnicode_Check(sipPy))
                return TRUE;
            return FALSE;
        }

        // Code to convert a compatible PyObject to a wxString
        PyObject* uni = sipPy;
        if (PyBytes_Check(sipPy)) {
            // if it's a string object convert it to unicode first, assuming utf-8
            uni = PyUnicode_FromEncodedObject(sipPy, "utf-8", "strict");
            if (PyErr_Occurred()) {
                *sipIsErr = 1;
                return 0;
            }
        }
        *sipCppPtr = new wxString();
        size_t len = PyUnicode_AsWideChar(uni, NULL, 0);
        if (len) {
            wxPyUnicode_AsWideChar(uni, wxStringBuffer(**sipCppPtr, len), len);
        }
        if (PyBytes_Check(sipPy))
            Py_DECREF(uni);  // release the temporary Unicode object we created
        return sipGetState(sipTransferObj);
    %End


    %ConvertFromTypeCode
        // Convert a wxString to a Python Unicode object.  See wxpy_api.sip
        return wx2PyString(*sipCpp);
    %End
};


// wxPyPathString is a typedef of wxString, so C++ sees no difference. etg
// uses it for parameters that are file system paths, and its distinct name
// lets SIP give them a converter that also accepts os.PathLike objects.

%MappedType wxPyPathString
{
    %TypeHeaderCode
        typedef wxString wxPyPathString;
    %End

    %ConvertToTypeCode
        if (!sipIsErr) {
            return PyBytes_Check(sipPy) || PyUnicode_Check(sipPy) ||
                   PyObject_HasAttrString(sipPy, "__fspath__");
        }

        // A str or bytes object is returned as a new reference
        PyObject* path = PyOS_FSPath(sipPy);
        if (!path) {
            *sipIsErr = 1;
            return 0;
        }
        PyObject* uni = path;
        if (PyBytes_Check(path)) {
            uni = PyUnicode_FromEncodedObject(path, "utf-8", "strict");
            Py_DECREF(path);
            if (!uni) {
                *sipIsErr = 1;
                return 0;
            }
        }
        *sipCppPtr = new wxPyPathString();
        size_t len = PyUnicode_AsWideChar(uni, NULL, 0);
        if (len) {
            wxPyUnicode_AsWideChar(uni, wxStringBuffer(**sipCppPtr, len), len);
        }
        Py_DECREF(uni);
        return sipGetState(sipTransferObj);
    %End

    %ConvertFromTypeCode
        return wx2PyString(*sipCpp);
    %End
};



// Used just for testing the MappedType code, it can be removed later
%ModuleCode
wxString testStringTypemap(const wxString& str)
{
    wxString local = str;
    return local;
}
%End
wxString testStringTypemap(const wxString& str);
