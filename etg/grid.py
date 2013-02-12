#---------------------------------------------------------------------------
# Name:        etg/grid.py
# Author:      Robin Dunn
#
# Created:     20-Dec-2012
# Copyright:   (c) 2013 by Total Control Software
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
           
           'wxGridCellRenderer',
           'wxGridCellAutoWrapStringRenderer',
           'wxGridCellBoolRenderer',
           'wxGridCellDateTimeRenderer',
           'wxGridCellEnumRenderer',
           'wxGridCellFloatRenderer',
           'wxGridCellNumberRenderer',
           'wxGridCellStringRenderer',
           
           'wxGridCellEditor',
           'wxGridCellAutoWrapStringEditor',
           'wxGridCellBoolEditor',
           'wxGridCellChoiceEditor',
           'wxGridCellEnumEditor',
           'wxGridCellTextEditor',
           'wxGridCellFloatEditor',
           'wxGridCellNumberEditor',
           
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
        GRID_VALUE_TEXT =      "string"
        GRID_VALUE_LONG =      "long"
        GRID_VALUE_CHOICEINT = "choiceint"
        GRID_VALUE_DATETIME =  "datetime"
        """)
    
    #-----------------------------------------------------------------
    c = module.find('wxGridCellCoords')
    assert isinstance(c, etgtools.ClassDef)
    tools.addAutoProperties(c)
    c.find('operator!').ignore()
    c.find('operator=').ignore()
    
    # Add a typemap for 2 element sequences
    c.convertFromPyObject = tools.convertTwoIntegersTemplate('wxGridCellCoords')
        
    c.addCppMethod('PyObject*', 'Get', '()', """\
        return sipBuildResult(0, "(ii)", self->GetRow(), self->GetCol());
        """, 
        pyArgsString="() -> (row,col)",
        briefDoc="Return the row and col properties as a tuple.")
    
    # Add sequence protocol methods and other goodies
    c.addPyMethod('__str__', '(self)',             'return str(self.Get())')
    c.addPyMethod('__repr__', '(self)',            'return "GridCellCoords"+str(self.Get())')
    c.addPyMethod('__len__', '(self)',             'return len(self.Get())')
    c.addPyMethod('__nonzero__', '(self)',         'return self.Get() != (0,0)')
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
        tools.wxArrayWrapperTemplate('wxGridCellCoordsArray', 'wxGridCellCoords', module))
    

    #-----------------------------------------------------------------
    c = module.find('wxGridSizesInfo')
    c.find('m_customSizes').ignore()   # TODO: Add support for wxUnsignedToIntHashMap??
        
        
    #-----------------------------------------------------------------
    def fixRendererClass(name):
        klass = module.find(name)
        assert isinstance(klass, etgtools.ClassDef)
        tools.addAutoProperties(klass)
        
        methods = [
            ('Clone',       "virtual wxGridCellRenderer* Clone() const;"),
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
    
    for name in ITEMS:
        if 'Cell' in name and 'Renderer' in name:
            fixRendererClass(name)            
            
    module.addPyCode("PyGridCellRenderer = wx.deprecated(GridCellRenderer, 'Use GridCellRenderer instead.')")
        
        
    #-----------------------------------------------------------------
    def fixEditorClass(name):
        klass = module.find(name)
        assert isinstance(klass, etgtools.ClassDef)
        tools.addAutoProperties(klass)

        methods = [
            ('BeginEdit',  "virtual void BeginEdit(int row, int col, wxGrid* grid);"),
            ('Clone',      "virtual wxGridCellEditor* Clone() const;"),
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
            # method, so we need to translate between the real C++ siganture
            # and the Python signature.
            virtualCatcherCode="""\
                // VirtualCatcherCode for wx.grid.GridCellEditor.EndEdit
                PyObject *result;
                result = sipCallMethod(0, sipMethod, "iiDN", row, col,
                                       const_cast<wxGrid *>(grid),sipType_wxGrid,NULL);
                if (result == Py_None) {
                    sipRes = false;
                } 
                else {
                    sipRes = true;
                    *newval = Py2wxString(result);
                }
                Py_DECREF(result);
                """  if pureVirtual else "",  # only used with the base class
            )
        
        
    c = module.find('wxGridCellEditor')
    c.addPrivateCopyCtor()
    c.find('~wxGridCellEditor').ignore(False)

    c = module.find('wxGridCellChoiceEditor')
    c.find('wxGridCellChoiceEditor').findOverload('count').ignore()
    
    for name in ITEMS:
        if 'Cell' in name and 'Editor' in name:
            fixEditorClass(name)            
    
    module.addPyCode("PyGridCellEditor = wx.deprecated(GridCellEditor, 'Use GridCellEditor instead.')")
    
    #-----------------------------------------------------------------
    c = module.find('wxGridCellAttr')
    c.addPrivateCopyCtor()
    c.find('~wxGridCellAttr').ignore(False)

    c.find('GetAlignment.hAlign').out = True
    c.find('GetAlignment.vAlign').out = True
    c.find('GetNonDefaultAlignment.hAlign').out = True
    c.find('GetNonDefaultAlignment.vAlign').out = True


    
    #----------------------------------------------------------------- 
    # The insanceCode attribute is code that is used to make a default
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


    #-----------------------------------------------------------------
    c = module.find('wxGridTableMessage')
    c.addPrivateCopyCtor()
    

    #-----------------------------------------------------------------
    c = module.find('wxGrid')
    tools.fixWindowClass(c, ignoreProtected=False)
    c.bases = ['wxScrolledWindow']

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
    c.find('SetCellEditor.editor').transfer = True
    c.find('SetCellRenderer.renderer').transfer = True

    # This overload is deprecated, so don't generate code for it.
    c.find('SetCellValue').findOverload('wxString &val').ignore()
    
    c.find('SetDefaultEditor.editor').transfer = True
    c.find('SetDefaultRenderer.renderer').transfer = True
    

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
        

    c.addPyCode("""\
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
        EVT_GRID_RANGE_SELECT = wx.PyEventBinder( wxEVT_GRID_RANGE_SELECT )
        EVT_GRID_CELL_CHANGING = wx.PyEventBinder( wxEVT_GRID_CELL_CHANGING )
        EVT_GRID_CELL_CHANGED = wx.PyEventBinder( wxEVT_GRID_CELL_CHANGED )
        EVT_GRID_SELECT_CELL = wx.PyEventBinder( wxEVT_GRID_SELECT_CELL )
        EVT_GRID_EDITOR_SHOWN = wx.PyEventBinder( wxEVT_GRID_EDITOR_SHOWN )
        EVT_GRID_EDITOR_HIDDEN = wx.PyEventBinder( wxEVT_GRID_EDITOR_HIDDEN )
        EVT_GRID_EDITOR_CREATED = wx.PyEventBinder( wxEVT_GRID_EDITOR_CREATED )
        EVT_GRID_CELL_BEGIN_DRAG = wx.PyEventBinder( wxEVT_GRID_CELL_BEGIN_DRAG )
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
        EVT_GRID_CMD_RANGE_SELECT =        wx.PyEventBinder( wxEVT_GRID_RANGE_SELECT,       1 )
        EVT_GRID_CMD_CELL_CHANGING =       wx.PyEventBinder( wxEVT_GRID_CELL_CHANGING,      1 )
        EVT_GRID_CMD_CELL_CHANGED =        wx.PyEventBinder( wxEVT_GRID_CELL_CHANGED,       1 )
        EVT_GRID_CMD_SELECT_CELL =         wx.PyEventBinder( wxEVT_GRID_SELECT_CELL,        1 )
        EVT_GRID_CMD_EDITOR_SHOWN =        wx.PyEventBinder( wxEVT_GRID_EDITOR_SHOWN,       1 )
        EVT_GRID_CMD_EDITOR_HIDDEN =       wx.PyEventBinder( wxEVT_GRID_EDITOR_HIDDEN,      1 )
        EVT_GRID_CMD_EDITOR_CREATED =      wx.PyEventBinder( wxEVT_GRID_EDITOR_CREATED,     1 )
        EVT_GRID_CMD_CELL_BEGIN_DRAG =     wx.PyEventBinder( wxEVT_GRID_CELL_BEGIN_DRAG,    1 )
        EVT_GRID_CMD_COL_MOVE =            wx.PyEventBinder( wxEVT_GRID_COL_MOVE,           1 )
        EVT_GRID_CMD_COL_SORT =            wx.PyEventBinder( wxEVT_GRID_COL_SORT,           1 )
        EVT_GRID_CMD_TABBING =             wx.PyEventBinder( wxEVT_GRID_TABBING,            1 )
        """)
        
    #-----------------------------------------------------------------    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

