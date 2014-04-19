#!/usr/bin/env python

import wx
import images
import random
import os, sys

try:
    dirName = os.path.dirname(os.path.abspath(__file__))
except:
    dirName = os.path.dirname(os.path.abspath(sys.argv[0]))

sys.path.append(os.path.split(dirName)[0])

try:
    from agw import ultimatelistctrl as ULC
except ImportError: # if it's not there locally, try the wxPython lib.
    from wx.lib.agw import ultimatelistctrl as ULC


def GenerateRandomList(imgList):

    rList = []
    chance = random.randint(0, 2)
    if chance < 2:
        return rList

    numImages = random.randint(1, 3)
    listSize = imgList.GetImageCount()

    for i in range(numImages):
        rList.append(random.randint(0, listSize-1))

    return rList


class TestUltimateListCtrl(ULC.UltimateListCtrl):

    def __init__(self, parent, log):

        ULC.UltimateListCtrl.__init__(self, parent, -1,
                                      agwStyle=wx.LC_REPORT|wx.LC_VIRTUAL|wx.LC_HRULES|wx.LC_VRULES|ULC.ULC_SHOW_TOOLTIPS)

        self.log = log

        self.il = wx.ImageList(16, 16)
        self.il.Add(images.Smiles.GetBitmap())
        self.il.Add(images.core.GetBitmap())
        self.il.Add(images.custom.GetBitmap())
        self.il.Add(images.exit.GetBitmap())
        self.il.Add(images.expansion.GetBitmap())

        self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)

        self.InsertColumn(0, "First")
        self.InsertColumn(1, "Second")
        self.InsertColumn(2, "Third")
        self.SetColumnWidth(0, 175)
        self.SetColumnWidth(1, 175)
        self.SetColumnWidth(2, 175)
        self.SetColumnToolTip(0,"First Column Tooltip!")
        self.SetColumnToolTip(1,"Second Column Tooltip!")
        self.SetColumnToolTip(2,"Third Column Tooltip!")

        # After setting the column width you can specify that
        # this column expands to fill the window. Only one
        # column may be specified.
        self.SetColumnWidth(2, ULC.ULC_AUTOSIZE_FILL)

        self.SetItemCount(1000000)

        self.attr1 = ULC.UltimateListItemAttr()
        self.attr1.SetBackgroundColour(wx.Colour("yellow"))

        self.attr2 = ULC.UltimateListItemAttr()
        self.attr2.SetBackgroundColour(wx.Colour("light blue"))

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected)

        self.randomLists = [GenerateRandomList(self.il) for i in range(5)]


    def OnItemSelected(self, event):

        self.currentItem = event.Index
        self.log.write("OnItemSelected: %s, %s, %s, %s\n" %(self.currentItem,
                                                          self.GetItemText(self.currentItem),
                                                          self.getColumnText(self.currentItem, 1),
                                                          self.getColumnText(self.currentItem, 2)))

    def OnItemActivated(self, event):
        self.currentItem = event.Index
        self.log.write("OnItemActivated: %s\nTopItem: %s\n" %(self.GetItemText(self.currentItem), self.GetTopItem()))

    def getColumnText(self, index, col):

        item = self.GetItem(index, col)
        return item.GetText()

    def OnItemDeselected(self, evt):
        self.log.write("OnItemDeselected: %s\n" % evt.Index)


    #---------------------------------------------------
    # These methods are callbacks for implementing the
    # "virtualness" of the list...  Normally you would
    # determine the text, attributes and/or image based
    # on values from some external data source, but for
    # this demo we'll just calculate them

    def OnGetItemText(self, item, col):
        return "Item %d, column %d" % (item, col)

    def OnGetItemToolTip(self, item, col):
        if item == 0:
            return "Tooltip: Item %d, column %d" % (item, col)
        return None

    def OnGetItemTextColour(self, item, col):
        if item == 0 and col == 0:
            return wx.Colour(255,0,0)
        elif item == 0 and col == 1:
            return wx.Colour(0,255,0)
        elif item == 0 and col == 2:
            return wx.Colour(0,0,255)
        else:
            return None


    def OnGetItemColumnImage(self, item, column):

        return self.randomLists[item%5]


    def OnGetItemImage(self, item):

        return self.randomLists[item%5]


    def OnGetItemAttr(self, item):
        if item % 3 == 1:
            return self.attr1
        elif item % 3 == 2:
            return self.attr2
        else:
            return None


    def OnGetItemColumnCheck(self, item, column):

        if item%3 == 0:
            return True

        return False


    def OnGetItemCheck(self, item):

        if item%3 == 1:
            return True

        return False


    def OnGetItemColumnKind(self, item, column):

        if item%3 == 0:
            return 2
        elif item%3 == 1:
            return 1

        return 0


#---------------------------------------------------------------------------

class TestFrame(wx.Frame):

    def __init__(self, parent, log):

        wx.Frame.__init__(self, parent, -1, "UltimateListCtrl in wx.LC_VIRTUAL mode", size=(700, 600))
        panel = wx.Panel(self, -1)
        sizer = wx.BoxSizer(wx.VERTICAL)

        listCtrl = TestUltimateListCtrl(panel, log)

        sizer.Add(listCtrl, 1, wx.EXPAND)
        panel.SetSizer(sizer)
        sizer.Layout()

        self.SetIcon(images.Mondrian.GetIcon())
        self.CenterOnScreen()
        self.Show()


#---------------------------------------------------------------------------

if __name__ == '__main__':
    import sys
    app = wx.App(0)
    frame = TestFrame(None, sys.stdout)
    frame.Show(True)
    app.MainLoop()


