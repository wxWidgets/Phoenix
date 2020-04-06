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
           "wxGenericAnimationCtrl",
           "wxAnimationDecoder",
           "wxANIDecoder",
           "wxGIFDecoder",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxAnimationCtrl')
    tools.fixWindowClass(c)
    play = c.find('Play')

    c = module.find('wxGenericAnimationCtrl')
    tools.fixWindowClass(c)
    # Insert a copy of the base class Play into this class. It's not in the
    # inteface docs, but sip needs to see it there.
    c.find('Play').overloads.append(play)

    module.addGlobalStr('wxAnimationCtrlNameStr', c)


    # move this before wxAnimationCtrl so it can be used for default arg values
    item = module.find('wxNullAnimation')
    module.items.remove(item)
    module.insertItemBefore(c, item)


    #-----------------------------------------------------------------
    module.addItem(tools.wxListWrapperTemplate('wxAnimationDecoderList', 'wxAnimationDecoder', module,
                                               header_extra='#include <wx/animate.h>'))

    c = module.find('wxAnimationDecoder')
    c.find('DoCanRead').ignore(False)

    c = module.find('wxANIDecoder')
    c.find('DoCanRead').ignore(False)

    c = module.find('wxGIFDecoder')
    c.find('DoCanRead').ignore(False)


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

