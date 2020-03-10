//--------------------------------------------------------------------------
// Name: wacky_ints.sip
//
// Purpose: Implements a %MappedType for size_t and others in order to
//          deal with different sizeof's on different platforms. They're
//          32bit on some, 64bit on others.
//
// Author:      Robin Dunn
//
// Created:     4-March-2016
// Copyright:   (c) 2016-2020 by Total Control Software
// Licence:     wxWindows license
//--------------------------------------------------------------------------


// This type is a signed integer value that is large enough to hold a
// pointer.  Again we'll use the results of wxWidgets configuration.
%MappedType wxIntPtr {

    %TypeHeaderCode
    #include <wx/setup.h>
    #include <wxPython/wxpy_api.h>
    %End

    %ConvertToTypeCode
        // Allow conversions from any number type
        if (!sipIsErr) {
            if (PyNumber_Check(sipPy))
                return TRUE;
            return FALSE;
        }

        // Do the conversion
        #if SIZEOF_LONG >= SIZEOF_VOID_P
            *sipCppPtr = new wxIntPtr(wxPyInt_AsLong(sipPy));
        #else
            *sipCppPtr = new wxIntPtr(wxPyInt_AsSsize_t(sipPy));
        #endif
        return sipGetState(sipTransferObj);
    %End

    %ConvertFromTypeCode
        #if SIZEOF_LONG >= SIZEOF_VOID_P
            return wxPyInt_FromLong(*sipCpp);
        #else
            return wxPyInt_FromSsize_t(*sipCpp);
        #endif
    %End
};


// This type is an unsigned integer value that is large enough to hold a
// pointer.  Again we'll use the results of wxWidgets configuration.
%MappedType wxUIntPtr {

    %TypeHeaderCode
    #include <wx/setup.h>
    #include <wxPython/wxpy_api.h>
    %End

    %ConvertToTypeCode
        // Allow conversions from any number type
        if (!sipIsErr) {
            if (PyNumber_Check(sipPy))
                return TRUE;
            return FALSE;
        }

        // Do the conversion
        #if SIZEOF_LONG >= SIZEOF_VOID_P
            *sipCppPtr = new wxUIntPtr(wxPyInt_AsUnsignedLong(sipPy));
        #else
            *sipCppPtr = new wxUIntPtr(wxPyInt_AsSize_t(sipPy));
        #endif
        return sipGetState(sipTransferObj);
    %End

    %ConvertFromTypeCode
        #if SIZEOF_LONG >= SIZEOF_VOID_P
            return wxPyInt_FromUnsignedLong(*sipCpp);
        #else
            return wxPyInt_FromSize_t(*sipCpp);
        #endif
    %End
};




// Used just for testing the MappedTypes
%ModuleCode
size_t testSizetTypemap(size_t value)
{
    size_t local = value;
    return local;
}

wxIntPtr testIntPtrTypemap(wxIntPtr value)
{
    wxIntPtr local = value;
    return local;
}

wxUIntPtr testUIntPtrTypemap(wxUIntPtr value)
{
    wxUIntPtr local = value;
    return local;
}
%End

size_t testSizetTypemap(size_t value);
wxIntPtr testIntPtrTypemap(wxIntPtr value);
wxUIntPtr testUIntPtrTypemap(wxUIntPtr value);




