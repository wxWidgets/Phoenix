#---------------------------------------------------------------------------
# Name:        etg/cmdproc.py
# Author:      Robin Dunn
#
# Created:     16-Jul-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "cmdproc"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxCommand",
           "wxCommandProcessor",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode('#include <wx/cmdproc.h>')

    c = module.find('wxCommand')
    assert isinstance(c, etgtools.ClassDef)
    c.addPrivateCopyCtor()


    c = module.find('wxCommandProcessor')
    c.addPrivateCopyCtor()

    c.find('Submit.command').transfer = True
    c.find('Store.command').transfer = True

    module.addItem(
        tools.wxListWrapperTemplate('wxList', 'wxCommand', module,
                                    fakeListClassName='wxCommandList'))
    c.find('GetCommands').type = 'wxCommandList&'
    c.find('GetCommands').noCopy = True

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

