#---------------------------------------------------------------------------
# Name:        etg/auibook.py
# Author:      Robin Dunn
#
# Created:     26-Oct-2016
# Copyright:   (c) 2016-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_aui"
NAME      = "auibook"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxAuiNotebook',
           'wxAuiNotebookPage',
           'wxAuiTabContainerButton',
           'wxAuiTabContainer',
           'wxAuiTabArt',
           'wxAuiDefaultTabArt',
           'wxAuiSimpleTabArt',
           'wxAuiNotebookEvent',
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.


    c = module.find('wxAuiNotebook')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixWindowClass(c)
    tools.fixBookctrlClass(c)
    c.find('SetArtProvider.art').transfer = True


    c = module.find('wxAuiTabContainer')
    tools.ignoreConstOverloads(c)

    module.addItem(tools.wxArrayWrapperTemplate(
            'wxAuiNotebookPageArray', 'wxAuiNotebookPage', module))

    module.addItem(tools.wxArrayWrapperTemplate(
            'wxAuiTabContainerButtonArray', 'wxAuiTabContainerButton', module))

    c = module.find('wxAuiTabArt')
    c.abstract = True

    c = module.find('wxAuiNotebookEvent')
    tools.fixEventClass(c)
    module.addPyCode("""\
        EVT_AUINOTEBOOK_PAGE_CLOSE = wx.PyEventBinder( wxEVT_AUINOTEBOOK_PAGE_CLOSE, 1 )
        EVT_AUINOTEBOOK_PAGE_CLOSED = wx.PyEventBinder( wxEVT_AUINOTEBOOK_PAGE_CLOSED, 1 )
        EVT_AUINOTEBOOK_PAGE_CHANGED = wx.PyEventBinder( wxEVT_AUINOTEBOOK_PAGE_CHANGED, 1 )
        EVT_AUINOTEBOOK_PAGE_CHANGING = wx.PyEventBinder( wxEVT_AUINOTEBOOK_PAGE_CHANGING, 1 )
        EVT_AUINOTEBOOK_BUTTON = wx.PyEventBinder( wxEVT_AUINOTEBOOK_BUTTON, 1 )
        EVT_AUINOTEBOOK_BEGIN_DRAG = wx.PyEventBinder( wxEVT_AUINOTEBOOK_BEGIN_DRAG, 1 )
        EVT_AUINOTEBOOK_END_DRAG = wx.PyEventBinder( wxEVT_AUINOTEBOOK_END_DRAG, 1 )
        EVT_AUINOTEBOOK_DRAG_MOTION = wx.PyEventBinder( wxEVT_AUINOTEBOOK_DRAG_MOTION, 1 )
        EVT_AUINOTEBOOK_ALLOW_DND = wx.PyEventBinder( wxEVT_AUINOTEBOOK_ALLOW_DND, 1 )
        EVT_AUINOTEBOOK_DRAG_DONE = wx.PyEventBinder( wxEVT_AUINOTEBOOK_DRAG_DONE, 1 )
        EVT_AUINOTEBOOK_TAB_MIDDLE_DOWN = wx.PyEventBinder( wxEVT_AUINOTEBOOK_TAB_MIDDLE_DOWN, 1 )
        EVT_AUINOTEBOOK_TAB_MIDDLE_UP = wx.PyEventBinder( wxEVT_AUINOTEBOOK_TAB_MIDDLE_UP, 1 )
        EVT_AUINOTEBOOK_TAB_RIGHT_DOWN = wx.PyEventBinder( wxEVT_AUINOTEBOOK_TAB_RIGHT_DOWN, 1 )
        EVT_AUINOTEBOOK_TAB_RIGHT_UP = wx.PyEventBinder( wxEVT_AUINOTEBOOK_TAB_RIGHT_UP, 1 )
        EVT_AUINOTEBOOK_BG_DCLICK = wx.PyEventBinder( wxEVT_AUINOTEBOOK_BG_DCLICK, 1 )
        """)




    #-----------------------------------------------------------------
    # Add AuiTabCtrl in.
    c = etgtools.ClassDef(name = "wxAuiTabCtrl",
        bases = ["wxControl", "wxAuiTabContainer"],
        mustHaveAppFlag = True,
        items = [
            etgtools.MethodDef(name = "wxAuiTabCtrl",
                classname="wxAuiTabCtrl", isCtor=True,
                items = [
                    etgtools.ParamDef(type = "wxWindow*", name = "parent"),
                    etgtools.ParamDef(type = "wxWindowID", name = "id", default="wxID_ANY"),
                    etgtools.ParamDef(type = "const wxPoint&", name = "pos", default = "wxDefaultPosition"),
                    etgtools.ParamDef(type = "const wxSize&", name = "size", default = "wxDefaultSize"),
                    etgtools.ParamDef(type = "long", name = "style", default = "0") ]),
            etgtools.MethodDef(type = "bool", name = "IsDragging", classname = "wxAuiTabCtrl", isConst = True)
            ])
    tools.fixWindowClass(c)
    module.addItem(c)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

