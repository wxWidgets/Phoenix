#---------------------------------------------------------------------------
# Name:        etg/ribbon_gallery.py
# Author:      Robin Dunn
#
# Created:     20-Jun-2016
# Copyright:   (c) 2016-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_ribbon"
NAME      = "ribbon_gallery"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxRibbonGallery',
           'wxRibbonGalleryEvent',
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode('#include <wx/ribbon/gallery.h>')
    module.insertItem(0, etgtools.WigCode("""\
        // forward declarations
        class wxRibbonGalleryItem;
        """))

    c = module.find('wxRibbonGallery')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixWindowClass(c)

    # Ignore the methods setting and fetching client data as a void*.  We have
    # a mapped type for the wxClientData alternatives that work well and are
    # hack free.
    c.find('Append').findOverload('void *').ignore()
    c.find('SetItemClientData').ignore()
    c.find('GetItemClientData').ignore()

    # Methods assigning wxClientData objects need to transfer ownership
    c.find('SetItemClientObject.data').transfer = True
    c.find('Append').findOverload('wxClientData').find('clientData').transfer = True

    # And let's change the names of the "Object" version of the methods
    c.find('SetItemClientObject').pyName = 'SetItemClientData'
    c.find('GetItemClientObject').pyName = 'GetItemClientData'


    c = module.find('wxRibbonGalleryEvent')
    tools.fixEventClass(c)

    module.addPyCode("""\
        EVT_RIBBONGALLERY_HOVER_CHANGED = wx.PyEventBinder( wxEVT_RIBBONGALLERY_HOVER_CHANGED, 1 )
        EVT_RIBBONGALLERY_SELECTED = wx.PyEventBinder( wxEVT_RIBBONGALLERY_SELECTED, 1 )
        EVT_RIBBONGALLERY_CLICKED = wx.PyEventBinder( wxEVT_RIBBONGALLERY_CLICKED, 1 )
        """)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

