//--------------------------------------------------------------------------
// Name:        filename.sip
// Purpose:     Implements a %MappedType for wxFileName
//
// Author:      Robin Dunn
//
// Created:     30-July-2012
// Copyright:   (c) 2012-2020 by Total Control Software
// Licence:     wxWindows license
//--------------------------------------------------------------------------


// wxFileNames are mapped to/from Unicode string objects

%MappedType wxFileName
{
    %ConvertToTypeCode
        // Code to test a PyObject for compatibility with wxFileName
        if (!sipIsErr) {
            return PyBytes_Check(sipPy) || PyUnicode_Check(sipPy) ||
                   PyObject_HasAttrString(sipPy, "__fspath__");
        }

        // Code to convert a compatible PyObject to a wxFileName
        PyObject* path = PyOS_FSPath(sipPy);
        if (!path) {
            *sipIsErr = 1;
            return 0;
        }
        *sipCppPtr = new wxFileName(Py2wxString(path));
        Py_DECREF(path);
        return sipGetState(sipTransferObj);
    %End


    %ConvertFromTypeCode
        // Convert a wxString to a Python Unicode object.  See wxpy_api.sip
        return wx2PyString(sipCpp->GetFullPath());
    %End
};




