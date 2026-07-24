
%ModuleHeaderCode

#include <wxPython/wxpy_api.h>
#include <wx/aui/tabart.h>

#if defined(__WXUNIVERSAL__) || !defined(__WXGTK__) || defined(__WXGTK3__)
class wxAuiGtkTabArt : public wxAuiGenericTabArt
{
public:
    wxAuiGtkTabArt() { wxPyRaiseNotImplemented(); }
};
#endif

#if defined(__WXUNIVERSAL__) || !defined(__WXMSW__)
class wxAuiMSWTabArt : public wxAuiGenericTabArt
{
public:
    wxAuiMSWTabArt() { wxPyRaiseNotImplemented(); }
};
#endif


#ifdef wxHAS_NATIVE_TABART
#undef wxHAS_NATIVE_TABART
#define wxHAS_NATIVE_TABART 1
#else
const int wxHAS_NATIVE_TABART = 0;
#endif

%End

class wxAuiGtkTabArt : wxAuiGenericTabArt
{
    %Docstring
        wxAuiGtkTabArt() -> None
        
        An art provider for wxAuiNotebook with native GTK2 controls.
    %End
    %TypeHeaderCode
        #include <wx/aui/tabart.h>
    %End
public:
    wxAuiGtkTabArt();
};  // end of class wxAuiGtkTabArt



class wxAuiMSWTabArt : wxAuiGenericTabArt
{
    %Docstring
        wxAuiMSWTabArt() -> None
        
        An art provider for wxAuiNotebook with native MSW controls.
    %End
    %TypeHeaderCode
        #include <wx/aui/tabart.h>
    %End
public:
    wxAuiMSWTabArt();
};  // end of class wxAuiMSWTabArt

const int wxHAS_NATIVE_TABART;
