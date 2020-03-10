#---------------------------------------------------------------------------
# Name:        etg/dcbuffer.h
# Author:      Robin Dunn
#
# Created:     2-Sept-2011
# Copyright:   (c) 2011-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "dcbuffer"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxBufferedDC',
           'wxBufferedPaintDC',
           'wxAutoBufferedPaintDC',
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode("#include <wx/dcbuffer.h>")

    c = module.find('wxBufferedDC')
    c.addPrivateCopyCtor()
    c.mustHaveApp()

    for m in c.find('wxBufferedDC').all() + c.find('Init').all():
        if m.findItem('dc'):
            m.findItem('dc').keepReference = True
        if m.findItem('buffer'):
            m.findItem('buffer').keepReference = True


    c = module.find('wxBufferedPaintDC')
    c.mustHaveApp()

    c.addPrivateCopyCtor()
    c.find('wxBufferedPaintDC').findOverload('wxBitmap').find('buffer').keepReference = True


    # wxAutoBufferedPaintDC is documented as a class deriving from
    # wxBufferedPaintDC, but on some platforms it derived directly from
    # wxPaintDC. This causes compilation errors when the code tries to
    # static_cast<> to a possibly incompatible base class, so we'll take a LCD
    # approach and pretend that it derives directly from wxDC instead, in
    # order to present a hierarchy that is valid and works on all platforms.
    c = module.find('wxAutoBufferedPaintDC')
    c.bases = ['wxDC']
    c.mustHaveApp()
    c.addPrivateCopyCtor()


    module.find('wxAutoBufferedPaintDCFactory').factory = True

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

