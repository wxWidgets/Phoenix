//--------------------------------------------------------------------------
// Name:        longlong.sip
// Purpose:     Implements a %MappedType for wxLongLong
//
// Author:      Robin Dunn
//
// Created:     29-Feb-2012
// Copyright:   (c) 2012-2020 by Total Control Software
// Licence:     wxWindows license
//--------------------------------------------------------------------------

typedef long long wxLongLong_t /NoTypeName/;
typedef unsigned long long wxULongLong_t /NoTypeName/;

%MappedType wxLongLong {

    %TypeHeaderCode
    #include <wx/longlong.h>
    %End

    %ConvertToTypeCode
        // Code to test a PyObject for compatibility
        if (!sipIsErr) {
            if (PyNumber_Check(sipPy))
                return TRUE;
            return FALSE;
        }

        // Code to convert from a compatible PyObject
        #if wxUSE_LONGLONG_NATIVE
            *sipCppPtr = new wxLongLong(PyLong_AsLongLong(sipPy));
        #else
            #error TODO. Get the hi/lo 32-bit dwords to construct the wxLongLong
        #endif
        return sipGetState(sipTransferObj);

    %End

    %ConvertFromTypeCode
        #if wxUSE_LONGLONG_NATIVE
            return PyLong_FromLongLong(sipCpp->GetValue());
        #else
            #error This is untested
            // Convert a wxLongLong to a Python Long by getting the hi/lo
            // dwords, then shifting and or-ing them together
            PyObject *hi, *lo, *shifter, *shifted, *result;
            hi = PyLong_FromLong( sipCpp->GetHi() );
            lo = PyLong_FromLong( sipCpp->GetLo() );
            shifter = PyLong_FromLong(32);
            shifted = PyNumber_Lshift(hi, shifter);
            result = PyNumber_Or(shifted, lo);
            Py_DECREF(hi);
            Py_DECREF(lo);
            Py_DECREF(shifter);
            Py_DECREF(shifted);
            return result;
        #endif
    %End
};


%MappedType wxULongLong {

    %TypeHeaderCode
    #include <wx/longlong.h>
    %End

    %ConvertToTypeCode
        // Code to test a PyObject for compatibility
        if (!sipIsErr) {
            if (PyNumber_Check(sipPy))
                return TRUE;
            return FALSE;
        }

        // Code to convert from a compatible PyObject
        #if wxUSE_LONGLONG_NATIVE
            *sipCppPtr = new wxULongLong(PyLong_AsUnsignedLongLong(sipPy));
        #else
            #error TODO. Get the hi/lo 32-bit dwords to construct the wxLongLong
        #endif
        return sipGetState(sipTransferObj);

    %End

    %ConvertFromTypeCode
        #if wxUSE_LONGLONG_NATIVE
            return PyLong_FromUnsignedLongLong(sipCpp->GetValue());
        #else
            #error This needs testing and fixing for unsigned
            // Convert a wxLongLong to a Python Long by getting the hi/lo
            // dwords, then shifting and or-ing them together
            PyObject *hi, *lo, *shifter, *shifted, *result;
            hi = PyLong_FromLong( sipCpp->GetHi() );
            lo = PyLong_FromLong( sipCpp->GetLo() );
            shifter = PyLong_FromLong(32);
            shifted = PyNumber_Lshift(hi, shifter);
            result = PyNumber_Or(shifted, lo);
            Py_DECREF(hi);
            Py_DECREF(lo);
            Py_DECREF(shifter);
            Py_DECREF(shifted);
            return result;
        #endif
    %End
};

