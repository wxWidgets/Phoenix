#---------------------------------------------------------------------------
# Name:        etg/bmpcbox.py
# Author:      Robin Dunn
#
# Created:     05-Jun-2012
# Copyright:   (c) 2012-2018 by Total Control Software
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


    # Ignore the old C array verison of the ctor and Create methods, and
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


    # wxItemContainer pure virtuals that have an implementation in this class
    c.addItem(etgtools.WigCode("""\
        virtual unsigned int GetCount() const;
        virtual wxString GetString(unsigned int n) const;
        virtual void SetString(unsigned int n, const wxString& s);
        virtual int GetSelection() const;
        virtual void SetSelection(int n);

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

