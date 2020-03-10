#---------------------------------------------------------------------------
# Name:        etg/settings.py
# Author:      Robin Dunn
#
# Created:     07-Apr-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "settings"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxSystemSettings",
           "wxSystemAppearance",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxSystemSettings')
    assert isinstance(c, etgtools.ClassDef)
    c.mustHaveApp()
    c.find('GetColour').mustHaveApp()
    c.find('GetFont').mustHaveApp()
    c.find('GetMetric').mustHaveApp()
    c.find('HasFeature').mustHaveApp()
    c.find('GetScreenType').mustHaveApp()


    c = module.find('wxSystemAppearance')
    assert isinstance(c, etgtools.ClassDef)
    c.addPrivateDefaultCtor()

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

