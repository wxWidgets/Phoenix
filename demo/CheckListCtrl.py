#!/usr/bin/env python

import sys
import wx

from ListCtrl import musicdata

#----------------------------------------------------------------------

class CheckListCtrl(wx.ListCtrl):
    def __init__(self, parent, log):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT)
        self.log = log

        self.EnableCheckBoxes()
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated)
        self.Bind(wx.EVT_LIST_ITEM_CHECKED, self.OnItemCheckChanged)
        self.Bind(wx.EVT_LIST_ITEM_UNCHECKED, self.OnItemCheckChanged)

    def ToggleItem(self, index):
        toggle = not self.IsItemChecked(index)
        self.CheckItem(index, toggle)

    def OnItemActivated(self, evt):
        self.ToggleItem(evt.Index)

    def OnItemCheckChanged(self, evt):
        index = evt.Index
        data = self.GetItemData(index)
        title = musicdata[data][1]
        what = "checked" if self.IsItemChecked(index) else "unchecked"
        self.log.write('item "%s", at index %d was %s\n' % (title, index, what))



class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        self.list = CheckListCtrl(self, log)
        sizer = wx.BoxSizer()
        sizer.Add(self.list, 1, wx.EXPAND)
        self.SetSizer(sizer)

        self.list.InsertColumn(0, "Artist")
        self.list.InsertColumn(1, "Title", wx.LIST_FORMAT_RIGHT)
        self.list.InsertColumn(2, "Genre")

        for key, data in musicdata.items():
            index = self.list.InsertItem(self.list.GetItemCount(), data[0])
            self.list.SetItem(index, 1, data[1])
            self.list.SetItem(index, 2, data[2])
            self.list.SetItemData(index, key)

        self.list.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.list.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        self.list.SetColumnWidth(2, 100)

        self.list.CheckItem(4, True)
        self.list.CheckItem(7, True)

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.list)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected, self.list)


    def OnItemSelected(self, evt):
        self.log.write('item selected: %s\n' % evt.Index)

    def OnItemDeselected(self, evt):
        self.log.write('item deselected: %s\n' % evt.Index)


#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------



overview = """<html><body>
<h2><center>CheckListCtrl</center></h2>

Starting with the wxPython 4.1 series the wx.ListCtrl is able to support checkboxes on the
items, and adds events to notify when the items are checked or unchecked.

</body></html>
"""



if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

