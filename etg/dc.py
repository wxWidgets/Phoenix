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
ITEMS  = [  'wxAutoBufferedPaintDC',
            'wxBufferedDC',
            'wxBufferedPaintDC',
            'wxDC',
            'wxClientDC', 
            'wxMemoryDC', 
            'wxPaintDC',
            'wxScreenDC',
            'wxWindowDC',
              ]    
    
#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.
    
    c = module.find('wxAutoBufferedPaintDC')
    c.addPrivateCopyCtor()
    
    c = module.find('wxBufferedDC')
    c.addPrivateCopyCtor()
    
    c = module.find('wxBufferedPaintDC')
    c.addPrivateCopyCtor()
    
    
    c = module.find('wxDC')
    c.addPrivateCopyCtor()
    c.find('GetMultiLineTextExtent').overloads = []
    c.find('GetTextExtent').overloads = []
    c.find('GetSize').overloads = []
    c.find('GetSizeMM').overloads = []
    
    # needs wxAffineMatrix2D support.
    c.find('GetTransformMatrix').ignore()
    c.find('SetTransformMatrix').ignore()
    
    # TODO: restore this once we add wxArrayInt type map
    c.find('GetPartialTextExtents').ignore()
    
    # TODO: add wxFloodFillStyle type map
    c.find('FloodFill').ignore()
    c.find('FloodFill').findOverload('int style').ignore()
    
    # remove wxPoint* overloads, we use the wxPointList ones
    c.find('DrawLines').findOverload('wxPoint points').ignore()
    c.find('DrawPolygon').findOverload('wxPoint points').ignore()
    c.find('DrawPolyPolygon').findOverload('wxPoint points').ignore()
    c.find('DrawSpline').findOverload('wxPoint points').ignore()
    
    c = module.find('wxClientDC')
    c.addPrivateCopyCtor()
    
    c = module.find('wxWindowDC')
    c.addPrivateCopyCtor()
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.addGetterSetterProps(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

