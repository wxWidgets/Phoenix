#---------------------------------------------------------------------------
# Name:        etg/dialog.py
# Author:      Kevin Ollivier
#
# Created:     26-Aug-2011
# Copyright:   (c) 2011 by Wide Open Technologies
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"   
MODULE    = "_core"
NAME      = "dialog"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  =    [
                'wxDialog',
                'wxDialogLayoutAdapter',       
                'wxWindowModalDialogEvent',
            ]
    
#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxDialog')
    assert isinstance(c, etgtools.ClassDef)
    module.addGlobalStr('wxDialogNameStr', c)
    
    c.find('wxDialog.title').default = 'wxEmptyString'
    c.find('Create.title').default = 'wxEmptyString'
    
    # PocketPC only, don't think we'll need these ;)
    c.find('DoOK').ignore() 
    c.find('GetToolBar').ignore()
    
    # The docs tell us to just use ShowModal instead, not sure why they 
    # doc this method then...
    c.find('SetModal').ignore()
    
    # Release the GIL for potentially blocking or long-running functions
    c.find('ShowModal').releaseGIL()
    
    # context manager methods
    c.addPyMethod('__enter__', '(self)', 'return self')
    c.addPyMethod('__exit__', '(self, exc_type, exc_val, exc_tb)', 'self.Destroy()')
        
    tools.fixTopLevelWindowClass(c)
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

