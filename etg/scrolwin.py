#---------------------------------------------------------------------------
# Name:        etg/scrolwin.py
# Author:      Kevin Ollivier
#
# Created:     16-Sept-2011
# Copyright:   (c) 2011 by Kevin Ollivier
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "scrolwin"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ 'wxScrolled' ]    
    
#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.
    
    
    # NOTE: We do a trick here, because wxScrolled requires a template argument,
    # which SIP doesn't handle well. So instead we just wrap the wxScrolledWindow
    # class, which is defined as wxScrolled<wxPanel>, copying the wxScrolled API over to it.
    module.find('wxScrolledWindow').ignore()
    module.find('wxScrolledCanvas').ignore()
    
    # TODO: Handle wxScrolledCanvas. Do we just copy the ClassDef,
    # change the name, and add it?
    c = module.find('wxScrolled')
    c.name = 'wxScrolledWindow'
    c.bases = ['wxPanel']
    for ctor in c.find('wxScrolled').all():
        ctor.name = 'wxScrolledWindow'
    c.find('GetViewStart').findOverload('(int *x, int *y)').ignore()

    c.addPrivateCopyCtor()
    c.addPrivateAssignOp()
    tools.fixWindowClass(c)
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

