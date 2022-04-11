#---------------------------------------------------------------------------
# Name:        etg/richtextformatdlg.py
# Author:      Robin Dunn
#
# Created:     16-May-2013
# Copyright:   (c) 2013-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_richtext"
NAME      = "richtextformatdlg"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxRichTextFormattingDialogFactory",
           "wxRichTextFormattingDialog",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxRichTextFormattingDialog')
    assert isinstance(c, etgtools.ClassDef)
    c.piBases = ['wx.adv.PropertySheetDialog']
    tools.fixTopLevelWindowClass(c)
    tools.ignoreConstOverloads(c)
    c.piBases = ['wx.adv.PropertySheetDialog']


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

