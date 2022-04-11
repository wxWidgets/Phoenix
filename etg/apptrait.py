#---------------------------------------------------------------------------
# Name:        etg/apptrait.py
# Author:      Robin Dunn
#
# Created:     22-Nov-2010
# Copyright:   (c) 2010-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "apptrait"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxAppTraits' ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.


    c = module.find('wxAppTraits')
    assert isinstance(c, etgtools.ClassDef)
    c.abstract = True


    # TODO: Enable these as etg scripts for their return types are added
    for name in [ 'CreateFontMapper',
                  'CreateMessageOutput',
                  'CreateRenderer',
                  ]:
        c.find(name).ignore()

    for name in [ 'CreateConfig',
                  'CreateEventLoop',
                  'CreateLogTarget',
                  #'GetStandardPaths',
                  ]:
        c.find(name).factory = True

    c.find('GetToolkitVersion.major').out = True
    c.find('GetToolkitVersion.minor').out = True
    c.find('GetToolkitVersion.micro').out = True

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

