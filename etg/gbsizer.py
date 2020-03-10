#---------------------------------------------------------------------------
# Name:        etg/gbsizer.py
# Author:      Robin Dunn
#
# Created:     06-Dec-2011
# Copyright:   (c) 2011-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "gbsizer"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxGBPosition",
           "wxGBSpan",
           "wxGBSizerItem",
           "wxGridBagSizer",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxGBPosition')
    assert isinstance(c, etgtools.ClassDef)

    # allow a 2 element sequence to be auto converted
    c.convertFromPyObject = tools.convertTwoIntegersTemplate('wxGBPosition')

    c.addCppMethod('PyObject*', 'Get', '()', """\
        wxPyThreadBlocker blocker;
        return sipBuildResult(0, "(ii)", self->GetRow(), self->GetCol());
        """,
        pyArgsString="() -> (row, col)",
        briefDoc="Return the row and col properties as a tuple.")
    c.addCppMethod('void', 'Set', '(int row=0, int col=0)', """\
        self->SetRow(row);
        self->SetCol(col);
        """,
        briefDoc="Set both the row and column properties.")

    tools.addGetIMMethodTemplate(module, c, ['row', 'col'])


    # Add sequence protocol methods and other goodies
    c.addPyMethod('__str__', '(self)',             'return str(self.Get())')
    c.addPyMethod('__repr__', '(self)',            'return "wx.GBPosition"+str(self.Get())')
    c.addPyMethod('__len__', '(self)',             'return len(self.Get())')
    c.addPyMethod('__nonzero__', '(self)',         'return self.Get() != (0,0)')
    c.addPyMethod('__bool__', '(self)',            'return self.Get() != (0,0)')
    c.addPyMethod('__reduce__', '(self)',          'return (GBPosition, self.Get())')
    c.addPyMethod('__getitem__', '(self, idx)',    'return self.Get()[idx]')
    c.addPyMethod('__setitem__', '(self, idx, val)',
                  """\
                  if idx == 0: self.Row = val
                  elif idx == 1: self.Col = val
                  else: raise IndexError
                  """)
    c.addPyCode('GBPosition.__safe_for_unpickling__ = True')

    # In addition to the normal Row and Col properties let's also have lower
    # case versions.
    c.addProperty("Row GetRow SetRow")
    c.addProperty("Col GetCol SetCol")
    c.addProperty("row GetRow SetRow")
    c.addProperty("col GetCol SetCol")


    #-----------------------------------------------------------------
    c = module.find('wxGBSpan')
    assert isinstance(c, etgtools.ClassDef)

    # allow a 2 element sequence to be auto converted
    c.convertFromPyObject = tools.convertTwoIntegersTemplate('wxGBSpan')

    c.addCppMethod('PyObject*', 'Get', '()', """\
        wxPyThreadBlocker blocker;
        return sipBuildResult(0, "(ii)", self->GetRowspan(), self->GetColspan());
        """,
        pyArgsString="() -> (rowspan, colspan)",
        briefDoc="Return the rowspan and colspan properties as a tuple.")
    c.addCppMethod('void', 'Set', '(int rowspan=0, int colspan=0)', """\
        self->SetRowspan(rowspan);
        self->SetColspan(colspan);
        """,
        briefDoc="Set both the rowspan and colspan properties.")

    tools.addGetIMMethodTemplate(module, c, ['rowspan', 'colspan'])

    # Add sequence protocol methods and other goodies
    c.addPyMethod('__str__', '(self)',             'return str(self.Get())')
    c.addPyMethod('__repr__', '(self)',            'return "wx.GBSpan"+str(self.Get())')
    c.addPyMethod('__len__', '(self)',             'return len(self.Get())')
    c.addPyMethod('__nonzero__', '(self)',         'return self.Get() != (0,0)')
    c.addPyMethod('__bool__', '(self)',            'return self.Get() != (0,0)')
    c.addPyMethod('__reduce__', '(self)',          'return (GBSpan, self.Get())')
    c.addPyMethod('__getitem__', '(self, idx)',    'return self.Get()[idx]')
    c.addPyMethod('__setitem__', '(self, idx, val)',
                  """\
                  if idx == 0: self.Rowspan = val
                  elif idx == 1: self.Colspan = val
                  else: raise IndexError
                  """)
    c.addPyCode('GBSpan.__safe_for_unpickling__ = True')

    # In addition to the normal Rowspan and Colspan properties let's also have lower
    # case versions.
    c.addProperty("Rowspan GetRowspan SetRowspan")
    c.addProperty("Colspan GetColspan SetColspan")
    c.addProperty("rowspan GetRowspan SetRowspan")
    c.addProperty("colspan GetColspan SetColspan")


    #-----------------------------------------------------------------
    c = module.find('wxGBSizerItem')
    assert isinstance(c, etgtools.ClassDef)

    # transfer ownership of a sizer if the item is managing one
    c.find('wxGBSizerItem.sizer').transfer = True

    # deal with userData args in the ctors
    for m in c.find('wxGBSizerItem').all():
        if isinstance(m, etgtools.MethodDef) and m.findItem('userData'):
            m.find('userData').transfer = True
            m.find('userData').type = 'wxPyUserData*'

    # ignore some overloads that would be ambiguous from Python
    c.find('GetPos').findOverload('row').ignore()
    c.find('GetSpan').findOverload('rowspan').ignore()

    c.find('GetEndPos.row').out = True
    c.find('GetEndPos.col').out = True

    #-----------------------------------------------------------------
    c = module.find('wxGridBagSizer')
    assert isinstance(c, etgtools.ClassDef)

    tools.fixSizerClass(c)

    for func in c.findAll('Add'):
        if func.findItem('sizer'):
            func.find('sizer').transfer = True
        if func.findItem('userData'):
            func.find('userData').transfer = True
            func.find('userData').type = 'wxPyUserData*'
        if func.findItem('item'):
            func.find('item').transfer = True

    c.addCppMethod('wxSizerItem*', 'Add',
                   '(const wxSize& size, const wxGBPosition& pos, '
                     'const wxGBSpan& span = wxDefaultSpan, int flag = 0, '
                     'int border = 0, wxObject* userData /Transfer/ = NULL)',
        doc="Add a spacer using a :class:`Size` object.",
        body="return self->Add(size->x, size->y, *pos, *span, flag, border, userData);")


    c.addPyCode(
        "GridBagSizer.CheckForIntersectionPos = wx.deprecated(GridBagSizer.CheckForIntersection, 'Use CheckForIntersection instead.')")

    # TODO: In Classic we had GetChildren return a list of wxGBSizerItems (in
    # a faked out way). Figure out how to do that here too....

    #module.addItem(
    #    tools.wxListWrapperTemplate('wxGBSizerItemList', 'wxGBSizerItem', module, 'wxSizerItem'))


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()
