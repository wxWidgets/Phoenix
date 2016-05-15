//--------------------------------------------------------------------------
// Name:        src/axbase.sip
// Purpose:     A wxWindow class and wrapper interface that virtualizes
// MSWTranslateMessage for use in ActiveX Controls. See _axbase in Classic
//
// Author:      Robin Dunn
//
// Created:     13-May-2016
// Copyright:   (c) 2016 by Total Control Software
// Licence:     wxWindows license
//--------------------------------------------------------------------------


%ModuleHeaderCode
class wxPyAxBaseWindow : public wxWindow
{
    DECLARE_DYNAMIC_CLASS(wxPyAxBaseWindow)

public:
    wxPyAxBaseWindow(wxWindow* parent, const wxWindowID id=-1,
                    const wxPoint& pos = wxDefaultPosition,
                    const wxSize& size = wxDefaultSize,
                    long style = 0,
                    const wxString& name = wxPanelNameStr)
    : wxWindow(parent, id, pos, size, style, name) {}

    wxPyAxBaseWindow() : wxWindow() {}

    virtual bool MSWTranslateMessage(WXMSG* msg)
    {
        return wxWindow::MSWTranslateMessage(msg);
    }
};

wxPyAxBaseWindow* wxPyAxBaseWindow_FromHWND(wxWindow* parent, unsigned long _hWnd);
%End

//--------------------------------------------------------------------------


%ModuleCode
IMPLEMENT_DYNAMIC_CLASS(wxPyAxBaseWindow, wxWindow);

wxPyAxBaseWindow* wxPyAxBaseWindow_FromHWND(wxWindow* parent, unsigned long _hWnd)
{
    WXHWND hWnd = (WXHWND)_hWnd;
    wxPyAxBaseWindow* win = new wxPyAxBaseWindow;
    if (parent)
        parent->AddChild(win);
    win->SetEventHandler(win);
    win->SetHWND(hWnd);
    win->SubclassWin(hWnd);
    win->AdoptAttributesFromHWND();
    win->SetupColours();
    return win;
}
%End


//--------------------------------------------------------------------------

typedef void WXMSG;


class wxPyAxBaseWindow : wxWindow
{
public:
    wxPyAxBaseWindow(wxWindow* parent, const wxWindowID id=-1,
                    const wxPoint& pos = wxDefaultPosition,
                    const wxSize& size = wxDefaultSize,
                    long style = 0,
                    const wxString& name = wxPanelNameStr);
    wxPyAxBaseWindow();
    virtual bool MSWTranslateMessage(WXMSG* msg);
};

//--------------------------------------------------------------------------


