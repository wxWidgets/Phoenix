//--------------------------------------------------------------------------
// Name:        treeitemdata.sip
// Purpose:     A MappedType for wxTreeItemData that handles containing 
//              arbitrary PyObjects, dealing with their refcounts, etc.
//
// Author:      Robin Dunn
//
// Created:     28-Mar-2012
// Copyright:   (c) 2012 by Total Control Software
// Licence:     wxWindows license
//--------------------------------------------------------------------------


%ModuleHeaderCode
#include <wx/treebase.h>

// A wxTreeItemData that knows what to do with PyObjects for maintianing the refcount
class wxPyTreeItemData : public wxTreeItemData {
public:
    wxPyTreeItemData(PyObject* obj = NULL) {
        if (obj == NULL)
            obj = Py_None;
        wxPyBLOCK_THREADS( Py_INCREF(obj) );
        m_obj = obj;
    }

    ~wxPyTreeItemData() {
        wxPyBLOCK_THREADS( Py_DECREF(m_obj) );
    }

    PyObject* m_obj;
};    
%End


%MappedType wxTreeItemData
{
    %ConvertToTypeCode
        // Code to test a PyObject for compatibility
        if (!sipIsErr) {
            return TRUE; // any python object is valid
        }
        
        // Code to create a new wxClientData from the PyObject
        wxPyTreeItemData* data =  new wxPyTreeItemData(sipPy);
        *sipCppPtr = data;
        return sipGetState(sipTransferObj);
    %End

         
    %ConvertFromTypeCode
        // Code to convert a wxPyTreeItemData back to the PyObject.
        PyObject* obj;
        if (sipCpp == NULL) {
            obj = Py_None;
        } else {            
            wxPyTreeItemData* data = static_cast<wxPyTreeItemData*>(sipCpp); 
            obj = data->m_obj;
        }
        Py_INCREF(obj);
        return obj;
    %End
    
};
