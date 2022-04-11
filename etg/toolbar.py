#---------------------------------------------------------------------------
# Name:        etg/toolbar.py
# Author:      Robin Dunn
#
# Created:     07-Mar-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools
from etgtools.extractors import ExtractorError

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "toolbar"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxToolBarToolBase",
           "wxToolBar",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.


    # Use wxPyUserData for the clientData values instead of a plain wxObject
    def _fixClientData(c):
        for item in c.allItems():
            if isinstance(item, etgtools.ParamDef) and item.name == 'clientData':
                item.type = 'wxPyUserData*'
                item.transfer = True


    #---------------------------------------------
    c = module.find('wxToolBarToolBase')
    assert isinstance(c, etgtools.ClassDef)
    c.abstract = True
    tools.removeVirtuals(c)
    _fixClientData(c)

    # Switch all wxToolBarBase to wxToolBar
    for item in c.allItems():
        if isinstance(item, etgtools.ParamDef) and item.name == 'tbar':
            item.type = 'wxToolBar*'

    c.find('GetToolBar').ignore()
    c.addCppMethod('wxToolBar*', 'GetToolBar', '()',
        doc="Return the toolbar this tool is a member of.",
        body="""\
            return (wxToolBar*)self->GetToolBar();
            """)

    gcd = c.find('GetClientData')
    gcd.type = 'wxPyUserData*'
    gcd.setCppCode('return dynamic_cast<wxPyUserData*>(self->GetClientData());')

    c.find('SetDropdownMenu.menu').transfer = True


    #---------------------------------------------
    c = module.find('wxToolBar')
    tools.fixWindowClass(c)
    tools.ignoreConstOverloads(c)
    _fixClientData(c)
    module.addGlobalStr('wxToolBarNameStr', c)

    gcd = c.find('GetToolClientData')
    gcd.type = 'wxPyUserData*'
    gcd.setCppCode('return dynamic_cast<wxPyUserData*>(self->GetToolClientData(toolId));')

    c.find('AddTool.tool').transfer = True
    c.find('InsertTool.tool').transfer = True

    # Conform the help text parameters.
    m = c.find('AddTool')
    for method in m.all():
        for helper in ('shortHelp', 'longHelp'):
            try:
                param = method.find("{}String".format(helper))
                param.name = helper
            except ExtractorError:
                pass

    c.find('OnLeftClick').ignore()
    c.find('OnMouseEnter').ignore()
    c.find('OnRightClick').ignore()
    c.find('OnLeftClick').ignore()

    c.find('SetDropdownMenu.menu').transfer = True


    # Add some deprecated methods to aid with Classic compatibility.
    # TODO: Which others are commonly enough used that they should be here too?
    c.addPyMethod('AddSimpleTool', '(self, toolId, bitmap, shortHelpString="", longHelpString="", isToggle=0)',
        doc='Old style method to add a tool to the toolbar.',
        deprecated='Use :meth:`AddTool` instead.',
        body="""\
            kind = wx.ITEM_NORMAL
            if isToggle: kind = wx.ITEM_CHECK
            return self.AddTool(toolId, '', bitmap, wx.NullBitmap, kind,
                                shortHelpString, longHelpString)
            """)
    c.addPyMethod('AddLabelTool',
                  '(self, id, label, bitmap, bmpDisabled=wx.NullBitmap, kind=wx.ITEM_NORMAL,'
                  ' shortHelp="", longHelp="", clientData=None)',
        doc='Old style method to add a tool in the toolbar.',
        deprecated='Use :meth:`AddTool` instead.',
        body="""\
            return self.AddTool(id, label, bitmap, bmpDisabled, kind,
                                shortHelp, longHelp, clientData)
            """)

    c.addPyMethod('InsertSimpleTool', '(self, pos, toolId, bitmap, shortHelpString="", longHelpString="", isToggle=0)',
        doc='Old style method to insert a tool in the toolbar.',
        deprecated='Use :meth:`InsertTool` instead.',
        body="""\
            kind = wx.ITEM_NORMAL
            if isToggle: kind = wx.ITEM_CHECK
            return self.InsertTool(pos, toolId, '', bitmap, wx.NullBitmap, kind,
                                   shortHelpString, longHelpString)
            """)
    c.addPyMethod('InsertLabelTool',
                  '(self, pos, id, label, bitmap, bmpDisabled=wx.NullBitmap, kind=wx.ITEM_NORMAL,'
                  ' shortHelp="", longHelp="", clientData=None)',
        doc='Old style method to insert a tool in the toolbar.',
        deprecated='Use :meth:`InsertTool` instead.',
        body="""\
            return self.InsertTool(pos, id, label, bitmap, bmpDisabled, kind,
                                   shortHelp, longHelp, clientData)
            """)




    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

