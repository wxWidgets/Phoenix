//--------------------------------------------------------------------------
// Name:        pyevent.h
// Purpose:     A set of event classes that can be derived from in Python
//              and that preserve their attributes when cloned.
//
// Author:      Robin Dunn
//
// Created:     18-Dec-2010
// Copyright:   (c) 2010-2020 by Total Control Software
// Licence:     wxWindows license
//--------------------------------------------------------------------------

#ifndef PYEVENT_H
#define PYEVENT_H

// The wxPyEvent and wxPyCommandEvent classes can be derived from in Python
// and passed through the event system without losing anything.

// This wxPyEvtDict class holds a Python dictionary object and is used to
// store any attributes that are set from Python code for the wx.PyEvent and
// wx.PyCommandEvent classes. This dictionary is used to make it easy to
// transport those attributes over to the clone when wx needs to make a copy
// of the event instance.

// NOTE: This class is intentionally not exposed to SIP as there is no
// need for it in Python code. Instead we just tell SIP that the __*attr__
// methods are in the event classes. (See wxPyEvent and wxPyCommandEvent
// below and in etg/pyevent.py.)

class wxPyEvtDict
{
public:
    wxPyEvtDict()
    {
        wxPyThreadBlocker blocker;
        m_dict = PyDict_New();
    }

    wxPyEvtDict(const wxPyEvtDict& other)
    {
        wxPyThreadBlocker blocker;
        m_dict = PyDict_Copy(other.m_dict);
    }

    ~wxPyEvtDict()
    {
        wxPyThreadBlocker blocker;
        Py_DECREF(m_dict);
        m_dict = NULL;
    }

    PyObject* _getAttrDict()
    {
        wxPyThreadBlocker blocker;
        Py_INCREF(m_dict);
        return m_dict;
    }

    PyObject* __getattr__(PyObject* name)
    {
        PyObject* value = NULL;
        wxPyThreadBlocker blocker;
        if (PyDict_Contains(m_dict, name)) {
            value = PyDict_GetItem(m_dict, name);
            Py_INCREF(value);
        }
        else {
            PyErr_SetObject(PyExc_AttributeError, name);
        }
        return value;
    }

    void __setattr__(PyObject* name, PyObject* value)
    {
        wxPyThreadBlocker blocker;
        PyDict_SetItem(m_dict, name, value);
    }

    void __delattr__(PyObject* name)
    {
        wxPyThreadBlocker blocker;
        if (PyDict_Contains(m_dict, name))
            PyDict_DelItem(m_dict, name);
        else
            PyErr_SetObject(PyExc_AttributeError, name);
    }

protected:
    PyObject* m_dict;
};


//--------------------------------------------------------------------------


class wxPyEvent : public wxEvent, public wxPyEvtDict
{
    DECLARE_DYNAMIC_CLASS(wxPyEvent)
public:
    wxPyEvent(int id=0, wxEventType eventType = wxEVT_NULL)
        : wxEvent(id, eventType) {}

    // NOTE: The default copy ctor is used here
    virtual wxEvent* Clone() const  { return new wxPyEvent(*this); }
};


//--------------------------------------------------------------------------


class wxPyCommandEvent : public wxCommandEvent, public wxPyEvtDict
{
    DECLARE_DYNAMIC_CLASS(wxPyCommandEvent)
public:
    wxPyCommandEvent(wxEventType eventType = wxEVT_NULL, int id=0)
        : wxCommandEvent(eventType, id) {}

    // NOTE: The default copy ctor is used here
    virtual wxEvent* Clone() const  { return new wxPyCommandEvent(*this); }
};



//--------------------------------------------------------------------------
#endif
