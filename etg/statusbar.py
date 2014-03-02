#---------------------------------------------------------------------------
# Name:        etg/statusbar.py
# Author:      Kevin Ollivier
#
# Created:     16-Sept-2011
# Copyright:   (c) 2013 by Kevin Ollivier
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "statusbar"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ 'wxStatusBar', 'wxStatusBarPane', ]    
    
#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.
    
    c = module.find('wxStatusBar')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixWindowClass(c)
    module.addGlobalStr('wxStatusBarNameStr', c)

    # We already have a MappedType for wxArrayInt, so just tweak the
    # interface to use that instead of an array size and a const int pointer.
    m = c.find('SetStatusWidths')
    m.find('n').ignore()
    m.find('widths_field').type = 'const wxArrayInt&'
    m.find('widths_field').name = 'widths'
    m.argsString = '(int n, const wxArrayInt& widths)'
    m.setCppCode("""\
        const int* ptr = &widths->front();
        self->SetStatusWidths(widths->size(), ptr);
        """)
    
    # Change GetFieldRect to return the rectangle (for Pythonicity and Classic compatibility)
    c.find('GetFieldRect').ignore()
    c.addCppMethod('wxRect*', 'GetFieldRect', '(int i)',
        doc="Returns the size and position of a field's internal bounding rectangle.",
        body="""\
            wxRect* r = new wxRect;
            self->GetFieldRect(i, *r);
            return r;
            """)
    
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

