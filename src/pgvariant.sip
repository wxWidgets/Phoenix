//--------------------------------------------------------------------------
// Name:        pgvariant.sip
// Purpose:     MappedType for wxPGVariant
//
// Author:      Robin Dunn
//
// Created:     24-Feb-2017
// Copyright:   (c) 2017-2020 by Total Control Software
// Licence:     wxWindows license
//--------------------------------------------------------------------------

%ModuleHeaderCode
// A wxPGVariant is really the same thing as a wxVariant.  We just create
// this new type so a different %MappedType can be created for it that
// also supports the variant data types that are in the propgrid APIs
// instead of core.
typedef wxVariant wxPGVariant;
typedef wxVariantList wxPGVariantList;

wxVariant wxPGVariant_in_helper(PyObject* source);
PyObject* wxPGVariant_out_helper(const wxVariant& value);
%End


%ModuleCode
wxVariant wxPGVariant_in_helper(PyObject* obj)
{
    wxVariant value;
    int state = 0;
    int isErr = 0;

    // Always check for None first so we don't just get NULL pointers for the
    // other types.
    if (obj == Py_None)
        value.MakeNull();

    else if (wxPyWrappedPtr_TypeCheck(obj, wxT("wxFont"))) {
        wxFont* ptr;
        wxPyConvertWrappedPtr(obj, (void**)&ptr, wxT("wxFont"));
        value << *ptr;
    }

    else if (wxPyWrappedPtr_TypeCheck(obj, wxT("wxPoint"))) {
        wxPoint* ptr;
        wxPyConvertWrappedPtr(obj, (void**)&ptr, wxT("wxPoint"));
        value << *ptr;
    }

    else if (wxPyWrappedPtr_TypeCheck(obj, wxT("wxSize"))) {
        wxSize* ptr;
        wxPyConvertWrappedPtr(obj, (void**)&ptr, wxT("wxSize"));
        value << *ptr;
    }

    else if (wxPyWrappedPtr_TypeCheck(obj, wxT("wxColourPropertyValue"))) {
        wxColourPropertyValue* ptr;
        wxPyConvertWrappedPtr(obj, (void**)&ptr, wxT("wxColourPropertyValue"));
        value << *ptr;
    }

    else if (wxPyCheckNumberSequence(obj)) {
        wxArrayInt* ptr;
        ptr = (wxArrayInt*)sipConvertToType(obj, sipType_wxArrayInt, NULL, 0, &state, &isErr);
        if (!isErr) {
            value << *ptr;
            sipReleaseType(ptr, sipType_wxArrayInt, state);
        }
    }

    else
        value = wxVariant_in_helper(obj);
    return value;
}


PyObject* wxPGVariant_out_helper(const wxVariant& value)
{
    PyObject* obj;


    if (value.IsNull()) {
        obj = Py_None;
        Py_INCREF(obj);
    }

    else if ( value.IsType("wxFont") ) {
        wxFont val;
        val << value;
        obj = wxPyConstructObject(new wxFont(val), "wxFont", true);
    }

    else if ( value.IsType("wxPoint") ) {
        const wxPoint& val = wxPointRefFromVariant(value);
        obj = wxPyConstructObject(new wxPoint(val), "wxPoint", true);
    }

    else if ( value.IsType("wxSize") ) {
        const wxSize& val = wxSizeRefFromVariant(value);
        obj = wxPyConstructObject(new wxSize(val), "wxSize", true);
    }

    else if ( value.IsType("wxColourPropertyValue") ) {
        wxColourPropertyValue val;
         val << value;
        obj = wxPyConstructObject(new wxColourPropertyValue(val), "wxColourPropertyValue", true);
    }

    else if ( value.IsType("wxArrayInt") ) {
        const wxArrayInt& arr = wxArrayIntRefFromVariant(value);
        obj = sipConvertFromType((void*)&arr, sipType_wxArrayInt, NULL);
    }

    else
        obj = wxVariant_out_helper(value);
    return obj;
}
%End



%MappedType wxPGVariant /AllowNone/
{
    %ConvertToTypeCode
        // Code to test a PyObject for compatibility.
        if (!sipIsErr) {
            // Any type should work since we'll just use the PyObject directly
            // if the type is not one that is explicitly supported.
            return TRUE;
        }

        // Code to create a new wxVariant from the PyObject
        wxVariant* value =  new wxVariant(wxPGVariant_in_helper(sipPy));
        *sipCppPtr = value;
        return sipGetState(sipTransferObj);
    %End


    %ConvertFromTypeCode
        // Code to convert a wxVariant to a PyObject.
        if (sipCpp == NULL) {
            return Py_None;
        } else {
            return wxPGVariant_out_helper(*sipCpp);
        }
    %End
};



// Add a typemap for wxVariantList
%MappedType wxPGVariantList
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
            value->Append(new wxVariant(wxPGVariant_in_helper(item)));
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
                PyObject* item = wxPGVariant_out_helper(sipCpp->Item(idx)->GetData());
                PyList_Append(value, item);
            }
            return value;
        }
    %End
};





// Used just for unit testing the MappedType code, it can be removed later
%ModuleCode
wxPGVariant testPGVariantTypemap(const wxPGVariant& var)
{
    wxVariant local = var;  // force a copy
    return local;
}

wxString testPGVariantTypeName(const wxPGVariant& var)
{
    return var.GetType();
}
%End
wxPGVariant testPGVariantTypemap(const wxPGVariant& var);
wxString testPGVariantTypeName(const wxPGVariant& var);
