#---------------------------------------------------------------------------
# Name:        etg/affinematrix2d.py
# Author:      Robin Dunn
#
# Created:     04-Apr-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "affinematrix2d"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxMatrix2D",
           "wxAffineMatrix2DBase",
           "wxAffineMatrix2D",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxAffineMatrix2DBase')
    assert isinstance(c, etgtools.ClassDef)
    c.abstract = True

    for c in [module.find('wxAffineMatrix2DBase'),
              module.find('wxAffineMatrix2D')]:

        c.find('Get.mat2D').out = True
        c.find('Get.tr').out = True

        c.find('TransformPoint.x').inOut = True
        c.find('TransformPoint.y').inOut = True

        c.find('TransformDistance.dx').inOut = True
        c.find('TransformDistance.dy').inOut = True

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

