#---------------------------------------------------------------------------
# Name:        etg/statusbar.py
# Author:      Kevin Ollivier
#
# Created:     16-Sept-2011
# Copyright:   (c) 2011 by Kevin Ollivier
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "statusbar"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxStatusBar', 'wxStatusBarPane', ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxStatusBar')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixWindowClass(c)
    module.addGlobalStr('wxStatusBarNameStr', c)

    # We already have a MappedType for wxArrayInt, so just tweak the
    # interface to use that instead of an array size and a const int pointer.
    tools.fixSetStatusWidths(c.find('SetStatusWidths'))

    # Same thing for SetStatusStyles
    m = c.find('SetStatusStyles')
    m.find('n').ignore()
    m.find('styles').type = 'const wxArrayInt&'
    m.argsString = '(int n, const wxArrayInt& styles)'
    m.setCppCode("""\
        const int* ptr = &styles->front();
        self->SetStatusStyles(styles->size(), ptr);
        """)

    # For SetFieldsCount just accept the number arg, and let the user set the
    # widths with SetStatusWidths like in Classic
    # TODO:
    #c.find('SetFieldsCount.widths').ignore()

    m = c.find('SetFieldsCount')
    m.find('widths').type = 'const wxArrayInt*'
    m.argsString = '(int number = 1, const wxArrayInt* widths = NULL)'
    m.setCppCode("""\
        if (widths) {
            const int* ptr = &widths->front();
            self->SetFieldsCount(number, ptr);
            }
        else {
            self->SetFieldsCount(number);
            }
        """)

    # Change GetFieldRect to return the rectangle (for Pythonicity and Classic compatibility)
    c.find('GetFieldRect').ignore()
    c.addCppMethod('wxRect*', 'GetFieldRect', '(int i)',
        doc="Returns the size and position of a field's internal bounding rectangle.",
        body="""\
            wxRect* r = new wxRect;
            self->GetFieldRect(i, *r);
            return r;
            """)


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

