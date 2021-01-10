#---------------------------------------------------------------------------
# Name:        etg/spinbutt.py
# Author:      Robin Dunn
#
# Created:     01-Nov-2011
# Copyright:   (c) 2011-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "spinbutt"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxSpinButton",
           "wxSpinEvent",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxSpinButton')
    assert isinstance(c, etgtools.ClassDef)

    c.addPyMethod('GetRange', '(self)', 'return (self.GetMin(), self.GetMax())')
    c.addPyMethod('SetMin', '(self, minVal)', 'self.SetRange(minVal, self.GetMax())')
    c.addPyMethod('SetMax', '(self, maxVal)', 'self.SetRange(self.GetMin(), maxVal)')
    module.addPyCode("""\
        EVT_SPIN_UP   = wx.PyEventBinder( wxEVT_SPIN_UP, 1)
        EVT_SPIN_DOWN = wx.PyEventBinder( wxEVT_SPIN_DOWN, 1)
        EVT_SPIN      = wx.PyEventBinder( wxEVT_SPIN, 1)
        """)

    tools.fixWindowClass(c)

    c = module.find('wxSpinEvent')
    tools.fixEventClass(c)


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

