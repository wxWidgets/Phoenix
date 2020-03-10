#---------------------------------------------------------------------------
# Name:        etg/scrolwin.py
# Author:      Kevin Ollivier
#              Robin Dunn
#
# Created:     16-Sept-2011
# Copyright:   (c) 2011 by Kevin Ollivier
# Copyright:   (c) 2011-2020 by Total Control Software
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

def parseAndTweakModule():
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

    # Just ignore this one and let the already tweaked versions be inherited from wx.Window.
    scrolled.find('GetVirtualSize').ignore()

    scrolled.addPrivateCopyCtor()
    scrolled.addPrivateAssignOp()
    tools.fixWindowClass(scrolled)

    # Add back some virtuals that were removed in fixWindowClass
    scrolled.find('OnDraw').isVirtual = True
    scrolled.find('GetSizeAvailableForScrollTarget').isVirtual = True
    scrolled.find('GetSizeAvailableForScrollTarget').ignore(False)
    scrolled.find('SendAutoScrollEvents').isVirtual = True
    scrolled.find('ShouldScrollToChildOnFocus').ignore(False)
    scrolled.find('ShouldScrollToChildOnFocus').isVirtual = True

    # The wxScrolledCanvas typedef will be output normally and SIP will treat
    # it like a class that has a wxScrolled mix-in as one of the base classes.
    # Let's add some more info to them for the doc generators.
    docBase = """\
    The :ref:`{name}` class is a combination of the :ref:`{base}` and
    :ref:`Scrolled` classes, and manages scrolling for its client area,
    transforming the coordinates according to the scrollbar positions,
    and setting the scroll positions, thumb sizes and ranges according to
    the area in view.
    """
    item = module.find('wxScrolledCanvas')
    item.docAsClass = True
    item.bases = ['wxWindow', 'wxScrolled']
    item.briefDoc = docBase.format(name='ScrolledCanvas', base='Window')
    item.detailedDoc[0] = "This scrolled window is not intended to have children "\
                          "so it doesn't have special handling for TAB traversal "\
                          "or focus management."
    # move it ahead of wxScrolledWindow
    sw = module.find('wxScrolledWindow')
    module.items.remove(item)
    module.insertItemBefore(sw, item)


    # wxScrolledWindow is documented as a typedef but it's actually a class.
    # So we need to implement it that way here too in order to keep
    # static_casts and such happy.
    assert isinstance(sw, TypedefDef)

    # First, let's add a typedef to serve as the base class of
    # wxScrolledWindow, since SIP doesn't yet understand using template
    # instantiations as base classes.  Setting noTypeName tells SIP to not use
    # the typedef name in the actual generated code, but the typedef's type
    # instead.
    td = TypedefDef(name='_ScrolledWindowBase',
                    type='wxScrolled<wxPanel>',
                    noTypeName=True,
                    piIgnored=True)
    module.insertItemAfter(sw, td)
    module.addHeaderCode('typedef wxScrolled<wxPanel> _ScrolledWindowBase;')
    sw.ignore()

    # Now implement the class definition
    klass = ClassDef(
        name='wxScrolledWindow',
        bases=['_ScrolledWindowBase'],
        piBases=['Window', 'Scrolled'],
        briefDoc=sw.briefDoc, detailedDoc=sw.detailedDoc,
        items=[
            MethodDef(name='wxScrolledWindow', isCtor=True, items=[],
                overloads=[
                    MethodDef(name='wxScrolledWindow', isCtor=True, items=[
                        ParamDef(name='parent', type='wxWindow*'),
                        ParamDef(name='id', type='wxWindowID', default='wxID_ANY'),
                        ParamDef(name='pos', type='const wxPoint&', default='wxDefaultPosition'),
                        ParamDef(name='size', type='const wxSize&', default='wxDefaultSize'),
                        ParamDef(name='style', type='long', default='wxScrolledWindowStyle'),
                        ParamDef(name='name', type='const wxString&', default='wxPanelNameStr'),
                        ]),
                    ]),
            MethodDef(name='SetFocusIgnoringChildren', type='void', items=[],
                briefDoc="""\
                    In contrast to SetFocus() this will set the focus to the panel even if
                    there are child windows in the panel. This is only rarely needed."""),
            ],
        )
    tools.fixWindowClass(klass)
    module.insertItemAfter(td, klass)

    module.addPyCode("PyScrolledWindow = wx.deprecated(ScrolledWindow, 'Use ScrolledWindow instead.')")

    # TODO: Can/should this be used from Python? If so then fix the declaration
    # so sip can understand it.
    module.find('wxCreateScrolled').ignore()

    return module

#-----------------------------------------------------------------
def run():
    module = parseAndTweakModule()
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

