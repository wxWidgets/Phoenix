#---------------------------------------------------------------------------
# Name:        etg/animate.py
# Author:      Robin Dunn
#
# Created:     21-May-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_adv"
NAME      = "animate"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxAnimation",
           "wxAnimationCtrl",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxAnimation')
    assert isinstance(c, etgtools.ClassDef)

    c = module.find('wxAnimationCtrl')
    tools.fixWindowClass(c)
    module.addGlobalStr('wxAnimationCtrlNameStr', c)

    # move this before wxAnimationCtrl so it can be used for default arg values
    item = module.find('wxNullAnimation')
    module.items.remove(item)
    module.insertItemBefore(c, item)


    # TODO: It would be nice to be able to use the generic verison on all
    # platforms since the native GTK version has some limitations...

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

