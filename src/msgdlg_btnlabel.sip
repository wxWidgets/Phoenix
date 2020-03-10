//--------------------------------------------------------------------------
// Name:        msgdlg_btnlabel.sip
// Purpose:     A mapped type to allow auto-converting strings and ints
//              to wxMessageDialog::ButtonLabel
//
// Author:      Robin Dunn
//
// Created:     18-Nov-2017
// Copyright:   (c) 2017-2020 by Total Control Software
// Licence:     wxWindows license
//--------------------------------------------------------------------------

%ModuleHeaderCode
    // Since the attributes of wxMessageDialogBase::ButtonLabel are declared
    // const the implicitly generated copy ctor and assignment operator will
    // cause compilation errors. Since the code generated for MappedTypes
    // expects to be able to copy and assign objects (even though they are not
    // really needed in this case) we need to use this little shim class so
    // there is an explicit copy ctor and assignment operator.

    class wxMessageDialogButtonLabel : public wxMessageDialogBase::ButtonLabel
    {
    public:
        wxMessageDialogButtonLabel()
            : wxMessageDialogBase::ButtonLabel("") {}

        wxMessageDialogButtonLabel(int stockId)
            : wxMessageDialogBase::ButtonLabel(stockId) {}

        wxMessageDialogButtonLabel(const wxString& label)
            : wxMessageDialogBase::ButtonLabel(label) {}

        wxMessageDialogButtonLabel(const char *label)
            : wxMessageDialogBase::ButtonLabel(label) {}

        wxMessageDialogButtonLabel(const wxMessageDialogButtonLabel& other)
            : wxMessageDialogBase::ButtonLabel(other.GetAsString()) {}

        wxMessageDialogButtonLabel& operator=(const wxMessageDialogButtonLabel& other)
            { return *this; }
    };
%End

%MappedType wxMessageDialogButtonLabel
{
    %ConvertToTypeCode
        // Code to test a PyObject for compatibility
        if (!sipIsErr) {
            return (PyBytes_Check(sipPy) || PyUnicode_Check(sipPy) || wxPyInt_Check(sipPy));
        }

        // Code to create a new wxMessageDialogButtonLabel from the PyObject
        wxMessageDialogButtonLabel* label;
        if (PyBytes_Check(sipPy))
            label = new wxMessageDialogButtonLabel(PyBytes_AsString(sipPy));
        else if (PyUnicode_Check(sipPy))
            label = new wxMessageDialogButtonLabel(Py2wxString(sipPy));
        else
            label = new wxMessageDialogButtonLabel(wxPyInt_AsLong(sipPy));

        *sipCppPtr = label;
        return sipGetState(sipTransferObj);
    %End

    %ConvertFromTypeCode
        Py_INCREF(Py_None); return Py_None;
    %End

};
