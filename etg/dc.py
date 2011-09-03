#---------------------------------------------------------------------------
# Name:        etg/stattext.py
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
NAME      = "dc"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ 'wxDC' ]    
    
#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.
    
        
    c = module.find('wxDC')
    assert isinstance(c, etgtools.ClassDef)

    c.addPrivateCopyCtor()
    tools.removeVirtuals(c)
    
    # rename the more complex overload for these two, like in classic wxPython
    c.find('GetTextExtent').findOverload('wxCoord *').pyName = 'GetFullTextExtent'
    c.find('GetMultiLineTextExtent').findOverload('wxCoord *').pyName = 'GetFullMultiLineTextExtent'
    
    # Switch this one to return the array instead of passing it through an arg
    c.find('GetPartialTextExtents').ignore()
    c.addCppMethod('wxArrayInt', 'GetPartialTextExtents', '(const wxString& text)', """\
                    wxArrayInt rval;
                    self->GetPartialTextExtents(*text, rval);
                    return rval;""")
                   
    
    # Keep the wxSize overloads of these
    c.find('GetSize').findOverload('wxCoord').ignore()
    c.find('GetSizeMM').findOverload('wxCoord').ignore()
    
    # needs wxAffineMatrix2D support.
    c.find('GetTransformMatrix').ignore()
    c.find('SetTransformMatrix').ignore()
        
    # remove wxPoint* overloads, we use the wxPointList ones
    c.find('DrawLines').findOverload('wxPoint points').ignore()
    c.find('DrawPolygon').findOverload('wxPoint points').ignore()
    c.find('DrawPolyPolygon').findOverload('wxPoint points').ignore()
    c.find('DrawSpline').findOverload('wxPoint points').ignore()
    
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.addGetterSetterProps(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

