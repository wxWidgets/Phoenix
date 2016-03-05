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
        // Code to test an incoming PyObject for compatibility
        if (!sipIsErr) {
            if (PyNumber_Check(sipPy))
                return TRUE;
            return FALSE;
        }

        // Code to convert from a compatible PyObject
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


// TODO: Do the same for wxIntPtr and wxUIntPtr?


// Used just for testing the MappedType code
//%ModuleCode
//size_t test_size_t(size_t value)
//{
//    size_t local = value;
//    return local;
//}
//
//void printIntSizes()
//{
//    printf("**** sizeof(int):          %d\n", sizeof(int));
//    printf("**** sizeof(long):         %d\n", sizeof(long));
//    printf("**** sizeof(long long):    %d\n", sizeof(long long));
//
//    printf("**** sizeof(size_t):       %d\n", sizeof(size_t));
//    printf("**** sizeof(time_t):       %d\n", sizeof(time_t));
//    
//    printf("**** sizeof(wxIntPtr):     %d\n", sizeof(wxIntPtr));
//    printf("**** sizeof(wxUIntPtr):    %d\n", sizeof(wxUIntPtr));
//    printf("**** sizeof(wxFileOffset): %d\n", sizeof(wxFileOffset));
//    
//}    
//%End
//
//size_t test_size_t(size_t value);
//void printIntSizes();




