#---------------------------------------------------------------------------
# Name:        etg/listctrl.py
# Author:      Robin Dunn
#
# Created:     23-Mar-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "listctrl"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxItemAttr",  # TODO: technically this should be in its own etg script...
           "wxListItem",
           "wxListCtrl",
           "wxListView",
           "wxListEvent",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    # Compatibility alias
    module.addPyCode("""\
        ListItemAttr = wx.deprecated(ItemAttr, 'Use ItemAttr instead')
        """)

    #-------------------------------------------------------
    c = module.find('wxListItem')
    assert isinstance(c, etgtools.ClassDef)
    c.find('SetData').findOverload('void *').ignore()
    c.find('GetData').type = 'long'

    #-------------------------------------------------------
    c = module.find('wxListCtrl')
    tools.fixWindowClass(c)

    module.addGlobalStr('wxListCtrlNameStr', before=c)

    # Unignore some protected virtual methods that we want to allow to be
    # overridden in derived classes
    for name in [ 'OnGetItemAttr',
                  #'OnGetItemColumnAttr',  # MSW only?
                  'OnGetItemColumnImage',
                  'OnGetItemImage',
                  'OnGetItemText',
                  'OnGetItemIsChecked',
                  ]:
        c.find(name).ignore(False)
        c.find(name).isVirtual = True

    tools.addEnableSystemTheme(c, 'wx.ListCtrl')

    # Tweaks to allow passing and using a Python callable object for the sort
    # compare function. First provide a sort callback function that can call the
    # Python function.
    c.addCppCode("""\
        static int wxCALLBACK wxPyListCtrl_SortItems(wxIntPtr item1, wxIntPtr item2, wxIntPtr funcPtr)
        {
            int retval = 0;
            PyObject* func = (PyObject*)funcPtr;
            wxPyThreadBlocker blocker;

        #if SIZEOF_LONG >= SIZEOF_VOID_P
            PyObject* args = Py_BuildValue("(ll)", item1, item2);
        #else
            PyObject* args = Py_BuildValue("(LL)", item1, item2);
        #endif

            PyObject* result = PyObject_CallObject(func, args);
            Py_DECREF(args);
            if (result) {
                retval = wxPyInt_AsLong(result);
                Py_DECREF(result);
            }
            return retval;
        }
        """)

    # Next, provide an alternate implementation of SortItems that will use that callback.
    sim = c.find('SortItems')
    assert isinstance(sim, etgtools.MethodDef)
    sim.find('fnSortCallBack').type = 'PyObject*'
    sim.find('data').ignore() # we will be using it to pass the python callback function
    sim.argsString = sim.argsString.replace('wxListCtrlCompare', 'PyObject*')
    sim.setCppCode("""\
        if (!PyCallable_Check(fnSortCallBack))
            return false;
        return self->SortItems((wxListCtrlCompare)wxPyListCtrl_SortItems,
                               (wxIntPtr)fnSortCallBack);
    """)

    # SetItemData takes a long, so lets return that type from GetItemData too,
    # instead of a wxUIntPtr.
    c.find('GetItemData').type = 'long'
    c.find('SetItemPtrData').ignore()


    # Change the semantics of GetColumn to return the item as the return
    # value instead of through a parameter.
    # bool GetColumn(int col, wxListItem& item) const;
    c.find('GetColumn').ignore()
    c.addCppMethod('wxListItem*', 'GetColumn', '(int col)',
        doc='Gets information about this column. See SetItem() for more information.',
        factory=True,
        body="""\
        wxListItem item;
        item.SetMask( wxLIST_MASK_STATE |
                      wxLIST_MASK_TEXT  |
                      wxLIST_MASK_IMAGE |
                      wxLIST_MASK_DATA  |
                      wxLIST_SET_ITEM   |
                      wxLIST_MASK_WIDTH |
                      wxLIST_MASK_FORMAT
                      );
        if (self->GetColumn(col, item))
            return new wxListItem(item);
        else
            return NULL;
        """)

    # Do the same for GetItem
    # bool GetItem(wxListItem& info) const;
    c.find('GetItem').ignore()
    c.addCppMethod('wxListItem*', 'GetItem', '(int itemIdx, int col=0)',
        doc='Gets information about the item. See SetItem() for more information.',
        factory=True,
        body="""\
        wxListItem* info = new wxListItem;
        info->m_itemId = itemIdx;
        info->m_col = col;
        info->m_mask = 0xFFFF;
        info->m_stateMask = 0xFFFF;
        self->GetItem(*info);
        return info;
        """)

    # bool GetItemPosition(long item, wxPoint& pos) const;
    c.find('GetItemPosition').ignore()
    c.addCppMethod('wxPoint*', 'GetItemPosition', '(long item)',
        doc='Returns the position of the item, in icon or small icon view.',
        factory=True,
        body="""\
        wxPoint* pos = new wxPoint;
        self->GetItemPosition(item, *pos);
        return pos;
        """)

    # bool GetItemRect(long item, wxRect& rect, int code = wxLIST_RECT_BOUNDS) const;
    c.find('GetItemRect').ignore()
    c.addCppMethod('wxRect*', 'GetItemRect', '(long item, int code = wxLIST_RECT_BOUNDS)',
        doc="""\
        Returns the rectangle representing the item's size and position, in physical coordinates.
        code is one of wx.LIST_RECT_BOUNDS, wx.LIST_RECT_ICON, wx.LIST_RECT_LABEL.""",
        factory=True,
        body="""\
        wxRect* rect = new wxRect;
        self->GetItemRect(item, *rect, code);
        return rect;
        """)


    c.find('EditLabel.textControlClass').ignore()
    c.find('EndEditLabel').ignore()
    c.find('AssignImageList.imageList').transfer = True
    c.find('HitTest.flags').out = True
    c.find('HitTest.ptrSubItem').ignore()

    c.addCppMethod(
        'PyObject*', 'HitTestSubItem', '(const wxPoint& point)',
        pyArgsString="(point) -> (item, flags, subitem)",
        doc="Determines which item (if any) is at the specified point, giving details in flags.",
        body="""\
            long item, subitem;
            int flags;
            item = self->HitTest(*point, flags, &subitem);
            wxPyThreadBlocker blocker;
            PyObject* rv = PyTuple_New(3);
            PyTuple_SetItem(rv, 0, wxPyInt_FromLong(item));
            PyTuple_SetItem(rv, 1, wxPyInt_FromLong(flags));
            PyTuple_SetItem(rv, 2, wxPyInt_FromLong(subitem));
            return rv;
            """)

    c.find('CheckItem.check').default = 'true'


    # Some deprecated aliases for Classic renames
    c.addPyCode('ListCtrl.FindItemData = wx.deprecated(ListCtrl.FindItem, "Use FindItem instead.")')
    c.addPyCode('ListCtrl.FindItemAtPos = wx.deprecated(ListCtrl.FindItem, "Use FindItem instead.")')
    c.addPyCode('ListCtrl.InsertStringItem = wx.deprecated(ListCtrl.InsertItem, "Use InsertItem instead.")')
    c.addPyCode('ListCtrl.InsertImageItem = wx.deprecated(ListCtrl.InsertItem, "Use InsertItem instead.")')
    c.addPyCode('ListCtrl.InsertImageStringItem = wx.deprecated(ListCtrl.InsertItem, "Use InsertItem instead.")')
    c.addPyCode('ListCtrl.SetStringItem = wx.deprecated(ListCtrl.SetItem, "Use SetItem instead.")')


    # Provide a way to determine if column ordering is possible
    c.addCppMethod('bool', 'HasColumnOrderSupport', '()',
        """\
        #ifdef wxHAS_LISTCTRL_COLUMN_ORDER
            return true;
        #else
            return false;
        #endif
        """)

    # And provide implementation of those methods that will work whether or
    # not wx has column ordering support
    c.find('GetColumnOrder').setCppCode("""\
        #ifdef wxHAS_LISTCTRL_COLUMN_ORDER
            return self->GetColumnOrder(col);
        #else
            wxPyRaiseNotImplemented();
            return 0;
        #endif
        """)

    c.find('GetColumnIndexFromOrder').setCppCode("""\
        #ifdef wxHAS_LISTCTRL_COLUMN_ORDER
            return self->GetColumnIndexFromOrder(pos);
        #else
            wxPyRaiseNotImplemented();
            return 0;
        #endif
        """)

    c.find('GetColumnsOrder').type = 'wxArrayInt*'
    c.find('GetColumnsOrder').factory=True
    c.find('GetColumnsOrder').setCppCode("""\
        #ifdef wxHAS_LISTCTRL_COLUMN_ORDER
            return new wxArrayInt(self->GetColumnsOrder());
        #else
            wxPyRaiseNotImplemented();
            return new wxArrayInt();
        #endif
        """)

    c.find('SetColumnsOrder').setCppCode("""\
        #ifdef wxHAS_LISTCTRL_COLUMN_ORDER
            return self->SetColumnsOrder(*orders);
        #else
            wxPyRaiseNotImplemented();
            return false;
        #endif
        """)


    # Add some Python helper methods
    c.addPyMethod('Select', '(self, idx, on=1)',
        doc='Selects/deselects an item.',
        body="""\
        if on: state = wx.LIST_STATE_SELECTED
        else: state = 0
        self.SetItemState(idx, state, wx.LIST_STATE_SELECTED)
        """)

    c.addPyMethod('Focus', '(self, idx)',
        doc='Focus and show the given item.',
        body="""\
        self.SetItemState(idx, wx.LIST_STATE_FOCUSED, wx.LIST_STATE_FOCUSED)
        self.EnsureVisible(idx)
        """)

    c.addPyMethod('GetFocusedItem', '(self)',
        doc='Gets the currently focused item or -1 if none is focused.',
        body='return self.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_FOCUSED)')

    c.addPyMethod('GetFirstSelected', '(self, *args)',
        doc='Returns the first selected item, or -1 when none is selected.',
        body="return self.GetNextSelected(-1)")

    c.addPyMethod('GetNextSelected', '(self, item)',
        doc='Returns subsequent selected items, or -1 when no more are selected.',
        body="return self.GetNextItem(item, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)")

    c.addPyMethod('IsSelected', '(self, idx)',
        doc='Returns ``True`` if the item is selected.',
        body="return (self.GetItemState(idx, wx.LIST_STATE_SELECTED) & wx.LIST_STATE_SELECTED) != 0")

    c.addPyMethod('SetColumnImage', '(self, col, image)',
        body="""\
        item = self.GetColumn(col)
        # preserve all other attributes too
        item.SetMask( wx.LIST_MASK_STATE |
                      wx.LIST_MASK_TEXT  |
                      wx.LIST_MASK_IMAGE |
                      wx.LIST_MASK_DATA  |
                      wx.LIST_SET_ITEM   |
                      wx.LIST_MASK_WIDTH |
                      wx.LIST_MASK_FORMAT )
        item.SetImage(image)
        self.SetColumn(col, item)
        """)

    c.addPyMethod('ClearColumnImage', '(self, col)',
        body="self.SetColumnImage(col, -1)")

    c.addPyMethod('Append', '(self, entry)',
        doc='''\
        Append an item to the list control.  The `entry` parameter should be a
        sequence with an item for each column''',
        body="""\
        if len(entry):
            from six import text_type
            pos = self.InsertItem(self.GetItemCount(), text_type(entry[0]))
            for i in range(1, len(entry)):
                self.SetItem(pos, i, text_type(entry[i]))
            return pos
        """)


    c.addCppMethod('wxWindow*', 'GetMainWindow', '()',
        body="""\
        #if defined(__WXMSW__) || defined(__WXMAC__)
            return self;
        #else
            return (wxWindow*)self->m_mainWin;
        #endif
        """)

    # Documented wrongly in 3.1.6
    c.find('RemoveSortIndicator').type = 'void'
    c.find('RemoveSortIndicator').isConst = False


    #-------------------------------------------------------
    c = module.find('wxListView')
    tools.fixWindowClass(c)

    #-------------------------------------------------------
    c = module.find('wxListEvent')
    tools.fixEventClass(c)

    module.addPyCode("""\
        EVT_LIST_BEGIN_DRAG        = PyEventBinder(wxEVT_LIST_BEGIN_DRAG       , 1)
        EVT_LIST_BEGIN_RDRAG       = PyEventBinder(wxEVT_LIST_BEGIN_RDRAG      , 1)
        EVT_LIST_BEGIN_LABEL_EDIT  = PyEventBinder(wxEVT_LIST_BEGIN_LABEL_EDIT , 1)
        EVT_LIST_END_LABEL_EDIT    = PyEventBinder(wxEVT_LIST_END_LABEL_EDIT   , 1)
        EVT_LIST_DELETE_ITEM       = PyEventBinder(wxEVT_LIST_DELETE_ITEM      , 1)
        EVT_LIST_DELETE_ALL_ITEMS  = PyEventBinder(wxEVT_LIST_DELETE_ALL_ITEMS , 1)
        EVT_LIST_ITEM_SELECTED     = PyEventBinder(wxEVT_LIST_ITEM_SELECTED    , 1)
        EVT_LIST_ITEM_DESELECTED   = PyEventBinder(wxEVT_LIST_ITEM_DESELECTED  , 1)
        EVT_LIST_KEY_DOWN          = PyEventBinder(wxEVT_LIST_KEY_DOWN         , 1)
        EVT_LIST_INSERT_ITEM       = PyEventBinder(wxEVT_LIST_INSERT_ITEM      , 1)
        EVT_LIST_COL_CLICK         = PyEventBinder(wxEVT_LIST_COL_CLICK        , 1)
        EVT_LIST_ITEM_RIGHT_CLICK  = PyEventBinder(wxEVT_LIST_ITEM_RIGHT_CLICK , 1)
        EVT_LIST_ITEM_MIDDLE_CLICK = PyEventBinder(wxEVT_LIST_ITEM_MIDDLE_CLICK, 1)
        EVT_LIST_ITEM_ACTIVATED    = PyEventBinder(wxEVT_LIST_ITEM_ACTIVATED   , 1)
        EVT_LIST_CACHE_HINT        = PyEventBinder(wxEVT_LIST_CACHE_HINT       , 1)
        EVT_LIST_COL_RIGHT_CLICK   = PyEventBinder(wxEVT_LIST_COL_RIGHT_CLICK  , 1)
        EVT_LIST_COL_BEGIN_DRAG    = PyEventBinder(wxEVT_LIST_COL_BEGIN_DRAG   , 1)
        EVT_LIST_COL_DRAGGING      = PyEventBinder(wxEVT_LIST_COL_DRAGGING     , 1)
        EVT_LIST_COL_END_DRAG      = PyEventBinder(wxEVT_LIST_COL_END_DRAG     , 1)
        EVT_LIST_ITEM_FOCUSED      = PyEventBinder(wxEVT_LIST_ITEM_FOCUSED     , 1)
        EVT_LIST_ITEM_CHECKED      = PyEventBinder(wxEVT_LIST_ITEM_CHECKED     , 1)
        EVT_LIST_ITEM_UNCHECKED    = PyEventBinder(wxEVT_LIST_ITEM_UNCHECKED   , 1)

        # deprecated wxEVT aliases
        wxEVT_COMMAND_LIST_BEGIN_DRAG         = wxEVT_LIST_BEGIN_DRAG
        wxEVT_COMMAND_LIST_BEGIN_RDRAG        = wxEVT_LIST_BEGIN_RDRAG
        wxEVT_COMMAND_LIST_BEGIN_LABEL_EDIT   = wxEVT_LIST_BEGIN_LABEL_EDIT
        wxEVT_COMMAND_LIST_END_LABEL_EDIT     = wxEVT_LIST_END_LABEL_EDIT
        wxEVT_COMMAND_LIST_DELETE_ITEM        = wxEVT_LIST_DELETE_ITEM
        wxEVT_COMMAND_LIST_DELETE_ALL_ITEMS   = wxEVT_LIST_DELETE_ALL_ITEMS
        wxEVT_COMMAND_LIST_ITEM_SELECTED      = wxEVT_LIST_ITEM_SELECTED
        wxEVT_COMMAND_LIST_ITEM_DESELECTED    = wxEVT_LIST_ITEM_DESELECTED
        wxEVT_COMMAND_LIST_KEY_DOWN           = wxEVT_LIST_KEY_DOWN
        wxEVT_COMMAND_LIST_INSERT_ITEM        = wxEVT_LIST_INSERT_ITEM
        wxEVT_COMMAND_LIST_COL_CLICK          = wxEVT_LIST_COL_CLICK
        wxEVT_COMMAND_LIST_ITEM_RIGHT_CLICK   = wxEVT_LIST_ITEM_RIGHT_CLICK
        wxEVT_COMMAND_LIST_ITEM_MIDDLE_CLICK  = wxEVT_LIST_ITEM_MIDDLE_CLICK
        wxEVT_COMMAND_LIST_ITEM_ACTIVATED     = wxEVT_LIST_ITEM_ACTIVATED
        wxEVT_COMMAND_LIST_CACHE_HINT         = wxEVT_LIST_CACHE_HINT
        wxEVT_COMMAND_LIST_COL_RIGHT_CLICK    = wxEVT_LIST_COL_RIGHT_CLICK
        wxEVT_COMMAND_LIST_COL_BEGIN_DRAG     = wxEVT_LIST_COL_BEGIN_DRAG
        wxEVT_COMMAND_LIST_COL_DRAGGING       = wxEVT_LIST_COL_DRAGGING
        wxEVT_COMMAND_LIST_COL_END_DRAG       = wxEVT_LIST_COL_END_DRAG
        wxEVT_COMMAND_LIST_ITEM_FOCUSED       = wxEVT_LIST_ITEM_FOCUSED
        """)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()
