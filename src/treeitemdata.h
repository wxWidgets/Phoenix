//--------------------------------------------------------------------------
// Name:        treeitemdata.h
// Purpose:     This class is used to associate a PyObject with a tree item.
//
// Author:      Robin Dunn
//
// Created:     26-Mar-2012
// Copyright:   (c) 2012 by Total Control Software
// Licence:     wxWindows license
//--------------------------------------------------------------------------

#ifndef TREEITEMDATA_H
#define TREEITEMDATA_H

#include <wx/treebase.h>

// A wxTreeItemData that knows what to do with PyObjects for maintianing the refcount
class TreeItemData : public wxTreeItemData {
public:
    TreeItemData(PyObject* obj = NULL) {
        if (obj == NULL)
            obj = Py_None;
        wxPyBLOCK_THREADS( Py_INCREF(obj) );
        m_obj = obj;
    }

    ~TreeItemData() {
        wxPyBLOCK_THREADS( Py_DECREF(m_obj) );
    }

    PyObject* GetData() {
        wxPyBLOCK_THREADS( Py_INCREF(m_obj) );
        return m_obj;
    }

    void SetData(PyObject* obj) {
        wxPyBlock_t blocked = wxPyBeginBlockThreads();
        Py_DECREF(m_obj);
        m_obj = obj;
        Py_INCREF(obj);
        wxPyEndBlockThreads(blocked);
    }
    
private:
    PyObject* m_obj;
};    

#endif
