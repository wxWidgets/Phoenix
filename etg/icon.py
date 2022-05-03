#---------------------------------------------------------------------------
# Name:        etg/icon.py
# Author:      Robin Dunn
#
# Created:     14-Nov-2011
# Copyright:   (c) 2011-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "icon"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxIcon", ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxIcon')
    assert isinstance(c, etgtools.ClassDef)
    tools.removeVirtuals(c)
    c.mustHaveApp()

    c.find('wxIcon').findOverload('*bits').ignore()
    c.find('wxIcon').findOverload('bits[]').ignore()

    c.find('wxIcon.type').default = 'wxBITMAP_TYPE_ANY'
    c.find('LoadFile.type').default = 'wxBITMAP_TYPE_ANY'

    c.find('ConvertToDisabled').ignore()

    c.addCppCtor('(const wxBitmap& bmp)',
        doc="Construct an Icon from a Bitmap.",
        body="""\
            wxIcon* icon = new wxIcon();
            icon->CopyFromBitmap(*bmp);
            return icon;
            """)

    c.addCppMethod('int', '__nonzero__', '()', "return self->IsOk();")
    c.addCppMethod('int', '__bool__', '()', "return self->IsOk();")

    c.addCppMethod('long', 'GetHandle', '()', """\
        #ifdef __WXMSW__
            return HandleToLong(self->GetHandle());
        #else
            return 0;
        #endif
        """)

    c.addCppMethod('void', 'SetHandle', '(long handle)', """\
        #ifdef __WXMSW__
            self->SetHandle((WXHANDLE)LongToHandle(handle));
        #endif
        """)

    c.find('CreateFromHICON').ignore()
    c.addCppMethod('bool', 'CreateFromHICON', '(long hicon)',
        doc='MSW-only method to create a wx.Icon from a native icon handle.',
        body="""\
            #ifdef __WXMSW__
                return self->CreateFromHICON((WXHICON)LongToHandle(hicon));
            #else
                return false;
            #endif
            """)

    # Documented wrongly in 3.1.6
    c.find('GetLogicalSize').type = 'wxSize'


    # For compatibility:
    module.addPyFunction('EmptyIcon', '()',
                         deprecated="Use :class:`Icon` instead",
                         doc='A compatibility wrapper for the :class:`Icon` constructor',
                         body='return Icon()')

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

