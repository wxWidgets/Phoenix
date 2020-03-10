//--------------------------------------------------------------------------
// Name:        src/arrayholder.h
// Purpose:     A simple template class that can hold and delete a pointer
//              to a C array
//
// Author:      Robin Dunn
//
// Created:     20-Oct-2011
// Copyright:   (c) 2011-2020 by Total Control Software
// Licence:     wxWindows license
//--------------------------------------------------------------------------

#ifndef ARRAYHOLDER_H
#define ARRAYHOLDER_H
// Sometimes we need to hold on to a C array and keep it alive, but typical
// SIP code will treat it as a temporary and delete it as soon as the ctor or
// method call is done. This class can hold a pointer to the array and will
// delete the array in its dtor, and by making this class be wrappable we can
// make a PyObject for it that is then owned by some other object, and
// Python's GC will take care of the delaying the cleanup until it's no longer
// needed.

template <class T>
class wxCArrayHolder
{
public:
    wxCArrayHolder() : m_array(NULL) {}
    ~wxCArrayHolder() {
        delete [] m_array;
        m_array = NULL;
    }
    T* m_array;
};

typedef wxCArrayHolder<int>      wxIntCArrayHolder;
typedef wxCArrayHolder<wxString> wxStringCArrayHolder;
typedef wxCArrayHolder<wxDash>   wxDashCArrayHolder;

#endif
//--------------------------------------------------------------------------
