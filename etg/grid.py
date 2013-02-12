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
    c = module.find('wxGridCellAttrProvider')
    c.addPrivateCopyCtor()
    

    #-----------------------------------------------------------------
    c = module.find('wxGrid')
    tools.fixWindowClass(c)
    c.bases = ['wxScrolledWindow']
    
    
    #-----------------------------------------------------------------
    c = module.find('wxGridSizesInfo')
    c.find('m_customSizes').ignore()   # TODO: Add support for wxUnsignedToIntHashMap??


    #-----------------------------------------------------------------
    for name in ['wxGridEvent',
                 'wxGridSizeEvent',
                 'wxGridRangeSelectEvent',
                 'wxGridEditorCreatedEvent',
                 ]:
        c = module.find(name)
        tools.fixEventClass(c)
        
        
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
            
    
    #-----------------------------------------------------------------
    def fixEditorClass(name):
        klass = module.find(name)
        assert isinstance(klass, etgtools.ClassDef)
        tools.addAutoProperties(klass)

        methods = [
            ('BeginEdit',  "virtual void BeginEdit(int row, int col, wxGrid* grid);"),
            ('Clone',      "virtual wxGridCellEditor* Clone() const;"),
            ('Create',     "virtual void Create(wxWindow* parent, wxWindowID id, wxEvtHandler* evtHandler);"),
            ('EndEdit',    "virtual bool EndEdit(int row, int col, const wxGrid* grid, const wxString& oldval, wxString* newval);"),
            ('ApplyEdit',  "virtual void ApplyEdit(int row, int col, wxGrid* grid);"),
            ('Reset',      "virtual void Reset();"),
            ]

    
    c = module.find('wxGridCellEditor')
    c.addPrivateCopyCtor()
    c.find('~wxGridCellEditor').ignore(False)

    c = module.find('wxGridCellChoiceEditor')
    c.find('wxGridCellChoiceEditor').findOverload('count').ignore()
    
    for name in ITEMS:
        if 'Cell' in name and 'Editor' in name:
            fixEditorClass(name)            
    
    
    #-----------------------------------------------------------------
    c = module.find('wxGridCellAttr')
    c.addPrivateCopyCtor()
    c.find('~wxGridCellAttr').ignore(False)

    
    #-----------------------------------------------------------------
    c = module.find('wxGridUpdateLocker')
    c.addPrivateCopyCtor()
        
    
    #-----------------------------------------------------------------
    c = module.find('wxGridTableBase')
    c.addPrivateCopyCtor()
    


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
    #-----------------------------------------------------------------    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

