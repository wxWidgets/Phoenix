#---------------------------------------------------------------------------
# Name:        etg/combo.py
# Author:      Robin Dunn
#
# Created:     31-May-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "combo"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxComboPopup",
           "wxComboCtrlFeatures",
           "wxComboCtrl",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxComboPopup')
    assert isinstance(c, etgtools.ClassDef)
    c.mustHaveApp()


    c = module.find('wxComboCtrl')
    tools.fixWindowClass(c)

    # These are protected methods that need to be unignored and also add back
    # their virtual flags
    for name in ['AnimateShow', 'DoSetPopupControl', 'DoShowPopup']:
        c.find(name).ignore(False)
        c.find(name).isVirtual = True

    # other methods that need the virtual flag turned back on
    for name in ['IsKeyPopupToggle', 'ShowPopup', 'HidePopup', 'OnButtonClick',
                 'DoShowPopup', 'Dismiss',]:  # 'Cut', 'Copy', 'Paste', ?
        c.find(name).isVirtual = True

    c.find('SetPopupControl.popup').transfer = True

    # from is a reserved word
    c.find('Remove.from').name = 'frm'
    c.find('Replace.from').name = 'frm'
    c.find('SetSelection.from').name = 'frm'


    # deprecated and removed
    c.find('GetTextIndent').ignore()
    c.find('SetTextIndent').ignore()

    #tools.fixItemContainerClass(c, False)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

