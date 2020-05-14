#---------------------------------------------------------------------------
# Name:        etg/font.py
# Author:      Robin Dunn
#
# Created:     27-Nov-2010
# Copyright:   (c) 2010-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "font"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [  'wxFontInfo',
            'wxFont',
            'wxFontList',
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxFontInfo')
    assert isinstance(c, etgtools.ClassDef)

    c = module.find('wxFont')
    assert isinstance(c, etgtools.ClassDef)
    tools.removeVirtuals(c)

    # Set mustHaveApp on all ctors except the default ctor
    for ctor in c.find('wxFont').all():
        if ctor.isCtor and ctor.argsString != '()':
            ctor.mustHaveApp()

    for func in c.find('New').all():
        func.mustHaveApp()

    c.find('GetDefaultEncoding').mustHaveApp()
    c.find('SetDefaultEncoding').mustHaveApp()

    # Tweak the documentation in this constructor a little, replacing the
    # link to another constructor with a simpler version of the text.
    ctor = c.find('wxFont').findOverload('int pointSize')
    # TODO: should implement an easier way to findDocNode() the node containing what we're looking for...
    ref = list(ctor.detailedDoc[0])[0]
    assert ref.text.startswith('wxFont(')
    ref.tag = 'para'
    ref.text = 'the constructor accepting a :ref:`wx.FontInfo`'

    # FFont factory function for backwards compatibility
    module.addCppFunction('wxFont*', 'FFont',
                          """(int pointSize,
                              wxFontFamily family,
                              int flags = wxFONTFLAG_DEFAULT,
                              const wxString& faceName = wxEmptyString,
                              wxFontEncoding encoding = wxFONTENCODING_DEFAULT)""",
        pyArgsString="(pointSize, family, flags=FONTFLAG_DEFAULT, faceName=EmptyString, encoding=FONTENCODING_DEFAULT)",
        body="""\
        wxFont* font = wxFont::New(pointSize, family, flags, *faceName, encoding);
        return font;
        """, factory=True)

    for item in c.findAll('New'):
        item.factory = True

    c.addProperty('Encoding GetEncoding SetEncoding')
    c.addProperty('FaceName GetFaceName SetFaceName')
    c.addProperty('Family GetFamily SetFamily')
    c.addProperty('NativeFontInfoDesc GetNativeFontInfoDesc SetNativeFontInfo')
    c.addProperty('NativeFontInfoUserDesc GetNativeFontInfoUserDesc SetNativeFontInfoUserDesc')
    c.addProperty('PointSize GetPointSize SetPointSize')
    c.addProperty('PixelSize GetPixelSize SetPixelSize')
    c.addProperty('Style GetStyle SetStyle')
    c.addProperty('Weight GetWeight SetWeight')

    # TODO, there is now an Underlined method so we can't have a
    # property of the same name.
    #c.addProperty('Underlined GetUnderlined SetUnderlined')
    #c.addProperty('Strikethrough GetStrikethrough SetStrikethrough')

    c.addCppMethod('int', '__nonzero__', '()', "return self->IsOk();")
    c.addCppMethod('int', '__bool__', '()', "return self->IsOk();")

    c.addCppMethod('void*', 'GetHFONT', '()',
        doc="Returns the font's native handle.",
        body="""\
        #ifdef __WXMSW__
            return self->GetHFONT();
        #else
            return 0;
        #endif
        """)

    c.addCppMethod('void*', 'OSXGetCGFont', '()',
        doc="Returns the font's native handle.",
        body="""\
        #ifdef __WXMAC__
            return self->OSXGetCGFont();
        #else
            return 0;
        #endif
        """)

    c.addCppMethod('void*', 'GetPangoFontDescription', '()',
        doc="Returns the font's native handle.",
        body="""\
        #ifdef __WXGTK__
            return self->GetNativeFontInfo()->description;
        #else
            return 0;
        #endif
        """)

    c.find('AddPrivateFont').setCppCode("""\
        #if wxUSE_PRIVATE_FONTS
            return wxFont::AddPrivateFont(*filename);
        #else
            wxPyRaiseNotImplemented();
            return false;
        #endif
        """)

    c.addCppMethod('bool', 'CanUsePrivateFont', '()', isStatic=True,
        doc="Returns ``True`` if this build of wxPython supports using :meth:`AddPrivateFont`.",
        body="return wxUSE_PRIVATE_FONTS;")


    # The stock Font items are documented as simple pointers, but in reality
    # they are macros that evaluate to a function call that returns a font
    # pointer, and that is only valid *after* the wx.App object has been
    # created. That messes up the code that SIP generates for them, so we need
    # to come up with another solution. So instead we will just create
    # uninitialized fonts in a block of Python code, that will then be
    # initialized later when the wx.App is created.
    c.addCppMethod('void', '_copyFrom', '(const wxFont* other)',
                   "*self = *other;",
                   briefDoc="For internal use only.")  # ??
    pycode = '# These stock fonts will be initialized when the wx.App object is created.\n'
    for item in module:
        if '_FONT' in item.name:
            item.ignore()
            pycode += '%s = Font()\n' % tools.removeWxPrefix(item.name)
    module.addPyCode(pycode)

    # it is delay-initialized, see stockgdi.sip
    module.find('wxTheFontList').ignore()

    module.find('wxFromString').ignore()
    module.find('wxToString').ignore()

    c.addPyMethod('SetNoAntiAliasing', '(self, no=True)', 'pass', deprecated=True)
    c.addPyMethod('GetNoAntiAliasing', '(self)', 'pass', deprecated=True)

    # Some aliases that should be phased out eventually, (sooner rather than
    # later.) They are already gone (or wrapped by an #if) in the C++ code,
    # and so are not found in the documentation...
    module.addPyCode("""\
        wx.DEFAULT    = int(wx.FONTFAMILY_DEFAULT)
        wx.DECORATIVE = int(wx.FONTFAMILY_DECORATIVE)
        wx.ROMAN      = int(wx.FONTFAMILY_ROMAN)
        wx.SCRIPT     = int(wx.FONTFAMILY_SCRIPT)
        wx.SWISS      = int(wx.FONTFAMILY_SWISS)
        wx.MODERN     = int(wx.FONTFAMILY_MODERN)
        wx.TELETYPE   = int(wx.FONTFAMILY_TELETYPE)

        wx.NORMAL = int(wx.FONTWEIGHT_NORMAL)
        wx.LIGHT  = int(wx.FONTWEIGHT_LIGHT)
        wx.BOLD   = int(wx.FONTWEIGHT_BOLD)

        wx.NORMAL = int(wx.FONTSTYLE_NORMAL)
        wx.ITALIC = int(wx.FONTSTYLE_ITALIC)
        wx.SLANT  = int(wx.FONTSTYLE_SLANT)
        """)


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)



#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

