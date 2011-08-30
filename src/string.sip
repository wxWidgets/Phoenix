//--------------------------------------------------------------------------
// Name:        string.sip
// Purpose:     Implements a %MappedType for wxString
//
// Author:      Robin Dunn
//
// Created:     9-Nov-2010
// Copyright:   (c) 2010 by Total Control Software
// Licence:     wxWindows license
//--------------------------------------------------------------------------


// We don't want the Python user to ever need to deal directly with wxString
// at all, so it will be mapped to and from Python Unicode objects using the
// code snippets below.

// NOTE: Currently we assume that string objects are encoding in utf-8.  

%MappedType wxString
{
    %ConvertToTypeCode
        // Code to test a PyObject for compatibility with wxString
        if (!sipIsErr) {
            if (PyString_Check(sipPy) || PyUnicode_Check(sipPy))
                return TRUE;
            return FALSE;
        }

        // Code to convert a compatible PyObject to a wxString
        PyObject* uni = sipPy;
        if (PyString_Check(sipPy)) {
            // if it's a string object convert it to unicode first, assuming utf-8
            uni = PyUnicode_FromEncodedObject(sipPy, "utf-8", "strict");
            if (PyErr_Occurred()) {
                *sipIsErr = 1;
                return 0;
            }
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
    %End

         
    %ConvertFromTypeCode
        // Code to convert a wxString to a Python Unicode object.
        return PyUnicode_FromWideChar(sipCpp->wc_str(), sipCpp->length());
    %End
    
};

%MappedType wxArrayString
{
    %ConvertToTypeCode
        if (!sipIsErr) {
            if (! PySequence_Check(sipPy)) {
                PyErr_SetString(PyExc_TypeError, "Sequence of strings expected.");
                return FALSE;
            } else
                return TRUE;
        }
        
        wxArrayString *array = new wxArrayString;
        int i, len=PySequence_Length(sipPy);
        for (i=0; i<len; i++) {
            PyObject* item = PySequence_GetItem(sipPy, i);

            if (PyString_Check(item)) {
                // if it's a string object convert it to unicode first, assuming utf-8
                item = PyUnicode_FromEncodedObject(item, "utf-8", "strict");
                if (PyErr_Occurred()) {
                    *sipIsErr = 1;
                    return 0;
                }
            }            
            wxString* string = new wxString();
            size_t len = PyUnicode_GET_SIZE(item);
            if (len) {
                PyUnicode_AsWideChar((PyUnicodeObject*)item,
                                     wxStringBuffer(*string, len), len);
            }
            if (PyErr_Occurred()) {
                *sipIsErr = 1;
                return 0;
            }
            array->Add(*string);
            delete string;
            Py_DECREF(item);
        }
        *sipCppPtr = array;
        return sipGetState(sipTransferObj);
    %End

         
    %ConvertFromTypeCode
        PyObject* list = PyList_New(0);
        for (size_t i=0; i < sipCpp->GetCount(); i++) {
            PyObject* str = PyUnicode_FromWideChar(sipCpp->Item(i).c_str(), sipCpp->Item(i).Len());
            PyList_Append(list, str);
            Py_DECREF(str);
        }
        return list;
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
