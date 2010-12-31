//--------------------------------------------------------------------------
// Name:        pyevent.sip
// Purpose:     A set of event classes that can be derived from in Python 
//              and that preserve their attributes when cloned.
//
// Author:      Robin Dunn
//
// Created:     18-Dec-2010
// Copyright:   (c) 2010 by Total Control Software
// Licence:     wxWindows license
//--------------------------------------------------------------------------

// The wxPyEvent and wxPyCommandEvent classes can be derived from in Python
// and passed through the event system without losing anything.

%ModuleHeaderCode
    // This class holds a Python dictionary object and is used to store any
    // attributes that are set from Python code for the wx.PyEvent and
    // wx.PyCommandEvent classes. This dictionary is used to make it easy to
    // transport those attributes over to the clone when wx needs to make a copy
    // of the event instance.
    
    // NOTE: This class is intentionally not exposed to SIP as there is no
    // need for it in Python code. Intead we just tell SIP that the __*attr__
    // methods are in the event classes. (See wxPyEvent and wxPyCommandEvent
    // below.)
    
    class wxPyEvtDict
    {
    public:
        wxPyEvtDict() 
        {
            m_dict = PyDict_New(); 
        }
            
        wxPyEvtDict(const wxPyEvtDict& other)
        {
            m_dict = PyDict_Copy(other.m_dict);
        }
        
        ~wxPyEvtDict()
        {
            wxPyBlock_t blocked = wxPyBeginBlockThreads();
            Py_DECREF(m_dict);
            m_dict = NULL;
            wxPyEndBlockThreads(blocked);
        }

        PyObject* _getAttrDict()
        {
            Py_INCREF(m_dict);
            return m_dict;
        }
        
        PyObject* __getattr__(PyObject* name)
        {
            PyObject* value = NULL;
            wxPyBlock_t blocked = wxPyBeginBlockThreads();
            if (PyDict_Contains(m_dict, name)) {
                value = PyDict_GetItem(m_dict, name);
                Py_INCREF(value);
            }
            else {
                PyErr_SetObject(PyExc_AttributeError, name);
            }
            wxPyEndBlockThreads(blocked);
            return value;
        }
        
        void __setattr__(PyObject* name, PyObject* value)
        {
            wxPyBlock_t blocked = wxPyBeginBlockThreads();
            PyDict_SetItem(m_dict, name, value);
            wxPyEndBlockThreads(blocked);
        }
        
        void __delattr__(PyObject* name)
        {
            wxPyBlock_t blocked = wxPyBeginBlockThreads();
            if (PyDict_Contains(m_dict, name))
                PyDict_DelItem(m_dict, name);
            else 
                PyErr_SetObject(PyExc_AttributeError, name);
            wxPyEndBlockThreads(blocked);
        }
        
    protected:
        PyObject* m_dict;
    };    
%End


//---------------------------------------------------------------------------

class wxPyEvent : wxEvent 
{
%Docstring
wx.PyEvent can be used as a base class for implementing custom event types 
in Python.  You should derive from this class instead of `wx.Event` because 
this class is Python-aware and is able to transport its Python bits safely 
through the wxWidgets event system and have them still be there when the 
event handler is invoked.  Note that since wx.PyEvent is taking care of 
preserving the extra attributes that have been set then you do not need to 
implement the Clone method in your derived classes.

:see: `wx.PyCommandEvent`
%End
    // first declare the C++ version of the class
    %TypeCode
        class wxPyEvent : public wxEvent, public wxPyEvtDict
        {
            DECLARE_DYNAMIC_CLASS(wxPyEvent)
        public:
            wxPyEvent(int id=0, wxEventType eventType = wxEVT_NULL)
                : wxEvent(id, eventType) {}
                
            virtual wxEvent* Clone() const  { return new wxPyEvent(*this); }
        };
        IMPLEMENT_DYNAMIC_CLASS(wxPyEvent, wxEvent);
    %End
    
public:
    wxPyEvent(int id=0, wxEventType eventType = wxEVT_NULL );
    virtual wxEvent* Clone() const /Factory/;
    PyObject* _getAttrDict();
    
    PyObject* __getattr__(PyObject* name);
    %MethodCode
        sipRes = sipCpp->__getattr__(name);
    %End
    
    void __setattr__(PyObject* name, PyObject* value);
    %MethodCode
        sipCpp->__setattr__(name, value);
    %End
    
    void __delattr__(PyObject* name);    
    %MethodCode
        sipCpp->__delattr__(name);
    %End
    
};



class wxPyCommandEvent : wxCommandEvent 
{
%Docstring
wx.PyCommandEvent can be used as a base class for implementing custom event types 
in Python.  You should derive from this class instead of `wx.CommandEvent` because 
this class is Python-aware and is able to transport its Python bits safely 
through the wxWidgets event system and have them still be there when the 
event handler is invoked.  Note that since wx.PyCommandEvent is taking care of 
preserving the extra attributes that have been set then you do not need to 
implement the Clone method in your derived classes.

:see: `wx.PyEvent`
%End
    // first declare the C++ version of the class
    %TypeCode
        class wxPyCommandEvent : public wxCommandEvent, public wxPyEvtDict
        {
            DECLARE_DYNAMIC_CLASS(wxPyCommandEvent)
        public:
            wxPyCommandEvent(wxEventType eventType = wxEVT_NULL, int id=0)
                : wxCommandEvent(eventType, id) {}
                
            virtual wxEvent* Clone() const  { return new wxPyCommandEvent(*this); }
        };
        IMPLEMENT_DYNAMIC_CLASS(wxPyCommandEvent, wxCommandEvent);
    %End
    
public:
    wxPyCommandEvent(wxEventType eventType = wxEVT_NULL, int id=0);
    virtual wxEvent* Clone() const /Factory/;
    PyObject* _getAttrDict();
    
    PyObject* __getattr__(PyObject* name);
    %MethodCode
        sipRes = sipCpp->__getattr__(name);
    %End
    
    void __setattr__(PyObject* name, PyObject* value);
    %MethodCode
        sipCpp->__setattr__(name, value);
    %End
    
    void __delattr__(PyObject* name);    
    %MethodCode
        sipCpp->__delattr__(name);
    %End
};



// TODO: Temporary testing code, get rid of this later
%ModuleCode
wxEvent* testCppClone(wxEvent& evt)
{
    return evt.Clone();
}
%End
wxEvent* testCppClone(wxEvent& evt);


