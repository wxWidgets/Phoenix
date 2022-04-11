#---------------------------------------------------------------------------
# Name:        etg/richtextstyles.py
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
NAME      = "richtextstyles"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxRichTextStyleListCtrl',
           'wxRichTextStyleListBox',
           'wxRichTextStyleComboCtrl',

           'wxRichTextStyleDefinition',
           'wxRichTextParagraphStyleDefinition',
           'wxRichTextCharacterStyleDefinition',
           'wxRichTextListStyleDefinition',

           'wxRichTextStyleSheet',
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxRichTextStyleListCtrl')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixWindowClass(c)


    c = module.find('wxRichTextStyleListBox')
    tools.fixWindowClass(c)
    c.piBases = ['wx.html.HtmlListBox']
    c.find('OnGetItem').ignore(False)
    c.find('CreateHTML.def').name = 'styleDef'


    c = module.find('wxRichTextStyleComboCtrl')
    tools.fixWindowClass(c)


    c = module.find('wxRichTextStyleDefinition')
    tools.ignoreConstOverloads(c)
    c.abstract = True


    c = module.find('wxRichTextStyleSheet')
    tools.ignoreConstOverloads(c)
    c.find('AddCharacterStyle.def').transfer = True
    c.find('AddListStyle.def').transfer = True
    c.find('AddParagraphStyle.def').transfer = True
    c.find('AddStyle.def').transfer = True

    # Change def --> styleDef
    for item in c.allItems():
        if isinstance(item, etgtools.ParamDef) and item.name == 'def':
            item.name = 'styleDef'

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

