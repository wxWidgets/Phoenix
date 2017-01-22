#---------------------------------------------------------------------------
# Name:        etg/scrolwin.py
# Author:      Kevin Ollivier
#              Robin Dunn
#
# Created:     16-Sept-2011
# Copyright:   (c) 2013 by Kevin Ollivier
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools
from etgtools import TypedefDef, ClassDef, MethodDef, ParamDef

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "scrolwin"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxScrolled' ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    scrolled = module.find('wxScrolled')
    assert isinstance(scrolled, etgtools.ClassDef)

    scrolled.find('GetViewStart').findOverload('()').ignore()
    scrolled.find('GetViewStart.x').out = True
    scrolled.find('GetViewStart.y').out = True

    m = scrolled.find('CalcScrolledPosition').findOverload('xx')
    m.find('xx').out = True
    m.find('yy').out = True

    m = scrolled.find('CalcUnscrolledPosition').findOverload('xx')
    m.find('xx').out = True
    m.find('yy').out = True

    scrolled.find('GetScrollPixelsPerUnit.xUnit').out = True
    scrolled.find('GetScrollPixelsPerUnit.yUnit').out = True

    scrolled.find('GetVirtualSize.x').out = True
    scrolled.find('GetVirtualSize.y').out = True

    scrolled.addPrivateCopyCtor()
    scrolled.addPrivateAssignOp()
    tools.fixWindowClass(scrolled)

    # Add back some virtuals that were removed in fixWindowClass
    scrolled.find('OnDraw').isVirtual = True
    scrolled.find('GetSizeAvailableForScrollTarget').isVirtual = True
    scrolled.find('GetSizeAvailableForScrollTarget').ignore(False)
    scrolled.find('SendAutoScrollEvents').isVirtual = True

    # The wxScrolledWindow and wxScrolledCanvas typedefs will be output
    # normally and SIP will treat them like classes that have a
    # wxScrolled mix-in as one of their base classes. Let's add some more
    # info to them for the doc generators.
    docBase = """\
    The :ref:`{name}` class is a combination of the :ref:`{base}` and
    :ref:`Scrolled` classes, and manages scrolling for its client area,
    transforming the coordinates according to the scrollbar positions,
    and setting the scroll positions, thumb sizes and ranges according to
    the area in view.
    """
    item = module.find('wxScrolledWindow')
    assert isinstance(item, etgtools.TypedefDef)
    item.docAsClass = True
    item.bases = ['wxPanel', 'wxScrolled']
    item.briefDoc = docBase.format(name='ScrolledWindow', base='Panel')

    item = module.find('wxScrolledCanvas')
    item.docAsClass = True
    item.bases = ['wxWindow', 'wxScrolled']
    item.briefDoc = docBase.format(name='ScrolledCanvas', base='Window')
    item.detailedDoc[0] = "This scrolled window is not intended to have children "\
                          "so it doesn't have special handling for TAB traversal "\
                          "or focus management."


    module.items.remove(item)
    # wxScrolledWindow is documented as a typedef but it's actually a class.
    # So we need to implement it that way here too in order to keep
    # static_casts happy.
    sw = module.find('wxScrolledWindow')
    assert isinstance(sw, TypedefDef)
    sw.name = '_ScrolledWindowBase'

    module.insertItemBefore(sw, item)


    klass = ClassDef(
        name='wxScrolledWindow',
        bases=['_ScrolledWindowBase'],
        ##bases=['wxScrolled<wxPanel>'],
        briefDoc=sw.briefDoc, detailedDoc=sw.detailedDoc,
        items=[
            MethodDef(name='wxScrolledWindow', isCtor=True, items=[]),
            MethodDef(name='wxScrolledWindow', isCtor=True, items=[
                ParamDef(name='parent', type='wxWindow*'),
                ParamDef(name='winid', type='wxWindowID', default='wxID_ANY'),
                ParamDef(name='pos', type='const wxPoint&', default='wxDefaultPosition'),
                ParamDef(name='size', type='const wxSize&', default='wxDefaultSize'),
                ParamDef(name='style', type='long', default='wxScrolledWindowStyle'),
                ParamDef(name='name', type='const wxString&', default='wxPanelNameStr'),
                ]),
            ],
        )

    module.insertItemAfter(sw, klass)
    ##sw.ignore()
    module.addHeaderCode('typedef wxScrolled<wxPanel> _ScrolledWindowBase;')


    module.addPyCode("PyScrolledWindow = wx.deprecated(ScrolledWindow, 'Use ScrolledWindow instead.')")

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

