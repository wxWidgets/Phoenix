#---------------------------------------------------------------------------
# Name:        etg/geometry.py
# Author:      Robin Dunn
#
# Created:     4-Nov-2010
# Copyright:   (c) 2010-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

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

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode('#include <wx/wx.h>')


    #---------------------------------------
    # wxPoint2D and wxRect2D tweaks

    c = module.find('wxPoint2DDouble')
    c.renameClass('Point2D')
    c.find('wxPoint2DDouble').findOverload('wxPoint2DInt').ignore()

    c.find('m_x').pyName = 'x'
    c.find('m_y').pyName = 'y'
    c.find('GetFloor.x').out = True
    c.find('GetFloor.y').out = True
    c.find('GetRounded.x').out = True
    c.find('GetRounded.y').out = True

    # these have link errors
    c.find('operator/=').findOverload('wxDouble').ignore()
    c.find('operator*=').findOverload('wxDouble').ignore()


    c.convertFromPyObject = tools.convertTwoDoublesTemplate('wxPoint2DDouble')

    c.addCppMethod('PyObject*', 'Get', '()', """\
        wxPyThreadBlocker blocker;
        return sipBuildResult(0, "(dd)", self->m_x, self->m_y);
        """,
        briefDoc="""\
        Get() -> (x,y)\n
        Return the x and y properties as a tuple.""")

    tools.addGetIMMethodTemplate(module, c, ['x', 'y'])

    # Add sequence protocol methods and other goodies
    c.addPyMethod('__str__', '(self)',             'return str(self.Get())')
    c.addPyMethod('__repr__', '(self)',            'return "wx.Point2D"+str(self.Get())')
    c.addPyMethod('__len__', '(self)',             'return len(self.Get())')
    c.addPyMethod('__nonzero__', '(self)',         'return self.Get() != (0,0)')
    c.addPyMethod('__bool__', '(self)',            'return self.Get() != (0,0)')
    c.addPyMethod('__reduce__', '(self)',          'return (Point2D, self.Get())')
    c.addPyMethod('__getitem__', '(self, idx)',    'return self.Get()[idx]')
    c.addPyMethod('__setitem__', '(self, idx, val)',
                  """\
                  if idx == 0: self.x = val
                  elif idx == 1: self.y = val
                  else: raise IndexError
                  """)
    c.addPyCode('Point2D.__safe_for_unpickling__ = True')


    # ignore these operator methods, since we are not wrapping the Int version
    c.find('operator*=').findOverload('wxInt32').ignore()
    c.find('operator/=').findOverload('wxInt32').ignore()


    # ignore all the global operators too, there is no equivallent in Python
    for item in module:
        if isinstance(item, etgtools.FunctionDef) and item.name.startswith('operator'):
            for f in item.all():
                f.ignore()


    c = module.find('wxRect2DDouble')
    c.renameClass('Rect2D')
    c.find('m_x').pyName = 'x'
    c.find('m_y').pyName = 'y'
    c.find('m_width').pyName = 'width'
    c.find('m_height').pyName = 'height'

    c.convertFromPyObject = tools.convertFourDoublesTemplate('wxRect2DDouble')

    c.addCppMethod('PyObject*', 'Get', '()', """\
        wxPyThreadBlocker blocker;
        return sipBuildResult(0, "(dddd)",
                    self->m_x, self->m_y, self->m_width, self->m_height);
        """,
        briefDoc="""\
        Get() -> (x, y, width, height)\n
        Return the rectangle's properties as a tuple.""")

    tools.addGetIMMethodTemplate(module, c, ['x', 'y', 'width', 'height'])

    # Add sequence protocol methods and other goodies
    c.addPyMethod('__str__', '(self)',             'return str(self.Get())')
    c.addPyMethod('__repr__', '(self)',            'return "wx.Rect2D"+str(self.Get())')
    c.addPyMethod('__len__', '(self)',             'return len(self.Get())')
    c.addPyMethod('__nonzero__', '(self)',         'return self.Get() != (0,0,0,0)')
    c.addPyMethod('__bool__', '(self)',            'return self.Get() != (0,0,0,0)')
    c.addPyMethod('__reduce__', '(self)',          'return (Rect2D, self.Get())')
    c.addPyMethod('__getitem__', '(self, idx)',    'return self.Get()[idx]')
    c.addPyMethod('__setitem__', '(self, idx, val)',
                  """\
                  if idx == 0: self.x = val
                  elif idx == 1: self.y = val
                  elif idx == 2: self.width = val
                  elif idx == 3: self.height = val
                  else: raise IndexError
                  """)
    c.addPyCode('Rect2D.__safe_for_unpickling__ = True')


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)



#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

