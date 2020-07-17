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

    # Grab some MethodDefs that need to be copied to wxGenericAnimationCtrl
    play = c.find('Play')
    play.isVirtual = True
    others = [
        c.find('Stop'),
        c.find('IsPlaying'),
        c.find('Load'),
        c.find('LoadFile'),
        c.find('GetAnimation'),
        c.find('SetAnimation'),
        c.find('SetInactiveBitmap'),
        c.find('GetInactiveBitmap'),
        c.find('CreateAnimation'),
        c.find('CreateCompatibleAnimation'),
    ]
    nonvirtual = [ 'GetAnimation', 'GetInactiveBitmap', 'CreateAnimation',
                   'CreateCompatibleAnimation',
                   ]


    c = module.find('wxGenericAnimationCtrl')
    c.bases = ['wxControl']
    c.addHeaderCode('#include <wx/generic/animate.h>')
    tools.fixWindowClass(c)

    # Insert a copy of the base class Play into this class. It's not in the
    # interface docs, but sip needs to see it there, since the one that is there
    # has a different signature.
    c.find('Play').overloads.append(play)

    # Since we pretend that the base class is wxControl (because there are
    # different parents in different builds) then we need to copy in some
    # methods it will be inheriting from the real base class, which is not
    # public.
    for m in others:
        if m.name not in nonvirtual:
            m.isVirtual = True
        c.addItem(m)



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

