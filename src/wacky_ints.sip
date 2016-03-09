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


// TODO: Do the same for wxIntPtr and wxUIntPtr as above?

typedef long long wxIntPtr;
typedef unsigned long long wxUIntPtr;



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




