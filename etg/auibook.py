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
           'wxAuiFlatTabArt',
           'wxAuiGenericTabArt',
           'wxAuiSimpleTabArt',
           'wxAuiNotebookEvent',
           'wxAuiNotebookPosition',
           'wxAuiBookDeserializer',
           'wxAuiBookSerializer',
           'wxAuiTabLayoutInfo',
           'wxAuiDockLayoutInfo'
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

    c.find('GetAllTabCtrls').ignore()
    c.find('GetPagesInDisplayOrder').ignore()

    c = module.find('wxAuiTabContainer')
    tools.ignoreConstOverloads(c)
    c.find('GetPages').ignore()

    notebook_page_equality_code = """
#include <wx/aui/auibook.h>

inline bool operator==(const wxAuiNotebookPage& a, const wxAuiNotebookPage& b) {

    if (a.window != b.window) return false;
    
    return true;
}
"""
    module.addItem(tools.stdVectorWrapperTemplate(
            'wxAuiNotebookPageArray', 'wxAuiNotebookPage', module, typeHeaderHelper=notebook_page_equality_code))
            
    tab_button_equality_code = """
#include <wx/aui/auibook.h> 

inline bool operator==(const wxAuiTabContainerButton& a, const wxAuiTabContainerButton& b) {
    return a.id == b.id;
}
"""

    module.addItem(tools.stdVectorWrapperTemplate(
            'wxAuiTabContainerButtonArray', 'wxAuiTabContainerButton', module, typeHeaderHelper=tab_button_equality_code))
                  
    c = module.find('wxAuiNotebookPage')
    c.find('buttons').ignore()
    
    c = module.find('wxAuiTabLayoutInfo')
    c.find('pages').ignore()
    c.find('pinned').ignore()

    c = module.find('wxAuiTabArt')
    c.abstract = True
    c.find('GetBestTabCtrlSize').ignore()
    
    c = module.find('wxAuiGenericTabArt')
    c.find('GetBestTabCtrlSize').ignore()
    c.find('ShowDropDown').ignore()
    
    c = module.find('wxAuiSimpleTabArt')
    c.find('GetBestTabCtrlSize').ignore()
    c.find('ShowDropDown').ignore()

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


        
    module.addPyCode("AuiDefaultTabArt = AuiFlatTabArt")
     
    c = module.find('wxAuiBookDeserializer')
    c.abstract = True
    c.find('LoadNotebookTabs').ignore()
    
    c = module.find('wxAuiBookSerializer')
    c.abstract = True
    
    c = module.find('wxAuiFlatTabArt')
    c.addPrivateCopyCtor()
    
    
    c = module.find('wxAuiNotebookPosition')
    c.find('operator bool').ignore()
    
    c = module.find('wxAuiTabContainer')
    s = c.find('HitTestResult')
    s.find('operator bool').ignore()


    #-----------------------------------------------------------------
    # Add AuiTabCtrl in.
    c = etgtools.ClassDef(name = "wxAuiTabCtrl",
        bases = ["wxControl", "wxAuiTabContainer"],
        mustHaveAppFlag = True,
        items = [
            etgtools.MethodDef(name = "wxAuiTabCtrl",
                classname="wxAuiTabCtrl", isCtor=True,
                items = [
                    etgtools.ParamDef(type = "wxAuiNotebook*", name = "parent"),
                    etgtools.ParamDef(type = "wxWindowID", name = "id", default="wxID_ANY"),
                ],
            ),
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

