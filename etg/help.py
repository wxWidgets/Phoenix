#---------------------------------------------------------------------------
# Name:        etg/help.py
# Author:      Robin Dunn
#
# Created:     06-Apr-2012
# Copyright:   (c) 2012-2018 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "help"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxHelpControllerBase",
           #"wxHelpController",        See note below
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxHelpControllerBase')
    assert isinstance(c, etgtools.ClassDef)
    c.abstract = True

    c.find('GetFrameParameters.size').out = True
    c.find('GetFrameParameters.pos').out = True
    c.find('GetFrameParameters.newFrameEachTime').out = True


    # NOTE: Since wxHelpController is an alias for wxHtmlHelpController on
    # Mac and GTK, and since we don't want to force the wx.core extension
    # module to link to the wxHTML library, then we won't provide a wrapper
    # for the wxHelpController 'class'. Later on when we've got all the help
    # controller classes that we'll want then we can add a wxHelpController
    # or factory of our own in Python code.


    #c = module.find('wxHelpController')
    #c.mustHaveApp()
    #c.addPrivateCopyCtor()
    ## Add pure virtuals with implemenations here
    #c.addItem(etgtools.WigCode("""\
    #virtual bool DisplayBlock(long blockNo);
    #virtual bool DisplayContents();
    #virtual bool DisplaySection(int sectionNo);
    #virtual bool KeywordSearch(const wxString& keyWord,
    #                           wxHelpSearchMode mode = wxHELP_SEARCH_ALL);
    #virtual bool LoadFile(const wxString& file = wxEmptyString);
    #virtual bool Quit();
    #"""))



    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

