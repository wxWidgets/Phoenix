#!/usr/bin/env python

import wx
import wx.lib.mixins.listctrl as listmix
from six import unichr

#----------------------------------------------------------------------

keyMap = {
    wx.WXK_BACK : "WXK_BACK",
    wx.WXK_TAB : "WXK_TAB",
    wx.WXK_RETURN : "WXK_RETURN",
    wx.WXK_ESCAPE : "WXK_ESCAPE",
    wx.WXK_SPACE : "WXK_SPACE",
    wx.WXK_DELETE : "WXK_DELETE",
    wx.WXK_START : "WXK_START",
    wx.WXK_LBUTTON : "WXK_LBUTTON",
    wx.WXK_RBUTTON : "WXK_RBUTTON",
    wx.WXK_CANCEL : "WXK_CANCEL",
    wx.WXK_MBUTTON : "WXK_MBUTTON",
    wx.WXK_CLEAR : "WXK_CLEAR",
    wx.WXK_SHIFT : "WXK_SHIFT",
    wx.WXK_ALT : "WXK_ALT",
    wx.WXK_MENU : "WXK_MENU",
    wx.WXK_PAUSE : "WXK_PAUSE",
    wx.WXK_CAPITAL : "WXK_CAPITAL",
    #wx.WXK_PRIOR : "WXK_PRIOR",
    #wx.WXK_NEXT : "WXK_NEXT",
    wx.WXK_END : "WXK_END",
    wx.WXK_HOME : "WXK_HOME",
    wx.WXK_LEFT : "WXK_LEFT",
    wx.WXK_UP : "WXK_UP",
    wx.WXK_RIGHT : "WXK_RIGHT",
    wx.WXK_DOWN : "WXK_DOWN",
    wx.WXK_SELECT : "WXK_SELECT",
    wx.WXK_PRINT : "WXK_PRINT",
    wx.WXK_EXECUTE : "WXK_EXECUTE",
    wx.WXK_SNAPSHOT : "WXK_SNAPSHOT",
    wx.WXK_INSERT : "WXK_INSERT",
    wx.WXK_HELP : "WXK_HELP",
    wx.WXK_NUMPAD0 : "WXK_NUMPAD0",
    wx.WXK_NUMPAD1 : "WXK_NUMPAD1",
    wx.WXK_NUMPAD2 : "WXK_NUMPAD2",
    wx.WXK_NUMPAD3 : "WXK_NUMPAD3",
    wx.WXK_NUMPAD4 : "WXK_NUMPAD4",
    wx.WXK_NUMPAD5 : "WXK_NUMPAD5",
    wx.WXK_NUMPAD6 : "WXK_NUMPAD6",
    wx.WXK_NUMPAD7 : "WXK_NUMPAD7",
    wx.WXK_NUMPAD8 : "WXK_NUMPAD8",
    wx.WXK_NUMPAD9 : "WXK_NUMPAD9",
    wx.WXK_MULTIPLY : "WXK_MULTIPLY",
    wx.WXK_ADD : "WXK_ADD",
    wx.WXK_SEPARATOR : "WXK_SEPARATOR",
    wx.WXK_SUBTRACT : "WXK_SUBTRACT",
    wx.WXK_DECIMAL : "WXK_DECIMAL",
    wx.WXK_DIVIDE : "WXK_DIVIDE",
    wx.WXK_F1 : "WXK_F1",
    wx.WXK_F2 : "WXK_F2",
    wx.WXK_F3 : "WXK_F3",
    wx.WXK_F4 : "WXK_F4",
    wx.WXK_F5 : "WXK_F5",
    wx.WXK_F6 : "WXK_F6",
    wx.WXK_F7 : "WXK_F7",
    wx.WXK_F8 : "WXK_F8",
    wx.WXK_F9 : "WXK_F9",
    wx.WXK_F10 : "WXK_F10",
    wx.WXK_F11 : "WXK_F11",
    wx.WXK_F12 : "WXK_F12",
    wx.WXK_F13 : "WXK_F13",
    wx.WXK_F14 : "WXK_F14",
    wx.WXK_F15 : "WXK_F15",
    wx.WXK_F16 : "WXK_F16",
    wx.WXK_F17 : "WXK_F17",
    wx.WXK_F18 : "WXK_F18",
    wx.WXK_F19 : "WXK_F19",
    wx.WXK_F20 : "WXK_F20",
    wx.WXK_F21 : "WXK_F21",
    wx.WXK_F22 : "WXK_F22",
    wx.WXK_F23 : "WXK_F23",
    wx.WXK_F24 : "WXK_F24",
    wx.WXK_NUMLOCK : "WXK_NUMLOCK",
    wx.WXK_SCROLL : "WXK_SCROLL",
    wx.WXK_PAGEUP : "WXK_PAGEUP",
    wx.WXK_PAGEDOWN : "WXK_PAGEDOWN",
    wx.WXK_NUMPAD_SPACE : "WXK_NUMPAD_SPACE",
    wx.WXK_NUMPAD_TAB : "WXK_NUMPAD_TAB",
    wx.WXK_NUMPAD_ENTER : "WXK_NUMPAD_ENTER",
    wx.WXK_NUMPAD_F1 : "WXK_NUMPAD_F1",
    wx.WXK_NUMPAD_F2 : "WXK_NUMPAD_F2",
    wx.WXK_NUMPAD_F3 : "WXK_NUMPAD_F3",
    wx.WXK_NUMPAD_F4 : "WXK_NUMPAD_F4",
    wx.WXK_NUMPAD_HOME : "WXK_NUMPAD_HOME",
    wx.WXK_NUMPAD_LEFT : "WXK_NUMPAD_LEFT",
    wx.WXK_NUMPAD_UP : "WXK_NUMPAD_UP",
    wx.WXK_NUMPAD_RIGHT : "WXK_NUMPAD_RIGHT",
    wx.WXK_NUMPAD_DOWN : "WXK_NUMPAD_DOWN",
    #wx.WXK_NUMPAD_PRIOR : "WXK_NUMPAD_PRIOR",
    wx.WXK_NUMPAD_PAGEUP : "WXK_NUMPAD_PAGEUP",
    #wx.WXK_NUMPAD_NEXT : "WXK_NUMPAD_NEXT",
    wx.WXK_NUMPAD_PAGEDOWN : "WXK_NUMPAD_PAGEDOWN",
    wx.WXK_NUMPAD_END : "WXK_NUMPAD_END",
    wx.WXK_NUMPAD_BEGIN : "WXK_NUMPAD_BEGIN",
    wx.WXK_NUMPAD_INSERT : "WXK_NUMPAD_INSERT",
    wx.WXK_NUMPAD_DELETE : "WXK_NUMPAD_DELETE",
    wx.WXK_NUMPAD_EQUAL : "WXK_NUMPAD_EQUAL",
    wx.WXK_NUMPAD_MULTIPLY : "WXK_NUMPAD_MULTIPLY",
    wx.WXK_NUMPAD_ADD : "WXK_NUMPAD_ADD",
    wx.WXK_NUMPAD_SEPARATOR : "WXK_NUMPAD_SEPARATOR",
    wx.WXK_NUMPAD_SUBTRACT : "WXK_NUMPAD_SUBTRACT",
    wx.WXK_NUMPAD_DECIMAL : "WXK_NUMPAD_DECIMAL",
    wx.WXK_NUMPAD_DIVIDE : "WXK_NUMPAD_DIVIDE",

    wx.WXK_WINDOWS_LEFT : "WXK_WINDOWS_LEFT",
    wx.WXK_WINDOWS_RIGHT : "WXK_WINDOWS_RIGHT",
    wx.WXK_WINDOWS_MENU : "WXK_WINDOWS_MENU",

    wx.WXK_SPECIAL1 : "WXK_SPECIAL1",
    wx.WXK_SPECIAL2 : "WXK_SPECIAL2",
    wx.WXK_SPECIAL3 : "WXK_SPECIAL3",
    wx.WXK_SPECIAL4 : "WXK_SPECIAL4",
    wx.WXK_SPECIAL5 : "WXK_SPECIAL5",
    wx.WXK_SPECIAL6 : "WXK_SPECIAL6",
    wx.WXK_SPECIAL7 : "WXK_SPECIAL7",
    wx.WXK_SPECIAL8 : "WXK_SPECIAL8",
    wx.WXK_SPECIAL9 : "WXK_SPECIAL9",
    wx.WXK_SPECIAL10 : "WXK_SPECIAL10",
    wx.WXK_SPECIAL11 : "WXK_SPECIAL11",
    wx.WXK_SPECIAL12 : "WXK_SPECIAL12",
    wx.WXK_SPECIAL13 : "WXK_SPECIAL13",
    wx.WXK_SPECIAL14 : "WXK_SPECIAL14",
    wx.WXK_SPECIAL15 : "WXK_SPECIAL15",
    wx.WXK_SPECIAL16 : "WXK_SPECIAL16",
    wx.WXK_SPECIAL17 : "WXK_SPECIAL17",
    wx.WXK_SPECIAL18 : "WXK_SPECIAL18",
    wx.WXK_SPECIAL19 : "WXK_SPECIAL19",
}

