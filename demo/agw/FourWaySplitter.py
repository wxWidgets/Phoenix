#!/usr/bin/env python

import wx

import os
import sys

try:
    dirName = os.path.dirname(os.path.abspath(__file__))
except:
    dirName = os.path.dirname(os.path.abspath(sys.argv[0]))

sys.path.append(os.path.split(dirName)[0])

try:
    from agw import fourwaysplitter as FWS
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.fourwaysplitter as FWS

import images

#----------------------------------------------------------------------
class SamplePane(wx.Panel):
    """
    Just a simple test window to put into the splitter.
    """
    def __init__(self, parent, colour, label):
        wx.Panel.__init__(self, parent, style=wx.BORDER_SUNKEN)
        self.SetBackgroundColour(colour)
        wx.StaticText(self, -1, label, (5,5))

    def SetOtherLabel(self, label):
        wx.StaticText(self, -1, label, (5, 30))



class ControlPane(wx.Panel):

    def __init__(self, parent):

        wx.Panel.__init__(self, parent)

        luCheck = wx.CheckBox(self, -1, "Live Update")
        luCheck.SetValue(True)
        self.Bind(wx.EVT_CHECKBOX, self.OnSetLiveUpdate, luCheck)

        btn1 = wx.Button(self, -1, "Swap 2 && 4")
        self.Bind(wx.EVT_BUTTON, self.OnSwapButton24, btn1)

        btn2 = wx.Button(self, -1, "Swap 1 && 3")
        self.Bind(wx.EVT_BUTTON, self.OnSwapButton13, btn2)

        static = wx.StaticText(self, -1, "Expand A Window")
        combo = wx.ComboBox(self, -1, choices=["None", "1", "2", "3", "4"],
                            style=wx.CB_READONLY|wx.CB_DROPDOWN)
        combo.SetStringSelection("None")

        self.Bind(wx.EVT_COMBOBOX, self.OnExpandWindow)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(luCheck, 0, wx.TOP, 5)
        sizer.Add(btn1, 0, wx.TOP, 5)
        sizer.Add(btn2, 0, wx.TOP, 5)
        sizer.Add(static, 0, wx.TOP, 10)
        sizer.Add(combo, 0, wx.EXPAND|wx.RIGHT|wx.TOP, 2)

        border = wx.BoxSizer()
        border.Add(sizer, 1, wx.EXPAND|wx.ALL, 5)
        self.SetSizer(border)


    def OnSetLiveUpdate(self, evt):

        check = evt.GetEventObject()
        self.GetParent().SetLiveUpdate(check.GetValue())


    def OnSwapButton24(self, evt):

        self.GetParent().Swap2and4()


    def OnSwapButton13(self, evt):

        self.GetParent().Swap1and3()


    def OnExpandWindow(self, event):

        self.GetParent().ExpandWindow(event.GetSelection())


