#---------------------------------------------------------------------------
# Name:        etg/property.py
# Author:      Robin Dunn
#
# Created:     23-Feb-2015
# Copyright:   (c) 2015 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"   
MODULE    = "_propgrid"
NAME      = "property"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ 'wxPGPaintData',
           'wxPGCellRenderer',
           'wxPGDefaultRenderer',
           'wxPGCellData',
           'wxPGCell',
           'wxPGAttributeStorage',

           'wxPGProperty',
           'wxPropertyCategory',
           'wxPGChoiceEntry',
           'wxPGChoicesData',
           'wxPGChoices',
           ]    
    
#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxPGAttributeStorage')
    assert isinstance(c, etgtools.ClassDef)
    
    # TODO: Add methods to add a Python iterator using these methods
    c.find('StartIteration').ignore()
    c.find('GetNext').ignore()
    c.find('const_iterator').ignore()


    c = module.find('wxPGProperty')
    tools.ignoreConstOverloads(c)


    c = module.find('wxPGChoicesData')
    tools.ignoreConstOverloads(c)
    

    c = module.find('wxPGChoices')
    c.find('wxPGChoices').findOverload('wxChar **').ignore()
    tools.ignoreConstOverloads(c)
    
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

