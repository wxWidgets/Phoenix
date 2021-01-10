#---------------------------------------------------------------------------
# Name:        etg/fontmap.py
# Author:      Robin Dunn
#
# Created:     19-Jun-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "fontmap"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxFontMapper",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxFontMapper')
    assert isinstance(c, etgtools.ClassDef)
    c.addPrivateCopyCtor()

    c.find('GetAltForEncoding').findOverload('wxNativeEncodingInfo').ignore()
    c.find('GetAltForEncoding.alt_encoding').out = True


    c.find('GetAllEncodingNames').ignore()
    c.addCppMethod('wxArrayString*', 'GetAllEncodingNames', '(wxFontEncoding encoding)',
        isStatic=True,
        doc="""\
            Returns the array of all possible names for the given encoding. If it
            isn't empty, the first name in it is the canonical encoding name,
            i.e. the same string as returned by GetEncodingName()
            """,
        body="""\
            wxArrayString* sArr = new wxArrayString;
            const wxChar** cArr = wxFontMapper::GetAllEncodingNames(encoding);
            if (cArr) {
                for (int idx=0; cArr[idx]; idx+=1)
                    sArr->Add(cArr[idx]);
            }
            return sArr;
            """)


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

