#---------------------------------------------------------------------------
# Name:        etg/font.py
# Author:      Robin Dunn
#
# Created:     27-Nov-2010
# Copyright:   (c) 2011 by Total Control Software
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
ITEMS  = [  'wxFont',
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
    
    c = module.find('wxFont')
    assert isinstance(c, etgtools.ClassDef)
    tools.removeVirtuals(c)
    
    # EXPERIMENTAL: See alternate implementation below that we can do when
    # the wxObject dtor is not marked virtual.
    ## TODO: Since the TypeCode is inserted before the derived class
    ## (sipwxFont) is defined, we can't use the new version of addCppCtor. Can
    ## this be fixed?
    #c.addCppCtor_sip("""(
    #    int pointSize,
    #    wxFontFamily family,
    #    int flags = wxFONTFLAG_DEFAULT,
    #    const wxString& faceName = wxEmptyString,
    #    wxFontEncoding encoding = wxFONTENCODING_DEFAULT )""",
    #    body="""\
    #    wxFont* font = wxFont::New(pointSize, family, flags, *faceName, encoding);
    #    sipCpp = new sipwxFont(*font);
    #    delete font;
    #    """)

    c.addCppCtor("""(int pointSize,
                     wxFontFamily family,
                     int flags = wxFONTFLAG_DEFAULT,
                     const wxString& faceName = wxEmptyString,
                     wxFontEncoding encoding = wxFONTENCODING_DEFAULT )""",
        body="""\
        wxFont* font = wxFont::New(pointSize, family, flags, *faceName, encoding);
        return font;
        """)

    # Same as the above, but as a factory function
    module.addCppFunction('wxFont*', 'FFont', 
                          """(int pointSize,
                              wxFontFamily family,
                              int flags = wxFONTFLAG_DEFAULT,
                              const wxString& faceName = wxEmptyString,
                              wxFontEncoding encoding = wxFONTENCODING_DEFAULT )""",
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

    # TODO, there is now a Underlined method so we can't have a
    # property of the same name.
    #c.addProperty('Underlined GetUnderlined SetUnderlined')

       
    # The stock Font items are documented as simple pointers, but in reality
    # they are macros that evaluate to a function call that returns a font
    # pointer, and that is only valid *after* the wx.App object has been
    # created. That messes up the code that SIP generates for them, so we need
    # to come up with another solution. So instead we will just create
    # uninitialized fonts in a block of Python code, that will then be
    # intialized later when the wx.App is created.
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

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

