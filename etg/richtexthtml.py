#---------------------------------------------------------------------------
# Name:        etg/richtexthtml.py
# Author:      Robin Dunn
#
# Created:     13-May-2013
# Copyright:   (c) 2013-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_richtext"
NAME      = "richtexthtml"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxRichTextHTMLHandler",

           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxRichTextHTMLHandler')
    assert isinstance(c, etgtools.ClassDef)

    # Let SIP know that the pure virtuals have implementations in this class
    c.addItem(etgtools.WigCode("""\
        protected:
        virtual bool DoLoadFile(wxRichTextBuffer *buffer, wxInputStream& stream);
        virtual bool DoSaveFile(wxRichTextBuffer *buffer, wxOutputStream& stream);
        """))

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