if 'wxMac' in wx.PlatformInfo:
    keyMap[wx.WXK_RAW_CONTROL] = 'WXK_RAW_CONTROL'
    keyMap[wx.WXK_CONTROL] = "WXK_CONTROL"
    keyMap[wx.WXK_COMMAND] = "WXK_COMMAND"
else:
    keyMap[wx.WXK_COMMAND] = "WXK_COMMAND"
    keyMap[wx.WXK_CONTROL] = "WXK_CONTROL"


#----------------------------------------------------------------------

class KeySink(wx.Window):
    def __init__(self, parent):
        wx.Window.__init__(self, parent, -1, style=wx.WANTS_CHARS
                          #| wx.RAISED_BORDER
                          #| wx.SUNKEN_BORDER
                           , name="sink")

        self.SetBackgroundColour(wx.BLUE)
        self.haveFocus = False
        self.callSkip = True
        self.logKeyDn = True
        self.logKeyUp = True
        self.logChar = True

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouse)

        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.Bind(wx.EVT_KEY_UP, self.OnKeyUp)
        self.Bind(wx.EVT_CHAR, self.OnChar)


    def SetCallSkip(self, skip):
        self.callSkip = skip

    def SetLogKeyUp(self, val):
        self.logKeyUp = val

    def SetLogKeyDn(self, val):
        self.logKeyDn = val

    def SetLogChar(self, val):
        self.logChar = val


    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        rect = self.GetClientRect()
        dc.SetTextForeground(wx.WHITE)
        dc.DrawLabel("Click here and then press some keys",
                     rect, wx.ALIGN_CENTER | wx.ALIGN_TOP)
        if self.haveFocus:
            dc.SetTextForeground(wx.GREEN)
            dc.DrawLabel("Have Focus", rect, wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM)
        else:
            dc.SetTextForeground(wx.RED)
            dc.DrawLabel("Need Focus!", rect, wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM)


    def OnSetFocus(self, evt):
        self.haveFocus = True
        self.Refresh()

    def OnKillFocus(self, evt):
        self.haveFocus = False
        self.Refresh()

    def OnMouse(self, evt):
        if evt.ButtonDown():
            self.SetFocus()


    def OnKeyDown(self, evt):
        if self.logKeyDn:
            self.GetParent().keylog.LogKeyEvent("KeyDown", evt)
        if self.callSkip:
            evt.Skip()

    def OnKeyUp(self, evt):
        if self.logKeyUp:
            self.GetParent().keylog.LogKeyEvent("KeyUp", evt)
        if self.callSkip:
            evt.Skip()

    def OnChar(self, evt):
        if self.logChar:
            self.GetParent().keylog.LogKeyEvent("Char", evt)


