#---------------------------------------------------------------------------
# Name:        etg/toolbar.py
# Author:      Robin Dunn
#
# Created:     07-Mar-2012
# Copyright:   (c) 2012 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

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
    
    module.insertItem(0, etgtools.WigCode("""\
        // forward declarations
        class wxToolBarBase;
        """))

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
    _fixClientData(c)

    gcd = c.find('GetClientData')
    gcd.type = 'wxPyUserData*'
    gcd.setCppCode('return dynamic_cast<wxPyUserData*>(self->GetClientData());')

    
   
    #---------------------------------------------                
    c = module.find('wxToolBar')
    tools.fixWindowClass(c)
    _fixClientData(c)
    c.find('SetBitmapResource').ignore()

    gcd = c.find('GetToolClientData')
    gcd.type = 'wxPyUserData*'
    gcd.setCppCode('return dynamic_cast<wxPyUserData*>(self->GetToolClientData(toolId));')

    c.find('AddTool.tool').transfer = True
    c.find('InsertTool.tool').transfer = True

    c.find('OnLeftClick').ignore()
    c.find('OnMouseEnter').ignore()
    c.find('OnRightClick').ignore()
    c.find('OnLeftClick').ignore()

    c.addPyMethod('AddSimpleTool', '(self, toolId, bitmap, shortHelpString="", longHelpString="", isToggle=0)',
        doc='Old style method to add a tool to the toolbar.',
        deprecated=True,
        body="""\
            kind = wx.ITEM_NORMAL
            if isToggle: kind = wx.ITEM_CHECK
            return self.AddTool(toolId, '', bitmap, wx.NullBitmap, kind,
                                shortHelpString, longHelpString)
            """)

    c.addPyMethod('InsertSimpleTool', '(self, pos, toolId, bitmap, shortHelpString="", longHelpString="", isToggle=0)',
        doc='Old style method to insert a tool in the toolbar.',
        deprecated=True,
        body="""\
            kind = wx.ITEM_NORMAL
            if isToggle: kind = wx.ITEM_CHECK
            return self.InsertTool(pos, toolId, '', bitmap, wx.NullBitmap, kind,
                                   shortHelpString, longHelpString)
            """)


    module.addGlobalStr('wxToolBarNameStr', c)



    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

