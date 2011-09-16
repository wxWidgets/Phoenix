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


    virtual void GetValue( wxVariant &variant,
                   const wxDataViewItem &item, unsigned int col ) const
    {
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
        return false;                                                         
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


    virtual void GetValue( wxVariant &variant,
                   const wxDataViewItem &item, unsigned int col ) const;

/* FIXME: This is how we want to implement the method, but when compiling it always wants
          the void version of this method, even if we add both.
    virtual wxVariant GetValue( wxVariant &variant,
                   const wxDataViewItem &item, unsigned int col ) const;
    %MethodCode
            Py_BEGIN_ALLOW_THREADS
                wxVariant result;
                sipCpp->wxDataViewModel::GetValue(result, item, col);
                sipRes = result;
            Py_END_ALLOW_THREADS
    %End
    %VirtualCatcherCode
            // Convert the 2 element array of integers to the two element
            // tuple.
    
            PyObject *result;
    
            result = sipCallMethod(&sipIsErr, sipMethod, "Oi", item, col);
    
            if (result != NULL)
            {
                // Convert the result to the C++ type.
                sipParseResult(&sipIsErr, sipMethod, result, "i", &sipRes);
    
                Py_DECREF(result);
            }
    %End
*/

    virtual bool SetValue( const wxVariant &variant,
                   const wxDataViewItem &item, unsigned int col );

    virtual bool GetAttr( const wxDataViewItem &item, unsigned int col, wxDataViewItemAttr &attr ) const;

    virtual bool IsEnabled(const wxDataViewItem &item, unsigned int col) const;
    
    virtual unsigned int GetColumnCount() const;
    
    virtual wxString GetColumnType(unsigned int) const;
    
    virtual wxDataViewItem GetParent(const wxDataViewItem&) const;
    
    virtual bool IsContainer(const wxDataViewItem&) const;
};


//--------------------------------------------------------------------------


