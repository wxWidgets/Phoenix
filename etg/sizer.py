#---------------------------------------------------------------------------
# Name:        etg/sizer.py
# Author:      Kevin Ollivier
#              Robin Dunn
#
# Created:     26-Aug-2011
# Copyright:   (c) 2011 by Wide Open Technologies
# Copyright:   (c) 2011-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

from textwrap import dedent

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "sizer"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [
            'wxSizerItem',
            'wxSizerFlags',

            'wxSizer',
            'wxBoxSizer',
            'wxStaticBoxSizer',
            'wxGridSizer',
            'wxFlexGridSizer',
            'wxStdDialogButtonSizer',
        ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.


    c = module.find('wxSizerItem')
    assert isinstance(c, etgtools.ClassDef)
    tools.removeVirtuals(c)

    # ctors taking a sizer transfer ownership
    for m in c.find('wxSizerItem').all():
        if m.findItem('sizer'):
            m.find('sizer').transfer = True

    c.find('AssignSizer.sizer').transfer = True

    # userData args transfer ownership too, and we'll use wxPyUserData
    # instead of any wxObject
    for m in c.allItems():
        if isinstance(m, etgtools.MethodDef) and m.findItem('userData'):
            m.find('userData').transfer = True
            m.find('userData').type = 'wxPyUserData*'

    good = c.find('GetUserData')
    good.type = 'wxPyUserData*'
    good.setCppCode('return dynamic_cast<wxPyUserData*>(self->GetUserData());')

    # these have been deprecated for a while so go ahead and get rid of them
    c.find('SetWindow').ignore()
    c.find('SetSizer').ignore()
    c.find('SetSpacer').ignore()

    c.addPrivateCopyCtor()

    #---------------------------------------------
    c = module.find('wxSizer')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixSizerClass(c)
    c.addPrivateCopyCtor()
    c.addPrivateAssignOp()

    for func in c.findAll('Add') + c.findAll('Insert') + c.findAll('Prepend'):
        if func.findItem('sizer'):
            func.find('sizer').transfer = True
        if func.findItem('userData'):
            func.find('userData').transfer = True
            func.find('userData').type = 'wxPyUserData*'
        if func.findItem('item'):
            func.find('item').transfer = True

    c.find('GetChildren').overloads = []
    c.find('GetChildren').noCopy = True

    # Needs wxWin 2.6 compatibility
    c.find('Remove').findOverload('(wxWindow *window)').ignore()

    # deprecated and removed
    c.find('SetVirtualSizeHints').ignore()

    c.addPyMethod('AddMany', '(self, items)',
        doc="""\
        :meth:`AddMany` is a convenience method for adding several items to a sizer
        at one time. Simply pass it a list of tuples, where each tuple
        consists of the parameters that you would normally pass to the :meth:`Add`
        method.
        """,
        body="""\
        for item in items:
            if not isinstance(item, (tuple, list)):
                item = (item, )
            self.Add(*item)
        """)

    c.addCppMethod('wxSizerItem*', 'Add',
                   '(const wxSize& size, int proportion=0, int flag=0, '
                   'int border=0, wxPyUserData* userData /Transfer/ = NULL)',
        doc="Add a spacer using a :class:`Size` object.",
        body="return self->Add(size->x, size->y, proportion, flag, border, userData);")

    c.addCppMethod('wxSizerItem*', 'Prepend',
                   '(const wxSize& size, int proportion=0, int flag=0, '
                   'int border=0, wxPyUserData* userData /Transfer/ = NULL)',
        doc="Prepend a spacer using a :class:`Size` object.",
        body="return self->Prepend(size->x, size->y, proportion, flag, border, userData);")

    c.addCppMethod('wxSizerItem*', 'Insert',
                   '(ulong index, const wxSize& size, int proportion=0, int flag=0, '
                   'int border=0, wxPyUserData* userData /Transfer/ = NULL)',
        doc="Insert a spacer using a :class:`Size` object.",
        body="return self->Insert(index, size->x, size->y, proportion, flag, border, userData);")


    c.addCppMethod('wxSizerItem*', 'Add',
                   '(const wxSize& size, const wxSizerFlags& flags)',
        doc="Add a spacer using a :class:`Size` object.",
        body="return self->Add(size->x, size->y, *flags);")

    c.addCppMethod('wxSizerItem*', 'Prepend',
                   '(const wxSize& size, const wxSizerFlags& flags)',
        doc="Prepend a spacer using a :class:`Size` object.",
        body="return self->Prepend(size->x, size->y, *flags);")

    c.addCppMethod('wxSizerItem*', 'Insert',
                   '(ulong index, const wxSize& size, const wxSizerFlags& flags)',
        doc="Insert a spacer using a :class:`Size` object.",
        body="return self->Insert(index, size->x, size->y, *flags);")

    c.addPyMethod('__nonzero__', '(self)',
        doc="Can be used to test if the C++ part of the sizer still exists, with \n"
            "code like this::\n\n"
            "    if theSizer:\n"
            "        doSomething()",
        body="""\
        import wx.siplib
        return not wx.siplib.isdeleted(self)
        """)

    c.addPyMethod('__iter__', '(self)',
        doc = "A Python convenience method that allows Sizers to act as iterables that will yield their wx.SizerItems.",
        body = "for item in self.GetChildren(): yield item")

    c.addPyCode('Sizer.__bool__ = Sizer.__nonzero__') # For Python 3

    m = etgtools.MethodDef(type='void', name='RecalcSizes', argsString='()', isVirtual=True,
        briefDoc="This is a deprecated version of RepositionChildren()",
        detailedDoc=[dedent("""\
            This is a deprecated version of RepositionChildren() which doesn't take
            the minimal size parameter which is not needed for very simple sizers
            but typically is for anything more complicated, so prefer to override
            RepositionChildren() in new code.

            If RepositionChildren() is not overridden, this method must be
            overridden, calling the base class version results in an assertion
            failure.
            """)],
        )
    c.insertItemAfter(c.find('RepositionChildren'), m)


    #---------------------------------------------
    c = module.find('wxBoxSizer')
    tools.fixSizerClass(c)
    c.find('wxBoxSizer.orient').default = 'wxHORIZONTAL'


    #---------------------------------------------
    c = module.find('wxStaticBoxSizer')
    tools.fixSizerClass(c)
    c.find('wxStaticBoxSizer.orient').default = 'wxHORIZONTAL'


    #---------------------------------------------
    c = module.find('wxGridSizer')
    tools.fixSizerClass(c)

    c.addPyMethod('CalcRowsCols', '(self)',
        doc="""\
        CalcRowsCols() -> (rows, cols)

        Calculates how many rows and columns will be in the sizer based
        on the current number of items and also the rows, cols specified
        in the constructor.
        """,
        body="""\
        nitems = len(self.GetChildren())
        rows = self.GetRows()
        cols = self.GetCols()
        assert rows != 0 or cols != 0, "Grid sizer must have either rows or columns fixed"
        if cols != 0:
            rows = (nitems + cols - 1) / cols
        elif rows != 0:
            cols = (nitems + rows - 1) / rows
        return (rows, cols)
        """)

    #---------------------------------------------
    c = module.find('wxFlexGridSizer')
    tools.fixSizerClass(c)


    #---------------------------------------------
    c = module.find('wxStdDialogButtonSizer')
    tools.fixSizerClass(c)



    module.addPyCode("PySizer = wx.deprecated(Sizer, 'Use Sizer instead.')")

    module.addItem(tools.wxListWrapperTemplate('wxSizerItemList', 'wxSizerItem', module))


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

