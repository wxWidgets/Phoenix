//--------------------------------------------------------------------------
// Name:        src/dataviewhelpers.sip
// Purpose:     Implements a %MappedType for wxArrayString and wxArrayInt
//
// Author:      Kevin Ollivier
//
// Created:     13-Sept-2011
// Copyright:   (c) 2011 by Kevin Ollivier
// Licence:     wxWindows license
//--------------------------------------------------------------------------


//--------------------------------------------------------------------------

// Create a C++ class for the Py version
%ModuleHeaderCode
#include <wx/dataview.h>

class wxPyDataViewModelBase: public wxDataViewModel
{
public:
    wxPyDataViewModelBase() {}
    
    virtual unsigned int GetChildren (const wxDataViewItem &item, wxDataViewItemArray &children) const
    {
        return 0;
    }

    virtual int Compare (const wxDataViewItem &item1, const wxDataViewItem &item2, unsigned int column, bool ascending) const
    {
        return 0;
    }

    void GetValue( wxVariant &variant,
                   const wxDataViewItem &item, unsigned int col ) const
    {
        variant = GetValue(item, col);
    }

    virtual wxVariant GetValue( const wxDataViewItem &item, unsigned int col ) const
    {
        return wxVariant();
    }

    virtual bool SetValue( const wxVariant &variant,
                   const wxDataViewItem &item, unsigned int col )
    {
        return false;
    }

    virtual bool GetAttr( const wxDataViewItem &item, unsigned int col, wxDataViewItemAttr &attr ) const
    {
        return false;
    }

    virtual bool IsEnabled(const wxDataViewItem &item, unsigned int col) const
    {
        return true;                                                        
    }

    virtual unsigned int GetColumnCount() const
    {
        return 0;
    }
    
    virtual wxString GetColumnType(unsigned int) const
    {
        return wxEmptyString;
    }
    
    virtual wxDataViewItem GetParent(const wxDataViewItem&) const
    {
        return wxDataViewItem();
    }
    
    virtual bool IsContainer(const wxDataViewItem&) const
    {
        return false;
    }
};
%End

class wxPyDataViewModelBase: wxDataViewModel
{
public:
    wxPyDataViewModelBase();
    
    virtual unsigned int GetChildren (const wxDataViewItem &item, wxDataViewItemArray &children) const;

    virtual int Compare (const wxDataViewItem &item1, const wxDataViewItem &item2, unsigned int column, bool ascending) const;

    virtual wxVariant GetValue( const wxDataViewItem &item, unsigned int col ) const;

    void GetValue( wxVariant &variant,
                   const wxDataViewItem &item, unsigned int col ) const;
    %MethodCode
            Py_BEGIN_ALLOW_THREADS
                // call the version that returns a variant so that it will call the Python callback
                *variant = sipCpp->GetValue(*item, col);
            Py_END_ALLOW_THREADS
    %End

    virtual bool SetValue( const wxVariant &variant,
                   const wxDataViewItem &item, unsigned int col );

    virtual bool GetAttr( const wxDataViewItem &item, unsigned int col, wxDataViewItemAttr &attr ) const;

    virtual bool IsEnabled(const wxDataViewItem &item, unsigned int col) const;
    
    virtual unsigned int GetColumnCount() const;
    
    virtual wxString GetColumnType(unsigned int) const;
    
    virtual wxDataViewItem GetParent(const wxDataViewItem&) const;
    
    virtual bool IsContainer(const wxDataViewItem&) const;
};

/*
%MappedType wxPyLongPtr
{
    %ConvertToTypeCode
        // Code to test a PyObject for compatibility
        if (!sipIsErr) {
            return PyLong_Check(sipPy) || PyInt_Check(sipPy); 
        }
        if (PyLong_Check(sipPy) || PyInt_Check(sipPy))
            *sipCppPtrV = (wxPyLongPtr)PyLong_AsVoidPtr(sipPy);
        
        return sipGetState(sipTransferObj);
    %End

         
    %ConvertFromTypeCode
        return PyLong_FromVoidPtr(sipCpp);
    %End
    
};
*/

//--------------------------------------------------------------------------


