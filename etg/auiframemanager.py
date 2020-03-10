#---------------------------------------------------------------------------
# Name:        etg/auiframemanager.py
# Author:      Robin Dunn
#
# Created:     25-Oct-2016
# Copyright:   (c) 2016-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_aui"
NAME      = "auiframemanager"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxAuiManager',
           'wxAuiPaneInfo',
           'wxAuiManagerEvent',
           'wxAuiDockInfo',
           'wxAuiDockUIPart',
           'wxAuiFloatingFrame'
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.


    c = module.find('wxAuiManager')
    assert isinstance(c, etgtools.ClassDef)
    c.find('ProcessDockResult').ignore(False)

    c = module.find('wxAuiPaneInfo')
    module.addItem(
        tools.wxArrayWrapperTemplate(
            'wxAuiPaneInfoArray', 'wxAuiPaneInfo', module))


    c = module.find('wxAuiManagerEvent')
    tools.fixEventClass(c)

    module.addPyCode("""\
        EVT_AUI_PANE_BUTTON = wx.PyEventBinder( wxEVT_AUI_PANE_BUTTON )
        EVT_AUI_PANE_CLOSE = wx.PyEventBinder( wxEVT_AUI_PANE_CLOSE )
        EVT_AUI_PANE_MAXIMIZE = wx.PyEventBinder( wxEVT_AUI_PANE_MAXIMIZE )
        EVT_AUI_PANE_RESTORE = wx.PyEventBinder( wxEVT_AUI_PANE_RESTORE )
        EVT_AUI_PANE_ACTIVATED = wx.PyEventBinder( wxEVT_AUI_PANE_ACTIVATED )
        EVT_AUI_RENDER = wx.PyEventBinder( wxEVT_AUI_RENDER )
        EVT_AUI_FIND_MANAGER = wx.PyEventBinder( wxEVT_AUI_FIND_MANAGER )
        """)


    module.addItem(tools.wxArrayWrapperTemplate(
            'wxAuiDockInfoArray', 'wxAuiDockInfo', module))

    module.addItem(tools.wxArrayWrapperTemplate(
            'wxAuiDockUIPartArray', 'wxAuiDockUIPart', module))

    module.addItem(tools.wxArrayWrapperTemplate(
            'wxAuiPaneInfoPtrArray', 'wxAuiPaneInfo', module, itemIsPtr=True))

    module.addItem(tools.wxArrayWrapperTemplate(
            'wxAuiDockInfoPtrArray', 'wxAuiDockInfo', module, itemIsPtr=True))


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

