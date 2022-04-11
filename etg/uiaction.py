#---------------------------------------------------------------------------
# Name:        etg/uiaction.py
# Author:      Robin Dunn
#
# Created:     09-Feb-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "uiaction"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxUIActionSimulator",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    tools.generateStubs('wxUSE_UIACTIONSIMULATOR', module,
                        # extraHdrCode='',
                        # typeValMap={}
                        )

    c = module.find('wxUIActionSimulator')
    assert isinstance(c, etgtools.ClassDef)
    c.addPrivateCopyCtor()
    c.addPrivateAssignOp()

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

