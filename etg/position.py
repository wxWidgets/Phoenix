#---------------------------------------------------------------------------
# Name:        etg/position.py
# Author:      Robin Dunn
#
# Created:     20-Dec-2011
# Copyright:   (c) 2011-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "position"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxPosition", ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxPosition')
    assert isinstance(c, etgtools.ClassDef)

    # (r,c) --> wxPosition typemap
    c.convertFromPyObject = tools.convertTwoIntegersTemplate('wxPosition')

    c.addCppMethod('PyObject*', 'Get', '()', """\
        wxPyThreadBlocker blocker;
        return sipBuildResult(0, "(ii)", self->GetRow(), self->GetCol());
        """,
        pyArgsString="() -> (row,col)",
        briefDoc="Return the row and col properties as a tuple.")

    tools.addGetIMMethodTemplate(module, c, ['Row', 'Col'])

    # Add sequence protocol methods and other goodies
    c.addPyMethod('__str__', '(self)',             'return str(self.Get())')
    c.addPyMethod('__repr__', '(self)',            'return "wx.Position"+str(self.Get())')
    c.addPyMethod('__len__', '(self)',             'return len(self.Get())')
    c.addPyMethod('__nonzero__', '(self)',         'return self.Get() != (0,0)')
    c.addPyMethod('__bool__', '(self)',            'return self.Get() != (0,0)')
    c.addPyMethod('__reduce__', '(self)',          'return (Position, self.Get())')
    c.addPyMethod('__getitem__', '(self, idx)',    'return self.Get()[idx]')
    c.addPyMethod('__setitem__', '(self, idx, val)',
                  """\
                  if idx == 0: self.Row = val
                  elif idx == 1: self.Col = val
                  else: raise IndexError
                  """)
    c.addPyCode('Position.__safe_for_unpickling__ = True')


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

