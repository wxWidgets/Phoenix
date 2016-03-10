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
// Copyright:   (c) 2016 by Total Control Software
// Licence:     wxWindows license
//--------------------------------------------------------------------------


// size_t will either be equivallent to an unsigned long, or to an 
// unsigned long long. wxWidgets' configure script has already figured out 
// which it is, so we can make it conditional on those results.

%MappedType size_t {

    %TypeHeaderCode
    #include <wx/setup.h>
    %End

    %ConvertToTypeCode
        // Allow conversions from any number type
        if (!sipIsErr) {
            if (PyNumber_Check(sipPy))
                return TRUE;
            return FALSE;
        }

        // Do the conversion
        #if wxSIZE_T_IS_ULONG
            *sipCppPtr = new size_t(PyLong_AsUnsignedLong(sipPy));
        #else
            *sipCppPtr = new size_t(PyLong_AsUnsignedLongLong(sipPy));
        #endif
        return sipGetState(sipTransferObj);
    %End

    %ConvertFromTypeCode
        #if wxSIZE_T_IS_ULONG
            return PyLong_FromUnsignedLong(*sipCpp);
        #else
            return PyLong_FromUnsignedLongLong(*sipCpp);
        #endif
    %End
};


// This type is a signed integer value that is large enough to hold a 
// pointer.  Again we'll use the results of wxWidgets configuration.
%MappedType wxIntPtr {

    %TypeHeaderCode
    #include <wx/setup.h>
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
            *sipCppPtr = new wxIntPtr(PyLong_AsLong(sipPy));
        #else
            *sipCppPtr = new wxIntPtr(PyLong_AsLongLong(sipPy));
        #endif
        return sipGetState(sipTransferObj);
    %End

    %ConvertFromTypeCode
        #if SIZEOF_LONG >= SIZEOF_VOID_P
            return PyLong_FromLong(*sipCpp);
        #else
            return PyLong_FromLongLong(*sipCpp);
        #endif
    %End
};


// This type is an unsigned integer value that is large enough to hold a 
// pointer.  Again we'll use the results of wxWidgets configuration.
%MappedType wxUIntPtr {

    %TypeHeaderCode
    #include <wx/setup.h>
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
            *sipCppPtr = new wxUIntPtr(PyLong_AsUnsignedLong(sipPy));
        #else
            *sipCppPtr = new wxUIntPtr(PyLong_AsUnsignedLongLong(sipPy));
        #endif
        return sipGetState(sipTransferObj);
    %End

    %ConvertFromTypeCode
        #if SIZEOF_LONG >= SIZEOF_VOID_P
            return PyLong_FromUnsignedLong(*sipCpp);
        #else
            return PyLong_FromUnsignedLongLong(*sipCpp);
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




