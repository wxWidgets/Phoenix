//--------------------------------------------------------------------------
// Name:        variant.sip
// Purpose:     
//
// Author:      Kevin Ollivier
//
// Created:     20-Sept-2011
// Copyright:   (c) 2011 by Kevin Ollivier
// Licence:     wxWindows license
//--------------------------------------------------------------------------

// We always convert wxVariant to / from the native Python types since its purpose
// is basically to allow a variable to be multiple types in C++
%MappedType wxVariant
{
    %ConvertToTypeCode
        // Code to test a PyObject for compatibility
        if (!sipIsErr) {
            if (PyBytes_Check(sipPy) || PyUnicode_Check(sipPy))
                return TRUE;
            else if (wxPyInt_Check(sipPy) || PyLong_Check(sipPy))
                return TRUE;
            else if (PyBool_Check(sipPy))
                return TRUE;
            else if (PyFloat_Check(sipPy))
                return TRUE;
            
            return FALSE;
        }
        
        // Code to create a new wxPyUserData from the PyObject
        wxVariant* data =  new wxVariant();
        if (PyBytes_Check(sipPy) || PyUnicode_Check(sipPy)) {
            // TODO: Can we just reuse the code in string.sip somehow?
            
            // TODO: check state or iserr?
            int iserr = 0;
            wxString* strPtr = (wxString*)sipConvertToType(sipPy, sipType_wxString, NULL, SIP_NOT_NONE, NULL, &iserr);
            *data = *strPtr;
        }
        else if (wxPyInt_Check(sipPy))
            *data = (long)wxPyInt_AS_LONG(sipPy);
        else if (PyLong_Check(sipPy))
            *data = (long)PyLong_AsLong(sipPy);
        else if (PyBool_Check(sipPy)) {
            if (sipPy == Py_True)
                *data = true;
            else
                *data = false;
        }
        else if (PyFloat_Check(sipPy))
            *data = PyFloat_AS_DOUBLE(sipPy);
        *sipCppPtr = data;
        return sipGetState(sipTransferObj);
    %End

         
    %ConvertFromTypeCode
        // Code to convert a wxClientData back to the PyObject.
        PyObject* obj;
        
        if (sipCpp == NULL) {
            obj = Py_None;
        } else {            
            if (sipCpp->GetType() == "string")
                obj = PyUnicode_FromWideChar(sipCpp->GetString().wc_str(), sipCpp->GetString().length());
            else if (sipCpp->GetType() == "long")
                obj = PyLong_FromLong(sipCpp->GetLong());
            else if (sipCpp->GetType() == "double")
                obj = PyFloat_FromDouble(sipCpp->GetDouble());
            else if (sipCpp->GetType() == "bool")
                obj = PyBool_FromLong((long)sipCpp->GetBool());
        }
        return obj;
    %End
    
};

// Used just for unittesting the MappedType code, it can be removed later
%ModuleCode
wxVariant testVariantTypemap(const wxVariant& arr)
{
    wxVariant local = arr;  // force a copy
    return local;
}
%End
wxVariant testVariantTypemap(const wxVariant& arr);
