//--------------------------------------------------------------------------
// Name:        variant.sip
// Purpose:     
//
// Author:      Kevin Ollivier
//
// Created:     20-Sept-2011
// Copyright:   (c) 2011 by Kevin Ollivier
// Licence:     wxWindows license
//--------------------------------------------------------------------------

// We always convert wxVariant to / from the native Python types since its purpose
// is basically to allow a variable to be multiple types in C++
%MappedType wxVariant
{
    %TypeCode
    // A wxVariantData class that can hold a PyObject
    class wxVariantDataPyObject : public wxPyUserDataHelper<wxVariantData>
    {
    public:
        explicit wxVariantDataPyObject(PyObject* obj = 0)
            : wxPyUserDataHelper<wxVariantData>(obj) {}
        
        virtual bool Eq(wxVariantData& data) const;
        
        virtual wxString GetType() const { return wxT("PyObject"); }
        wxVariantData* Clone() const { return new wxVariantDataPyObject(BorrowData()); }
    };
    
    bool wxVariantDataPyObject::Eq(wxVariantData& data) const
    {
        wxASSERT_MSG( (data.GetType() == wxT("PyObject")),
                      wxT("wxVariantDataPyObject::Eq: argument mismatch") );
        wxVariantDataPyObject& otherData = (wxVariantDataPyObject&) data;
    
        int result;
        wxPyThreadBlocker blocker;
        PyObject_Cmp(BorrowData(), otherData.BorrowData(), &result);
        return result == 0;
    }
    %End
    
    
    
    %ConvertToTypeCode
        // Code to test a PyObject for compatibility.  
        if (!sipIsErr) {
            // Any type should work since we'll just use the PyObject directly 
            // if the type is not recognized.
            return TRUE;
        }
        
        // Code to create a new wxVariant from the PyObject
        wxVariant* value =  new wxVariant();
        if (PyBytes_Check(sipPy) || PyUnicode_Check(sipPy)) 
            *value = Py2wxString(sipPy);
        else if (wxPyInt_Check(sipPy))
            *value = (long)wxPyInt_AS_LONG(sipPy);
        else if (PyLong_Check(sipPy))
            *value = (long)PyLong_AsLong(sipPy);
        else if (PyBool_Check(sipPy))
            *value = (sipPy == Py_True);
        else if (PyFloat_Check(sipPy))
            *value = PyFloat_AS_DOUBLE(sipPy);
        else if (wxPyWrappedPtr_TypeCheck(sipPy, wxT("wxDateTime"))) {
            wxDateTime* ptr;
            wxPyConvertWrappedPtr(sipPy, (void**)&ptr, wxT("wxDateTime"));
            *value = *ptr;
        }
        else if (wxPyWrappedPtr_TypeCheck(sipPy, wxT("wxBitmap"))) {
            wxBitmap* ptr;
            wxPyConvertWrappedPtr(sipPy, (void**)&ptr, wxT("wxBitmap"));
            *value << *ptr;
        }
        else if (wxPyWrappedPtr_TypeCheck(sipPy, wxT("wxIcon"))) {
            wxIcon* ptr;
            wxPyConvertWrappedPtr(sipPy, (void**)&ptr, wxT("wxIcon"));
            *value <<*ptr;
        }
        else
            *value = new wxVariantDataPyObject(sipPy);
            
        *sipCppPtr = value;
        return sipGetState(sipTransferObj);
    %End

         
    %ConvertFromTypeCode
        // Code to convert a wxVariant to a PyObject.
        PyObject* obj;
        
        if (sipCpp == NULL) {
            obj = Py_None;
        } else {        
            wxVariant& value = *sipCpp;

            if (value.IsType("string"))
                obj = wx2PyString(value.GetString());
            else if (value.IsType("long"))
                obj = PyLong_FromLong(value.GetLong());
            else if (value.IsType("double"))
                obj = PyFloat_FromDouble(value.GetDouble());
            else if (value.IsType("bool"))
                obj = PyBool_FromLong((long)value.GetBool());
            else if ( value.IsType("datetime") )
            {
                wxDateTime val = value.GetDateTime();
                obj = wxPyConstructObject(new wxDateTime(val), wxT("wxDateTime"));
            }
            else if ( value.IsType("wxBitmap") )
            {
                wxBitmap val;
                val << value;
                obj = wxPyConstructObject(new wxBitmap(val), wxT("wxBitmap"));
            }
            else if ( value.IsType("wxIcon") )
            {
                wxIcon val;
                val << value;
                obj = wxPyConstructObject(new wxIcon(val), wxT("wxIcon"));
            }
            else if ( value.IsType("PyObject") )
            {
                wxVariantDataPyObject* data = (wxVariantDataPyObject*)value.GetData();
                obj = data->GetData();
            }
            else
            {
                wxString msg = "Unexpected type (\"" + value.GetType() + "\") in wxVariant.";
                wxPyErr_SetString(PyExc_TypeError, msg.mb_str());
                obj = NULL;
            }                
        }
        return obj;
    %End
    
};

// Used just for unittesting the MappedType code, it can be removed later
%ModuleCode
wxVariant testVariantTypemap(const wxVariant& var)
{
    wxVariant local = var;  // force a copy
    return local;
}
%End
wxVariant testVariantTypemap(const wxVariant& var);
