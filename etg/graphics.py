#---------------------------------------------------------------------------
# Name:        etg/graphics.py
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
NAME      = "graphics"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ 
            'wxGraphicsBrush',
            'wxGraphicsContext',
            'wxGraphicsFont',
            'wxGraphicsGradientStop',
            'wxGraphicsGradientStops',
            'wxGraphicsMatrix',
            'wxGraphicsObject',
            'wxGraphicsPath',
            'wxGraphicsPen',
            'wxGraphicsRenderer',
        ]
    
#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    
    module.addHeaderCode('#include <wx/gdicmn.h>')
    
    def markFactories(klass):
        for func in klass.allItems():
            if isinstance(func, etgtools.FunctionDef) and func.name.startswith('Create'):
                func.factory = True
    
    c = module.find('wxGraphicsContext')
    markFactories(c)
    c.abstract = True
    
    # FIXME: Handle wxEnhMetaFileDC?
    c.find('Create').findOverload('wxEnhMetaFileDC').ignore()
    
    # FIXME: Reintroduce the default value once we get wxBLACK and co. working
    c.find('CreateFont.col').default = ''
    
    c = module.find('wxGraphicsPath')
    c.find('GetBox').findOverload('wxDouble *x, wxDouble *y').ignore()
    c.find('GetCurrentPoint').findOverload('wxDouble *x, wxDouble *y').ignore()
    
    c = module.find('wxGraphicsRenderer')
    markFactories(c)
    c.abstract = True
    
    # FIXME: Handle wxEnhMetaFileDC?
    c.find('CreateContext').findOverload('wxEnhMetaFileDC').ignore()

    # FIXME: Reintroduce the default value once we get wxBLACK and co. working
    c.find('CreateFont.col').default = ''
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.
    

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.addGetterSetterProps(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

