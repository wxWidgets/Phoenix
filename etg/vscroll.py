#---------------------------------------------------------------------------
# Name:        etg/vscrol.py
# Author:      Robin Dunn
#
# Created:     20-Dec-2011
# Copyright:   (c) 2011-2020 by Total Control Software
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
    assert isinstance(c, etgtools.ClassDef)
    tools.fixWindowClass(c)

    # These methods are listed in the docs for wxVScrolledWindow as present
    # but deprecated, but are not actually documented so we don't see them in
    # the incoming XML. Since they're deprecated lets just add simple wrappers
    # here instead of formally documenting them.

    # NOTE: Some of these are virtual, and there are also OnGetLineHeight and
    # OnGetLinesHint protected virtual methods, but trying to support them as
    # virtuals from here is causing more troubles than it is probably worth
    # due to ambiguities, etc... Revisit later if people complain.

    c.addPyMethod('HitTest', '(self, *args)',
        doc="Deprecated compatibility helper.",
        deprecated='Use VirtualHitTest instead.',
        body="""\
            if len(args) == 2:
                x, y = args
                return self.VirtualHitTest(y)
            else:
                pt = args[0]
                return self.VirtualHitTest(pt[1])
            """)

    c.addCppMethod('unsigned long',  'GetFirstVisibleLine', '()',
        doc="Deprecated compatibility helper.",
        deprecated='Use GetVisibleRowsBegin instead.',
        body="return self->GetVisibleRowsBegin();")

    c.addCppMethod('unsigned long',  'GetLastVisibleLine', '()',
        doc="Deprecated compatibility helper.",
        deprecated='Use GetVisibleRowsEnd instead.',
        body="return self->GetVisibleRowsEnd();")

    c.addCppMethod('unsigned long',  'GetLineCount', '()',
        doc="Deprecated compatibility helper.",
        deprecated='Use GetRowCount instead.',
        body="return self->GetRowCount();")

    c.addCppMethod('void',  'SetLineCount', '(unsigned long count)',
        doc="Deprecated compatibility helper.",
        deprecated='Use SetRowCount instead.',
        body="self->SetRowCount(count);")

    c.addCppMethod('void',  'RefreshLine', '(unsigned long line)',
        doc="Deprecated compatibility helper.",
        deprecated='Use RefreshRow instead.',
        body="self->RefreshRow(line);")

    c.addCppMethod('void',  'RefreshLines', '(unsigned long from_, unsigned long to_)',
        doc="Deprecated compatibility helper.",
        deprecated='Use RefreshRows instead.',
        body="self->RefreshRows(from_, to_);")

    c.addCppMethod('bool',  'ScrollToLine', '(unsigned long line)',
        doc="Deprecated compatibility helper.",
        deprecated='Use ScrollToRow instead.',
        body="return self->ScrollToRow(line);")

    c.addCppMethod('bool',  'ScrollLines', '(int lines)',
        doc="Deprecated compatibility helper.",
        deprecated='Use ScrollRows instead.',
        #body="return self->wxVarVScrollLegacyAdaptor::ScrollLines(lines);")
        body="return self->ScrollRows(lines);")

    c.addCppMethod('bool',  'ScrollPages', '(int pages)',
        doc="Deprecated compatibility helper.",
        deprecated='Use ScrollRowPages instead.',
        #body="return self->wxVarVScrollLegacyAdaptor::ScrollPages(pages);")
        body="return self->ScrollRowPages(pages);")



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

