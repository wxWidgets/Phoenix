#---------------------------------------------------------------------------
# Name:        etg/dnd.py
# Author:      Robin Dunn
#
# Created:     29-Apr-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "dnd"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "interface_2wx_2dnd_8h.xml",
           "wxDropSource",
           "wxDropTarget",
           "wxTextDropTarget",
           "wxFileDropTarget",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode('#include <wx/dnd.h>')

    c = module.find('wxDropSource')
    assert isinstance(c, etgtools.ClassDef)
    c.addPrivateCopyCtor()

    for m in c.find('wxDropSource').all():
        if 'wxIcon' in m.argsString:
            # Ignore the ctors taking wxIcon parameters. They are GTK only
            # and we don't have an easy way yet to support platform specific
            # APIs in the ctors.
            m.ignore()
        else:
            # Ignore the cursor parameters. We'll need to use SetCursor or
            # SetIcon instead.
            m.find('iconCopy').ignore()
            m.find('iconMove').ignore()
            m.find('iconNone').ignore()

    # void SetCursor(wxDragResult res, const wxCursor& cursor);
    c.find('SetCursor').setCppCode("""\
        #ifdef __WXGTK__
            wxPyRaiseNotImplementedMsg("Cursors not supported, use SetIcon on wxGTK instead.");
        #else
            self->SetCursor(res, *cursor);
        #endif
        """)

    # void SetIcon(wxDragResult res, const wxIcon& icon)
    c.find('SetIcon').setCppCode("""\
        #ifdef __WXGTK__
            self->SetIcon(res, *icon);
        #else
            wxPyRaiseNotImplementedMsg("Icons not supported, use SetCursor on non-wxGTK ports.");
        #endif
        """)



    c = module.find('wxDropTarget')
    c.addPrivateCopyCtor()
    c.find('wxDropTarget.data').transfer = True
    c.find('SetDataObject.data').transfer = True

    module.addPyCode("PyDropTarget = wx.deprecated(DropTarget, 'Use DropTarget instead.')")


    c = module.find('wxTextDropTarget')
    c.addItem(etgtools.WigCode("virtual wxDragResult OnData(wxCoord x, wxCoord y, wxDragResult def);"))

    c = module.find('wxFileDropTarget')
    c.addItem(etgtools.WigCode("virtual wxDragResult OnData(wxCoord x, wxCoord y, wxDragResult def);"))


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

