//--------------------------------------------------------------------------
// Name:        clntdata.sip
// Purpose:
//
// Author:      Robin Dunn
//
// Created:     16-Nov-2010
// Copyright:   (c) 2010-2020 by Total Control Software
// Licence:     wxWindows license
//--------------------------------------------------------------------------


// We'll use the wxPyClientData defined above wherever a wxClientData parameter or
// return value is specified in the API.  This MappedType code will convert to/from a
// PyObject so it will be totally transparent to the programmer and from their
// perspective any python object is being stored as the client data.
%MappedType wxClientData
{
    %ConvertToTypeCode
        // Code to test a PyObject for compatibility
        if (!sipIsErr) {
            return TRUE; // any python object is valid
        }

        // Code to create a new wxClientData from the PyObject
        wxClientData* data =  new wxPyClientData(sipPy);
        *sipCppPtr = data;
        return sipGetState(sipTransferObj);
    %End


    %ConvertFromTypeCode
        // Code to convert a wxClientData back to the PyObject.
        PyObject* obj;
        obj = wxPyClientData::SafeGetData(static_cast<wxPyClientData*>(sipCpp));
        return obj;
    %End

};
