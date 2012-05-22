#---------------------------------------------------------------------------
# Name:        etg/textctrl.py
# Author:      Kevin Ollivier
#              Robin Dunn
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
ITEMS  = [ 'wxTextAttr', 'wxTextCtrl', ]
    
#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxTextAttr')
    assert isinstance(c, etgtools.ClassDef)
    c.find('operator=').ignore()

    c.find('SetFont').pyArgsString = '(font, flags=TEXT_ATTR_FONT & ~TEXT_ATTR_FONT_PIXEL_SIZE)'

    c = module.find('wxTextCtrl')
    module.addGlobalStr('wxTextCtrlNameStr', c)
    
    # Split the HitTest overloads into separately named methods since once
    # the output parameters are applied they will have the same function
    # signature.
    ht1 = c.find('HitTest')
    ht2 = ht1.overloads[0]
    ht1.overloads = []
    c.insertItemAfter(ht1, ht2)
    ht1.pyName = 'HitTestPos'
    ht1.find('pos').out = True
    ht2.find('row').out = True
    ht2.find('col').out = True
    
    c.find('PositionToXY.x').out = True
    c.find('PositionToXY.y').out = True

    for op in c.findAll('operator<<'):
        op.ignore()

    tools.fixWindowClass(c)
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

