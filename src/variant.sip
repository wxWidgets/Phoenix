//--------------------------------------------------------------------------
// Name:        variant.sip
// Purpose:     MappedType for wxVariant
//
// Author:      Kevin Ollivier, Robin Dunn
//
// Created:     20-Sept-2011
// Copyright:   (c) 2011 by Kevin Ollivier
// Copyright:   (c) 2011-2020 by Total Control Software
// Licence:     wxWindows license
//--------------------------------------------------------------------------

// We always convert wxVariant to / from the native Python types since its purpose
// is basically to allow a variable to be multiple types in C++
%MappedType wxVariant /AllowNone/
{
    %ConvertToTypeCode
        // Code to test a PyObject for compatibility.
        if (!sipIsErr) {
            // Any type should work since we'll just use the PyObject directly
            // if the type is not one that is explicitly supported.
            return TRUE;
        }

        // Code to create a new wxVariant from the PyObject
        wxVariant* value =  new wxVariant(wxVariant_in_helper(sipPy));
        *sipCppPtr = value;
        return sipGetState(sipTransferObj);
    %End


    %ConvertFromTypeCode
        // Code to convert a wxVariant to a PyObject.
        if (sipCpp == NULL) {
            return Py_None;
        } else {
            return wxVariant_out_helper(*sipCpp);
        }
    %End
};




// Add a typemap for wxVariantList
%MappedType wxVariantList
{
    %ConvertToTypeCode
        // Code to test a PyObject for compatibility.
        if (!sipIsErr) {
            // Any type sequence type is okay.
            int success = PySequence_Check(sipPy);
            if (!success)
                PyErr_SetString(PyExc_TypeError, "Sequence type expected.");
            return success;
        }

        // Code to create a new wxVariantList from the PyObject sequence
        wxVariantList* value =  new wxVariantList();
        Py_ssize_t len = PySequence_Length(sipPy);
        Py_ssize_t idx = 0;
        while (idx < len) {
            PyObject* item = PySequence_GetItem(sipPy, idx);
            value->Append(new wxVariant(wxVariant_in_helper(item)));
            Py_DECREF(item);
        }
        *sipCppPtr = value;
        return sipGetState(sipTransferObj);
    %End


    %ConvertFromTypeCode
        // Code to convert a wxVariantList to a Python list.
        if (sipCpp == NULL) {
            return Py_None;
        } else {
            size_t idx = 0;
            PyObject* value = PyList_New(0);
            for (idx=0; idx < sipCpp->GetCount(); idx++) {
                PyObject* item = wxVariant_out_helper(sipCpp->Item(idx)->GetData());
                PyList_Append(value, item);
            }
            return value;
        }
    %End
};




// Used just for unit testing the MappedType code, it can be removed later
%ModuleCode
wxVariant testVariantTypemap(const wxVariant& var)
{
    wxVariant local = var;  // force a copy
    return local;
}

wxString testVariantTypeName(const wxVariant& var)
{
    return var.GetType();
}
%End
wxVariant testVariantTypemap(const wxVariant& var);
wxString testVariantTypeName(const wxVariant& var);
