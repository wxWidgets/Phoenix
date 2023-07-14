#---------------------------------------------------------------------------
# Name:        etg/dataview.py
# Author:      Kevin Ollivier
#              Robin Dunn
#
# Created:     10-Sept-2011
# Copyright:   (c) 2011 by Kevin Ollivier
# Copyright:   (c) 2011-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools
from etgtools import PyFunctionDef, ParamDef

PACKAGE   = "wx"
MODULE    = "_dataview"
NAME      = "dataview"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [
            'wxDataViewItem',
            'wxDataViewItemAttr',
            'wxDataViewIconText',
            'wxDataViewCheckIconText',
            'wxDataViewModelNotifier',

            'wxDataViewModel',
            'wxDataViewListModel',
            'wxDataViewIndexListModel',
            'wxDataViewVirtualListModel',

            'wxDataViewRenderer',
            'wxDataViewCustomRenderer',
            'wxDataViewTextRenderer',
            'wxDataViewIconTextRenderer',
            'wxDataViewCheckIconTextRenderer',
            'wxDataViewProgressRenderer',
            'wxDataViewSpinRenderer',
            'wxDataViewToggleRenderer',
            'wxDataViewChoiceRenderer',
            #'wxDataViewChoiceByIndexRenderer',  # only available in generic dvc
            'wxDataViewDateRenderer',
            'wxDataViewBitmapRenderer',

            'wxDataViewColumn',
            'wxDataViewCtrl',
            'wxDataViewEvent',
            'wxDataViewValueAdjuster',

            'wxDataViewListCtrl',
            'wxDataViewListStore',

            'wxDataViewTreeCtrl',
            'wxDataViewTreeStore',
         ]


