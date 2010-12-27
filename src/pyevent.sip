/////////////////////////////////////////////////////////////////////////////
// Name:        pyevent.sip
// Purpose:     A set of event classes that can be derived from in Python 
//              and that preserve their attributes when cloned.
//
// Author:      Robin Dunn
//
// Created:     18-Dec-2010
// Copyright:   (c) 2010 by Total Control Software
// Licence:     wxWindows license
/////////////////////////////////////////////////////////////////////////////

// These Event classes can be derived from in Python and passed through the
// event system without loosing anything. They do this by keeping a seaparate
// dictionary for storring any extra attributes set from Python code. When the
// event object is cloned then the clone gets a new reference to the same
// dictionary held by the original object.


//---------------------------------------------------------------------------

// TODO: Use this comment for a docstring

// wx.PyEvent can be used as a base class for implementing custom event
// types in Python.  You should derive from this class instead of
// `wx.Event` because this class is Python-aware and is able to transport
// its Python bits safely through the wxWidgets event system and have
// them still be there when the event handler is invoked.
// :see: `wx.PyCommandEvent`
class wxPyEvent : wxEvent {
    %TypeCode
        class wxPyEvent : public wxEvent
        {
            DECLARE_DYNAMIC_CLASS(wxPyEvent)
            public:
            wxPyEvent(int winid=0, wxEventType commandType = wxEVT_NULL)
                : wxEvent(winid, commandType) {}
                
            // Create a new instance of the Python object for the cloned event, 
            // and then copy the attributes from the original Python instance to 
            // the clone.
            virtual wxEvent* Clone() const
            {
                wxPyEvent* newEvent = new wxPyEvent(*this);
                wxPyBlock_t blocked = wxPyBeginBlockThreads();
                PyObject* thisObj = sipGetPyObject((void*)this, sipType_wxPyEvent);
                PyObject* newObj = sipConvertFromType((void*)newEvent,
                                                      sipType_wxPyEvent,
                                                      NULL); 
                PyObject* newDict = PyObject_GetAttrString(newObj, "__dict__");
                PyObject* thisDict = PyObject_GetAttrString(thisObj, "__dict__");
                PyDict_Update(newDict, thisDict);
                Py_DECREF(newDict);
                Py_DECREF(thisDict);
                wxPyEndBlockThreads(blocked);
                return newEvent;
            }
        };
        IMPLEMENT_DYNAMIC_CLASS(wxPyEvent, wxEvent);
    %End
    
public:
    wxPyEvent(int winid=0, wxEventType eventType = wxEVT_NULL );

    virtual wxEvent* Clone() const /Factory, NoArgParser/;
    %MethodCode
        PyObject *sipParseErr = NULL;
        bool sipSelfWasArg = (!sipSelf || sipIsDerived((sipSimpleWrapper *)sipSelf));
        wxPyEvent *sipCpp;
        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxPyEvent, &sipCpp))
        {
            wxEvent *sipRes;
            sipRes = (sipSelfWasArg ? sipCpp->wxPyEvent::Clone() : sipCpp->Clone());
            // Note that this MethodCode is nearly identical to what is normally generated, 
            // except for the following lines.  wxPyEvent::Clone already made a PyObject, 
            // so just fetch it.
            PyObject* obj = sipGetPyObject(sipRes, sipType_wxPyEvent);
            sipTransferBack(obj);
            return obj;
        }
        sipNoMethod(sipParseErr, sipName_PyEvent, sipName_Clone, NULL); //doc_wxPyEvent_Clone);
        return NULL;
    %End
};



// wx.PyCommandEvent can be used as a base class for implementing custom
// event types in Python, where the event should travel up to parent
// windows looking for a handler.  You should derived from this class
// instead of `wx.CommandEvent` because this class is Python-aware and is
// able to transport its Python bits safely through the wxWidgets event
// system and have them still be there when the event handler is invoked.
// :see: `wx.PyEvent`
class wxPyCommandEvent : wxCommandEvent {
    %TypeCode
        class wxPyCommandEvent : public wxCommandEvent
        {
            DECLARE_DYNAMIC_CLASS(wxPyCommandEvent)
        public:
            wxPyCommandEvent(wxEventType eventType = wxEVT_NULL, int id=0)
                : wxCommandEvent(eventType, id) {}

            // Create a new instance of the Python object for the cloned event, 
            // and then copy the attributes from the original Python instance to 
            // the clone.
            virtual wxEvent* Clone() const
            {
                wxPyCommandEvent* newEvent = new wxPyCommandEvent(*this);
                wxPyBlock_t blocked = wxPyBeginBlockThreads();
                PyObject* thisObj = sipGetPyObject((void*)this, sipType_wxPyCommandEvent);
                PyObject* newObj = sipConvertFromNewType((void*)newEvent,
                                                         sipType_wxPyCommandEvent,
                                                         NULL);
                PyObject* newDict = PyObject_GetAttrString(newObj, "__dict__");
                PyObject* thisDict = PyObject_GetAttrString(thisObj, "__dict__");
                PyDict_Update(newDict, thisDict);
                Py_DECREF(newDict);
                Py_DECREF(thisDict);
                wxPyEndBlockThreads(blocked);
                return newEvent;
            }
        };
        IMPLEMENT_DYNAMIC_CLASS(wxPyCommandEvent, wxCommandEvent);
    %End
    
public:
    wxPyCommandEvent(wxEventType eventType = wxEVT_NULL, int id=0);

    virtual wxEvent* Clone() const /Factory, NoArgParser/;
    %MethodCode
        PyObject *sipParseErr = NULL;
        bool sipSelfWasArg = (!sipSelf || sipIsDerived((sipSimpleWrapper *)sipSelf));
        wxPyCommandEvent *sipCpp;
        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxPyCommandEvent, &sipCpp))
        {
            wxEvent *sipRes;
            sipRes = (sipSelfWasArg ? sipCpp->wxPyCommandEvent::Clone() : sipCpp->Clone());
            // Note that this MethodCode is nearly identical to what is normally generated, 
            // except for the following lines.  wxPyCommandEvent::Clone already made a PyObject, 
            // so just fetch it.
            PyObject* obj = sipGetPyObject(sipRes, sipType_wxPyCommandEvent);
            sipTransferBack(obj);
            return obj;
        }
        sipNoMethod(sipParseErr, sipName_PyCommandEvent, sipName_Clone, NULL); //doc_wxPyEvent_Clone);
        return NULL;
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


