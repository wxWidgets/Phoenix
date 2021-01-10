#---------------------------------------------------------------------------
# Name:        etg/brush.py
# Author:      Robin Dunn
#
# Created:     2-Sept-2011
# Copyright:   (c) 2011-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "brush"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxBrush', 'wxBrushList', ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.


    c = module.find('wxBrush')
    assert isinstance(c, etgtools.ClassDef)
    tools.removeVirtuals(c)

    # Set mustHaveApp on all ctors except the default ctor
    for ctor in c.find('wxBrush').all():
        if ctor.isCtor and ctor.argsString != '()':
            ctor.mustHaveApp()

    c.addCppMethod('int', '__nonzero__', '()', "return self->IsOk();")
    c.addCppMethod('int', '__bool__', '()', "return self->IsOk();")

    c.addCppCode("""\
        #ifdef __WXMAC__
        #include <wx/osx/private.h>
        #endif
        """)
    c.addCppMethod('void', 'MacSetTheme', '(int macThemeBrushID)', """\
        #ifdef __WXMAC__
            self->SetColour(wxColour(wxMacCreateCGColorFromHITheme(macThemeBrushID)));
        #else
            wxPyRaiseNotImplemented();
        #endif
        """)


    c.addAutoProperties()


    # The stock Brush items are documented as simple pointers, but in reality
    # they are macros that evaluate to a function call that returns a brush
    # pointer, and that is only valid *after* the wx.App object has been
    # created. That messes up the code that SIP generates for them, so we need
    # to come up with another solution. So instead we will just create
    # uninitialized brush in a block of Python code, that will then be
    # initialized later when the wx.App is created.
    c.addCppMethod('void', '_copyFrom', '(const wxBrush* other)',
                   "*self = *other;",
                   briefDoc="For internal use only.")  # ??
    pycode = '# These stock brushes will be initialized when the wx.App object is created.\n'
    for item in module:
        if '_BRUSH' in item.name:
            item.ignore()
            pycode += '%s = Brush()\n' % tools.removeWxPrefix(item.name)
    module.addPyCode(pycode)


    # it is delay-initialized, see stockgdi.sip
    module.find('wxTheBrushList').ignore()


    # Some aliases that should be phased out eventually, (sooner rather than
    # later.) They are already gone (or wrapped by an #if) in the C++ code,
    # and so are not found in the documentation...
    module.addPyCode("""\
        wx.STIPPLE_MASK_OPAQUE = int(wx.BRUSHSTYLE_STIPPLE_MASK_OPAQUE)
        wx.STIPPLE_MASK        = int(wx.BRUSHSTYLE_STIPPLE_MASK)
        wx.STIPPLE             = int(wx.BRUSHSTYLE_STIPPLE)
        wx.BDIAGONAL_HATCH     = int(wx.BRUSHSTYLE_BDIAGONAL_HATCH)
        wx.CROSSDIAG_HATCH     = int(wx.BRUSHSTYLE_CROSSDIAG_HATCH)
        wx.FDIAGONAL_HATCH     = int(wx.BRUSHSTYLE_FDIAGONAL_HATCH)
        wx.CROSS_HATCH         = int(wx.BRUSHSTYLE_CROSS_HATCH)
        wx.HORIZONTAL_HATCH    = int(wx.BRUSHSTYLE_HORIZONTAL_HATCH)
        wx.VERTICAL_HATCH      = int(wx.BRUSHSTYLE_VERTICAL_HATCH)
        """)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

