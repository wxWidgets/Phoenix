//--------------------------------------------------------------------------
// Name:        pgattributestorage.sip
// Purpose:     MappedType for wxPGAttributeStorage
//
// Author:      Robin Dunn
//
// Created:     11-March-2017
// Copyright:   (c) 2017 by Total Control Software
// Licence:     wxWindows license
//--------------------------------------------------------------------------



%MappedType wxPGAttributeStorage
{
    %ConvertToTypeCode
        // Code to test a PyObject for compatibility.
        if (!sipIsErr) {
            // Currently this is output only, so just reject everything
            return FALSE;
        }

        // Code to create a new wxVariant from the PyObject
        // ...
        return sipGetState(sipTransferObj);
    %End


    %ConvertFromTypeCode
        // Code to convert to a PyObject.
        wxPGAttributeStorage::const_iterator it = sipCpp->StartIteration();
        wxVariant v;

        PyObject* dict = PyDict_New();
        if ( !dict ) return dict;

        while ( sipCpp->GetNext( it, v ) ) {
            const wxString& name = v.GetName();
            PyObject* pyStr = wx2PyString(name);
            PyObject* pyVal = wxPGVariant_out_helper(v);
            int res = PyDict_SetItem( dict, pyStr, pyVal );
        }
        return dict;
    %End
};

