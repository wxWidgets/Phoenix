//--------------------------------------------------------------------------
// Name:        clntdata.sip
// Purpose:     
//
// Author:      Robin Dunn
//
// Created:     16-Nov-2010
// Copyright:   (c) 2010 by Total Control Software
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
            if (incref)
                Py_INCREF(m_obj);
        }
        ~wxPyClientData() 
        {
            if (m_incRef) {
                //wxPyBlock_t blocked = wxPyBeginBlockThreads();
                Py_DECREF(m_obj);
                //wxPyEndBlockThreads(blocked);
            }
            m_obj = NULL;
        }
        PyObject* m_obj;
        bool      m_incRef;
    };
 
%End


// TODO: Can we just use a MappedType for wxClientData instead of writing
// CppMethods where it needs to be used?
