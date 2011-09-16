#---------------------------------------------------------------------------
# Name:        etg/config.py
# Author:      Kevin Ollivier
#
# Created:     10-Sept-2011
# Copyright:   (c) 2011 by Kevin Ollivier
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "config"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ 'wxConfigBase', 'wxFileConfig', ]
    
#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.
    
    c = module.find('wxConfigBase')
    c.abstract = True
    ctor = c.find('wxConfigBase')
    ctor.items.remove(ctor.find('conv'))
    c.find('ReadObject').ignore()
    #c.find('Read').findOverload('defaultVal').ignore()
    #c.find('Read').findOverload('str').ignore()
    for func in c.findAll('Read'):
        if not 'wxString' in func.type:
            func.ignore()
        else:
            func.find('defaultVal').default = 'wxEmptyString'
            
    c.addCppMethod('long', 'ReadInt', '(const wxString& key, long defaultVal = 0)', """
        double rv;
        self->Read(*key, &rv, defaultVal);
        return rv;
    """)
    c.find('Write').overloads = []
    c.addCppMethod('bool', 'WriteInt', '(const wxString& key, long value)', """
        return self->Write(*key, value);
    """)
    c.addCppMethod('bool', 'WriteFloat', '(const wxString& key, double value)', """
        return self->Write(*key, value);
    """)
    c.addCppMethod('bool', 'WriteBool', '(const wxString& key, bool value)', """
        return self->Write(*key, value);
    """)
    
    c = module.find('wxFileConfig')
    c.addPrivateCopyCtor()
    c.find('wxFileConfig').findOverload('wxInputStream').ignore()
    ctor = c.find('wxFileConfig').findOverload('wxString')
    ctor.items.remove(ctor.find('conv'))
    ctor = c.find('Save').ignore()
    c.find('GetGlobalFile').ignore()
    c.find('GetLocalFile').ignore()
    
    module.addPyCode('Config = FileConfig')
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.addGetterSetterProps(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

