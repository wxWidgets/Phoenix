#---------------------------------------------------------------------------
# Name:        etg/htmlprint.py
# Author:      Robin Dunn
#
# Created:     29-Oct-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_html"
NAME      = "htmlprint"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxHtmlDCRenderer",
           "wxHtmlEasyPrinting",
           "wxHtmlPrintout",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxHtmlDCRenderer')
    assert isinstance(c, etgtools.ClassDef)
    c.mustHaveApp()
    c.addPrivateCopyCtor()
    tools.fixHtmlSetFonts(c)

    c.find('Render.from').name = 'from_'
    c.find('Render.to').name = 'to_'

    c = module.find('wxHtmlEasyPrinting')
    c.mustHaveApp()
    c.addPrivateCopyCtor()
    tools.fixHtmlSetFonts(c)

    c = module.find('wxHtmlPrintout')
    c.mustHaveApp()
    c.addPrivateCopyCtor()
    tools.fixHtmlSetFonts(c)

    # Ensure sip knows these virtuals are present in this class.
    c.addItem(etgtools.WigCode("""\
        bool OnPrintPage(int page);
        bool HasPage(int page);
        void GetPageInfo(int *minPage, int *maxPage, int *selPageFrom, int *selPageTo);
        bool OnBeginDocument(int startPage, int endPage);
        void OnPreparePrinting();
        """))

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

