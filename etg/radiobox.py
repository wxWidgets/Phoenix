#---------------------------------------------------------------------------
# Name:        etg/radiobox.py
# Author:      Kevin Ollivier
#              Robin Dunn
#
# Created:     16-Sept-2011
# Copyright:   (c) 2011 by Kevin Ollivier
# Copyright:   (c) 2011-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "radiobox"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxRadioBox' ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxRadioBox')
    assert isinstance(c, etgtools.ClassDef)

    module.addGlobalStr('wxRadioBoxNameStr', c)

    c.find('wxRadioBox').findOverload('wxString choices').ignore()
    c.find('Create').findOverload('wxString choices').ignore()

    c.find('wxRadioBox').findOverload('wxArrayString').find('label').default = 'wxEmptyString'
    c.find('Create').findOverload('wxArrayString').find('label').default = 'wxEmptyString'
    c.find('wxRadioBox').findOverload('wxArrayString').find('choices').default = 'wxArrayString()'
    c.find('Create').findOverload('wxArrayString').find('choices').default = 'wxArrayString()'

    # Avoid name clashes with base class methods with different signatures
    c.find('Enable').pyName = 'EnableItem'
    c.find('Show').pyName = 'ShowItem'

    c.addPyMethod('GetItemLabel', '(self, n)',
                  doc="""\
                  GetItemLabel(self, n) -> string\n
                  Return the text of the n'th item in the radio box.""",
                  body='return self.GetString(n)')
    c.addPyMethod('SetItemLabel', '(self, n, text)',
                  doc="""\
                  SetItemLabel(self, n, text)\n
                  Set the text of the n'th item in the radio box.""",
                  body='self.SetString(n, text)')


    tools.fixWindowClass(c)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