class FWSPanel(wx.Panel):

    def __init__(self, parent, log):

        wx.Panel.__init__(self, parent, -1)
        self.log = log

        cp = ControlPane(self)
        splitter = FWS.FourWaySplitter(self, agwStyle=wx.SP_LIVE_UPDATE)
        self.splitter = splitter
        self.log = log

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(cp)
        sizer.Add(splitter, 1, wx.EXPAND)
        self.SetSizer(sizer)

        p1 = SamplePane(splitter, "pink", "Panel One")
        p1.SetOtherLabel(
            "There are three ways\n"
            "to drag sashes. Try\n"
            "dragging the horizontal\n"
            "sash, the vertical sash\n"
            "or position the mouse at\n"
            "the intersection of the\n"
            "two sashes."
        )
        splitter.AppendWindow(p1)

        p2 = SamplePane(splitter, "sky blue", "Panel Two")
        p2.SetOtherLabel("Hello From wxPython!")
        p2.SetMinSize(p2.GetBestSize())
        splitter.AppendWindow(p2)

        p3 = SamplePane(splitter, "yellow", "Panel Three")
        splitter.AppendWindow(p3)

        p4 = SamplePane(splitter, "Lime Green", "Panel Four")
        splitter.AppendWindow(p4)

        self.log.write("Welcome to the FourWaySplitterDemo!\n")

        self.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGED, self.OnChanged)
        self.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGING, self.OnChanging)


    def GetSashIdx(self, event):

        if event.GetSashIdx() == wx.HORIZONTAL:
            idx = "Horizontal"
        elif event.GetSashIdx() == wx.VERTICAL:
            idx = "Vertical"
        else:
            idx = "Horizontal & Vertical"

        return idx


    def OnChanging(self, event):

        idx = self.GetSashIdx(event)
        self.log.write("Changing sash: %s  %s\n" %(idx, event.GetSashPosition()))

        # This is one way to control the sash limits
        #if event.GetSashPosition().x < 50:
        #    event.Veto()

        event.Skip()


    def OnChanged(self, event):

        idx = self.GetSashIdx(event)
        self.log.write("Changed sash: %s  %s\n" %(idx, event.GetSashPosition()))

        event.Skip()


    def SetLiveUpdate(self, enable):

        if enable:
            self.splitter.SetAGWWindowStyleFlag(wx.SP_LIVE_UPDATE)
        else:
            self.splitter.SetAGWWindowStyleFlag(0)


    def Swap2and4(self):

        win2 = self.splitter.GetWindow(1)
        win4 = self.splitter.GetWindow(3)
        self.splitter.ExchangeWindows(win2, win4)


    def Swap1and3(self):

        win1 = self.splitter.GetWindow(0)
        win3 = self.splitter.GetWindow(2)
        self.splitter.ExchangeWindows(win1, win3)


    def ExpandWindow(self, selection):

        self.splitter.SetExpanded(selection-1)


class FourWaySplitterDemo(wx.Frame):

    def __init__(self, parent, log, id=wx.ID_ANY, title="FourWaySplitter Demo",
                 size=(700, 500)):

        wx.Frame.__init__(self, parent, id, title, size=size)

        self.log = log
        panel = FWSPanel(self, log)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        sizer.Layout()

        statusbar = self.CreateStatusBar(2)
        statusbar.SetStatusWidths([-2, -1])
        # statusbar fields
        statusbar_fields = [("FourWaySplitter wxPython Demo, Andrea Gavana @ 03 Nov 2006"),
                            ("Welcome To wxPython!")]

        for i in range(len(statusbar_fields)):
            statusbar.SetStatusText(statusbar_fields[i], i)

        self.CreateMenu()

        self.SetIcon(images.Mondrian.GetIcon())
        self.CenterOnScreen()


    def CreateMenu(self):

        menuBar = wx.MenuBar(wx.MB_DOCKABLE)
        fileMenu = wx.Menu()
        helpMenu = wx.Menu()

        item = wx.MenuItem(fileMenu, wx.ID_ANY, "E&xit")
        self.Bind(wx.EVT_MENU, self.OnQuit, item)
        fileMenu.Append(item)

        item = wx.MenuItem(helpMenu, wx.ID_ANY, "About")
        self.Bind(wx.EVT_MENU, self.OnAbout, item)
        helpMenu.Append(item)

        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        self.SetMenuBar(menuBar)


    def OnQuit(self, event):

        self.Destroy()


    def OnAbout(self, event):

        msg = "This Is The About Dialog Of The FourWaySplitter Demo.\n\n" + \
            "Author: Andrea Gavana @ 03 Nov 2006\n\n" + \
            "Please Report Any Bug/Requests Of Improvements\n" + \
            "To Me At The Following Addresses:\n\n" + \
            "andrea.gavana@gmail.com\n" + "andrea.gavana@maerskoil.com\n\n" + \
            "Welcome To wxPython " + wx.VERSION_STRING + "!!"

        dlg = wx.MessageDialog(self, msg, "FourWaySplitter wxPython Demo",
                               wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()


#---------------------------------------------------------------------------


class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        b = wx.Button(self, -1, " Test FourWaySplitter ", (50,50))
        self.Bind(wx.EVT_BUTTON, self.OnButton, b)


    def OnButton(self, evt):
        self.win = FourWaySplitterDemo(self, self.log)
        self.win.Show(True)

#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------


overview = FWS.__doc__


if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

