/////////////////////////////////////////////////////////////////////////////
// Name:        string.sip
// Purpose:     Implements a %MappedType for wxString
//
// Author:      Robin Dunn
//
// Created:     9-Nov-2010
// Copyright:   (c) 2010 by Total Control Software
// Licence:     wxWindows license
/////////////////////////////////////////////////////////////////////////////


// We don't want the Python user to ever need to deal directly with wxString
// at all, so it will be mapped to and from Python Unicode objects using the
// code snippets below.

// NOTE: Currently we assume that string objects are encoding in utf-8.  Decide if we
// want to do this or to use the default encoding for the locale like the old
// wxPython does.

%MappedType wxString
{
    // Code to test a PyObject for compatibility and to convert from a 
    // PyObject to a wxString
    %ConvertToTypeCode
        // just check the type?
        if (!sipIsErr) {
            if (PyString_Check(sipPy) || PyUnicode_Check(sipPy))
                return 1;
            return 0;
        }
        // Or do the conversion
#if wxUSE_UNICODE_WCHAR
        // wxString will contain wide chars (wchar_t)
        PyObject* uni = sipPy;
        if (PyString_Check(sipPy)) {
            // if it's a string object convert it to unicode first
            uni = PyUnicode_FromEncodedObject(sipPy,
                                              "utf-8", /*wxPyDefaultEncoding*/
                                              "strict");
            if (PyErr_Occurred()) return 0;
        }            
        *sipCppPtr = new wxString();
        size_t len = PyUnicode_GET_SIZE(uni);
        if (len) {
            PyUnicode_AsWideChar((PyUnicodeObject*)uni,
                                 wxStringBuffer(**sipCppPtr, len), len);
        }
        if (PyString_Check(sipPy))
            Py_DECREF(uni);  // release the temporary Unicode object we created
        return sipGetState(sipTransferObj);
#else
        // wxString will contain a utf-8 encoded byte string.  If source is
        // already a string then use it as-is, (assuming utf-8) otherwise
        // the Unicode object to utf-8 and use the converted value.
        char* tmpPtr; Py_ssize_t tmpSize;
        PyObject* str = NULL;
        //PyObject* uni = NULL;
        if (PyString_Check(sipPy) /*&& wxPyDefaultEncodingIsUTF8 */) {
            PyString_AsStringAndSize(sipPy, &tmpPtr, &tmpSize);
        }
        //else if (PyString_Check(sipPy)) {
        //    uni = PyUnicode_FromEncodedObject(sipPy, wxPyDefaultEncoding, "strict");
        //    if (PyErr_Occurred()) return NULL;
        //    str = PyUnicode_AsUTF8String(uni);
        //    PyString_AsStringAndSize(sipPy, &tmpPtr, &tmpSize);
        //}
        else {
            str = PyUnicode_AsUTF8String(sipPy);
            PyString_AsStringAndSize(str, &tmpPtr, &tmpSize);
        }
        *sipCppPtr = new wxString(tmpPtr, tmpSize);
        Py_XDECREF(str);
        //Py_XDECREF(uni);    
        return sipGetState(sipTransferObj);        
#endif
    %End

         
    // Code to convert a wxString to a PyObject
    %ConvertFromTypeCode
         return sipBuildResult(NULL, "G", sipCpp->c_str(), sipCpp->length());
    %End
    
};
