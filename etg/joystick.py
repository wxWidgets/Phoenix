#---------------------------------------------------------------------------
# Name:        etg/joystick.py
# Author:      Robin Dunn
#
# Created:     19-May-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools
from etgtools import MethodDef

PACKAGE   = "wx"
MODULE    = "_adv"
NAME      = "joystick"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxJoystick",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxJoystick')
    assert isinstance(c, etgtools.ClassDef)
    c.mustHaveApp()

    c.addItem(MethodDef(name='GetMaxButtons', type='int', isConst=True, argsString='() const'))
    c.addItem(MethodDef(name='GetMaxAxes', type='int', isConst=True, argsString='() const'))

    tools.generateStubs('wxUSE_JOYSTICK', module)


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

