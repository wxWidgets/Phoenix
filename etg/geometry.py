#---------------------------------------------------------------------------
# Name:        geometry.py
# Author:      Robin Dunn
#
# Created:     4-Nov-2010
# RCS-ID:      $Id:$
# Copyright:   (c) 2010 by Total Control Software
# Licence:     wxWindows license
#---------------------------------------------------------------------------

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "geometry"
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ 
    'wxPoint2DDouble',
    'wxRect2DDouble',
]    
    
#---------------------------------------------------------------------------
# Parse the XML file(s) building a collection of Extractor objects

import etgtools
module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
etgtools.parseDoxyXML(module, ITEMS)

#---------------------------------------------------------------------------
# Tweak the parsed meta objects in the module object as needed for customizing
# the generated code and docstrings.

import etgtools.tweaker_tools
etgtools.tweaker_tools.ignoreAssignmentOperators(module)
etgtools.tweaker_tools.removeWxPrefixes(module)


module.addHeaderCode('#include <wx/wx.h>')


#---------------------------------------
# wxPoint2D and wxRect2D tweaks

c = module.find('wxPoint2DDouble')
c.pyName = 'Point2D'
c.find('wxPoint2DDouble').findOverload('wxPoint2DInt').ignore()

c.find('m_x').pyName = 'x'
c.find('m_y').pyName = 'y'
c.find('GetFloor.x').out = True
c.find('GetFloor.y').out = True
c.find('GetRounded.x').out = True
c.find('GetRounded.y').out = True

# these have link errors
c.find('SetPolarCoordinates').ignore()
c.find('operator/=').findOverload('wxDouble').ignore()
c.find('operator*=').findOverload('wxDouble').ignore()


# ignore these operator methods, since we are not wrapping the Int version
c.find('operator*=').findOverload('wxInt32').ignore()
c.find('operator/=').findOverload('wxInt32').ignore()

# ignore some of the global operators too
for item in module:
    if isinstance(item, etgtools.FunctionDef) and item.type == 'wxPoint2DInt':
        item.ignore()
    if item.name in ['operator*', 'operator/'] and 'wxInt32' in item.argsString:
        item.ignore()
    
        
c = module.find('wxRect2DDouble')
c.pyName = 'Rect2D'
c.find('m_x').pyName = 'x'
c.find('m_y').pyName = 'y'
c.find('m_width').pyName = 'width'
c.find('m_height').pyName = 'height'


#---------------------------------------------------------------------------
#---------------------------------------------------------------------------
# Run the generators

# Create the code generator and make the wrapper code
wg = etgtools.getWrapperGenerator()
wg.generate(module)

# Create a documentation generator and let it do its thing
dg = etgtools.getDocsGenerator()
dg.generate(module)

#---------------------------------------------------------------------------
