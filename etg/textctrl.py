#---------------------------------------------------------------------------
# Name:        etg/textctrl.py
# Author:      Kevin Ollivier
#
# Created:     9-Sept-2011
# Copyright:   (c) 2011 by Kevin Ollivier
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "textctrl"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ 'wxTextCtrl', 'wxTextEntry', 'wxTextCompleter', 'wxTextAttr', ]
    
#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    
    module.items.append(etgtools.TypedefDef(type='long', name='wxTextPos'))
    module.items.append(etgtools.TypedefDef(type='long', name='wxTextCoord'))
    
    etgtools.parseDoxyXML(module, ITEMS)
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxTextAttr')
    for op in c.allItems():
        if 'operator' in op.name:
            op.ignore()

    c = module.find('wxTextCompleter')
    c.addPrivateCopyCtor()
    
    c = module.find('wxTextEntry')
    c.abstract = True
    tools.removeVirtuals(c)

    c = module.find('wxTextCtrl')
    c.find('HitTest').overloads = []
    
    for op in c.findAll('operator<<'):
        op.ignore()

    assert isinstance(c, etgtools.ClassDef)

    tools.fixWindowClass(c)
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.addGetterSetterProps(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

