#!/usr/bin/env python

import random

import wx

globalItems = ['New', 'Open', 'Save', 'Save As...', 'Cut', 'Copy', 'Paste',
               'Delete', 'Select All', 'Find', 'About', 'Help', 'Exit',
               'Python is the Best!']
random.shuffle(globalItems)
globalOrder = []
length = len(globalItems)
# print(length)
for num in range(0, length):
    globalOrder.append(num)
random.shuffle(globalOrder)
# print(len(globalOrder))

randomShuffleCheckedOnce = True
globalCheckedStrings = []


class MyRearrangeDialog(wx.RearrangeDialog):
    def __init__(self, parent, message, title, order, items, log):
        wx.RearrangeDialog.__init__(self, parent, message, title, order, items)

        self.log = log
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.lc = self.GetList()
        sizer.Add(wx.StaticText(panel, wx.ID_ANY,
                                "Number of checked boxes:"))
        self.lenItems = len(items)
        self.tc = wx.TextCtrl(panel, wx.ID_ANY, "%s" % self.lenItems,
                              style=wx.TE_READONLY)
        self.lc.Bind(wx.EVT_CHECKLISTBOX, self.OnCheck)
        self.lc.Bind(wx.EVT_LISTBOX, self.OnListBox)
        self.lc.Bind(wx.EVT_CONTEXT_MENU, self.OnContextMenu)
        sizer.Add(self.tc)
        panel.SetSizer(sizer)
        self.AddExtraControls(panel)

        global randomShuffleCheckedOnce
        global globalCheckedStrings
        if randomShuffleCheckedOnce:
            globalCheckedStrings = []
            for i in range(0, self.lenItems):
                bool = random.randint(0, 1)
                # print(bool)
                if bool:
                    self.lc.Check(item=i, check=False)
                    globalCheckedStrings.append(0)
                else:
                    globalCheckedStrings.append(1)
            randomShuffleCheckedOnce = False
        else:
            for i in range(0, self.lenItems):
                if globalCheckedStrings[i]:
                    self.lc.Check(item=i, check=True)
                else:
                    self.lc.Check(item=i, check=False)

        self.checkedItems = self.lc.GetCheckedItems()
        self.checkedStrings = self.lc.GetCheckedStrings()
        #Update the TextCtrl
        self.tc.SetValue("%s" % len(self.checkedItems))

    def OnListBox(self, event):
        self.log.write('You Selected %s\n' % (self.lc.GetString(event.GetSelection())))

    def OnCheck(self, event):
        self.log.write('You Checked %s %s\n' % (self.lc.GetString(event.GetSelection()),
                                    self.lc.IsChecked(event.GetSelection())))
        #Update the TextCtrl
        self.checkedItems = self.lc.GetCheckedItems()
        self.tc.SetValue("%s" % len(self.checkedItems))

    def OnUnCheckOrCheckAll(self, event):
        doWhat = str(event.GetId()).endswith('1')
        # print('doWhat', doWhat)
        for i in range(0, self.lenItems):
            if doWhat:
                self.lc.Check(i, True)
            else:
                self.lc.Check(i, False)
        self.checkedItems = self.lc.GetCheckedItems()
        self.tc.SetValue("%s" % len(self.checkedItems))

    def OnContextMenu(self, event):
        menu = wx.Menu()
        ID_UNCHECKALL = 1000
        ID_CHECKALL = 1001
        mi1 = wx.MenuItem(menu, ID_UNCHECKALL, 'UnCheck All', 'UnCheck All')
        mi2 = wx.MenuItem(menu, ID_CHECKALL, 'Check All', 'Check All')
        menu.Append(mi1)
        menu.Append(mi2)
        menu.Bind(wx.EVT_MENU, self.OnUnCheckOrCheckAll, id=ID_UNCHECKALL)
        menu.Bind(wx.EVT_MENU, self.OnUnCheckOrCheckAll, id=ID_CHECKALL)
        self.PopupMenu(menu)
        menu.Destroy()

#---------------------------------------------------------------------------


class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        b = wx.Button(self, -1, "Create and Show a RearrangeDialog", (50, 50))
        self.Bind(wx.EVT_BUTTON, self.OnButton, b)

    def OnButton(self, evt):
        global globalOrder
        global globalItems
        global globalCheckedStrings
        rd = MyRearrangeDialog(self, message="Rearrangeify Stuff!",
                               title="This is a wx.RearrangeDialog",
                               order=globalOrder, items=globalItems, log=self.log)
        if rd.ShowModal() == wx.ID_OK:
            # print('GetOrder: ', rd.GetOrder())
            globalOrder = list(range(rd.lenItems))
            globalItems = []

            globalCheckedStrings = []
            for i in range(0, rd.lenItems):
                # print(rd.lc.GetString(i))
                globalItems.append(rd.lc.GetString(i))
                # print(rd.lc.IsChecked(i))
                if rd.lc.IsChecked(i):
                    globalCheckedStrings.append(1)
                else:
                    globalCheckedStrings.append(0)


#---------------------------------------------------------------------------


def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win


#---------------------------------------------------------------------------


overview = """\
A RearrangeDialog is a dialog that allows the user to rearrange
the specified items.

This dialog can be used to allow the user to modify the order
of the items and to enable or disable them individually.
"""


if __name__ == '__main__':
    import sys
    import os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])
