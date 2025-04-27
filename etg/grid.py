#---------------------------------------------------------------------------
# Name:        etg/grid.py
# Author:      Robin Dunn
#
# Created:     20-Dec-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_grid"
NAME      = "grid"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxGridCellCoords',

           'wxGridBlockCoords',
           'wxGridBlockDiffResult',
           'wxGridBlocks',

           'wxGridCellRenderer',
           'wxGridCellStringRenderer',
           'wxGridCellAutoWrapStringRenderer',
           'wxGridCellBoolRenderer',
           'wxGridCellDateRenderer',
           'wxGridCellDateTimeRenderer',
           'wxGridCellEnumRenderer',
           'wxGridCellFloatRenderer',
           'wxGridCellNumberRenderer',

           'wxGridActivationResult',
           'wxGridActivationSource',

           'wxGridCellEditor',
           'wxGridCellActivatableEditor',
           'wxGridCellTextEditor',
           'wxGridCellDateEditor',
           'wxGridCellAutoWrapStringEditor',
           'wxGridCellBoolEditor',
           'wxGridCellChoiceEditor',
           'wxGridCellEnumEditor',
           'wxGridCellFloatEditor',
           'wxGridCellNumberEditor',

           'wxGridFitMode',
           'wxGridCellAttr',

           'wxGridCornerHeaderRenderer',
           'wxGridHeaderLabelsRenderer',
           'wxGridRowHeaderRenderer',
           'wxGridColumnHeaderRenderer',
           'wxGridRowHeaderRendererDefault',
           'wxGridColumnHeaderRendererDefault',
           'wxGridCornerHeaderRendererDefault',

           'wxGridCellAttrProvider',
           'wxGridTableBase',
           'wxGridTableMessage',
           'wxGridStringTable',
           'wxGridSizesInfo',

           'wxGrid',
           'wxGridUpdateLocker',

           'wxGridEvent',
           'wxGridSizeEvent',
           'wxGridRangeSelectEvent',
           'wxGridEditorCreatedEvent',

           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addGlobalStr('wxGridNameStr', module.items[0])
    module.addPyCode("""\
        GRID_VALUE_STRING =    "string"
        GRID_VALUE_BOOL =      "bool"
        GRID_VALUE_NUMBER =    "long"
        GRID_VALUE_FLOAT =     "double"
        GRID_VALUE_CHOICE =    "choice"
        GRID_VALUE_DATE =      "date"
        GRID_VALUE_TEXT =      "string"
        GRID_VALUE_LONG =      "long"
        GRID_VALUE_CHOICEINT = "choiceint"
        GRID_VALUE_DATETIME =  "datetime"
        """)

    # Add compatibility constants for these since they've been removed from wxWidgets
    # TODO: Remove these in a future release.
    module.addPyCode("""\
        GRIDTABLE_REQUEST_VIEW_GET_VALUES = 2000
        GRIDTABLE_REQUEST_VIEW_SEND_VALUES = 2001
        """)

    module.insertItem(0, etgtools.TypedefDef(type='wxWindow', name='wxGridWindow'))

    #-----------------------------------------------------------------
    c = module.find('wxGridCellCoords')
    assert isinstance(c, etgtools.ClassDef)
    tools.addAutoProperties(c)
    c.find('operator!').ignore()
    c.find('operator=').ignore()

    # Add a typemap for 2 element sequences
    c.convertFromPyObject = tools.convertTwoIntegersTemplate('wxGridCellCoords')

    c.addCppMethod('PyObject*', 'Get', '()', """\
        wxPyThreadBlocker blocker;
        return sipBuildResult(0, "(ii)", self->GetRow(), self->GetCol());
        """,
        pyArgsString="() -> (row,col)",
        briefDoc="Return the row and col properties as a tuple.")

    tools.addGetIMMethodTemplate(module, c, ['Row', 'Col'])

    # Add sequence protocol methods and other goodies
    c.addPyMethod('__str__', '(self)',             'return str(self.Get())')
    c.addPyMethod('__repr__', '(self)',            'return "GridCellCoords"+str(self.Get())')
    c.addPyMethod('__len__', '(self)',             'return len(self.Get())')
    c.addPyMethod('__nonzero__', '(self)',         'return self.Get() != (0,0)')
    c.addPyMethod('__bool__', '(self)',            'return self.Get() != (0,0)')
    c.addPyMethod('__reduce__', '(self)',          'return (GridCellCoords, self.Get())')
    c.addPyMethod('__getitem__', '(self, idx)',    'return self.Get()[idx]')
    c.addPyMethod('__setitem__', '(self, idx, val)',
                  """\
                  if idx == 0: self.Row = val
                  elif idx == 1: self.Col = val
                  else: raise IndexError
                  """)
    c.addPyCode('GridCellCoords.__safe_for_unpickling__ = True')

    module.addItem(
        tools.wxArrayWrapperTemplate('wxGridCellCoordsArray', 'wxGridCellCoords', module,
                                     getItemCopy=True))


    #-----------------------------------------------------------------
    c = module.find('wxGridBlockCoords')
    tools.addAutoProperties(c)

    c.find('operator!').ignore()
    c.addCppMethod('int', '__bool__', '()', "return self->operator!();")

    c.addCppMethod('PyObject*', 'Get', '()', """\
        wxPyThreadBlocker blocker;
        return sipBuildResult(0, "(iiii)", self->GetTopRow(), self->GetLeftCol(), self->GetBottomRow(), self->GetRightCol());
        """,
        pyArgsString="() -> (topRow, leftCol, bottomRow, rightCol)",
        briefDoc="Return the block coordinants as a tuple.")

    c.addPyMethod('__str__', '(self)',             'return str(self.Get())')
    c.addPyMethod('__repr__', '(self)',            'return "GridBlockCoords"+str(self.Get())')

    #-----------------------------------------------------------------
    c = module.find('wxGridBlockDiffResult')
    c.find('m_parts').ignore()

    c.addCppMethod('PyObject*', '_getParts', '()',
        """\
        wxPyThreadBlocker blocker;
        PyObject* ret = PyTuple_New(4);
        if (ret) {
            PyTuple_SET_ITEM(ret, 0, wxPyConstructObject(&self->m_parts[0], "wxGridBlockCoords", false));
            PyTuple_SET_ITEM(ret, 1, wxPyConstructObject(&self->m_parts[1], "wxGridBlockCoords", false));
            PyTuple_SET_ITEM(ret, 2, wxPyConstructObject(&self->m_parts[2], "wxGridBlockCoords", false));
            PyTuple_SET_ITEM(ret, 3, wxPyConstructObject(&self->m_parts[3], "wxGridBlockCoords", false));
        }
        return ret;
        """)
    c.addProperty('m_parts', '_getParts')


    #-----------------------------------------------------------------
    c = module.find('wxGridBlocks')
    c.addPrivateDefaultCtor()
    c.addPrivateAssignOp()

    c.addPyMethod('__iter__', '(self)',
                  'return PyGridBlocksIterator(self)',
                  "Returns a Python iterator for accessing the collection of grid blocks.")

    # This class is the Python iterator that knows how to fetch blocks from the
    # wxGridBlocks object
    c.addPyCode("""\
        class PyGridBlocksIterator(object):
            "A Python iterator for GridBlocks objects"
            def __init__(self, blocks):
                self._blocks = blocks
                self._iterator = self._blocks.begin()

            def __next__(self):
                if self._iterator == self._blocks.end():
                    raise StopIteration
                obj = self._iterator._get()
                self._iterator = self._iterator._next()
                return obj
        """)


    # c.find('iterator').addCppMethod('wxGridBlocks::iterator', '_next', '()',
    #                                 "return self->operator++();")
    # c.find('iterator').addCppMethod('const wxGridBlockCoords&', '_get', '()',
    #                                 "return self->operator*();")

    # TODO: Doing these the normal way (above) breaks because it tries to use just
    # "iterator" for the self param type, instead of wxGridBlocks::iterator.
    # That should be fixable, but until then just add these methods the manual
    # sip way.
    c.find('iterator').addItem(etgtools.WigCode("""\
        iterator& _next();
        %MethodCode
            PyErr_Clear();
            Py_BEGIN_ALLOW_THREADS
            sipRes = &sipCpp->operator++();
            Py_END_ALLOW_THREADS
            if (PyErr_Occurred()) return 0;
        %End

        const wxGridBlockCoords& _get() const;
        %MethodCode
            PyErr_Clear();
            Py_BEGIN_ALLOW_THREADS
            sipRes =  new ::wxGridBlockCoords(sipCpp->operator*());
            Py_END_ALLOW_THREADS
            if (PyErr_Occurred()) return 0;
        %End

        bool __eq__(const iterator& it) const;
        bool __ne__(const iterator& it) const;
        """))


    #-----------------------------------------------------------------
    c = module.find('wxGridSizesInfo')
    c.find('m_customSizes').ignore()   # TODO: Add support for wxUnsignedToIntHashMap??


    #-----------------------------------------------------------------
    def fixRendererClass(name):
        klass = module.find(name)
        assert isinstance(klass, etgtools.ClassDef)
        tools.fixRefCountedClass(klass)
        tools.addAutoProperties(klass)

        methods = [
            ('Clone',       "virtual wxGridCellRenderer* Clone() const /Factory/;"),
            ('Draw',        "virtual void Draw(wxGrid& grid, wxGridCellAttr& attr, wxDC& dc, "
                            "    const wxRect& rect, int row, int col, bool isSelected);"),
            ('GetBestSize', "virtual wxSize GetBestSize(wxGrid& grid, wxGridCellAttr& attr, "
                            "    wxDC& dc, int row, int col);"),
            ]
        for method, code in methods:
            if not klass.findItem(method):
                klass.addItem(etgtools.WigCode(code))


    c = module.find('wxGridCellRenderer')
    c.addPrivateCopyCtor()
    c.find('~wxGridCellRenderer').ignore(False)
    c.find('Clone').factory = True
    c.find('Draw').isPureVirtual = False
    tools.fixRefCountedClass(c)

    for name in ITEMS:
        if 'Cell' in name and 'Renderer' in name:
            fixRendererClass(name)

    module.addPyCode("PyGridCellRenderer = wx.deprecated(GridCellRenderer, 'Use GridCellRenderer instead.')")


    #-----------------------------------------------------------------

    c = module.find('wxGridActivationResult')
    c.addPrivateAssignOp()
    c.addPrivateDefaultCtor()
    c.instanceCode = """\
        wxGridActivationResult result = wxGridActivationResult::DoNothing();
        sipCpp = &result;
        """


    c = module.find('wxGridActivationSource')
    c.noDefCtor = True
    c.addPrivateAssignOp()


    #-----------------------------------------------------------------
    def fixEditorClass(name):
        klass = module.find(name)
        assert isinstance(klass, etgtools.ClassDef)
        tools.fixRefCountedClass(klass)
        tools.addAutoProperties(klass)

        methods = [
            ('BeginEdit',  "virtual void BeginEdit(int row, int col, wxGrid* grid);"),
            ('Clone',      "virtual wxGridCellEditor* Clone() const /Factory/;"),
            ('Create',     "virtual void Create(wxWindow* parent, wxWindowID id, wxEvtHandler* evtHandler);"),
            #('EndEdit',    "virtual bool EndEdit(int row, int col, const wxGrid* grid, const wxString& oldval, wxString* newval);"),
            ('ApplyEdit',  "virtual void ApplyEdit(int row, int col, wxGrid* grid);"),
            ('Reset',      "virtual void Reset();"),
            ('GetValue',   "virtual wxString GetValue() const;"),
            ]
        for method, code in methods:
            if not klass.findItem(method):
                klass.addItem(etgtools.WigCode(code))


        # Fix up EndEdit so it returns newval on success or None on failure
        pureVirtual = False
        if klass.findItem('EndEdit'):
            klass.find('EndEdit').ignore()
            pureVirtual = True

        # The Python version of EndEdit has a different signature than the
        # C++ version, so we need to take care of mapping between them so the
        # C++ compiler still recognizes this as a match for the virtual
        # method in the base class.
        klass.addCppMethod('PyObject*', 'EndEdit', '(int row, int col, const wxGrid* grid, const wxString& oldval)',
            cppSignature='bool (int row, int col, const wxGrid* grid, const wxString& oldval, wxString* newval)',
            pyArgsString='(row, col, grid, oldval)',
            isVirtual=True,
            isPureVirtual=pureVirtual,
            doc="""\
                End editing the cell.

                This function must check if the current value of the editing cell
                is valid and different from the original value in its string
                form. If not then simply return None.  If it has changed then
                this method should save the new value so that ApplyEdit can
                apply it later and the string representation of the new value
                should be returned.

                Notice that this method shoiuld not modify the grid as the
                change could still be vetoed.
                """,

            # Code for Python --> C++ calls.  Make it return newval or None.
            body="""\
                bool rv;
                wxString newval;
                rv = self->EndEdit(row, col, grid, *oldval, &newval);
                if (rv) {
                    return wx2PyString(newval);
                }
                else {
                    Py_INCREF(Py_None);
                    return Py_None;
                }
                """,

            # Code for C++ --> Python calls. This is used when a C++ method
            # call needs to be reflected to a call to the overridden Python
            # method, so we need to translate between the real C++ signature
            # and the Python signature.
            virtualCatcherCode="""\
                // VirtualCatcherCode for wx.grid.GridCellEditor.EndEdit
                PyObject *result;
                result = sipCallMethod(0, sipMethod, "iiDN", row, col,
                                       const_cast<wxGrid *>(grid),sipType_wxGrid,NULL,
                                       new wxString(oldval),sipType_wxString,NULL);
                if (result == NULL) {
                    if (PyErr_Occurred())
                        PyErr_Print();
                    sipRes = false;
                }
                else if (result == Py_None) {
                    sipRes = false;
                }
                else {
                    sipRes = true;
                    *newval = Py2wxString(result);
                }
                Py_XDECREF(result);
                """  if pureVirtual else "",  # only used with the base class
            )


    c = module.find('wxGridCellEditor')
    c.addPrivateCopyCtor()
    c.find('~wxGridCellEditor').ignore(False)
    c.find('Clone').factory = True
    tools.fixRefCountedClass(c)


    c = module.find('wxGridCellActivatableEditor')


    c = module.find('wxGridCellChoiceEditor')
    c.find('wxGridCellChoiceEditor').findOverload('count').ignore()

    for name in ITEMS:
        if 'Cell' in name and 'Editor' in name and name != 'wxGridCellActivatableEditor':
            fixEditorClass(name)

    module.addPyCode("PyGridCellEditor = wx.deprecated(GridCellEditor, 'Use GridCellEditor instead.')")

    #-----------------------------------------------------------------
    c = module.find('wxGridCellAttr')
    c.addPrivateCopyCtor()
    c.find('~wxGridCellAttr').ignore(False)
    c.find('Clone').factory = True
    tools.fixRefCountedClass(c)

    c.find('GetAlignment.hAlign').out = True
    c.find('GetAlignment.vAlign').out = True
    c.find('GetNonDefaultAlignment.hAlign').out = True
    c.find('GetNonDefaultAlignment.vAlign').out = True
    c.find('GetSize.num_rows').out = True
    c.find('GetSize.num_cols').out = True

    c.find('SetEditor.editor').transfer = True  # these are probably redundant now...
    c.find('SetRenderer.renderer').transfer = True

    c.find('GetRendererPtr').ignore()

    #-----------------------------------------------------------------
    module.find('wxGridCellRendererPtr').piIgnored = True
    module.find('wxGridCellEditorPtr').piIgnored = True
    module.find('wxGridCellAttrPtr').piIgnored = True

    #-----------------------------------------------------------------
    # The instanceCode attribute is code that is used to make a default
    # instance of the class. We can't create them using the same class in
    # this case because they are abstract.

    c = module.find('wxGridCornerHeaderRenderer')
    c.instanceCode = 'sipCpp = new wxGridCornerHeaderRendererDefault;'

    c = module.find('wxGridRowHeaderRenderer')
    c.instanceCode = 'sipCpp = new wxGridRowHeaderRendererDefault;'

    c = module.find('wxGridColumnHeaderRenderer')
    c.instanceCode = 'sipCpp = new wxGridColumnHeaderRendererDefault;'



    #-----------------------------------------------------------------
    c = module.find('wxGridCellAttrProvider')
    c.addPrivateCopyCtor()

    c.find('SetAttr.attr').transfer = True
    c.find('SetRowAttr.attr').transfer = True
    c.find('SetColAttr.attr').transfer = True

    module.addPyCode("PyGridCellAttrProvider = wx.deprecated(GridCellAttrProvider, 'Use GridCellAttrProvider instead.')")


    #-----------------------------------------------------------------
    c = module.find('wxGridTableBase')
    c.addPrivateCopyCtor()

    c.find('SetAttr.attr').transfer = True
    c.find('SetRowAttr.attr').transfer = True
    c.find('SetColAttr.attr').transfer = True

    module.addPyCode("PyGridTableBase = wx.deprecated(GridTableBase, 'Use GridTableBase instead.')")


    # Make the GetValue methods easier to use from Python.  For example,
    # instead of needing to always return a string, the GetValue in the derived
    # class can return any type (as long as the renderer and editor knows how
    # to deal with it, and the value can be converted to a string for display).
    m = c.find('GetValue')
    m.type = 'PyObject*'
    m.cppSignature = 'wxString (int row, int col)'
    m.setCppCode("return wx2PyString(self->GetValue(row, col));")
    m.virtualCatcherCode = """\
        // virtualCatcherCode for GridTableBase.GetValue
        PyObject *result = sipCallMethod(&sipIsErr, sipMethod, "ii", row, col);
        if (result == NULL) {
            if (PyErr_Occurred())
                PyErr_Print();
            sipRes = "";
        }
        else if (result == Py_None) {
            sipRes = "";
        }
        else {
            if (!PyBytes_Check(result) && !PyUnicode_Check(result)) {
                PyObject* old = result;
                result = PyObject_Str(result);
                Py_DECREF(old);
            }
            sipRes = Py2wxString(result);
        }
        Py_XDECREF(result);
        """

    # SetValue is okay as-is...


    # Replace these virtuals in the base class with Python methods, they just
    # need to call GetValue or SetValue directly since they must already be
    # implemented in the derived Python class because they are pure virtual.
    c.addPyMethod('GetValueAsLong', '(self, row, col)',
        body="""\
            val = self.GetValue(row, col)
            try:
                return int(val)
            except ValueError:
                return 0
            """, docsIgnored=True)

    c.addPyMethod('GetValueAsDouble', '(self, row, col)',
        body="""\
            val = self.GetValue(row, col)
            try:
                return float(val)
            except ValueError:
                return 0.0
            """, docsIgnored=True)

    c.addPyMethod('GetValueAsBool', '(self, row, col)',
        body="""\
            val = self.GetValue(row, col)
            try:
                return bool(val)
            except ValueError:
                return False
            """, docsIgnored=True)

    c.addPyMethod('SetValueAsLong', '(self, row, col, value)',
        body="self.SetValue(row, col, int(value))", docsIgnored=True)

    c.addPyMethod('SetValueAsDouble', '(self, row, col, value)',
        body="self.SetValue(row, col, float(value))", docsIgnored=True)

    c.addPyMethod('SetValueAsBool', '(self, row, col, value)',
        body="self.SetValue(row, col, bool(value))", docsIgnored=True)


    # Should we add support for using generic PyObjects in the *AsCustom
    # methods? I don't think it is necessary due to the GetValue
    # modifications above, so for now, at least, let.s just ignore them.
    c.find('GetValueAsCustom').ignore()
    c.find('SetValueAsCustom').ignore()


    #-----------------------------------------------------------------
    c = module.find('wxGridStringTable')
    c.addPrivateCopyCtor()


    #-----------------------------------------------------------------
    c = module.find('wxGridTableMessage')
    c.addPrivateCopyCtor()


    #-----------------------------------------------------------------
    c = module.find('wxGrid')
    tools.fixWindowClass(c, ignoreProtected=False)
    c.bases = ['wxScrolledCanvas']

    c.find('GetColLabelAlignment.horiz').out = True
    c.find('GetColLabelAlignment.vert').out = True
    c.find('GetRowLabelAlignment.horiz').out = True
    c.find('GetRowLabelAlignment.vert').out = True

    c.find('GetCellAlignment.horiz').out = True
    c.find('GetCellAlignment.vert').out = True
    c.find('GetDefaultCellAlignment.horiz').out = True
    c.find('GetDefaultCellAlignment.vert').out = True


    c.find('RegisterDataType.renderer').transfer = True
    c.find('RegisterDataType.editor').transfer = True

    c.find('SetRowAttr.attr').transfer = True
    c.find('SetColAttr.attr').transfer = True
    c.find('SetCellEditor.editor').transfer = True
    c.find('SetCellRenderer.renderer').transfer = True

    # This overload is deprecated, so don't generate code for it.
    c.find('SetCellValue').findOverload('wxString &val').ignore()

    c.find('SetDefaultEditor.editor').transfer = True
    c.find('SetDefaultRenderer.renderer').transfer = True

    for n in ['GetColGridLinePen', 'GetDefaultGridLinePen', 'GetRowGridLinePen']:
        c.find(n).isVirtual = True


    # The SetTable method can optionally pass ownership of the table
    # object to the grid, so we need to optionally update the
    # ownership of the Python proxy object to match.
    c.find('SetTable').pyName = '_SetTable'
    c.addPyMethod('SetTable', '(self, table, takeOwnership=False, selmode=Grid.GridSelectCells)',
        piArgsString='(self, table, takeOwnership=False, selmode=GridSelectCells)',
        doc="Set the Grid Table to be used by this grid.",
        body="""\
            val = self._SetTable(table, takeOwnership, selmode)
            if takeOwnership:
                import wx.siplib
                wx.siplib.transferto(table, self)
            return val
        """)


    # SIP will normally try to add support for overriding this method since
    # it is inherited from super classes, but in this case we want it to be
    # ignored (because IRL it is private in one of the intermediate classes)
    # so we'll tell SIP that it is private here instead.
    c.addItem(etgtools.WigCode("""\
        wxSize GetSizeAvailableForScrollTarget(const wxSize& size);
        """, protection='private'))


    # Add a simpler set of names for the wxGridSelectionModes enum
    c.addPyCode("""\
        Grid.SelectCells = Grid.GridSelectCells
        Grid.SelectRows = Grid.GridSelectRows
        Grid.SelectColumns = Grid.GridSelectColumns
        Grid.SelectRowsOrColumns = Grid.GridSelectRowsOrColumns
        """)


    c.find('SetCellAlignment').findOverload('align').ignore()
    c.find('SetCellTextColour').overloads = []

    c.find('GetGridWindowOffset').findOverload('int &x').ignore()


    # Custom code to deal with the wxGridBlockCoordsVector return type of these
    # methods. It's a wxVector, which we'll just convert to a list.

    # TODO: There are a few of these now so we ought to either wrap wxVector, or add
    #       something in tweaker_tools to make adding code like this easier and more
    #       automated.
    code = """\
        wxPyThreadBlocker blocker;
        PyObject* result = PyList_New(0);
        wxGridBlockCoordsVector vector = self->{method}();
        for (size_t idx=0; idx < vector.size(); idx++) {{
            PyObject* obj;
            wxGridBlockCoords* item = new wxGridBlockCoords(vector[idx]);
            obj = wxPyConstructObject((void*)item, "wxGridBlockCoords", true);
            PyList_Append(result, obj);
            Py_DECREF(obj);
        }}
        return result;
        """
    c.find('GetSelectedRowBlocks').type = 'PyObject*'
    c.find('GetSelectedRowBlocks').setCppCode(code.format(method='GetSelectedRowBlocks'))
    c.find('GetSelectedColBlocks').type = 'PyObject*'
    c.find('GetSelectedColBlocks').setCppCode(code.format(method='GetSelectedColBlocks'))


    #-----------------------------------------------------------------
    c = module.find('wxGridUpdateLocker')
    c.addPrivateCopyCtor()

    # context manager methods
    c.addPyMethod('__enter__', '(self)', 'return self')
    c.addPyMethod('__exit__', '(self, exc_type, exc_val, exc_tb)', 'return False')


    #-----------------------------------------------------------------

    for name in ['wxGridSizeEvent',
                 'wxGridRangeSelectEvent',
                 'wxGridEditorCreatedEvent',
                 'wxGridEvent'
                 ]:
        c = module.find(name)
        tools.fixEventClass(c)


    module.addPyCode("""\
        EVT_GRID_CELL_LEFT_CLICK = wx.PyEventBinder( wxEVT_GRID_CELL_LEFT_CLICK )
        EVT_GRID_CELL_RIGHT_CLICK = wx.PyEventBinder( wxEVT_GRID_CELL_RIGHT_CLICK )
        EVT_GRID_CELL_LEFT_DCLICK = wx.PyEventBinder( wxEVT_GRID_CELL_LEFT_DCLICK )
        EVT_GRID_CELL_RIGHT_DCLICK = wx.PyEventBinder( wxEVT_GRID_CELL_RIGHT_DCLICK )
        EVT_GRID_LABEL_LEFT_CLICK = wx.PyEventBinder( wxEVT_GRID_LABEL_LEFT_CLICK )
        EVT_GRID_LABEL_RIGHT_CLICK = wx.PyEventBinder( wxEVT_GRID_LABEL_RIGHT_CLICK )
        EVT_GRID_LABEL_LEFT_DCLICK = wx.PyEventBinder( wxEVT_GRID_LABEL_LEFT_DCLICK )
        EVT_GRID_LABEL_RIGHT_DCLICK = wx.PyEventBinder( wxEVT_GRID_LABEL_RIGHT_DCLICK )
        EVT_GRID_ROW_SIZE = wx.PyEventBinder( wxEVT_GRID_ROW_SIZE )
        EVT_GRID_COL_SIZE = wx.PyEventBinder( wxEVT_GRID_COL_SIZE )
        EVT_GRID_COL_AUTO_SIZE = wx.PyEventBinder( wxEVT_GRID_COL_AUTO_SIZE )
        EVT_GRID_RANGE_SELECTING = wx.PyEventBinder( wxEVT_GRID_RANGE_SELECTING )
        EVT_GRID_RANGE_SELECTED = wx.PyEventBinder( wxEVT_GRID_RANGE_SELECTED )
        EVT_GRID_CELL_CHANGING = wx.PyEventBinder( wxEVT_GRID_CELL_CHANGING )
        EVT_GRID_CELL_CHANGED = wx.PyEventBinder( wxEVT_GRID_CELL_CHANGED )
        EVT_GRID_SELECT_CELL = wx.PyEventBinder( wxEVT_GRID_SELECT_CELL )
        EVT_GRID_EDITOR_SHOWN = wx.PyEventBinder( wxEVT_GRID_EDITOR_SHOWN )
        EVT_GRID_EDITOR_HIDDEN = wx.PyEventBinder( wxEVT_GRID_EDITOR_HIDDEN )
        EVT_GRID_EDITOR_CREATED = wx.PyEventBinder( wxEVT_GRID_EDITOR_CREATED )
        EVT_GRID_CELL_BEGIN_DRAG = wx.PyEventBinder( wxEVT_GRID_CELL_BEGIN_DRAG )
        EVT_GRID_ROW_MOVE = wx.PyEventBinder( wxEVT_GRID_ROW_MOVE )
        EVT_GRID_COL_MOVE = wx.PyEventBinder( wxEVT_GRID_COL_MOVE )
        EVT_GRID_COL_SORT = wx.PyEventBinder( wxEVT_GRID_COL_SORT )
        EVT_GRID_TABBING = wx.PyEventBinder( wxEVT_GRID_TABBING )

        # The same as above but with the ability to specify an identifier
        EVT_GRID_CMD_CELL_LEFT_CLICK =     wx.PyEventBinder( wxEVT_GRID_CELL_LEFT_CLICK,    1 )
        EVT_GRID_CMD_CELL_RIGHT_CLICK =    wx.PyEventBinder( wxEVT_GRID_CELL_RIGHT_CLICK,   1 )
        EVT_GRID_CMD_CELL_LEFT_DCLICK =    wx.PyEventBinder( wxEVT_GRID_CELL_LEFT_DCLICK,   1 )
        EVT_GRID_CMD_CELL_RIGHT_DCLICK =   wx.PyEventBinder( wxEVT_GRID_CELL_RIGHT_DCLICK,  1 )
        EVT_GRID_CMD_LABEL_LEFT_CLICK =    wx.PyEventBinder( wxEVT_GRID_LABEL_LEFT_CLICK,   1 )
        EVT_GRID_CMD_LABEL_RIGHT_CLICK =   wx.PyEventBinder( wxEVT_GRID_LABEL_RIGHT_CLICK,  1 )
        EVT_GRID_CMD_LABEL_LEFT_DCLICK =   wx.PyEventBinder( wxEVT_GRID_LABEL_LEFT_DCLICK,  1 )
        EVT_GRID_CMD_LABEL_RIGHT_DCLICK =  wx.PyEventBinder( wxEVT_GRID_LABEL_RIGHT_DCLICK, 1 )
        EVT_GRID_CMD_ROW_SIZE =            wx.PyEventBinder( wxEVT_GRID_ROW_SIZE,           1 )
        EVT_GRID_CMD_COL_SIZE =            wx.PyEventBinder( wxEVT_GRID_COL_SIZE,           1 )
        EVT_GRID_CMD_COL_AUTO_SIZE =       wx.PyEventBinder( wxEVT_GRID_COL_AUTO_SIZE,      1 )
        EVT_GRID_CMD_RANGE_SELECTING =     wx.PyEventBinder( wxEVT_GRID_RANGE_SELECTING,    1 )
        EVT_GRID_CMD_RANGE_SELECTED =      wx.PyEventBinder( wxEVT_GRID_RANGE_SELECTED,     1 )
        EVT_GRID_CMD_CELL_CHANGING =       wx.PyEventBinder( wxEVT_GRID_CELL_CHANGING,      1 )
        EVT_GRID_CMD_CELL_CHANGED =        wx.PyEventBinder( wxEVT_GRID_CELL_CHANGED,       1 )
        EVT_GRID_CMD_SELECT_CELL =         wx.PyEventBinder( wxEVT_GRID_SELECT_CELL,        1 )
        EVT_GRID_CMD_EDITOR_SHOWN =        wx.PyEventBinder( wxEVT_GRID_EDITOR_SHOWN,       1 )
        EVT_GRID_CMD_EDITOR_HIDDEN =       wx.PyEventBinder( wxEVT_GRID_EDITOR_HIDDEN,      1 )
        EVT_GRID_CMD_EDITOR_CREATED =      wx.PyEventBinder( wxEVT_GRID_EDITOR_CREATED,     1 )
        EVT_GRID_CMD_CELL_BEGIN_DRAG =     wx.PyEventBinder( wxEVT_GRID_CELL_BEGIN_DRAG,    1 )
        EVT_GRID_CMD_ROW_MOVE =            wx.PyEventBinder( wxEVT_GRID_ROW_MOVE,           1 )
        EVT_GRID_CMD_COL_MOVE =            wx.PyEventBinder( wxEVT_GRID_COL_MOVE,           1 )
        EVT_GRID_CMD_COL_SORT =            wx.PyEventBinder( wxEVT_GRID_COL_SORT,           1 )
        EVT_GRID_CMD_TABBING =             wx.PyEventBinder( wxEVT_GRID_TABBING,            1 )

        # Just for compatibility, remove them in a future release
        EVT_GRID_RANGE_SELECT =            EVT_GRID_RANGE_SELECTED
        EVT_GRID_CMD_RANGE_SELECT =        EVT_GRID_CMD_RANGE_SELECTED
        wxEVT_GRID_RANGE_SELECT =          wxEVT_GRID_RANGE_SELECTED

        """)

    #-----------------------------------------------------------------
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

