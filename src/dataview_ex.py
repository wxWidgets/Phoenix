import wx

class DataViewItemObjectMapper(object):
    """
    This class provides a mechanism for mapping between Python objects and the
    DataViewItem objects used by the DataViewModel for tracking the items in
    the view. The ID used for the item is the id() of the Python object. Use
    `ObjectToItem` to create a DataViewItem using a Python object as its ID,
    and use `ItemToObject` to fetch that Python object again later for a given
    DataViewItem.
    
    By default a regular dictionary is used to implement the ID to object
    mapping. Optionally a WeakValueDictionary can be useful when there will be
    a high turnover of objects and mantaining an extra reference to the
    objects would be unwise.  If weak references are used then the objects
    associated with data items must be weak-referenceable.  (Things like
    stock lists and dictionaries are not.)  See `UseWeakRefs`.
    
    Each `PyDataViewModel` is derived from this class.
    """
    def __init__(self):
        self.mapper = dict()
        self.usingWeakRefs = False
        
    def ObjectToItem(self, obj):
        """
        Create a DataViewItem for the object, and remember the ID-->obj mapping.
        """
        oid = id(obj)
        self.mapper[oid] = obj
        return DataViewItem(oid)

    def ItemToObject(self, item):
        """
        Retrieve the object that was used to create an item.
        """
        oid = int(item.GetID())
        return self.mapper[oid]

    def UseWeakRefs(self, flag):
        """
        Switch to or from using a weak value dictionary for keeping the ID to
        object map.
        """
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
        
class PyDataViewModel(PyDataViewModelBase, DataViewItemObjectMapper):
    def __init__(self):
        PyDataViewModelBase.__init__(self)
        DataViewItemObjectMapper.__init__(self)

NullDataViewItem = DataViewItem()

EVT_DATAVIEW_SELECTION_CHANGED = wx.PyEventBinder(wxEVT_COMMAND_DATAVIEW_SELECTION_CHANGED, 1)

EVT_DATAVIEW_ITEM_ACTIVATED = wx.PyEventBinder(wxEVT_COMMAND_DATAVIEW_ITEM_ACTIVATED, 1)
EVT_DATAVIEW_ITEM_COLLAPSING = wx.PyEventBinder(wxEVT_COMMAND_DATAVIEW_ITEM_COLLAPSING, 1)
EVT_DATAVIEW_ITEM_COLLAPSED = wx.PyEventBinder(wxEVT_COMMAND_DATAVIEW_ITEM_COLLAPSED, 1)
EVT_DATAVIEW_ITEM_EXPANDING = wx.PyEventBinder(wxEVT_COMMAND_DATAVIEW_ITEM_EXPANDING, 1)
EVT_DATAVIEW_ITEM_EXPANDED = wx.PyEventBinder(wxEVT_COMMAND_DATAVIEW_ITEM_EXPANDED, 1)
EVT_DATAVIEW_ITEM_START_EDITING = wx.PyEventBinder(wxEVT_COMMAND_DATAVIEW_ITEM_START_EDITING, 1)
EVT_DATAVIEW_ITEM_EDITING_STARTED = wx.PyEventBinder(wxEVT_COMMAND_DATAVIEW_ITEM_EDITING_STARTED, 1)
EVT_DATAVIEW_ITEM_EDITING_DONE = wx.PyEventBinder(wxEVT_COMMAND_DATAVIEW_ITEM_EDITING_DONE, 1)
EVT_DATAVIEW_ITEM_VALUE_CHANGED = wx.PyEventBinder(wxEVT_COMMAND_DATAVIEW_ITEM_VALUE_CHANGED, 1)

EVT_DATAVIEW_ITEM_CONTEXT_MENU = wx.PyEventBinder(wxEVT_COMMAND_DATAVIEW_ITEM_CONTEXT_MENU, 1)

EVT_DATAVIEW_COLUMN_HEADER_CLICK = wx.PyEventBinder(wxEVT_COMMAND_DATAVIEW_COLUMN_HEADER_CLICK, 1)
EVT_DATAVIEW_COLUMN_HEADER_RIGHT_CLICKED = wx.PyEventBinder(wxEVT_COMMAND_DATAVIEW_COLUMN_HEADER_RIGHT_CLICK, 1)
EVT_DATAVIEW_COLUMN_SORTED = wx.PyEventBinder(wxEVT_COMMAND_DATAVIEW_COLUMN_SORTED, 1)
EVT_DATAVIEW_COLUMN_REORDERED = wx.PyEventBinder(wxEVT_COMMAND_DATAVIEW_COLUMN_REORDERED, 1)
EVT_DATAVIEW_CACHE_HINT = wx.PyEventBinder(wxEVT_COMMAND_DATAVIEW_CACHE_HINT, 1)

EVT_DATAVIEW_ITEM_BEGIN_DRAG = wx.PyEventBinder(wxEVT_COMMAND_DATAVIEW_ITEM_BEGIN_DRAG, 1)
EVT_DATAVIEW_ITEM_DROP_POSSIBLE = wx.PyEventBinder(wxEVT_COMMAND_DATAVIEW_ITEM_DROP_POSSIBLE, 1)
EVT_DATAVIEW_ITEM_DROP = wx.PyEventBinder(wxEVT_COMMAND_DATAVIEW_ITEM_DROP, 1)

