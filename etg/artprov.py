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

    # TEMPORARY WORKAROUND: The following will likely not be needed after an update to the
    # newest wxWidgets master...
    #
    # In C++ the art constants are actually macros that create a wxString on the fly, and
    # that doesn't work in the generated wrapper code because it tries to take the address
    # of the ID, but in reality it's a temporary object. So we'll create a new set of
    # globals which are actual global variables.
    artConsts = list()
    newConsts = list()
    newConsts_cpp = list()
    for item in module:
        if isinstance(item, etgtools.GlobalVarDef):
            if item.type in ['wxArtClient', 'wxArtID']:
                artConsts.append(item)

                # Make a new GlobalVarDef with the wx-less name as a wxString
                name = old_name = item.name
                name = name.replace('wx', '')
                gvd = etgtools.GlobalVarDef(type=item.type, name=name)
                newConsts.append(gvd)

                # add some c++ code to implement that new constant
                newConsts_cpp.append('{} {}({});'.format(item.type, name, old_name))

    # Now remove the old, add the new, and insert the c++ code
    for item in artConsts:
        module.items.remove(item)
    for item in newConsts:
        module.items.insert(0, item)
    module.addCppCode('\n'.join(newConsts_cpp))


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

