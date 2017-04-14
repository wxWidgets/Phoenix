#---------------------------------------------------------------------------
# Name:        etg/vscrol.py
# Author:      Robin Dunn
#
# Created:     20-Dec-2011
# Copyright:   (c) 2011-2017 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools
from etgtools import WigCode

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "vscroll"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxVarScrollHelperBase",
           "wxVarVScrollHelper",
           "wxVarHScrollHelper",
           "wxVarHVScrollHelper",
           "wxVScrolledWindow",
           "wxHScrolledWindow",
           "wxHVScrolledWindow",
           ]


#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.


    c = module.find('wxVarScrollHelperBase')
    assert isinstance(c, etgtools.ClassDef)
    c.abstract = True

    c.find('OnGetUnitsSizeHint').ignore(False)
    c.find('EstimateTotalSize').ignore(False)
    c.find('OnGetUnitSize').ignore(False)

    c.find('GetTargetWindow').isVirtual = False
    c.find('SetTargetWindow').isVirtual = False
    c.find('RefreshAll').isVirtual = False
    c.find('UpdateScrollbar').isVirtual = False

    # Ensure that SIP knows that there are implementations of these base
    # class virtual methods in each of the two helper classes below.
    baseVirtuals = """\
    virtual void OnGetUnitsSizeHint(size_t unitMin, size_t unitMax) const;
    virtual wxCoord EstimateTotalSize() const;
    virtual int GetNonOrientationTargetSize() const;
    virtual wxOrientation GetOrientation() const;
    virtual int GetOrientationTargetSize() const;
    virtual wxCoord OnGetUnitSize(size_t unit) const;
    """

    c = module.find('wxVarVScrollHelper')
    c.addItem(WigCode(baseVirtuals, protection='protected'))
    c.find('EstimateTotalHeight').ignore(False)
    c.find('OnGetRowsHeightHint').ignore(False)
    c.find('OnGetRowHeight').ignore(False)
    c.find('RefreshRows.from').name = 'from_'
    c.find('RefreshRows.to').name = 'to_'

    c = module.find('wxVarHScrollHelper')
    c.addItem(WigCode(baseVirtuals, protection='protected'))
    c.find('EstimateTotalWidth').ignore(False)
    c.find('OnGetColumnsWidthHint').ignore(False)
    c.find('OnGetColumnWidth').ignore(False)
    c.find('RefreshColumns.from').name = 'from_'
    c.find('RefreshColumns.to').name = 'to_'


    c = module.find('wxVarHVScrollHelper')
    # For this class those base methods shouldn't be overridden, (since there
    # are orientation-specfic versions in the 2 superclasses) so tell SIP
    # that they are private so it won't add support for them and end up with
    # multiple inheritance ambiguities.
    c.addItem(WigCode(baseVirtuals, protection='private'))



    c = module.find('wxVScrolledWindow')
    tools.fixWindowClass(c)

    c = module.find('wxHScrolledWindow')
    tools.fixWindowClass(c)

    c = module.find('wxHVScrolledWindow')
    tools.fixWindowClass(c)


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

