//--------------------------------------------------------------------------
// Name:        helpchm.sip
// Purpose:     SIP wrapper details for wxCHMHelpController
//
// Author:      Robin Dunn
//
// Created:     02-March-2020
// Copyright:   (c) 2020 by Total Control Software
// Licence:     wxWindows license
//--------------------------------------------------------------------------


// NOTE: This class is defined here instead of an etg file because it is not
// documented in the wxWidgets interface files. However since it implements the
// same API as all the other help controller classes then I think it's an okay
// workaround for now.


class wxCHMHelpController : public wxHelpControllerBase
{
    %TypeHeaderCode
    #include <wx/msw/helpchm.h>
    %End

public:
    wxCHMHelpController(wxWindow* parentWindow = NULL);

    virtual bool Initialize(const wxString& file);

    virtual bool LoadFile(const wxString& file = wxEmptyString);
    virtual bool DisplayContents();
    virtual bool DisplaySection(int sectionNo);
    virtual bool DisplaySection(const wxString& section);
    virtual bool DisplayBlock(long blockNo);
    virtual bool DisplayContextPopup(int contextId);
    virtual bool DisplayTextPopup(const wxString& text, const wxPoint& pos);
    virtual bool KeywordSearch(const wxString& k,
                               wxHelpSearchMode mode = wxHELP_SEARCH_ALL);
    virtual bool Quit();

    wxString GetHelpFile() const;

    static bool ShowContextHelpPopup(const wxString& text,
                                     const wxPoint& pos,
                                     wxWindow *window);
};
