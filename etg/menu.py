#---------------------------------------------------------------------------
# Name:        etg/menu.py
# Author:      Kevin Ollivier
#
# Created:     25-Aug-2011
# Copyright:   (c) 2011 by Wide Open Technologies
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "menu"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ 'wxMenu', 'wxMenuBar' ]    
    
#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    def addTransferAnnotations(c, arg):
        for method in c.findAll('Append') + c.findAll('Insert') + c.findAll('Replace'):
            arg_def = method.findItem(arg)
            if arg_def:
                arg_def.transfer = True
                
        for method in c.findAll('Remove') + c.findAll('Replace'):
            method.transferBack = True

    c = module.find('wxMenu')
    assert isinstance(c, etgtools.ClassDef)
    addTransferAnnotations(c, 'menuItem')
    c.find('GetMenuItems').overloads[0].ignore()
    tools.removeVirtuals(c)

    c = module.find('wxMenuBar')
    addTransferAnnotations(c, 'menu')
    c.find('wxMenuBar').findOverload('wxMenu *menus[], const wxString titles[], long style=0)').ignore()
    c.find('FindItem').ignore()
    mac_scmb = c.find('MacSetCommonMenuBar')
    mac_scmb.setCppCode("""\
    #ifdef __WXMAC__
        wxMenuBar::MacSetCommonMenuBar(menubar);
    #endif
    """)
    
    mac_gcmb = c.find('MacGetCommonMenuBar')
    mac_gcmb.setCppCode("""\
    #ifdef __WXMAC__
        return wxMenuBar::MacGetCommonMenuBar();
    #else
        return NULL;
    #endif
    """)
    
    # don't transfer on other platforms, as this is a no-op there.
    import sys
    if sys.platform.startswith('darwin'):
        mac_scmb.find('menubar').transfer = True
    
    assert isinstance(c, etgtools.ClassDef)
    c.find('FindItem.menu').out = True
    tools.removeVirtuals(c)

    module.addItem(tools.wxListWrapperTemplate('wxMenuList', 'wxMenu', module))

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

