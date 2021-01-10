#---------------------------------------------------------------------------
# Name:        etg/choice.py
# Author:      Kevin Ollivier
#
# Created:     26-Aug-2011
# Copyright:   (c) 2013 by Wide Open Technologies
# Copyright:   (c) 2011-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "choice"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxChoice' ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxChoice')
    c.abstract = False
    c.find('wxChoice').findOverload('wxString choices').ignore()
    c.find('wxChoice').findOverload('wxArrayString').find('choices').default = 'wxArrayString()'

    c.find('Create').findOverload('wxString choices').ignore()
    c.find('Create').findOverload('wxArrayString').find('choices').default = 'wxArrayString()'

    tools.fixItemContainerClass(c, False)
    tools.fixWindowClass(c)

    module.addGlobalStr('wxChoiceNameStr', c)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