#----------------------------------------------------------------------

class KeyLog(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    colHeaders = [ "Event Type",
                   "Key Name",
                   "Key Code",
                   "Modifiers",
                   "Unicode",
                   "UniChr",
                   "RawKeyCode",
                   "RawKeyFlags",
                   ]

    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1,
                            style = wx.LC_REPORT|wx.LC_VRULES|wx.LC_HRULES)
        listmix.ListCtrlAutoWidthMixin.__init__(self)

        for idx, header in enumerate(self.colHeaders):
            self.InsertColumn(idx, header)
        idx += 1
        self.InsertColumn(idx, "")

        for x in range(idx):
            self.SetColumnWidth(x, wx.LIST_AUTOSIZE_USEHEADER)

        self.SetColumnWidth(1, 125)


    def LogKeyEvent(self, evType, evt):
        keycode = evt.GetKeyCode()
        keyname = keyMap.get(keycode, None)

        if keyname is None:
            if keycode < 256:
                if keycode == 0:
                    keyname = "NUL"
                elif keycode < 27:
                    keyname = u"Ctrl-%s" % unichr(ord('A') + keycode-1)
                else:
                    keyname = u"\"%s\"" % unichr(keycode)
            else:
                keyname = u"(%s)" % keycode

        UniChr = ''
        if "unicode" in wx.PlatformInfo:
            UniChr = "\"" + unichr(evt.GetUnicodeKey()) + "\""

        modifiers = ""
        for mod, ch in [(evt.ControlDown(),    'C'),
                        (evt.AltDown(),        'A'),
                        (evt.ShiftDown(),      'S'),
                        (evt.MetaDown(),       'M'),
                        (evt.RawControlDown(), 'R'),]:
            if mod:
                modifiers += ch
            else:
                modifiers += '-'

        id = self.InsertItem(self.GetItemCount(), evType)
        self.SetItem(id, 1, keyname)
        self.SetItem(id, 2, str(keycode))
        self.SetItem(id, 3, modifiers)
        self.SetItem(id, 4, str(evt.GetUnicodeKey()))
        self.SetItem(id, 5, UniChr)
        self.SetItem(id, 6, str(evt.GetRawKeyCode()))
        self.SetItem(id, 7, str(evt.GetRawKeyFlags()))

        self.EnsureVisible(id)


    def ClearLog(self):
        self.DeleteAllItems()

    def CopyLog(self):
        # build a newline and tab delimited string to put into the clipboard
        if "unicode" in wx.PlatformInfo:
            st = u""
        else:
            st = ""
        for h in self.colHeaders:
            st += h + "\t"
        st += "\n"

        for idx in range(self.GetItemCount()):
            for col in range(self.GetColumnCount()):
                item = self.GetItem(idx, col)
                st += item.GetText() + "\t"
            st += "\n"

        data = wx.TextDataObject()
        data.SetText(st)
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(data)
            wx.TheClipboard.Close()
        else:
            wx.MessageBox("Unable to open the clipboard", "Error")




