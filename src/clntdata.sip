//--------------------------------------------------------------------------
// Name:        clntdata.sip
// Purpose:     
//
// Author:      Robin Dunn
//
// Created:     16-Nov-2010
// Copyright:   (c) 2011 by Total Control Software
// Licence:     wxWindows license
//--------------------------------------------------------------------------


%ModuleHeaderCode
    // A wxClientData that holds a reference to a Python object
    class wxPyClientData : public wxClientData 
    {
    public:
        wxPyClientData(PyObject* obj, bool incref=true) 
        {
            m_obj = obj;
            m_incRef = incref;
            if (incref) {
                wxPyBLOCK_THREADS( Py_INCREF(m_obj) );
                }
        }
        ~wxPyClientData() 
        {
            if (m_incRef) {
                wxPyBLOCK_THREADS( Py_DECREF(m_obj) );
            }
            m_obj = NULL;
        }
        PyObject* m_obj;
        bool      m_incRef;
    };
 
%End


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
        if (sipCpp == NULL) {
            obj = Py_None;
        } else {            
            wxPyClientData* data = static_cast<wxPyClientData*>(sipCpp);  // TODO: verify poitner type?
            obj = data->m_obj;
        }
        Py_INCREF(obj);
        return obj;
    %End
    
};
