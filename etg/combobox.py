#---------------------------------------------------------------------------
# Name:        etg/combobox.py
# Author:      Kevin Ollivier
#              Robin Dunn
#
# Created:     09-Sept-2011
# Copyright:   (c) 2011 by Kevin Ollivier
# Copyright:   (c) 2011-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "combobox"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxComboBox' ]

#---------------------------------------------------------------------------

def parseAndTweakModule():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxComboBox')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixWindowClass(c)

    tools.fixTextClipboardMethods(c)

    c.find('wxComboBox').findOverload('wxString choices').ignore()
    c.find('wxComboBox').findOverload('wxArrayString').find('choices').default = 'wxArrayString()'
    c.find('wxComboBox').findOverload('wxArrayString').find('value').default = 'wxEmptyString'

    c.find('Create').findOverload('wxString choices').ignore()
    c.find('Create').findOverload('wxArrayString').find('choices').default = 'wxArrayString()'
    c.find('Create').findOverload('wxArrayString').find('value').default = 'wxEmptyString'

    # When the from,to are set as output parameters the overloaded methods
    # will be ambiguous, so let's give this one a new name.
    m = c.find('GetSelection').renameOverload('long *from, long *to', 'GetTextSelection')
    m.find('from').out = True
    m.find('to').out = True

    # For SetSelection we want to keep the existing method since it is
    # inherited from base classes and has no ambiguities, so just add a new
    # method for SetTextSelection instead of renaming.
    orig = c.find('SetSelection').findOverload('from')
    orig.find('from').name = 'from_'
    orig.find('to').name = 'to_'
    m = etgtools.CppMethodDef.FromMethod(orig)
    m.overloads = []
    m.name = 'SetTextSelection'
    m.argsString = '(long from_, long to_)'
    m.body = "self->SetSelection(from_, to_);"
    c.insertItemAfter(c.find('SetSelection'), m)


    # The docs say to not use this one.
    c.find('IsEmpty').ignore()

    c.addPyCode("ComboBox.SetMark = wx.deprecated(ComboBox.SetTextSelection, 'Use SetTextSelection instead.')")
    c.addPyCode("ComboBox.GetMark = wx.deprecated(ComboBox.GetTextSelection, 'Use GetTextSelection instead.')")

    module.addGlobalStr('wxComboBoxNameStr', c)
    return module

#-----------------------------------------------------------------

def run():
    module = parseAndTweakModule()
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

