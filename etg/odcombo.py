#---------------------------------------------------------------------------
# Name:        etg/odcombo.py
# Author:      Robin Dunn
#
# Created:     04-Jun-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_adv"
NAME      = "odcombo"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxOwnerDrawnComboBox",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode('#include <wx/odcombo.h>')

    c = module.find('wxOwnerDrawnComboBox')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixWindowClass(c)


    # Ignore the old C array version of the ctor and Create methods, and
    # fixup the remaining ctor and Create with the typical default values for
    # the args
    c.find('wxOwnerDrawnComboBox').findOverload('wxString choices').ignore()
    m = c.find('wxOwnerDrawnComboBox').findOverload('wxArrayString')
    m.find('value').default = 'wxEmptyString'
    m.find('choices').default = 'wxArrayString()'

    c.find('Create').ignore()
    c.find('Create').findOverload('wxString choices').ignore()
    m = c.find('Create').findOverload('wxArrayString')
    m.find('value').default = 'wxEmptyString'
    m.find('choices').default = 'wxArrayString()'

    c.find('IsEmpty').ignore()

    # Unignore the protected methods that should be overridable in Python
    c.find('OnDrawBackground').ignore(False).isVirtual = True
    c.find('OnDrawItem').ignore(False).isVirtual = True
    c.find('OnMeasureItem').ignore(False).isVirtual = True
    c.find('OnMeasureItemWidth').ignore(False).isVirtual = True


    # wxItemContainer pure virtuals that have an implementation in this class
    tools.fixItemContainerClass(c, False)
    c.addItem(etgtools.WigCode("""\
        virtual wxString GetStringSelection() const;
        %MethodCode
            sipRes = new wxString(sipCpp->wxItemContainerImmutable::GetStringSelection());
        %End
        %VirtualCallCode
            sipRes = wxItemContainerImmutable::GetStringSelection();
        %End
        """))

    # wxComboCtrl virtuals that have an implementation in this class
    c.addItem(etgtools.WigCode("""\
        protected:
        virtual void DoSetPopupControl(wxComboPopup* popup);
        virtual void DoShowPopup(const wxRect& rect, int flags);
        """))


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

