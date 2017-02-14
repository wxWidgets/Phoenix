#---------------------------------------------------------------------------
# Name:        samples/combo/combo1.py
# Author:      Robin Dunn
#
# Created:     1-June-2012
# Copyright:   (c) 2012-2017 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

"""
A simple test case for wx.ComboCtrl using a wx.ListCtrl for the popup
"""

import wx



class NullLog:
    def write(self, *args):
        #print(' '.join(args))
        pass


#----------------------------------------------------------------------
# This class is used to provide an interface between a ComboCtrl and the
# ListCtrl that is used as the popoup for the combo widget.

class ListCtrlComboPopup(wx.ComboPopup):

    def __init__(self):
        wx.ComboPopup.__init__(self)
        self.log = NullLog()
        self.lc = None


    def AddItem(self, txt):
        self.lc.InsertItem(self.lc.GetItemCount(), txt)

    def OnMotion(self, evt):
        item, flags = self.lc.HitTest(evt.GetPosition())
        if item >= 0:
            self.lc.Select(item)
            self.curitem = item

    def OnLeftDown(self, evt):
        self.value = self.curitem
        self.Dismiss()


    # The following methods are those that are overridable from the
    # ComboPopup base class.  Most of them are not required, but all
    # are shown here for demonstration purposes.


    # This is called immediately after construction finishes.  You can
    # use self.GetCombo if needed to get to the ComboCtrl instance.
    def Init(self):
        self.log.write("ListCtrlComboPopup.Init")
        self.value = -1
        self.curitem = -1


    # Create the popup child control.  Return true for success.
    def Create(self, parent):
        self.log.write("ListCtrlComboPopup.Create")
        self.lc = wx.ListCtrl(parent, style=wx.LC_LIST|wx.LC_SINGLE_SEL|wx.SIMPLE_BORDER)
        self.lc.Bind(wx.EVT_MOTION, self.OnMotion)
        self.lc.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        return True


    # Return the widget that is to be used for the popup
    def GetControl(self):
        #self.log.write("ListCtrlComboPopup.GetControl")
        return self.lc

    # Called just prior to displaying the popup, you can use it to
    # 'select' the current item.
    def SetStringValue(self, val):
        self.log.write("ListCtrlComboPopup.SetStringValue")
        idx = self.lc.FindItem(-1, val)
        if idx != wx.NOT_FOUND:
            self.lc.Select(idx)

    # Return a string representation of the current item.
    def GetStringValue(self):
        self.log.write("ListCtrlComboPopup.GetStringValue: %d" % self.value)
        if self.value >= 0:
            return self.lc.GetItemText(self.value)
        return ""

    # Called immediately after the popup is shown
    def OnPopup(self):
        self.log.write("ListCtrlComboPopup.OnPopup")
        wx.ComboPopup.OnPopup(self)

    # Called when popup is dismissed
    def OnDismiss(self):
        self.log.write("ListCtrlComboPopup.OnDismiss")
        wx.ComboPopup.OnDismiss(self)

    # This is called to custom paint in the combo control itself
    # (ie. not the popup).  Default implementation draws value as
    # string.
    def PaintComboControl(self, dc, rect):
        self.log.write("ListCtrlComboPopup.PaintComboControl")
        wx.ComboPopup.PaintComboControl(self, dc, rect)

    # Receives key events from the parent ComboCtrl.  Events not
    # handled should be skipped, as usual.
    def OnComboKeyEvent(self, event):
        self.log.write("ListCtrlComboPopup.OnComboKeyEvent")
        wx.ComboPopup.OnComboKeyEvent(self, event)

    # Implement if you need to support special action when user
    # double-clicks on the parent wxComboCtrl.
    def OnComboDoubleClick(self):
        self.log.write("ListCtrlComboPopup.OnComboDoubleClick")
        wx.ComboPopup.OnComboDoubleClick(self)

    # Return final size of popup. Called on every popup, just prior to OnPopup.
    # minWidth = preferred minimum width for window
    # prefHeight = preferred height. Only applies if > 0,
    # maxHeight = max height for window, as limited by screen size
    #   and should only be rounded down, if necessary.
    def GetAdjustedSize(self, minWidth, prefHeight, maxHeight):
        self.log.write("ListCtrlComboPopup.GetAdjustedSize: %d, %d, %d" % (minWidth, prefHeight, maxHeight))
        return wx.ComboPopup.GetAdjustedSize(self, minWidth, prefHeight, maxHeight)

    # Return true if you want delay the call to Create until the popup
    # is shown for the first time. It is more efficient, but note that
    # it is often more convenient to have the control created
    # immediately.
    # Default returns false.
    def LazyCreate(self):
        self.log.write("ListCtrlComboPopup.LazyCreate")
        return wx.ComboPopup.LazyCreate(self)




#----------------------------------------------------------------------

class TestFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title='combo1.py')
        pnl = wx.Panel(self)

        # Create a ComboCtrl
        cc = self.cc = wx.ComboCtrl(pnl, pos=(10,10), size=(275,-1))
        cc.SetHint('Click the button -->')

        # Create a Popup
        popup = ListCtrlComboPopup()

        # Associate them with each other.  This also triggers the
        # creation of the ListCtrl.
        cc.SetPopupControl(popup)

        # Add some items to the listctrl.
        for x in range(75):
            popup.AddItem("Item-%02d" % x)


#----------------------------------------------------------------------


if __name__ == '__main__':
    app = wx.App(False)
    frm = TestFrame(None)
    frm.Show()
    app.MainLoop()