#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.


    module.addHeaderCode("#include <wx/dataview.h>")

    for item in module.allItems():
        if hasattr(item, 'type') and 'wxVariant' in item.type:
            item.type = item.type.replace('wxVariant', 'wxDVCVariant')


    #-----------------------------------------------------------------
    c = module.find('wxDataViewItem')
    assert isinstance(c, etgtools.ClassDef)

    c.addCppMethod('int', '__nonzero__', '()', "return self->IsOk();")
    c.addCppMethod('int', '__bool__', '()', "return self->IsOk();")
    c.addCppMethod('long', '__hash__', '()', "return (long)(intptr_t)self->GetID();")

    c.addCppMethod('bool', '__eq__', '(wxDataViewItem* other)',
                   "return other ? (self->GetID() == other->GetID()) : false;")
    c.addCppMethod('bool', '__ne__', '(wxDataViewItem* other)',
                   "return other ? (self->GetID() != other->GetID()) : true;")
    c.addAutoProperties()


    module.addItem(
        tools.wxArrayWrapperTemplate('wxDataViewItemArray', 'wxDataViewItem', module))
    module.addPyCode("NullDataViewItem = DataViewItem()")


    #-----------------------------------------------------------------
    c = module.find('wxDataViewModel')
    c.addAutoProperties()
    tools.fixRefCountedClass(c)

    c.find('~wxDataViewModel').ignore(False)

    c.find('AddNotifier.notifier').transfer = True
    c.find('RemoveNotifier.notifier').transferBack = True

    # Change the GetValue method to return the value instead of passing it
    # through a parameter for modification.
    c.find('GetValue.variant').out = True
    c.find('GetValue').cppSignature = 'void (wxVariant& variant, const wxDataViewItem& item, unsigned int col)'

    # The DataViewItemObjectMapper class helps map from data items to Python
    # objects, and is used as a base class of PyDataViewModel as a
    # convenience.
    module.addPyClass('DataViewItemObjectMapper', ['object'],
        doc="""\
            This class provides a mechanism for mapping between Python objects and the
            :class:`DataViewItem` objects used by the :class:`DataViewModel` for tracking the items in
            the view. The ID used for the item is the id() of the Python object. Use
            :meth:`ObjectToItem` to create a :class:`DataViewItem` using a Python object as its ID,
            and use :meth:`ItemToObject` to fetch that Python object again later for a given
            :class:`DataViewItem`.

            By default a regular dictionary is used to implement the ID to object
            mapping. Optionally a WeakValueDictionary can be useful when there will be
            a high turnover of objects and maintaining an extra reference to the
            objects would be unwise.  If weak references are used then the objects
            associated with data items must be weak-referenceable.  (Things like
            stock lists and dictionaries are not.)  See :meth:`UseWeakRefs`.

            This class is used in :class:`PyDataViewModel` as a mixin for convenience.
            """,
        items=[
            PyFunctionDef('__init__', '(self)',
                body="""\
                    self.mapper = dict()
                    self.usingWeakRefs = False
                    """),

            PyFunctionDef('ObjectToItem', '(self, obj)',
                doc="Create a :class:`DataViewItem` for the object, and remember the ID-->obj mapping.",
                body="""\
                    import sys
                    oid = id(obj)
                    while oid > sys.maxsize:
                        # risk of conflict here... May need some more thought.
                        oid -= sys.maxsize
                    self.mapper[oid] = obj
                    return DataViewItem(oid)
                    """),

            PyFunctionDef('ItemToObject', '(self, item)',
                doc="Retrieve the object that was used to create an item.",
                body="""\
                    oid = int(item.GetID())
                    return self.mapper[oid]
                    """),

            PyFunctionDef('UseWeakRefs', '(self, flag)',
                doc="""\
                    Switch to or from using a weak value dictionary for keeping the ID to
                    object map.""",
                body="""\
                    if flag == self.usingWeakRefs:
                        return
                    if flag:
                        import weakref
                        newmap = weakref.WeakValueDictionary()
                    else:
                        newmap = dict()
                    newmap.update(self.mapper)
                    self.mapper = newmap
                    self.usingWeakRefs = flag
                    """),
            ])

    module.addPyClass('PyDataViewModel', ['DataViewModel', 'DataViewItemObjectMapper'],
        doc="A convenience class that is a :class:`DataViewModel` combined with an object mapper.",
        items=[
            PyFunctionDef('__init__', '(self)',
                body="""\
                    DataViewModel.__init__(self)
                    DataViewItemObjectMapper.__init__(self)
                    """)
            ])


    #-----------------------------------------------------------------
    c = module.find('wxDataViewListModel')
    c.addAutoProperties()
    tools.fixRefCountedClass(c)

    # Change the GetValueByRow method to return the value instead of passing
    # it through a parameter for modification.
    c.find('GetValueByRow.variant').out = True
    c.find('GetValueByRow').cppSignature = 'void (wxVariant& variant, unsigned int row, unsigned int col)'

    # declare implementations for base class virtuals
    c.addItem(etgtools.WigCode("""\
        virtual wxDataViewItem GetParent( const wxDataViewItem &item ) const;
        virtual bool IsContainer( const wxDataViewItem &item ) const;
        virtual void GetValue( wxDVCVariant &variant /Out/, const wxDataViewItem &item, unsigned int col ) const [void ( wxDVCVariant &variant, const wxDataViewItem &item, unsigned int col )];
        virtual bool SetValue( const wxDVCVariant &variant, const wxDataViewItem &item, unsigned int col );
        virtual bool GetAttr(const wxDataViewItem &item, unsigned int col, wxDataViewItemAttr &attr) const;
        virtual bool IsEnabled(const wxDataViewItem &item, unsigned int col) const;
        virtual bool IsListModel() const;
        """))


    # Add some of the pure virtuals since there are undocumented
    # implementations of them in these classes. The others will need to be
    # implemented in Python classes derived from these.
    for name in ['wxDataViewIndexListModel', 'wxDataViewVirtualListModel']:
        c = module.find(name)

        c.addItem(etgtools.WigCode("""\
            virtual unsigned int GetRow(const wxDataViewItem& item) const;
            virtual unsigned int GetCount() const;
            virtual unsigned int GetChildren( const wxDataViewItem &item, wxDataViewItemArray &children ) const;
            """))


    # compatibility aliases
    module.addPyCode("""\
        PyDataViewIndexListModel = wx.deprecated(DataViewIndexListModel)
        PyDataViewVirtualListModel = wx.deprecated(DataViewVirtualListModel)
        """)


    #-----------------------------------------------------------------

    def _fixupBoolGetters(method, sig):
        method.type = 'void'
        method.find('value').out = True
        method.find('value').type = 'wxDVCVariant&'
        method.cppSignature = sig

    def _fixupTypeParam(klass):
        param = klass.findItem('{}.varianttype'.format(klass.name))
        if param and param.default == 'GetDefaultType()':
            param.default = '{}::GetDefaultType()'.format(klass.name)

    c = module.find('wxDataViewRenderer')
    c.addPrivateCopyCtor()
    c.abstract = True
    c.find('GetView').ignore(False)

    # TODO: This is only available when wxUSE_ACCESSIBILITY is set to 1
    c.find('GetAccessibleDescription').ignore()

    c.addAutoProperties()

    # Change variant getters to return the value
    for name, sig in [
        ('GetValue',               'bool (wxVariant& value)'),
        ('GetValueFromEditorCtrl', 'bool (wxWindow * editor, wxVariant& value)'),
        ]:
        _fixupBoolGetters(c.find(name), sig)

    m = c.find('SetValue')
    m.find('value').type = 'const wxDVCVariant&'
    m.cppSignature = 'bool (const wxVariant& value)'

    m = c.find('CreateEditorCtrl')
    m.cppSignature = 'wxWindow* (wxWindow * parent, wxRect labelRect, const wxVariant& value)'

    c.find('GetView').ignore(False)



    c = module.find('wxDataViewCustomRenderer')
    _fixupTypeParam(c)
    m = c.find('GetValueFromEditorCtrl')
    _fixupBoolGetters(m, 'bool (wxWindow * editor, wxVariant& value)')

    # Change the virtual method handler code to follow the same pattern as the
    # tweaked public API, namely that the value is the return value instead of
    # an out parameter.
    m.virtualCatcherCode = """\
        PyObject *sipResObj = sipCallMethod(&sipIsErr, sipMethod, "D", editor, sipType_wxWindow, NULL);
        if (sipResObj == NULL) {
            if (PyErr_Occurred())
                PyErr_Print();
            sipRes = false;
        }
        else if (sipResObj == Py_None) {
            sipRes = false;
        } else {
            sipRes = true;
            sipParseResult(&sipIsErr, sipMethod, sipResObj, "H5", sipType_wxDVCVariant, &value);
        }
        """

    c.find('GetTextExtent').ignore(False)

    m = c.find('CreateEditorCtrl')
    m.cppSignature = 'wxWindow* (wxWindow * parent, wxRect labelRect, const wxVariant& value)'


    module.addPyCode("""\
        PyDataViewCustomRenderer = wx.deprecated(DataViewCustomRenderer,
                                                 "Use DataViewCustomRenderer instead")""")


    # Add the pure virtuals since there are undocumented implementations of
    # them in all these classes
    for name in [ 'wxDataViewTextRenderer',
                  'wxDataViewIconTextRenderer',
                  'wxDataViewCheckIconTextRenderer',
                  'wxDataViewProgressRenderer',
                  'wxDataViewSpinRenderer',
                  'wxDataViewToggleRenderer',
                  'wxDataViewChoiceRenderer',
                  #'wxDataViewChoiceByIndexRenderer',
                  'wxDataViewDateRenderer',
                  'wxDataViewBitmapRenderer',
                  ]:
        c = module.find(name)
        c.addAutoProperties()
        _fixupTypeParam(c)

        c.addItem(etgtools.WigCode("""\
            virtual bool SetValue( const wxDVCVariant &value ) [bool (const wxVariant& value)];
            virtual void GetValue( wxDVCVariant &value /Out/ ) const [bool (wxVariant& value)];
            %Property(name=Value, get=GetValue, set=SetValue)
            """, protection='public'))

    # The SpinRenderer has a few additional pure virtuals that need to be declared
    # since it derives from DataViewCustomRenderer
    c = module.find('wxDataViewSpinRenderer')
    c.addItem(etgtools.WigCode("""\
        virtual wxSize GetSize() const;
        virtual bool Render(wxRect cell, wxDC* dc, int state);
        """, protection='public'))


    #-----------------------------------------------------------------
    c = module.find('wxDataViewColumn')
    for m in c.find('wxDataViewColumn').all():
        m.find('renderer').transfer = True

    # declare the virtuals from wxSettableHeaderColumn
    c.addItem(etgtools.WigCode("""\
        virtual void SetTitle(const wxString& title);
        virtual wxString GetTitle() const;
        virtual void SetBitmap(const wxBitmapBundle& bitmap);
        virtual wxBitmap GetBitmap() const;
        virtual void SetWidth(int width);
        virtual int GetWidth() const;
        virtual void SetMinWidth(int minWidth);
        virtual int GetMinWidth() const;
        virtual void SetAlignment(wxAlignment align);
        virtual wxAlignment GetAlignment() const;
        virtual void SetFlags(int flags);
        virtual int GetFlags() const;
        virtual bool IsSortKey() const;
        virtual void SetSortOrder(bool ascending);
        virtual bool IsSortOrderAscending() const;

        virtual void SetResizeable(bool resizable);
        virtual void SetSortable(bool sortable);
        virtual void SetReorderable(bool reorderable);
        virtual void SetHidden(bool hidden);
        """))

    c.addAutoProperties()
    c.addProperty('Title', 'GetTitle', 'SetTitle')
    c.addProperty('Bitmap', 'GetBitmap', 'SetBitmap')
    c.addProperty('Width', 'GetWidth', 'SetWidth')
    c.addProperty('MinWidth', 'GetMinWidth', 'SetMinWidth')
    c.addProperty('Alignment', 'GetAlignment', 'SetAlignment')
    c.addProperty('Flags', 'GetFlags', 'SetFlags')
    c.addProperty('SortOrder', 'IsSortOrderAscending', 'SetSortOrder')



    #-----------------------------------------------------------------
    c = module.find('wxDataViewCtrl')
    tools.fixWindowClass(c)
    module.addGlobalStr('wxDataViewCtrlNameStr', c)

    tools.addEnableSystemTheme(c, 'wx.dataview.DataViewCtrl')

    c.find('AssociateModel.model').transfer = True
    c.find('AssociateModel').pyName = '_AssociateModel'
    c.addPyMethod('AssociateModel', '(self, model)',
        doc="""\
            Associates a :class:`DataViewModel` with the control.
            Ownership of the model object is passed to C++, however it
            is reference counted so it can be shared with other views.
            """,
        body="""\
            import wx.siplib
            wasPyOwned = wx.siplib.ispyowned(model)
            self._AssociateModel(model)
            # Ownership of the python object has just been transferred to
            # C++, so DecRef the C++ instance associated with this python
            # reference.
            if wasPyOwned:
                model.DecRef()
            """)

    c.find('PrependColumn.col').transfer = True
    c.find('InsertColumn.col').transfer = True
    c.find('AppendColumn.col').transfer = True

    c.addPyMethod('GetColumns', '(self)',
        doc="Returns a list of column objects.",
        body="return [self.GetColumn(i) for i in range(self.GetColumnCount())]")

    c.find('GetSelections').ignore()
    c.addCppMethod('wxDataViewItemArray*', 'GetSelections', '()',
        isConst=True, factory=True,
        doc="Returns a list of the currently selected items.",
        body="""\
            wxDataViewItemArray* selections = new wxDataViewItemArray;
            self->GetSelections(*selections);
            return selections;
            """)

    # Pythonize HitTest
    c.find('HitTest').ignore()
    c.addCppMethod('PyObject*', 'HitTest', '(const wxPoint& point)',
        isConst=True,
        doc="""\
            HitTest(point) -> (item, col)\n
            Returns the item and column located at point, as a 2 element tuple.
            """,
        body="""\
            wxDataViewItem*   item = new wxDataViewItem();;
            wxDataViewColumn* col = NULL;

            self->HitTest(*point, *item, col);

            wxPyThreadBlocker blocker;
            PyObject* value = PyTuple_New(2);
            PyObject* item_obj =
                wxPyConstructObject((void*)item, wxT("wxDataViewItem"), 1);   // owned
            PyObject* col_obj;
            if (col) {
                col_obj = wxPyConstructObject((void*)col, wxT("wxDataViewColumn"), 0);  // not owned
            } else {
                col_obj = Py_None;
                Py_INCREF(Py_None);
            }
            PyTuple_SET_ITEM(value, 0, item_obj);
            PyTuple_SET_ITEM(value, 1, col_obj);
            // PyTuple steals a reference, so we don't need to decref the items here
            return value;
            """)


    # TODO: add support for wxVector templates
    c.find('GetSortingColumns').ignore()


    #-----------------------------------------------------------------
    c = module.find('wxDataViewEvent')
    tools.fixEventClass(c)

    c.find('SetCache.from').name = 'from_'
    c.find('SetCache.to').name = 'to_'

    c.find('GetDataBuffer').ignore()
    c.addCppMethod('PyObject*', 'GetDataBuffer', '()', isConst=True,
        doc="Gets the data buffer for a drop data transfer",
        body="""\
            wxPyThreadBlocker blocker;
            return wxPyMakeBuffer(self->GetDataBuffer(), self->GetDataSize(), true);
            """)

    # TODO: SetDataBuffer

    c.find('SetDataObject.obj').transfer = True


    module.addPyCode("""\
        EVT_DATAVIEW_SELECTION_CHANGED         = wx.PyEventBinder( wxEVT_DATAVIEW_SELECTION_CHANGED, 1)
        EVT_DATAVIEW_ITEM_ACTIVATED            = wx.PyEventBinder( wxEVT_DATAVIEW_ITEM_ACTIVATED, 1)
        EVT_DATAVIEW_ITEM_COLLAPSED            = wx.PyEventBinder( wxEVT_DATAVIEW_ITEM_COLLAPSED, 1)
        EVT_DATAVIEW_ITEM_EXPANDED             = wx.PyEventBinder( wxEVT_DATAVIEW_ITEM_EXPANDED, 1)
        EVT_DATAVIEW_ITEM_COLLAPSING           = wx.PyEventBinder( wxEVT_DATAVIEW_ITEM_COLLAPSING, 1)
        EVT_DATAVIEW_ITEM_EXPANDING            = wx.PyEventBinder( wxEVT_DATAVIEW_ITEM_EXPANDING, 1)
        EVT_DATAVIEW_ITEM_START_EDITING        = wx.PyEventBinder( wxEVT_DATAVIEW_ITEM_START_EDITING, 1)
        EVT_DATAVIEW_ITEM_EDITING_STARTED      = wx.PyEventBinder( wxEVT_DATAVIEW_ITEM_EDITING_STARTED, 1)
        EVT_DATAVIEW_ITEM_EDITING_DONE         = wx.PyEventBinder( wxEVT_DATAVIEW_ITEM_EDITING_DONE, 1)
        EVT_DATAVIEW_ITEM_VALUE_CHANGED        = wx.PyEventBinder( wxEVT_DATAVIEW_ITEM_VALUE_CHANGED, 1)
        EVT_DATAVIEW_ITEM_CONTEXT_MENU         = wx.PyEventBinder( wxEVT_DATAVIEW_ITEM_CONTEXT_MENU, 1)
        EVT_DATAVIEW_COLUMN_HEADER_CLICK       = wx.PyEventBinder( wxEVT_DATAVIEW_COLUMN_HEADER_CLICK, 1)
        EVT_DATAVIEW_COLUMN_HEADER_RIGHT_CLICK = wx.PyEventBinder( wxEVT_DATAVIEW_COLUMN_HEADER_RIGHT_CLICK, 1)
        EVT_DATAVIEW_COLUMN_SORTED             = wx.PyEventBinder( wxEVT_DATAVIEW_COLUMN_SORTED, 1)
        EVT_DATAVIEW_COLUMN_REORDERED          = wx.PyEventBinder( wxEVT_DATAVIEW_COLUMN_REORDERED, 1)
        EVT_DATAVIEW_ITEM_BEGIN_DRAG           = wx.PyEventBinder( wxEVT_DATAVIEW_ITEM_BEGIN_DRAG, 1)
        EVT_DATAVIEW_ITEM_DROP_POSSIBLE        = wx.PyEventBinder( wxEVT_DATAVIEW_ITEM_DROP_POSSIBLE, 1)
        EVT_DATAVIEW_ITEM_DROP                 = wx.PyEventBinder( wxEVT_DATAVIEW_ITEM_DROP, 1)
        EVT_DATAVIEW_CACHE_HINT                = wx.PyEventBinder( wxEVT_DATAVIEW_CACHE_HINT, 1 )

        # deprecated wxEVT aliases
        wxEVT_COMMAND_DATAVIEW_SELECTION_CHANGED          = wxEVT_DATAVIEW_SELECTION_CHANGED
        wxEVT_COMMAND_DATAVIEW_ITEM_ACTIVATED             = wxEVT_DATAVIEW_ITEM_ACTIVATED
        wxEVT_COMMAND_DATAVIEW_ITEM_COLLAPSED             = wxEVT_DATAVIEW_ITEM_COLLAPSED
        wxEVT_COMMAND_DATAVIEW_ITEM_EXPANDED              = wxEVT_DATAVIEW_ITEM_EXPANDED
        wxEVT_COMMAND_DATAVIEW_ITEM_COLLAPSING            = wxEVT_DATAVIEW_ITEM_COLLAPSING
        wxEVT_COMMAND_DATAVIEW_ITEM_EXPANDING             = wxEVT_DATAVIEW_ITEM_EXPANDING
        wxEVT_COMMAND_DATAVIEW_ITEM_START_EDITING         = wxEVT_DATAVIEW_ITEM_START_EDITING
        wxEVT_COMMAND_DATAVIEW_ITEM_EDITING_STARTED       = wxEVT_DATAVIEW_ITEM_EDITING_STARTED
        wxEVT_COMMAND_DATAVIEW_ITEM_EDITING_DONE          = wxEVT_DATAVIEW_ITEM_EDITING_DONE
        wxEVT_COMMAND_DATAVIEW_ITEM_VALUE_CHANGED         = wxEVT_DATAVIEW_ITEM_VALUE_CHANGED
        wxEVT_COMMAND_DATAVIEW_ITEM_CONTEXT_MENU          = wxEVT_DATAVIEW_ITEM_CONTEXT_MENU
        wxEVT_COMMAND_DATAVIEW_COLUMN_HEADER_CLICK        = wxEVT_DATAVIEW_COLUMN_HEADER_CLICK
        wxEVT_COMMAND_DATAVIEW_COLUMN_HEADER_RIGHT_CLICK  = wxEVT_DATAVIEW_COLUMN_HEADER_RIGHT_CLICK
        wxEVT_COMMAND_DATAVIEW_COLUMN_SORTED              = wxEVT_DATAVIEW_COLUMN_SORTED
        wxEVT_COMMAND_DATAVIEW_COLUMN_REORDERED           = wxEVT_DATAVIEW_COLUMN_REORDERED
        wxEVT_COMMAND_DATAVIEW_CACHE_HINT                 = wxEVT_DATAVIEW_CACHE_HINT
        wxEVT_COMMAND_DATAVIEW_ITEM_BEGIN_DRAG            = wxEVT_DATAVIEW_ITEM_BEGIN_DRAG
        wxEVT_COMMAND_DATAVIEW_ITEM_DROP_POSSIBLE         = wxEVT_DATAVIEW_ITEM_DROP_POSSIBLE
        wxEVT_COMMAND_DATAVIEW_ITEM_DROP                  = wxEVT_DATAVIEW_ITEM_DROP
        """)

    #-----------------------------------------------------------------
    c = module.find('wxDataViewListCtrl')
    tools.fixWindowClass(c)

    c.find('GetStore').overloads = []

    c.find('AppendItem.values').type = 'const wxVariantVector&'
    c.find('PrependItem.values').type = 'const wxVariantVector&'
    c.find('InsertItem.values').type = 'const wxVariantVector&'

    c.find('GetValue.value').out = True

    for name in 'AppendColumn InsertColumn PrependColumn'.split():
        for m in c.find(name).all():
            m.find('column').transfer = True


    c = module.find('wxDataViewListStore')
    c.find('AppendItem.values').type = 'const wxVariantVector&'
    c.find('PrependItem.values').type = 'const wxVariantVector&'
    c.find('InsertItem.values').type = 'const wxVariantVector&'
    c.find('GetValueByRow.value').out = True
    c.find('GetValueByRow').cppSignature = 'void (wxVariant& value, unsigned int row, unsigned int col)'

    c.addAutoProperties()


    #-----------------------------------------------------------------
    def _setClientDataTrasfer(klass):
        for item in klass.allItems():
            if isinstance(item, ParamDef) and item.type == 'wxClientData *':
                item.transfer = True

    c = module.find('wxDataViewTreeCtrl')
    tools.fixWindowClass(c)
    _setClientDataTrasfer(c)
    c.find('GetStore').overloads = []

    c = module.find('wxDataViewTreeStore')
    c.addAutoProperties()
    tools.fixRefCountedClass(c)
    _setClientDataTrasfer(c)


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

