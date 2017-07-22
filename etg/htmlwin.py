#---------------------------------------------------------------------------
# Name:        etg/htmlwin.py
# Author:      Robin Dunn
#
# Created:     29-Oct-2012
# Copyright:   (c) 2012-2017 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_html"
NAME      = "htmlwin"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxHtmlWindowInterface",
           "wxHtmlWindow",
           "wxHtmlLinkEvent",
           "wxHtmlCellEvent",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxHtmlWindow')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixWindowClass(c)
    c.bases = ['wxScrolledWindow']

    c.find('OnCellClicked').ignore(False)
    c.find('OnCellMouseHover').ignore(False)
    c.find('AddFilter.filter').transfer = True

    tools.fixHtmlSetFonts(c)

    # Pure virtuals inherited from wxHtmlWindowInterface
    c.addItem(etgtools.WigCode("""\
        virtual void SetHTMLWindowTitle(const wxString& title);
        virtual void OnHTMLLinkClicked(const wxHtmlLinkInfo& link);
        virtual wxHtmlOpeningStatus OnHTMLOpeningURL(wxHtmlURLType type,
                                                     const wxString& url,
                                                     wxString *redirect) const;
        virtual wxPoint HTMLCoordsToWindow(wxHtmlCell *cell,
                                           const wxPoint& pos) const;
        virtual wxWindow* GetHTMLWindow();
        virtual wxColour GetHTMLBackgroundColour() const;
        virtual void SetHTMLBackgroundColour(const wxColour& clr);
        virtual void SetHTMLBackgroundImage(const wxBitmap& bmpBg);
        virtual void SetHTMLStatusText(const wxString& text);
        virtual wxCursor GetHTMLCursor(wxHtmlWindowInterface::HTMLCursor type) const;
        """))

    c = module.find('wxHtmlLinkEvent')
    tools.fixEventClass(c)

    c = module.find('wxHtmlCellEvent')
    tools.fixEventClass(c)

    module.addPyCode("""\
        EVT_HTML_CELL_CLICKED = wx.PyEventBinder( wxEVT_HTML_CELL_CLICKED, 1 )
        EVT_HTML_CELL_HOVER   = wx.PyEventBinder( wxEVT_HTML_CELL_HOVER, 1 )
        EVT_HTML_LINK_CLICKED = wx.PyEventBinder( wxEVT_HTML_LINK_CLICKED, 1 )

        # deprecated wxEVT aliases
        wxEVT_COMMAND_HTML_CELL_CLICKED  = wxEVT_HTML_CELL_CLICKED
        wxEVT_COMMAND_HTML_CELL_HOVER    = wxEVT_HTML_CELL_HOVER
        wxEVT_COMMAND_HTML_LINK_CLICKED  = wxEVT_HTML_LINK_CLICKED
        """)


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

