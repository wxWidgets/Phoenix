#---------------------------------------------------------------------------
# Name:        etg/variant.py
# Author:      Kevin Ollivier
#
# Created:     15-Sept-2010
# Copyright:   (c) 2011 by Kevin Ollivier
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"   
MODULE    = "_core"
NAME      = "variant"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ 'wxVariant', 'wxVariantData', ]    
    
#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.
    
    
    c = module.find('wxVariant')
    
    # FIXME: No matter what I do here, I always get 'same signature' errors
    # for the various constructors. I've tried removing the ones that seem 
    # similar, and renaming parameters in the wx interface file, but neither 
    # approach changes things. Do we just need to use a mapped type for all conversions?
    c.find('wxVariant').overloads = []
    #c.find('wxVariant').findOverload('wxAny').ignore()
    #c.find('wxVariant').findOverload('wxChar *').ignore()
    #c.find('wxVariant').findOverload('wxChar').ignore()
    #c.find('wxVariant').findOverload('wxLongLong').ignore()
    #c.find('wxVariant').findOverload('wxULongLong').ignore()
    #c.find('wxVariant').findOverload('void *').ignore()
    
    c.find('GetAny').ignore()
    
    # SIP doesn't like the syntax on these methods. I don't know if it's 
    # something wrong about the SIP output, or if SIP doesn't support these.
    c.find('operator double').ignore()
    c.find('operator long').ignore()
    c.find('operator wxLongLong').ignore()
    c.find('operator wxULongLong').ignore()
    
    c.find('operator void *').ignore()
    c.find('operator wxChar').ignore()
    c.find('operator wxDateTime').ignore()
    c.find('operator wxString').ignore()
    
    assert isinstance(c, etgtools.ClassDef)

    
    
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

