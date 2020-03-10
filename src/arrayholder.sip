//--------------------------------------------------------------------------
// Name:        arrayholder.sip
// Purpose:
//
// Author:      Robin Dunn
//
// Created:     14-March-2012
// Copyright:   (c) 2012-2020 by Total Control Software
// Licence:     wxWindows license
//--------------------------------------------------------------------------

// Sometimes we need to hold on to a C array and keep it alive, but typical
// SIP code will treat it as a temporary and delete it as soon as the ctor or
// method call is done. This class can hold a pointer to the array and will
// delete the array in its dtor, and by making this class be wrappable we can
// make a PyObject for it that is then owned by some other object, and
// Python's GC will take care of the delaying the cleanup until it's no longer
// needed.
template <Type>
class wxCArrayHolder
{
%TypeHeaderCode
#include "arrayholder.h"
%End

public:
    wxCArrayHolder();
    ~wxCArrayHolder();

private:
    wxCArrayHolder(const wxCArrayHolder<Type>&);  // no copies
    wxCArrayHolder& operator=(wxCArrayHolder<Type>); // no assignment
};

typedef wxCArrayHolder<int>      wxIntCArrayHolder;
typedef wxCArrayHolder<wxString> wxStringCArrayHolder;
typedef wxCArrayHolder<wxDash>   wxDashCArrayHolder;

//--------------------------------------------------------------------------
