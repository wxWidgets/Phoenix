#---------------------------------------------------------------------------
# Name:        etg/textentry.py
# Author:      Robin Dunn
#
# Created:     03-Nov-2011
# Copyright:   (c) 2013 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"   
MODULE    = "_core"
NAME      = "textentry"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ "wxTextEntry", ]    
    
#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING, False)
    etgtools.parseDoxyXML(module, ITEMS)
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.
    
    c = module.find('wxTextEntry')
    assert isinstance(c, etgtools.ClassDef)
    c.abstract = True
    tools.removeVirtuals(c)

    c.find('GetSelection.from').out = True
    c.find('GetSelection.to').out = True
    c.find('GetRange.from').name = 'from_'
    c.find('GetRange.to').name = 'to_'
    c.find('Remove.from').name = 'from_'
    c.find('Remove.to').name = 'to_'
    c.find('Replace.from').name = 'from_'
    c.find('Replace.to').name = 'to_'
    c.find('SetSelection.from').name = 'from_'
    c.find('SetSelection.to').name = 'to_'

    
    # Rename the class to wxTextEntryBase and then add a new wxTextEntry
    # which derives from that class. This is needed because the backend
    # generator will need to know that the real wxTextEntryBase exists so
    # wxTextCtrlIface can derive from it.
    c.name = 'wxTextEntryBase'
    textEntry = etgtools.ClassDef(name='wxTextEntry', bases=['wxTextEntryBase'],
                                  abstract=True)
    module.insertItemAfter(c, textEntry)
    
    
    # Now add wxTextAreaBase and wxTextCtrlIface
    # TODO:  Do we need the wx.TextAreaBase methods defined?
    textAreaBase = etgtools.ClassDef(name='wxTextAreaBase', bases=[], abstract=True)
    module.insertItemAfter(textEntry, textAreaBase)
    
    textIface = etgtools.ClassDef(name='wxTextCtrlIface', 
                                  bases=['wxTextAreaBase', 'wxTextEntryBase'], 
                                  abstract=True)
    module.insertItemAfter(textAreaBase, textIface)
    
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

