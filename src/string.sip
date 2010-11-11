/////////////////////////////////////////////////////////////////////////////
// Name:        string.sip
// Purpose:     Implements a %MappedType for wxString
//
// Author:      Robin Dunn
//
// Created:     9-Nov-2010
// Copyright:   (c) 2010 by Total Control Software
// Licence:     wxWindows license
/////////////////////////////////////////////////////////////////////////////


// We don't want the Python user to ever need to deal with wxString, so it
// will be mapped to and from Python UNicode objects using the code snippets
// below.

%MappedType wxString
{
    // Code to test a PyObject for compatibility and to convert from a 
    // PyObject to a wxString
    %ConvertToTypeCode
        // TODO
    %End
    
    // Code to convert a wxString to a PyObject
    %ConvertFromTypeCode
        // TODO
    %End
    
};
