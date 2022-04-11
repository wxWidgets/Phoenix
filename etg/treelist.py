#---------------------------------------------------------------------------
# Name:        etg/treelist.py
# Author:      Robin Dunn
#
# Created:     06-Jun-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_dataview"
NAME      = "treelist"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxTreeListItem",
           "wxTreeListItemComparator",
           "wxTreeListCtrl",
           "wxTreeListEvent",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode('#include <wx/treelist.h>')
    module.find('wxTreeListEventHandler').ignore()
    module.find('wxTreeListItems').ignore()


    #-----------------------------------------------------------------
    c = module.find('wxTreeListItem')
    assert isinstance(c, etgtools.ClassDef)

    c.addCppMethod('int', '__nonzero__', '()', "return self->IsOk();")
    c.addCppMethod('int', '__bool__', '()', "return self->IsOk();")

    c.addCppMethod('long', '__hash__', '()', """\
        return (long)(intptr_t)self->GetID();
        """)

    c.addCppMethod('bool', '__eq__', '(wxTreeListItem* other)',
                   "return other ? (self->GetID() == other->GetID()) : false;")
    c.addCppMethod('bool', '__ne__', '(wxTreeListItem* other)',
                   "return other ? (self->GetID() != other->GetID()) : true;")

    #-----------------------------------------------------------------
    c = module.find('wxTreeListItemComparator')
    c.addPrivateCopyCtor()


    #-----------------------------------------------------------------
    c = module.find('wxTreeListCtrl')
    tools.fixWindowClass(c)

    module.addGlobalStr('wxTreeListCtrlNameStr', c)

    # Change NO_IMAGE default arg values to just -1, as the pi code has
    # problems when using the class name before the class is fully defined.
    for item in c.allItems():
        if isinstance(item, etgtools.ParamDef) and item.default == 'NO_IMAGE':
            item.default = '-1'

    # transfer ownership of some parameters
    c.find('AssignImageList.imageList').transfer = True
    c.find('SetItemData.data').transfer = True
    c.find('AppendItem.data').transfer = True
    c.find('InsertItem.data').transfer = True
    c.find('PrependItem.data').transfer = True


    # Replace GetSelections with an implementation that returns a Python list
    c.find('GetSelections').ignore()
    c.addCppMethod('PyObject*', 'GetSelections', '()',
        doc="""\
            Returns a list of all selected items. This method can be used in
            both single and multi-selection case.""",
        body="""\
            unsigned count;
            wxTreeListItems items;
            count = self->GetSelections(items);

            wxPyThreadBlocker blocker;
            PyObject* list = PyList_New(count);
            for (size_t i=0; i<count; i++) {
                wxTreeListItem* item = new wxTreeListItem(items[i]);
                PyObject* obj = wxPyConstructObject((void*)item, wxT("wxTreeListItem"), true);
                PyList_SET_ITEM(list, i, obj); // PyList_SET_ITEM steals a reference
            }
            return list;
        """)

    # Set output parameter flags
    c.find('GetSortColumn.col').out = True
    c.find('GetSortColumn.ascendingOrder').out = True

    # Replace NO_IMAGE with wxTreeListCtrl::NO_IMAGE in parameter default values
    for item in c.allItems():
        if isinstance(item, etgtools.ParamDef) and item.default == 'NO_IMAGE':
            item.default = 'wxTreeListCtrl::NO_IMAGE'

    #-----------------------------------------------------------------
    c = module.find('wxTreeListEvent')
    tools.fixEventClass(c)

    module.addPyCode("""\
        EVT_TREELIST_SELECTION_CHANGED = wx.PyEventBinder( wxEVT_TREELIST_SELECTION_CHANGED )
        EVT_TREELIST_ITEM_EXPANDING =    wx.PyEventBinder( wxEVT_TREELIST_ITEM_EXPANDING )
        EVT_TREELIST_ITEM_EXPANDED =     wx.PyEventBinder( wxEVT_TREELIST_ITEM_EXPANDED )
        EVT_TREELIST_ITEM_CHECKED =      wx.PyEventBinder( wxEVT_TREELIST_ITEM_CHECKED )
        EVT_TREELIST_ITEM_ACTIVATED =    wx.PyEventBinder( wxEVT_TREELIST_ITEM_ACTIVATED )
        EVT_TREELIST_ITEM_CONTEXT_MENU = wx.PyEventBinder( wxEVT_TREELIST_ITEM_CONTEXT_MENU )
        EVT_TREELIST_COLUMN_SORTED =     wx.PyEventBinder( wxEVT_TREELIST_COLUMN_SORTED )

        # deprecated wxEVT aliases
        wxEVT_COMMAND_TREELIST_SELECTION_CHANGED  = wxEVT_TREELIST_SELECTION_CHANGED
        wxEVT_COMMAND_TREELIST_ITEM_EXPANDING     = wxEVT_TREELIST_ITEM_EXPANDING
        wxEVT_COMMAND_TREELIST_ITEM_EXPANDED      = wxEVT_TREELIST_ITEM_EXPANDED
        wxEVT_COMMAND_TREELIST_ITEM_CHECKED       = wxEVT_TREELIST_ITEM_CHECKED
        wxEVT_COMMAND_TREELIST_ITEM_ACTIVATED     = wxEVT_TREELIST_ITEM_ACTIVATED
        wxEVT_COMMAND_TREELIST_ITEM_CONTEXT_MENU  = wxEVT_TREELIST_ITEM_CONTEXT_MENU
        wxEVT_COMMAND_TREELIST_COLUMN_SORTED      = wxEVT_TREELIST_COLUMN_SORTED
        """)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

