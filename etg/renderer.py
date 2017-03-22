#---------------------------------------------------------------------------
# Name:        etg/renderer.py
# Author:      Robin Dunn
#
# Created:     27-Jun-2012
# Copyright:   (c) 2012-2017 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "renderer"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxSplitterRenderParams",
           "wxHeaderButtonParams",
           "wxRendererNative",
           "wxDelegateRendererNative",
           "wxRendererVersion",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxRendererNative')
    assert isinstance(c, etgtools.ClassDef)
    c.addPrivateCopyCtor()
    c.mustHaveApp()
    c.find('Get').mustHaveApp()
    c.find('GetGeneric').mustHaveApp()
    c.find('GetDefault').mustHaveApp()
    c.find('Set').mustHaveApp()


    #virtual void DrawTitleBarBitmap(wxWindow *win,
    #                                wxDC& dc,
    #                                const wxRect& rect,
    #                                wxTitleBarButton button,
    #                                int flags = 0) = 0;
    c.find('DrawTitleBarBitmap').setCppCode("""\
    #ifdef wxHAS_DRAW_TITLE_BAR_BITMAP
        self->DrawTitleBarBitmap(win, *dc, *rect, button, flags);
    #endif
    """)


    c = module.find('wxDelegateRendererNative')
    c.mustHaveApp()
    c.addPrivateCopyCtor()


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

