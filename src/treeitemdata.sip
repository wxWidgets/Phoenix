//--------------------------------------------------------------------------
// Name:        treeitemdata.sip
// Purpose:     A MappedType for wxTreeItemData that handles containing
//              arbitrary PyObjects, dealing with their refcounts, etc.
//
// Author:      Robin Dunn
//
// Created:     28-Mar-2012
// Copyright:   (c) 2012-2020 by Total Control Software
// Licence:     wxWindows license
//--------------------------------------------------------------------------


%ModuleHeaderCode
#include <wx/treebase.h>

// A wxTreeItemData that knows what to do with PyObjects for maintaining the refcount
class wxPyTreeItemData : public wxPyUserDataHelper<wxTreeItemData>
{
public:
    wxPyTreeItemData(PyObject* obj = NULL)
        : wxPyUserDataHelper<wxTreeItemData>(obj)
    { }
};

%End


%MappedType wxTreeItemData
{
    %ConvertToTypeCode
        // Code to test a PyObject for compatibility
        if (!sipIsErr) {
            return TRUE; // any python object is valid
        }

        // Code to create a new wxTreeItemData from the PyObject
        wxPyTreeItemData* data =  new wxPyTreeItemData(sipPy);
        *sipCppPtr = data;
        return sipGetState(sipTransferObj);
    %End


    %ConvertFromTypeCode
        // Code to convert a wxPyTreeItemData back to the PyObject.
        PyObject* obj;
        obj = wxPyTreeItemData::SafeGetData(static_cast<wxPyTreeItemData*>(sipCpp));
        return obj;
    %End

};
