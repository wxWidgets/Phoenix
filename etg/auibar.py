#---------------------------------------------------------------------------
# Name:        etg/auibar.py
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
NAME      = "auibar"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxAuiToolBarItem',
           'wxAuiToolBarArt',
           'wxAuiDefaultToolBarArt',
           'wxAuiToolBar',
           'wxAuiToolBarEvent',
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxAuiToolBar')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixWindowClass(c)


    c = module.find('wxAuiToolBarEvent')
    tools.fixEventClass(c)

    module.addPyCode("""\
        EVT_AUITOOLBAR_TOOL_DROPDOWN = wx.PyEventBinder( wxEVT_AUITOOLBAR_TOOL_DROPDOWN, 1 )
        EVT_AUITOOLBAR_OVERFLOW_CLICK = wx.PyEventBinder( wxEVT_AUITOOLBAR_OVERFLOW_CLICK, 1 )
        EVT_AUITOOLBAR_RIGHT_CLICK = wx.PyEventBinder( wxEVT_AUITOOLBAR_RIGHT_CLICK, 1 )
        EVT_AUITOOLBAR_MIDDLE_CLICK = wx.PyEventBinder( wxEVT_AUITOOLBAR_MIDDLE_CLICK, 1 )
        EVT_AUITOOLBAR_BEGIN_DRAG = wx.PyEventBinder( wxEVT_AUITOOLBAR_BEGIN_DRAG, 1 )
        """)


    module.addItem(tools.wxArrayWrapperTemplate(
            'wxAuiToolBarItemArray', 'wxAuiToolBarItem', module))


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

