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

    # TODO: We'll need a different way to handle things when the native version
    # is configured. The stubs generator expects that it is an all or nothing
    # situaton, but that is not the case for wxAnimation and wxAnimationCtrl...

    # module.addHeaderCode('#include <wx/animate.h>')
    # tools.generateStubs('wxUSE_GENERIC_ANIMATIONCTRL', module,
    #                      typeValMap={'wxAnimation': 'wxNullAnimation',
    #                                  'wxAnimationDisposal': 'wxANIM_UNSPECIFIED',
    #                                  'wxAnimationType': 'wxANIMATION_TYPE_INVALID',
    #                       },)

    c = module.find('wxAnimation')
    assert isinstance(c, etgtools.ClassDef)

    #c.find('GetHandlers').ignore()
    module.addItem(tools.wxListWrapperTemplate('wxAnimationDecoderList', 'wxAnimationDecoder', module,
                                               header_extra='#include <wx/animate.h>'))


    c = module.find('wxAnimationCtrl')
    tools.fixWindowClass(c)
    module.addGlobalStr('wxAnimationCtrlNameStr', c)

    # Add the generic class too
    gen = tools.copyClassDef(c, 'wxGenericAnimationCtrl')
    module.insertItemAfter(c, gen)

    # move this before wxAnimationCtrl so it can be used for default arg values
    item = module.find('wxNullAnimation')
    module.items.remove(item)
    module.insertItemBefore(c, item)


    #-----------------------------------------------------------------
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

