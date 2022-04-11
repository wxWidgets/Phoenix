#---------------------------------------------------------------------------
# Name:        etg/translation.py
# Author:      Robin Dunn
#
# Created:     07-Apr-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "translation"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxTranslations",
           "wxTranslationsLoader",
           "wxFileTranslationsLoader",
           #"wxMsgCatalog",              TODO: Getting link errors on this
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxTranslations')
    assert isinstance(c, etgtools.ClassDef)
    c.find('Set.t').transfer = True
    c.find('SetLoader.loader').transfer = True
    c.find('AddCatalog').findOverload('msgIdCharset').ignore()


    c = module.find('wxTranslationsLoader')
    c.abstract = True
    c.find('LoadCatalog').factory = True


    c = module.find('wxFileTranslationsLoader')
    c.addItem(etgtools.WigCode("""\
    virtual wxMsgCatalog *LoadCatalog(const wxString& domain, const wxString& lang);
    virtual wxArrayString GetAvailableTranslations(const wxString& domain) const;
    """))


    #c = module.find('wxMsgCatalog')
    #c.find('CreateFromFile').factory = True
    #c.find('CreateFromData').ignore()          # Needs wxScopedCharBuffer
    ##c.find('CreateFromData').factory = True
    #c.addPrivateCopyCtor()

    # Just add a forward declaration for now
    module.insertItem(0, etgtools.WigCode("class wxMsgCatalog;"))


    module.find('_').ignore()


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

