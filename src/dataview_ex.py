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
        oid = item.GetID()
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
        
class PyDataViewModel(DataViewModelBase, DataViewItemObjectMapper):
    def __init__(self, *a, **kw):
        super(PyDataViewModel, self).__init__(*a, **kw)

    
