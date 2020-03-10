#---------------------------------------------------------------------------
# Name:        etg/artprov.py
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
NAME      = "artprov"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxArtProvider",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.


    c = module.find('wxArtProvider')
    assert isinstance(c, etgtools.ClassDef)
    c.mustHaveApp()

    # These are protected and so they are ignored by default.  Unignore them.
    c.find('CreateBitmap').ignore(False)
    c.find('CreateIconBundle').ignore(False)

    # deal with ownership transfers
    c.find('Push.provider').transfer = True
    c.find('PushBack.provider').transfer = True
    c.find('Insert.provider').transfer = True
    c.find('Remove.provider').transferBack = True

    c.find('GetBitmap').mustHaveApp()
    c.find('GetIcon').mustHaveApp()

    # deprecated and removed
    c.find('Insert').ignore()

    # Change the types of the art constants from wxString to const char*
    # since that is what they really are.
    artConsts = list()
    for item in module:
        if isinstance(item, etgtools.GlobalVarDef):
            if item.type in ['wxArtClient', 'wxArtID']:
                item.type = 'const char*'
                artConsts.append(item)
    # move them to the front of the module
    for item in artConsts:
        module.items.remove(item)
        module.items.insert(0, item)


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

