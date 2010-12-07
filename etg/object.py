#---------------------------------------------------------------------------
# Name:        etg/object.py
# Author:      Robin Dunn
#
# Created:     9-Nov-2010
# Copyright:   (c) 2010 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"   
MODULE    = "_core"
NAME      = "object"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ 
    'wxRefCounter',
    'wxObject',       
#    'wxClassInfo',
]    
    
#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.
    
    
    module.find('wxObject.operator delete').ignore()
    module.find('wxObject.operator new').ignore()
    module.find('wxCreateDynamicObject').ignore()
    
    
    #module.find('wxClassInfo').abstract = True
    #module.find('wxClassInfo.wxClassInfo').ignore()
    
    module.find('wxObject.GetClassInfo').ignore()
    module.find('wxObject.IsKindOf').ignore()
    
    module.find('wxRefCounter.~wxRefCounter').ignore(False)
    
    c = module.find('wxObject')
    assert isinstance(c, etgtools.ClassDef)

    c.addCppMethod('const wxChar*', 'GetClassName', '()',
        body='return self->GetClassInfo()->GetClassName();',
        doc='Returns the class name of the C++ class using wxRTTI.')
    
    c.addCppMethod('void', 'Destroy', '()',
        body='delete self;',
        doc='Deletes the C++ object this Python object is a proxy for.',
        transferThis=True)  # TODO: Check this
        
        
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

