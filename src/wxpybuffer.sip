//--------------------------------------------------------------------------
// Name:        src/wxpybuffer.sip
// Purpose:     A MappedType for wxPyBuffer to automatically convert buffer-
//              compatible objects to a C pointer and length.
//
// Author:      Robin Dunn
//
// Created:     26-Apr-2012
// Copyright:   (c) 2012 by Total Control Software
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
            if (PyObject_CheckBuffer(sipPy))
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
