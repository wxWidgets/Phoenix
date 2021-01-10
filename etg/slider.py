#---------------------------------------------------------------------------
# Name:        etg/slider.py
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
NAME      = "slider"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxSlider' ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    def addDefaults(func):
        func.find('value').default = '0'
        func.find('minValue').default = '0'
        func.find('maxValue').default = '100'


    c = module.find('wxSlider')
    assert isinstance(c, etgtools.ClassDef)
    addDefaults(c.find('wxSlider'))
    addDefaults(c.find('Create'))

    module.addGlobalStr('wxSliderNameStr', c)

    c.addPyMethod('GetRange', '(self)', 'return (self.GetMin(), self.GetMax())')

    tools.fixWindowClass(c)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

