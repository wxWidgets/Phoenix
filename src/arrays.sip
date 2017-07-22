//--------------------------------------------------------------------------
// Name:        src/arrays.sip
// Purpose:     Implements a %MappedType for wxArrayString and wxArrayInt
//
// Author:      Robin Dunn
//
// Created:     2-Sept-2011
// Copyright:   (c) 2011-2017 by Total Control Software
// Licence:     wxWindows license
//--------------------------------------------------------------------------


// Some SIP MappedTypes that automatically convert Python lists of
// strings/ints to and from wxArrayString/wxArrayInt.

//--------------------------------------------------------------------------

%MappedType wxArrayString
{
    %ConvertToTypeCode
        // Code to test a PyObject for compatibility
        if (!sipIsErr) {
            int success = TRUE;
            // ensure that it is a sequence
            if (! PySequence_Check(sipPy))
                success = FALSE;
            // Ensure it is not a string or unicode object (they are sequences)
            else if (PyBytes_Check(sipPy) || PyUnicode_Check(sipPy))
                success = FALSE;
            // ensure each item is a string/unicode object
            else {
                Py_ssize_t i, len = PySequence_Length(sipPy);
                for (i=0; i<len; i++) {
                    PyObject* item = PySequence_GetItem(sipPy, i);
                    if (!PyBytes_Check(item) && !PyUnicode_Check(item)) {
                        Py_DECREF(item);
                        success = FALSE;
                        break;
                    }
                    Py_DECREF(item);
                }
            }
            if (!success)
                PyErr_SetString(PyExc_TypeError, "Sequence of string or unicode objects expected.");
            return success;
        }

        // Code to create a new wxArrayString and convert a compatible PyObject
        wxArrayString *array = new wxArrayString;
        Py_ssize_t i, len = PySequence_Length(sipPy);
        for (i=0; i<len; i++) {
            PyObject* item = PySequence_GetItem(sipPy, i);

            // if it's a string object convert it to unicode first, assuming utf-8
            if (PyBytes_Check(item)) {
                Py_DECREF(item);
                item = PyUnicode_FromEncodedObject(item, "utf-8", "strict");
                if (PyErr_Occurred()) {
                    *sipIsErr = 1;
                    delete array;
                    Py_DECREF(item);
                    return 0;
                }
            }
            PyErr_Clear();
            wxString string;
            size_t len = PyUnicode_GET_SIZE(item);
            if (len) {
                wxPyUnicode_AsWideChar(item, wxStringBuffer(string, len), len);
            }
            if (PyErr_Occurred()) {
                *sipIsErr = 1;
                delete array;
                Py_DECREF(item);
                return 0;
            }
            array->Add(string);
            Py_DECREF(item);
        }
        *sipCppPtr = array;
        return sipGetState(sipTransferObj);
    %End


    %ConvertFromTypeCode
        // Code to convert a wxArrayString to a Python list of strings.
        PyObject* list = PyList_New(0);
        for (size_t i=0; i < sipCpp->GetCount(); i++) {
            PyObject* str = wx2PyString(sipCpp->Item(i));
            PyList_Append(list, str);
            Py_DECREF(str);
        }
        return list;
    %End

};


// Used just for unittesting the MappedType code, it can be removed later
%ModuleCode
wxArrayString testArrayStringTypemap(const wxArrayString& arr)
{
    wxArrayString local = arr;  // force a copy
    return local;
}
%End
wxArrayString testArrayStringTypemap(const wxArrayString& arr);


//--------------------------------------------------------------------------