#----------------------------------------------------------------------


class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1, style=0)
        self.keysink = KeySink(self)
        self.keysink.SetMinSize((100, 65))
        self.keylog = KeyLog(self)

        btn = wx.Button(self, -1, "Clear", style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.OnClearBtn, btn)
        btn.SetToolTip(
            "Clear the items from the log window")

        btn2 = wx.Button(self, -1, "Copy", style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.OnCopyBtn, btn2)
        btn2.SetToolTip(
            "Copy the contents of the log window to the clipboard")

        cb1 = wx.CheckBox(self, -1, "Call evt.Skip in Key* events")
        self.Bind(wx.EVT_CHECKBOX, self.OnSkipCB, cb1)
        cb1.SetValue(True)

        cb2 = wx.CheckBox(self, -1, "KEY_UP")
        self.Bind(wx.EVT_CHECKBOX, self.OnKeyUpCB, cb2)
        cb2.SetValue(True)

        cb3 = wx.CheckBox(self, -1, "KEY_DOWN")
        self.Bind(wx.EVT_CHECKBOX, self.OnKeyDnCB, cb3)
        cb3.SetValue(True)

        cb4 = wx.CheckBox(self, -1, "CHAR")
        self.Bind(wx.EVT_CHECKBOX, self.OnCharCB, cb4)
        cb4.SetValue(True)

        buttons = wx.BoxSizer(wx.HORIZONTAL)
        buttons.Add(btn, 0, wx.ALL, 4)
        buttons.Add(btn2, 0, wx.ALL, 4)
        buttons.Add(cb1, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 6)
        buttons.Add(cb2, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 6)
        buttons.Add(cb3, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 6)
        buttons.Add(cb4, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 6)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.keysink, 0, wx.GROW)
        sizer.Add(buttons)
        sizer.Add(self.keylog, 1, wx.GROW)

        self.SetSizer(sizer)


    def OnClearBtn(self, evt):
        self.keylog.ClearLog()

    def OnCopyBtn(self, evt):
        self.keylog.CopyLog()

    def OnSkipCB(self, evt):
        self.keysink.SetCallSkip(evt.GetInt())

    def OnKeyUpCB(self, evt):
        self.keysink.SetLogKeyUp(evt.GetInt())

    def OnKeyDnCB(self, evt):
        self.keysink.SetLogKeyDn(evt.GetInt())

    def OnCharCB(self, evt):
        self.keysink.SetLogChar(evt.GetInt())


#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------



overview = """<html><body>
<h2><center>wxKeyEvents</center></h2>

This demo simply catches all key events and prints info about them.
It is meant to be used as a compatibility test for cross platform work.

</body></html>
"""



if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

