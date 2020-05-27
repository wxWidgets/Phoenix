#---------------------------------------------------------------------------
# Name:        etg/menuitem.py
# Author:      Robin Dunn
#
# Created:     10-Sept-2011
# Copyright:   (c) 2011-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "menuitem"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxMenuItem' ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.


    c = module.find('wxMenuItem')
    assert isinstance(c, etgtools.ClassDef)
    c.addPrivateCopyCtor()
    tools.removeVirtuals(c)

    c.find('wxMenuItem.subMenu').transfer = True
    c.find('SetSubMenu.menu').transfer = True

    # deprecated and removed
    c.find('GetLabel').ignore()
    c.find('GetName').ignore()
    c.find('GetText').ignore()
    c.find('SetText').ignore()
    c.find('GetLabelFromText').ignore()


    # These are MSW only. Make them be empty stubs for the other ports
    c.find('GetBackgroundColour').type = 'const wxColour*'
    c.find('GetBackgroundColour').setCppCode("""\
        #ifdef __WXMSW__
            return &self->GetBackgroundColour();
        #else
            return &wxNullColour;
        #endif
        """)

    c.find('SetBackgroundColour').setCppCode("""\
        #ifdef __WXMSW__
            self->SetBackgroundColour(*colour);
        #endif
        """)

    c.find('GetFont').type = 'const wxFont*'
    c.find('GetFont').setCppCode("""\
        #ifdef __WXMSW__
            return &self->GetFont();
        #else
            return &wxNullFont;
        #endif
        """)

    c.find('SetFont').setCppCode("""\
        #ifdef __WXMSW__
            self->SetFont(*font);
        #endif
        """)

    c.find('GetMarginWidth').setCppCode("""\
        #ifdef __WXMSW__
            return self->GetMarginWidth();
        #else
            return -1;
        #endif
        """)

    c.find('SetMarginWidth').setCppCode("""\
        #ifdef __WXMSW__
            self->SetMarginWidth(width);
        #endif
        """)

    c.find('GetTextColour').type = 'const wxColour*'
    c.find('GetTextColour').setCppCode("""\
        #ifdef __WXMSW__
            return &self->GetTextColour();
        #else
            return &wxNullColour;
        #endif
        """)

    c.find('SetTextColour').setCppCode("""\
        #ifdef __WXMSW__
            self->SetTextColour(*colour);
        #endif
        """)


    c.find('GetBitmap').type = 'const wxBitmap*'
    c.find('GetBitmap').setCppCode("""\
        #ifdef __WXMSW__
            return &self->GetBitmap(checked);
        #else
            return &self->GetBitmap();
        #endif
        """)

    c.find('SetBitmap').setCppCode("""\
        #ifdef __WXMSW__
            self->SetBitmap(*bmp, checked);
        #else
            self->SetBitmap(*bmp); // no checked arg in this case
        #endif
        """)

    c.find('SetBitmaps').setCppCode("""\
        #ifdef __WXMSW__
            self->SetBitmaps(*checked, *unchecked);
        #else
            self->SetBitmap(*checked);
        #endif
        """)


    c.find('GetDisabledBitmap').type = 'const wxBitmap*'
    c.find('GetDisabledBitmap').setCppCode("""\
        #ifdef __WXMSW__
            return &self->GetDisabledBitmap();
        #else
            return &wxNullBitmap;
        #endif
        """)

    c.find('SetDisabledBitmap').setCppCode("""\
        #ifdef __WXMSW__
            self->SetDisabledBitmap(*disabled);
        #endif
        """)

    c.addAutoProperties()
    c.addItem(etgtools.PropertyDef('Enabled', 'IsEnabled', 'Enable'))

    c.find('GetAccel').factory = True
    c.find('GetAccelFromString').ignore()  # Not implemented anywere?

    module.addItem(tools.wxListWrapperTemplate('wxMenuItemList', 'wxMenuItem', module))



    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

