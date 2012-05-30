//--------------------------------------------------------------------------
// Name:        userdata.sip
// Purpose:     
//
// Author:      Kevin Ollivier
//
// Created:     06-Sept-2011
// Copyright:   (c) 2011 by Wide Open Technologies
// Licence:     wxWindows license
//--------------------------------------------------------------------------


%ModuleHeaderCode
    // A wxPyUserData object that holds a reference to a Python object
    class wxPyUserData : public wxObject 
    {
    public:
        wxPyUserData() : wxObject()
        {
            m_obj = NULL;
            m_incRef = false;
        }
        
        wxPyUserData(PyObject* obj, bool incref=true) 
        : wxObject()
        {
            m_obj = obj;
            m_incRef = incref;
            if (incref) {
                wxPyBLOCK_THREADS( Py_INCREF(m_obj) );
            }
        }
        virtual ~wxPyUserData() 
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
        if (sipCpp == NULL) {
            obj = Py_None;
        } else {            
            wxPyUserData* data = static_cast<wxPyUserData*>(sipCpp);  // TODO: verify pointer type?
            obj = data->m_obj;
        }
        Py_INCREF(obj);
        return obj;
    %End
};


// NOTE TO SELF: It looks like the GIL is already held by the current thread
// in ConvertToTypeCode and ConvertFromTypeCode code blocks...
