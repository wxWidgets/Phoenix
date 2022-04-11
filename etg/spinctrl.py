#---------------------------------------------------------------------------
# Name:        etg/spinctrl.py
# Author:      Kevin Ollivier
#              Robin Dunn
#
# Created:     16-Sept-2011
# Copyright:   (c) 2011 by Kevin Ollivier
# Copyright:   (c) 2011-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "spinctrl"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxSpinCtrl',
           'wxSpinCtrlDouble',
           'wxSpinDoubleEvent',
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode("#include <wx/spinctrl.h>")

    c = module.find('wxSpinCtrl')
    assert isinstance(c, etgtools.ClassDef)
    c.addPyMethod('GetRange', '(self)', 'return (self.GetMin(), self.GetMax())')
    c.addPyMethod('SetMin', '(self, minVal)', 'self.SetRange(minVal, self.GetMax())')
    c.addPyMethod('SetMax', '(self, maxVal)', 'self.SetRange(self.GetMin(), maxVal)')
    c.find('SetSelection.from').name = 'from_'
    c.find('SetSelection.to').name = 'to_'
    tools.fixWindowClass(c)


    c = module.find('wxSpinCtrlDouble')
    c.addPyMethod('GetRange', '(self)', 'return (self.GetMin(), self.GetMax())')
    c.addPyMethod('SetMin', '(self, minVal)', 'self.SetRange(minVal, self.GetMax())')
    c.addPyMethod('SetMax', '(self, maxVal)', 'self.SetRange(self.GetMin(), maxVal)')
    tools.fixWindowClass(c)


    c = module.find('wxSpinDoubleEvent')
    tools.fixEventClass(c)

    module.addPyCode("""\
        EVT_SPINCTRL = wx.PyEventBinder( wxEVT_SPINCTRL, 1)
        EVT_SPINCTRLDOUBLE = wx.PyEventBinder( wxEVT_SPINCTRLDOUBLE, 1)

        # deprecated wxEVT aliases
        wxEVT_COMMAND_SPINCTRL_UPDATED        = wxEVT_SPINCTRL
        wxEVT_COMMAND_SPINCTRLDOUBLE_UPDATED  = wxEVT_SPINCTRLDOUBLE
        """)


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

