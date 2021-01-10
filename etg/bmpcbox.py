#---------------------------------------------------------------------------
# Name:        etg/bmpcbox.py
# Author:      Robin Dunn
#
# Created:     05-Jun-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_adv"
NAME      = "bmpcbox"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxBitmapComboBox",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode("#include <wx/bmpcbox.h>")

    c = module.find('wxBitmapComboBox')
    assert isinstance(c, etgtools.ClassDef)
    module.addGlobalStr('wxBitmapComboBoxNameStr', c)
    tools.fixWindowClass(c)

    # The MSW and GTK version of this class derive from wxComboBox, but the
    # OSX version derives from wxOwnerDrawnCombo. To make all platforms happy
    # with the generated wrapper code switch the declared base with the bases
    # that both of those classes have in common.
    c.bases = ['wxControl', 'wxTextEntry', 'wxItemContainer']

    # Copy any method definitions from wx.ComboBox that are not declared here
    import combobox
    mod = combobox.parseAndTweakModule()
    klass = mod.find('wxComboBox')
    items = [item for item in klass.items if isinstance(item, etgtools.MethodDef) and
                                             not item.isCtor and
                                             not item.isDtor and
                                             not item.ignored and
                                             not c.findItem(item.name)]
    c.items.extend(items)
    #print([i.name for i in items])
    c.find('GetCurrentSelection').ignore()

    # Ignore the old C array version of the ctor and Create methods, and
    # fixup the remaining ctor and Create with the typical default values for
    # the args
    c.find('wxBitmapComboBox').findOverload('wxString choices').ignore()
    m = c.find('wxBitmapComboBox').findOverload('wxArrayString')
    m.find('value').default = 'wxEmptyString'
    m.find('choices').default = 'wxArrayString()'
    m.find('style').default = '0'

    c.find('Create').findOverload('wxString choices').ignore()
    m = c.find('Create').findOverload('wxArrayString')
    m.find('value').default = 'wxEmptyString'
    m.find('choices').default = 'wxArrayString()'

    # Ignore the Append and Insert taking a void* for clientData
    c.find('Append').findOverload('void *').ignore()
    c.find('Insert').findOverload('void *').ignore()

    # And set the ownership transfer for the other one
    c.find('Append').findOverload('wxClientData *').find('clientData').transfer = True
    c.find('Insert').findOverload('wxClientData *').find('clientData').transfer = True

    # We need to disambiguate GetStringSelection since it is implemented in
    # multiple base classes
    c.find('GetStringSelection').ignore()
    c.addItem(etgtools.WigCode("""\
        virtual wxString GetStringSelection() const;
        %MethodCode
            sipRes = new wxString(sipCpp->wxItemContainerImmutable::GetStringSelection());
        %End
        %VirtualCallCode
            sipRes = wxItemContainerImmutable::GetStringSelection();
        %End
        """))

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

