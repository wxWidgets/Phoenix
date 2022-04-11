#---------------------------------------------------------------------------
# Name:        etg/textcompleter.py
# Author:      Robin Dunn
#
# Created:     03-Nov-2011
# Copyright:   (c) 2011-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "textcompleter"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxTextCompleter",
           "wxTextCompleterSimple",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING, False)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = tc = module.find('wxTextCompleter')
    assert isinstance(c, etgtools.ClassDef)
    c.addPrivateCopyCtor()
    c.addDefaultCtor(prot='public')

    c = module.find('wxTextCompleterSimple')
    c.addDefaultCtor(prot='public')
    c.copyFromClass(tc, 'Start')
    c.copyFromClass(tc, 'GetNext')

    # Change GetCompletions to return the wxArrayString instead of passing it
    # as a parameter
    c.find('GetCompletions.res').out = True


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