%MappedType wxArrayInt
{
    %ConvertToTypeCode
        // Code to test a PyObject for compatibility
        if (!sipIsErr) {
            int success = TRUE;
            // ensure that it is a sequence
            if (! PySequence_Check(sipPy))
                success = FALSE;
            // ensure each item is a number object
            else {
                Py_ssize_t i, len = PySequence_Length(sipPy);
                for (i=0; i<len; i++) {
                    PyObject* item = PySequence_GetItem(sipPy, i);
                    if (!PyNumber_Check(item)) {
                        Py_DECREF(item);
                        success = FALSE;
                        break;
                    }
                    Py_DECREF(item);
                }
            }
            if (!success)
                PyErr_SetString(PyExc_TypeError, "Sequence of numbers expected.");
            return success;
        }

        // Code to create a new wxArrayInt and convert a compatible PyObject
        wxArrayInt *array = new wxArrayInt;
        Py_ssize_t i, len = PySequence_Length(sipPy);
        for (i=0; i<len; i++) {
            PyObject* item = PySequence_GetItem(sipPy, i);
            PyObject* number = wxPyNumber_Int(item);
            if (PyErr_Occurred()) {
                *sipIsErr = 1;
                delete array;
                Py_DECREF(item);
                return 0;
            }
            array->Add(wxPyInt_AS_LONG(number));
            Py_DECREF(item);
            Py_DECREF(number);
        }
        *sipCppPtr = array;
        return sipGetState(sipTransferObj);
    %End


    %ConvertFromTypeCode
        // Code to convert a wxArrayInt to a Python list of integers.
        PyObject* list = PyList_New(0);
        for (size_t i=0; i < sipCpp->GetCount(); i++) {
            PyObject* number = wxPyInt_FromLong(sipCpp->Item(i));
            PyList_Append(list, number);
            Py_DECREF(number);
        }
        return list;
    %End

};


// Used just for unittesting the MappedType code, it can be removed later
%ModuleCode
wxArrayInt testArrayIntTypemap(const wxArrayInt& arr)
{
    wxArrayInt local = arr;  // force a copy
    return local;
}
%End
wxArrayInt testArrayIntTypemap(const wxArrayInt& arr);


//--------------------------------------------------------------------------


%MappedType wxArrayDouble
{
    %ConvertToTypeCode
        // Code to test a PyObject for compatibility
        if (!sipIsErr) {
            int success = TRUE;
            // ensure that it is a sequence
            if (! PySequence_Check(sipPy))
                success = FALSE;
            // ensure each item is a number object
            else {
                Py_ssize_t i, len = PySequence_Length(sipPy);
                for (i=0; i<len; i++) {
                    PyObject* item = PySequence_GetItem(sipPy, i);
                    if (!PyNumber_Check(item)) {
                        Py_DECREF(item);
                        success = FALSE;
                        break;
                    }
                    Py_DECREF(item);
                }
            }
            if (!success)
                PyErr_SetString(PyExc_TypeError, "Sequence of numbers expected.");
            return success;
        }

        // Code to create a new wxArrayDouble and convert a compatible PyObject
        wxArrayDouble *array = new wxArrayDouble;
        Py_ssize_t i, len = PySequence_Length(sipPy);
        for (i=0; i<len; i++) {
            PyObject* item = PySequence_GetItem(sipPy, i);
            PyObject* number = PyNumber_Float(item);
            if (PyErr_Occurred()) {
                *sipIsErr = 1;
                delete array;
                Py_DECREF(item);
                return 0;
            }
            array->Add(PyFloat_AS_DOUBLE(number));
            Py_DECREF(item);
            Py_DECREF(number);
        }
        *sipCppPtr = array;
        return sipGetState(sipTransferObj);
    %End


    %ConvertFromTypeCode
        // Code to convert a wxArrayDouble to a Python list of floating point values.
        PyObject* list = PyList_New(0);
        for (size_t i=0; i < sipCpp->GetCount(); i++) {
            PyObject* number = PyFloat_FromDouble(sipCpp->Item(i));
            PyList_Append(list, number);
            Py_DECREF(number);
        }
        return list;
    %End

};


// Used just for unittesting the MappedType code, it can be removed later
%ModuleCode
wxArrayDouble testArrayDoubleTypemap(const wxArrayDouble& arr)
{
    wxArrayDouble local = arr;  // force a copy
    return local;
}
%End
wxArrayDouble testArrayDoubleTypemap(const wxArrayDouble& arr);

//--------------------------------------------------------------------------
