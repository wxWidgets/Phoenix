//--------------------------------------------------------------------------
// Name:        dvcvariant.sip
// Purpose:     MappedType for wxDVCVariant
//
// Author:      Robin Dunn
//
// Created:     9-Nov-2012
// Copyright:   (c) 2012-2020 by Total Control Software
// Licence:     wxWindows license
//--------------------------------------------------------------------------

%ModuleHeaderCode
// A wxDVCVariant is really the same thing as a wxVariant.  We just create
// this new type so a different %MappedType can be created for it that also
// knows how to put DVC types in and out of a variant.
typedef wxVariant wxDVCVariant;

wxVariant wxDVCVariant_in_helper(PyObject* source);
PyObject* wxDVCVariant_out_helper(const wxVariant& value);

#include <wx/vector.h>
typedef wxVector<wxVariant> wxVariantVector;
%End


%ModuleCode
wxVariant wxDVCVariant_in_helper(PyObject* source)
{
    wxVariant ret;

    if (source == Py_None) {
        ret.MakeNull();
    }
    else if (wxPyWrappedPtr_TypeCheck(source, wxT("wxDataViewCheckIconText"))) {
        wxDataViewCheckIconText* ptr;
        wxPyConvertWrappedPtr(source, (void**)&ptr, wxT("wxDataViewCheckIconText"));
        ret << *ptr;
    }
    else if (wxPyWrappedPtr_TypeCheck(source, wxT("wxDataViewIconText"))) {
        wxDataViewIconText* ptr;
        wxPyConvertWrappedPtr(source, (void**)&ptr, wxT("wxDataViewIconText"));
        ret << *ptr;
    }
    else
        ret = wxVariant_in_helper(source);
    return ret;
}


PyObject* wxDVCVariant_out_helper(const wxVariant& value)
{
    PyObject* ret;
    if (value.IsType("wxDataViewCheckIconText") )
    {
        wxDataViewCheckIconText val;
        val << value;
        ret = wxPyConstructObject(new wxDataViewCheckIconText(val), wxT("wxDataViewCheckIconText"), 0);
    }
    else if ( value.IsType("wxDataViewIconText") )
    {
        wxDataViewIconText val;
        val << value;
        ret = wxPyConstructObject(new wxDataViewIconText(val), wxT("wxDataViewIconText"), 0);
    }
    else
        ret = wxVariant_out_helper(value);
    return ret;
}
%End



%MappedType wxDVCVariant /AllowNone/
{
    %ConvertToTypeCode
        // Code to test a PyObject for compatibility.
        if (!sipIsErr) {
            // Any type should work since we'll just use the PyObject directly
            // if the type is not one that is explicitly supported.
            return TRUE;
        }

        // Code to create a new wxVariant from the PyObject
        wxVariant* value =  new wxVariant(wxDVCVariant_in_helper(sipPy));
        *sipCppPtr = value;
        return sipGetState(sipTransferObj);
    %End


    %ConvertFromTypeCode
        // Code to convert a wxVariant to a PyObject.
        if (sipCpp == NULL) {
            return Py_None;
        } else {
            return wxDVCVariant_out_helper(*sipCpp);
        }
    %End
};



// Some DVC classes also make use of a wxVector<wxVariant> type.  This code
// will convert Python sequences to that type.
%MappedType wxVariantVector
{
    %ConvertToTypeCode
        if (!sipIsErr) {
            // We expect a sequence
            return PySequence_Check(sipPy);
        }

        wxVariantVector* vector = new wxVariantVector;
        Py_ssize_t size = PySequence_Length(sipPy);
        Py_ssize_t idx;
        for (idx=0; idx<size; idx+=1) {
            PyObject* item = PySequence_GetItem(sipPy, idx);
            vector->push_back( wxDVCVariant_in_helper(item) );
            Py_DECREF(item);
        }

        *sipCppPtr = vector;
        return sipGetState(sipTransferObj);
    %End


    %ConvertFromTypeCode
         // no C++ --> Python convert needed yet...
         return NULL;
    %End
};



