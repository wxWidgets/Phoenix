//--------------------------------------------------------------------------
// Name:        variant.sip
// Purpose:     MappedType for wxVariant
//
// Author:      Kevin Ollivier, Robin Dunn
//
// Created:     20-Sept-2011
// Copyright:   (c) 2013 by Kevin Ollivier, Robin Dunn
// Licence:     wxWindows license
//--------------------------------------------------------------------------

// We always convert wxVariant to / from the native Python types since its purpose
// is basically to allow a variable to be multiple types in C++
%MappedType wxVariant
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

// Used just for unittesting the MappedType code, it can be removed later
%ModuleCode
wxVariant testVariantTypemap(const wxVariant& var)
{
    wxVariant local = var;  // force a copy
    return local;
}
%End
wxVariant testVariantTypemap(const wxVariant& var);
