#---------------------------------------------------------------------------
# Name:        etg/bookctrl.py
# Author:      Robin Dunn
#
# Created:     31-Aug-2011
# Copyright:   (c) 2011-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "bookctrl"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'interface_2wx_2bookctrl_8h.xml',
           'wxBookCtrlBase',
           'wxBookCtrlEvent',
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    # Ignore the macro.  We'll add a Python alias in notebook.py instead.
    module.find('wxBookCtrl').ignore()

    c = module.find('wxBookCtrlBase')
    assert isinstance(c, etgtools.ClassDef)
    c.abstract = True

    c.find('HitTest.flags').out = True


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

