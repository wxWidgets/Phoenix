#---------------------------------------------------------------------------
# Name:        etg/htmllbox.py
# Author:      Robin Dunn
#
# Created:     18-Mar-2013
# Copyright:   (c) 2013-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_html"
NAME      = "htmllbox"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxHtmlListBox",
           "wxSimpleHtmlListBox",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode("#include <wx/htmllbox.h>")


    c = module.find('wxHtmlListBox')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixWindowClass(c, False, False)
    tools.addWindowVirtuals(c)

    module.addGlobalStr('wxHtmlListBoxNameStr', c)

    # We only need one of these
    c.find('GetFileSystem').ignore()

    # let sip know that these pure virtuals have been implemented in this class
    c.addItem(etgtools.WigCode("""\
        protected:
        virtual void OnDrawItem(wxDC& dc, const wxRect& rect, size_t n) const;
        virtual wxCoord OnMeasureItem(size_t n) const;
        """))


    c = module.find('wxSimpleHtmlListBox')
    tools.fixWindowClass(c)

    # ignore the ctor and Create method taking the C array
    c.find('wxSimpleHtmlListBox').findOverload('int n').ignore()
    c.find('Create').findOverload('int n').ignore()

    c.find('wxSimpleHtmlListBox.choices').default = 'wxArrayString()'
    c.find('Create.choices').default = 'wxArrayString()'

    # let sip know that these pure virtuals have been implemented in this class
    tools.fixItemContainerClass(c, False)
    c.addItem(etgtools.WigCode("""\
        protected:
        virtual wxString OnGetItem(size_t n) const;
        """))

    module.addGlobalStr('wxSimpleHtmlListBoxNameStr', c)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

