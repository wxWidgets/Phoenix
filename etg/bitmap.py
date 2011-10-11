#---------------------------------------------------------------------------
# Name:        etg/bitmap.py
# Author:      Kevin Ollivier
#              Robin Dunn
#
# Created:     25-Aug-2011
# Copyright:   (c) 2011 by Wide Open Technologies
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "bitmap"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ 'wxBitmap', 'wxBitmapHandler', 'wxMask' ]    
    
#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxBitmap')
    assert isinstance(c, etgtools.ClassDef)
    
    tools.removeVirtuals(c)

    c.find('wxBitmap').findOverload('(const char *const *bits)').ignore()
    c.find('wxBitmap.type').default = 'wxBITMAP_TYPE_ANY'
    c.find('LoadFile.type').default = 'wxBITMAP_TYPE_ANY'

    c.find('SetMask.mask').transfer = True

    c.addCppMethod('void', 'SetMaskColour', '(const wxColour& colour)', """\
        wxMask* mask = new wxMask(*self, *colour);
        self->SetMask(mask);
        """)

    c.addCppMethod('int', '__nonzero__', '()', """\
        return self->IsOk();
        """)
        
    # On MSW the handler classes are different than what is documented, and
    # this causes compile errors. Nobody has needed them from Python thus far,
    # so just ignore them all for now.
    for m in c.find('FindHandler').all():
        m.ignore()
    c.find('AddHandler').ignore()
    c.find('CleanUpHandlers').ignore()
    c.find('GetHandlers').ignore()
    c.find('InsertHandler').ignore()
    c.find('RemoveHandler').ignore()
    
    # This one is called from the wx startup code, it's not needed in Python
    # so nuke it too since we're nuking all the others.
    c.find('InitStandardHandlers').ignore()
    
    module.find('wxBitmapHandler').ignore()
    #module.addItem(tools.wxListWrapperTemplate('wxList', 'wxBitmapHandler', module))

    # TODO: The ctors and methods from Classic for converting to/from
    #       buffer objects with raw bitmap access.
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.addGetterSetterProps(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

