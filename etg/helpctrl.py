#---------------------------------------------------------------------------
# Name:        etg/helpctrl.py
# Author:      Robin Dunn
#
# Created:     30-Oct-2012
# Copyright:   (c) 2012-2018 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_html"
NAME      = "helpctrl"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxHtmlHelpController",
           "wxHtmlModalHelp",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxHtmlHelpController')
    assert isinstance(c, etgtools.ClassDef)
    c.mustHaveApp()
    c.addPrivateCopyCtor()

    c.find('CreateHelpDialog').ignore(False)
    c.find('CreateHelpFrame').ignore(False)

    c.addItem(etgtools.WigCode("""\
        // Add implementations for the pure virtuals in the base class
        virtual bool DisplayBlock(long blockNo);
        virtual bool DisplaySection(int sectionNo);
        virtual bool LoadFile(const wxString& file = wxEmptyString);
        virtual bool Quit();
        """))

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

