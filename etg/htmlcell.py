#---------------------------------------------------------------------------
# Name:        etg/htmlcell.py
# Author:      Robin Dunn
#
# Created:     27-Oct-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools
from etgtools import MethodDef, ParamDef

PACKAGE   = "wx"
MODULE    = "_html"
NAME      = "htmlcell"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxHtmlSelection",
           "wxHtmlRenderingState",
           "wxHtmlRenderingStyle",
           "wxHtmlRenderingInfo",
           "wxHtmlCell",
           "wxHtmlContainerCell",
           "wxHtmlLinkInfo",
           "wxHtmlColourCell",
           "wxHtmlWidgetCell",
           "wxHtmlWordCell",
           "wxHtmlWordWithTabsCell",
           "wxHtmlFontCell",
           ]

#---------------------------------------------------------------------------

def fixCellClass(klass):
    klass.addItem(etgtools.WigCode("""\
        virtual void Draw(wxDC& dc, int x, int y, int view_y1, int view_y2, wxHtmlRenderingInfo& info);
        virtual void DrawInvisible(wxDC& dc, int x , int y, wxHtmlRenderingInfo& info);
        virtual wxCursor GetMouseCursor(wxHtmlWindowInterface* window) const;
        virtual void Layout(int w);
        """))


def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.


    c = module.find('wxHtmlCell')
    assert isinstance(c, etgtools.ClassDef)
    c.addPrivateCopyCtor()
    c.find('SetNext.cell').transfer = True
    c.find('AdjustPagebreak.pagebreak').inOut = True

    m = c.find('Find')
    assert isinstance(m, etgtools.MethodDef)
    m.find('param').type = 'const char*'
    m.cppSignature = 'const wxHtmlCell* (int condition, const void* param)'

    m = MethodDef(name='GetAbsPos', type='wxPoint', isConst=True,
        items=[ParamDef(type='wxHtmlCell*', name='rootCell', default='NULL')],
        doc="""\
        Returns absolute position of the cell on HTML canvas.\n
        If rootCell is provided, then it's considered to be the root of the
        hierarchy and the returned value is relative to it.
        """)
    c.addItem(m)

    m = MethodDef(name='GetRootCell', type='wxHtmlCell*', isConst=True,
        doc="Returns the root cell of the hierarchy.")
    c.addItem(m)


    c = module.find('wxHtmlContainerCell')
    c.find('InsertCell.cell').transfer = True
    fixCellClass(c)

    c = module.find('wxHtmlColourCell')
    fixCellClass(c)

    c = module.find('wxHtmlWidgetCell')
    fixCellClass(c)

    c = module.find('wxHtmlWordCell')
    fixCellClass(c)

    c = module.find('wxHtmlWordWithTabsCell')
    fixCellClass(c)

    c = module.find('wxHtmlFontCell')
    fixCellClass(c)




    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

