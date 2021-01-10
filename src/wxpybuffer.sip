//--------------------------------------------------------------------------
// Name:        src/wxpybuffer.sip
// Purpose:     A MappedType for wxPyBuffer to automatically convert buffer-
//              compatible objects to a C pointer and length.
//
//              Also MappedTypes for wxMemoryBuffer and wxCharBuffer
//
// Author:      Robin Dunn
//
// Created:     26-Apr-2012
// Copyright:   (c) 2012-2020 by Total Control Software
// Licence:     wxWindows license
//--------------------------------------------------------------------------


%ModuleHeaderCode
#include "wxpybuffer.h"
%End


%MappedType wxPyBuffer
{
    %ConvertToTypeCode
        // Code to test a PyObject for compatibility
        if (!sipIsErr) {
            if (PyObject_CheckBuffer(sipPy)              // New buffer interface
                #if PY_MAJOR_VERSION < 3
                    || PyObject_CheckReadBuffer(sipPy)   // or old buffer interface
                #endif
                )
                return TRUE;
            return FALSE;
        }

        // Code to create a new wxPyBuffer from the PyObject
        wxPyBuffer* buf =  new wxPyBuffer();
        buf->create(sipPy);
        *sipCppPtr = buf;
        return sipGetState(sipTransferObj);
    %End


    // This isn't being used anywhere yet, but it should work.
    %ConvertFromTypeCode
        return wxPyMakeBuffer(sipCpp->m_ptr, sipCpp->m_len);
    %End
};


//--------------------------------------------------------------------------
// The wxMemoryBuffer class can be mapped to/from Python buffer objects
// similarly, and we'll use a wxPyBuffer to help out.

%ModuleHeaderCode
#include <wx/buffer.h>
%End


%MappedType wxMemoryBuffer
{
    %ConvertToTypeCode
        // Code to test a PyObject for compatibility
        if (!sipIsErr) {
            if (PyObject_CheckBuffer(sipPy))
                return TRUE;
            return FALSE;
        }

        // Code to create a new wxMemoryBuffer from the PyObject
        wxPyBuffer pybuf;
        pybuf.create(sipPy);
        wxMemoryBuffer* buf = new wxMemoryBuffer(pybuf.m_len);
        buf->AppendData(pybuf.m_ptr, pybuf.m_len);
        *sipCppPtr = buf;
        return sipGetState(sipTransferObj);
    %End


    // Code to convert a wxMemoryBuffer to a Python object
    %ConvertFromTypeCode
        return wxPyMakeBuffer(sipCpp->GetData(), sipCpp->GetDataLen());
    %End
};

//--------------------------------------------------------------------------
// wxCharBuffers will be converted to/from bytes objects

%MappedType wxCharBuffer
{
    %ConvertToTypeCode
        // Code to test a PyObject for compatibility
        if (!sipIsErr) {
            if (PyBytes_Check(sipPy))
                return TRUE;
            return FALSE;
        }

        // Code to create a new wxCharBuffer from the PyObject
        char* bbuf;
        Py_ssize_t blen;
        PyBytes_AsStringAndSize(sipPy, &bbuf, &blen);
        wxCharBuffer* cbuf = new wxCharBuffer(blen);
        memcpy(cbuf->data(), bbuf, blen);
        *sipCppPtr = cbuf;
        return sipGetState(sipTransferObj);
    %End


    // Code to convert a wxCharBuffer to a Python object
    %ConvertFromTypeCode
        return PyBytes_FromStringAndSize(sipCpp->data(), sipCpp->length());
    %End
};


//--------------------------------------------------------------------------
