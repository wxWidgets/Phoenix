//--------------------------------------------------------------------------
// Name:        userdata.sip
// Purpose:
//
// Author:      Kevin Ollivier
//
// Created:     06-Sept-2011
// Copyright:   (c) 2011 by Wide Open Technologies
// Copyright:   (c) 2011-2020 by Total Control Software
// Licence:     wxWindows license
//--------------------------------------------------------------------------


// We'll use the wxPyUserData defined above wherever a wxObject parameter or
// return value is specified in the API.  This MappedType code will convert to/from a
// PyObject so it will be totally transparent to the programmer and from their
// perspective any python object is being stored as the client data.
%MappedType wxPyUserData
{
    %ConvertToTypeCode
        // Code to test a PyObject for compatibility
        if (!sipIsErr) {
            return TRUE; // any python object is valid
        }

        // Code to create a new wxPyUserData from the PyObject
        wxPyUserData* data =  new wxPyUserData(sipPy);
        *sipCppPtr = data;
        return sipGetState(sipTransferObj);
    %End


    %ConvertFromTypeCode
        // Code to convert a wxPyUserData back to the PyObject.
        PyObject* obj;
        obj = wxPyUserData::SafeGetData(static_cast<wxPyUserData*>(sipCpp));
        return obj;
    %End
};

