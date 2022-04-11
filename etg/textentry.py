#---------------------------------------------------------------------------
# Name:        etg/textentry.py
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
NAME      = "textentry"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxTextEntry", ]

#---------------------------------------------------------------------------

def parseAndTweakModule():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING, False)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxTextEntry')
    assert isinstance(c, etgtools.ClassDef)
    c.abstract = True
    tools.removeVirtuals(c)

    c.find('GetSelection.from').out = True
    c.find('GetSelection.to').out = True
    c.find('GetRange.from').name = 'from_'
    c.find('GetRange.to').name = 'to_'
    c.find('Remove.from').name = 'from_'
    c.find('Remove.to').name = 'to_'
    c.find('Replace.from').name = 'from_'
    c.find('Replace.to').name = 'to_'
    c.find('SetSelection.from').name = 'from_'
    c.find('SetSelection.to').name = 'to_'
    c.find('AutoComplete').findOverload('wxTextCompleter').find('completer').transfer = True

    # Re-enable virtualness for (Can)Cut/Copy/Paste/Undo/Redo
    tools.fixTextClipboardMethods(c)

    return module

#-----------------------------------------------------------------
def run():
    module = parseAndTweakModule()
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

