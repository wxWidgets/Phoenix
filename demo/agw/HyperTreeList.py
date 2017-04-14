#!/usr/bin/env python
#   Tags: phoenix-port, py3-port

import os
import string
import random

import wx
import wx.lib.colourselect as csel
import wx.lib.colourutils as cutils

import sys

from six import BytesIO

try:
    dirName = os.path.dirname(os.path.abspath(__file__))
except:
    dirName = os.path.dirname(os.path.abspath(sys.argv[0]))

sys.path.append(os.path.split(dirName)[0])

try:
    from agw import hypertreelist as HTL
    bitmapDir = "bitmaps/"
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.hypertreelist as HTL
    bitmapDir = "agw/bitmaps/"

import ListCtrl
import images


penstyle = ["wx.PENSTYLE_SOLID", "wx.PENSTYLE_TRANSPARENT", "wx.PENSTYLE_DOT",
            "wx.PENSTYLE_LONG_DASH", "wx.PENSTYLE_DOT_DASH", "wx.PENSTYLE_USER_DASH",
            "wx.PENSTYLE_BDIAGONAL_HATCH", "wx.PENSTYLE_CROSSDIAG_HATCH",
            "wx.PENSTYLE_FDIAGONAL_HATCH", "wx.PENSTYLE_CROSS_HATCH",
            "wx.PENSTYLE_HORIZONTAL_HATCH", "wx.PENSTYLE_VERTICAL_HATCH"]

ArtIDs = [ "None",
           "wx.ART_ADD_BOOKMARK",
           "wx.ART_DEL_BOOKMARK",
           "wx.ART_HELP_SIDE_PANEL",
           "wx.ART_HELP_SETTINGS",
           "wx.ART_HELP_BOOK",
           "wx.ART_HELP_FOLDER",
           "wx.ART_HELP_PAGE",
           "wx.ART_GO_BACK",
           "wx.ART_GO_FORWARD",
           "wx.ART_GO_UP",
           "wx.ART_GO_DOWN",
           "wx.ART_GO_TO_PARENT",
           "wx.ART_GO_HOME",
           "wx.ART_FILE_OPEN",
           "wx.ART_PRINT",
           "wx.ART_HELP",
           "wx.ART_TIP",
           "wx.ART_REPORT_VIEW",
           "wx.ART_LIST_VIEW",
           "wx.ART_NEW_DIR",
           "wx.ART_HARDDISK",
           "wx.ART_FLOPPY",
           "wx.ART_CDROM",
           "wx.ART_REMOVABLE",
           "wx.ART_FOLDER",
           "wx.ART_FOLDER_OPEN",
           "wx.ART_GO_DIR_UP",
           "wx.ART_EXECUTABLE_FILE",
           "wx.ART_NORMAL_FILE",
           "wx.ART_TICK_MARK",
           "wx.ART_CROSS_MARK",
           "wx.ART_ERROR",
           "wx.ART_QUESTION",
           "wx.ART_WARNING",
           "wx.ART_INFORMATION",
           "wx.ART_MISSING_IMAGE",
           "SmileBitmap"
           ]

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
    wx.WXK_CONTROL : "WXK_CONTROL",
    wx.WXK_MENU : "WXK_MENU",
    wx.WXK_PAUSE : "WXK_PAUSE",
    wx.WXK_CAPITAL : "WXK_CAPITAL",
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
    wx.WXK_NUMPAD_PAGEUP : "WXK_NUMPAD_PAGEUP",
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
    wx.WXK_NUMPAD_DIVIDE : "WXK_NUMPAD_DIVIDE"
    }


#----------------------------------------------------------------------
def GetMondrianData():
    return \
'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00 \x00\x00\x00 \x08\x06\x00\
\x00\x00szz\xf4\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\x00\x00qID\
ATX\x85\xed\xd6;\n\x800\x10E\xd1{\xc5\x8d\xb9r\x97\x16\x0b\xad$\x8a\x82:\x16\
o\xda\x84pB2\x1f\x81Fa\x8c\x9c\x08\x04Z{\xcf\xa72\xbcv\xfa\xc5\x08 \x80r\x80\
\xfc\xa2\x0e\x1c\xe4\xba\xfaX\x1d\xd0\xde]S\x07\x02\xd8>\xe1wa-`\x9fQ\xe9\
\x86\x01\x04\x10\x00\\(Dk\x1b-\x04\xdc\x1d\x07\x14\x98;\x0bS\x7f\x7f\xf9\x13\
\x04\x10@\xf9X\xbe\x00\xc9 \x14K\xc1<={\x00\x00\x00\x00IEND\xaeB`\x82'

def GetMondrianBitmap():
    return wx.Bitmap(GetMondrianImage())

def GetMondrianImage():
    stream = BytesIO(GetMondrianData())
    return wx.Image(stream)

def GetMondrianIcon():
    icon = wx.Icon()
    icon.CopyFromBitmap(GetMondrianBitmap())
    return icon


#----------------------------------------------------------------------
def GetSmilesData():
    return \
'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\
\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\
\x00\x02\x89IDAT8\x8dm\x93\xddK\x93a\x18\xc6\x7f\xef\xc7\xb3\xa6\xc3 aV\xcc\
\xad\x99\x8d\\\x08\x11AAd\x91\x95\x85F\'\x9dD\x8d\xa8\xe9\xb6X\x87\xe1\x7f\
\xd0A\xe2y\'\xe6I\x7f@\'!T\x96\'A\x10A\xf4!\xcc\xd1\xb7&DP \xba\xe5\xde\xd7\
\xed\xea\xc0\xcdF\xf9\xc0u\xf2<\xcf\xc5}\xdf\xd7u\xddX\xb6\xc3\xbfH\xa5.)\
\x1e\xdf)\xd7\xb5d\x8c\xadD"\xaa\\.\xa3\xcd\xfe\xda4\x9dl&\xad\xceHP\xbd\xbd\
\x9fx\xf0\xe0\x08\xe5\xf2eJ\xa5\x8b\xdc\xbf\xbf\x9f\xae\xaeGtFj\xcaf\xae\xa9\
\x99cY\xb6\x03\xc0\xe9S\xc7\x14\x8b\xfd\xe4\xce\x9d\xf3\x18\xe3\x01%`\x05\
\xa8\x02\x15\xe0#\xbe_ \x9f\xf7\x98\x9f?\xc2\xf4\x93\xe7\x16\xb0\xdeA6\x93V,\
\x06\x13\x13\xb71&\t\x84\xea\xc4F\xb1U\xa0\x8c1\x16\x13\x13[\x88\xc5\x9e\x91\
\xcd\\]\x7f\xb4l\x87h\xb4]\x9eW\x90\xf4E\xd2c\x8d\x8e\x8e\n\x90\x94\x92\x94\
\x12\xa0p8,\xa9UR\x8b<\x0fE;\x91e;\xb8\xd9LZ]]k\x18\xd3\x028@\x8d\xf1\xf1\
\xf1\xa6)\x97\xe8\xe9\xe9ann\x0eh\x05\xd50\x04\xb9q\xbd\xca\xe7\xf9\x94\xec\
\x99\x99\x87\x0c\rE\x80E\xe0#\xf0\xba\x89\\\x01\x16YXXh\xba\xabA\xa5\x95\xa1\
\x93m\xcc\xccLa\x19c\xabT\xba\x891m\xc0*\xc3\xc3\xdf\x99\x9c\xf46\x84\x83\
\x85\xba\xa0ur\xb5\nK\x1d\xf8\xab\x0e\xa1]\xf3\r\x1b\xbd\xba\xe2\xcbLN\xfa\
\xc0\x12\xf0\x0e(6\x91\x05Zcwg\x10\xfc\x16\xf0\x83\x00\xd8\xf1x\x84b\xf1\x1b\
\xf0\x03(\x92L\xbe\x04^\xd4+\xeb/\x19\x1f\xaa6\x9f\xbf/C\xb9\x8d\xe2\x9cE|W\
\x18\xb7\xbf\xff\x0cSS\xf7\xe8\xed\r\x00\xa2P\x80PH\x94\x1a\x85\xa9\x01kP\
\xb58\xb8\xaf\r}\x89@y+S\x8f\x7f\xd1\x7f\xfcd\xc3FK\x9e\xd7R\xb7i\xdd*\x05\
\x83\n\x04\x02r]G\xa1\xa0\xab\xfd\xdd\xed\xd2\xe2^\xa9\xd0\'\xef\xd5\tEw\x04\
\xb4\x11\xe5\xc1\xc14\xf9\xfc\xeaz\x9b\r\xfc\xf6\xa9\xf8>\xbecq8\xd9\xc1\xeb\
\xa7QX\x0e\xc3Z\x80\xfc\xad"\x83g\xce\xb1\x11$\xcbv\x18\x18\xe8\xd3\xc8\x08\
\xf2<$\xd5Q\xb5\xa5\x95m\xd2\xb7\xa4\xf4\xe1\x90\xbc7G5ra\x87\x06\x8e\x1f\
\xd0\x7f\xcb4\xfd\xe4\xb9\xe58\xc3tw\xc3\xd8\x18\xcc\xce\x82_q\xf0+6\xb3\xef\
W\x18\xbb\xfb\x95\xee\xb3/p\xb6\xf61\xfd\xec\xad\xb5\x11\x8b\xcdV4\x97K+\x91\
\xd8.\xe3"\xe3\xa2\xc4\x9e\x0e\xe52W6]\xe7?\xc6#-\xf1\x056\x98<\x00\x00\x00\
\x00IEND\xaeB`\x82'

def GetSmilesBitmap():
    return wx.Bitmap(GetSmilesImage())

def GetSmilesImage():
    stream = BytesIO(GetSmilesData())
    return wx.Image(stream)


#-----------------------------------------------------------------------------
# PATH & FILE FILLING (OS INDEPENDENT)
#-----------------------------------------------------------------------------

def opj(path):
    """Convert paths to the platform-specific separator"""
    str = apply(os.path.join, tuple(path.split('/')))
    # HACK: on Linux, a leading / gets lost...
    if path.startswith('/'):
        str = '/' + str
    return str

#-----------------------------------------------------------------------------

#---------------------------------------------------------------------------
# Just A Dialog To Select Pen Styles
#---------------------------------------------------------------------------
class PenDialog(wx.Dialog):

    def __init__(self, parent=None, id=-1, title="", pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE, oldpen=None,
                 pentype=0):

        wx.Dialog.__init__(self, parent, id, title, pos, size, style)

        self.colourbutton = wx.Button(self, -1, "")
        self.spinwidth = wx.SpinCtrl(self, -1, "1", min=1, max=3, style=wx.SP_ARROW_KEYS)

        self.combostyle = wx.ComboBox(self, -1, choices=penstyle, style=wx.CB_DROPDOWN|wx.CB_READONLY)

        choices = ["[1, 1]", "[2, 2]", "[3, 3]", "[4, 4]"]
        self.combodash = wx.ComboBox(self, -1, choices=choices, style=wx.CB_DROPDOWN|wx.CB_READONLY)

        self.okbutton = wx.Button(self, -1, "Ok")
        self.cancelbutton = wx.Button(self, -1, "Cancel")

        self.oldpen = oldpen
        self.parent = parent
        self.pentype = pentype

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.OnColour, self.colourbutton)
        self.Bind(wx.EVT_COMBOBOX, self.OnStyle, self.combostyle)
        self.Bind(wx.EVT_BUTTON, self.OnOk, self.okbutton)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, self.cancelbutton)


    def __set_properties(self):

        self.SetTitle("Pen Dialog Selector")
        self.colourbutton.SetMinSize((25, 25))
        self.colourbutton.SetBackgroundColour(self.oldpen.GetColour())

        style = self.oldpen.GetStyle()
        for count, st in enumerate(penstyle):
            if eval(st) == style:
                self.combostyle.SetSelection(count)
                if count == 5:
                    self.combodash.Enable(True)
                else:
                    self.combodash.Enable(False)
                break

        if self.combodash.IsEnabled():
            dashes = repr(self.oldpen.GetDashes())
            self.combodash.SetValue(dashes)

        self.spinwidth.SetValue(self.oldpen.GetWidth())
        self.okbutton.SetDefault()

        if self.pentype == 1:
            self.spinwidth.Enable(False)


    def __do_layout(self):

        mainsizer = wx.BoxSizer(wx.VERTICAL)
        bottomsizer = wx.BoxSizer(wx.HORIZONTAL)
        middlesizer = wx.BoxSizer(wx.VERTICAL)
        stylesizer = wx.BoxSizer(wx.HORIZONTAL)
        widthsizer = wx.BoxSizer(wx.HORIZONTAL)
        coloursizer = wx.BoxSizer(wx.HORIZONTAL)
        label_1 = wx.StaticText(self, -1, "Please Choose The Pen Settings:")
        label_1.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        mainsizer.Add(label_1, 0, wx.ALL|wx.ADJUST_MINSIZE, 10)
        label_2 = wx.StaticText(self, -1, "Pen Colour")
        coloursizer.Add(label_2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 5)
        coloursizer.Add((5, 5), 1, wx.ADJUST_MINSIZE, 0)
        coloursizer.Add(self.colourbutton, 0, wx.ALL|wx.ADJUST_MINSIZE, 5)
        middlesizer.Add(coloursizer, 0, wx.EXPAND, 0)
        label_3 = wx.StaticText(self, -1, "Pen Width")
        widthsizer.Add(label_3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 5)
        widthsizer.Add((5, 5), 1, wx.ADJUST_MINSIZE, 0)
        widthsizer.Add(self.spinwidth, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 5)
        middlesizer.Add(widthsizer, 0, wx.EXPAND, 0)
        label_4 = wx.StaticText(self, -1, "Pen Style")
        stylesizer.Add(label_4, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 5)
        stylesizer.Add((5, 5), 1, wx.ADJUST_MINSIZE, 0)
        stylesizer.Add(self.combostyle, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 5)
        stylesizer.Add(self.combodash, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 5)
        middlesizer.Add(stylesizer, 0, wx.BOTTOM|wx.EXPAND, 5)
        mainsizer.Add(middlesizer, 1, wx.EXPAND, 0)
        bottomsizer.Add(self.okbutton, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 20)
        bottomsizer.Add((20, 20), 1, wx.ADJUST_MINSIZE, 0)
        bottomsizer.Add(self.cancelbutton, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 20)
        mainsizer.Add(bottomsizer, 0, wx.EXPAND, 0)
        self.SetAutoLayout(True)
        self.SetSizer(mainsizer)
        mainsizer.Fit(self)
        mainsizer.SetSizeHints(self)
        self.Layout()
        self.Centre()


    def OnColour(self, event):

        obj = event.GetEventObject()
        old = obj.GetBackgroundColour()
        colourdata = wx.ColourData()
        colourdata.SetColour(old)
        dlg = wx.ColourDialog(self, colourdata)

        dlg.GetColourData().SetChooseFull(True)

        if dlg.ShowModal() == wx.ID_OK:

            # If the user selected OK, then the dialog's wx.ColourData will
            # contain valid information. Fetch the data ...
            data = dlg.GetColourData()

            # ... then do something with it. The actual colour data will be
            # returned as a three-tuple (r, g, b) in this particular case.
            col1 = data.GetColour().Get()
            obj.SetBackgroundColour(col1)
        # Once the dialog is destroyed, Mr. wx.ColourData is no longer your
        # friend. Don't use it again!
        dlg.Destroy()

        event.Skip()


    def OnStyle(self, event):

        choice = event.GetEventObject().GetValue()
        self.combodash.Enable(choice==5)
        event.Skip()


    def OnOk(self, event):

        colour = self.colourbutton.GetBackgroundColour()
        style = eval(self.combostyle.GetValue())
        width = int(self.spinwidth.GetValue())

        dashes = None
        if self.combostyle.GetSelection() == 5:
            dashes = eval(self.combodash.GetValue())

        pen = wx.Pen(colour, width, style)

        if dashes:
            pen.SetDashes(dashes)

        pen.SetCap(wx.CAP_BUTT)

        if self.pentype == 0:
            self.parent.SetConnectionPen(pen)
        else:
            self.parent.SetBorderPen(pen)

        self.Destroy()
        event.Skip()


    def OnCancel(self, event):

        self.Destroy()
        event.Skip()


#---------------------------------------------------------------------------
# Just A Dialog To Select Tree Buttons Icons
#---------------------------------------------------------------------------
class TreeDialog(wx.Dialog):

    def __init__(self, parent=None, id=-1, title="", pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE, oldicons=None):

        wx.Dialog.__init__(self, parent, id, title, pos, size, style)

        self.listicons = wx.ListBox(self, -1, choices=["Set 1", "Set 2", "Set 3", "Set 4", "Set 5"], style=wx.LB_SINGLE)

        bitmap_plus = opj(bitmapDir + "plus" + str(oldicons+1) + ".ico")
        bitmap_minus = opj(bitmapDir+ "minus" + str(oldicons+1) + ".ico")

        bitmap_plus = wx.Image(bitmap_plus, wx.BITMAP_TYPE_ICO)
        bitmap_plus.Rescale(24, 24)
        bitmap_plus = bitmap_plus.ConvertToBitmap()
        bitmap_minus = wx.Image(bitmap_minus, wx.BITMAP_TYPE_ICO)
        bitmap_minus.Rescale(24, 24)
        bitmap_minus = bitmap_minus.ConvertToBitmap()

        self.bitmap_plus = wx.StaticBitmap(self, -1, bitmap_plus)
        self.bitmap_minus = wx.StaticBitmap(self, -1, bitmap_minus)

        self.okbutton = wx.Button(self, -1, "Ok")
        self.cancelbutton = wx.Button(self, -1, "Cancel")

        self.parent = parent

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.OnOk, self.okbutton)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, self.cancelbutton)
        self.Bind(wx.EVT_LISTBOX, self.OnListBox, self.listicons)


    def __set_properties(self):

        self.SetTitle("Tree Buttons Selector")
        self.listicons.SetSelection(0)
        self.okbutton.SetDefault()


    def __do_layout(self):

        mainsizer = wx.BoxSizer(wx.VERTICAL)
        bottomsizer = wx.BoxSizer(wx.HORIZONTAL)
        topsizer = wx.BoxSizer(wx.HORIZONTAL)
        rightsizer = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        label_1 = wx.StaticText(self, -1, "Please Choose One Of These Sets Of Icons:")
        label_1.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        mainsizer.Add(label_1, 0, wx.ALL|wx.ADJUST_MINSIZE, 10)
        topsizer.Add(self.listicons, 0, wx.ALL|wx.EXPAND|wx.ADJUST_MINSIZE, 5)
        label_2 = wx.StaticText(self, -1, "Collapsed")
        sizer_1.Add(label_2, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 10)
        sizer_1.Add((20, 20), 1, wx.ALIGN_RIGHT|wx.ADJUST_MINSIZE, 0)
        sizer_1.Add(self.bitmap_plus, 1, wx.RIGHT|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 10)
        rightsizer.Add(sizer_1, 0, wx.EXPAND, 0)
        label_3 = wx.StaticText(self, -1, "Expanded")
        sizer_2.Add(label_3, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 10)
        sizer_2.Add((20, 20), 1, wx.ADJUST_MINSIZE, 0)
        sizer_2.Add(self.bitmap_minus, 1, wx.RIGHT|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 10)
        rightsizer.Add(sizer_2, 0, wx.EXPAND, 0)
        topsizer.Add(rightsizer, 0, wx.ALL|wx.EXPAND, 5)
        mainsizer.Add(topsizer, 1, wx.EXPAND, 0)
        bottomsizer.Add(self.okbutton, 0, wx.ALL|wx.ADJUST_MINSIZE, 20)
        bottomsizer.Add((20, 20), 1, wx.ADJUST_MINSIZE, 0)
        bottomsizer.Add(self.cancelbutton, 0, wx.ALL|wx.ADJUST_MINSIZE, 20)
        mainsizer.Add(bottomsizer, 0, wx.EXPAND, 0)
        self.SetAutoLayout(True)
        self.SetSizer(mainsizer)
        mainsizer.Fit(self)
        mainsizer.SetSizeHints(self)
        self.Layout()


    def OnListBox(self, event):

        selection = self.listicons.GetSelection()
        bitmap_plus = opj(bitmapDir + "plus" + str(selection+1) + ".ico")
        bitmap_minus = opj(bitmapDir+ "minus" + str(selection+1) + ".ico")

        bitmap_plus = wx.Image(bitmap_plus, wx.BITMAP_TYPE_ICO)
        bitmap_plus.Rescale(24, 24)
        bitmap_plus = bitmap_plus.ConvertToBitmap()
        bitmap_minus = wx.Image(bitmap_minus, wx.BITMAP_TYPE_ICO)
        bitmap_minus.Rescale(24, 24)
        bitmap_minus = bitmap_minus.ConvertToBitmap()

        self.bitmap_plus.SetBitmap(bitmap_plus)
        self.bitmap_minus.SetBitmap(bitmap_minus)

        self.bitmap_plus.Refresh()
        self.bitmap_minus.Refresh()
        event.Skip()


    def OnOk(self, event):

        selection = self.listicons.GetSelection()
        self.parent.SetTreeButtons(selection)
        self.Destroy()
        event.Skip()


    def OnCancel(self, event):

        self.Destroy()
        event.Skip()


#---------------------------------------------------------------------------
# Just A Dialog To Select Tree Cehck/Radio Item Icons
#---------------------------------------------------------------------------
class CheckDialog(wx.Dialog):

    def __init__(self, parent=None, id=-1, title="", pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE):

        wx.Dialog.__init__(self, parent, id, title, pos, size, style)

        self.listicons = wx.ListBox(self, -1, choices=["Set 1", "Set 2"], style=wx.LB_SINGLE)

        bitmap_check = wx.Bitmap(opj(bitmapDir+ "checked.ico"), wx.BITMAP_TYPE_ICO)
        bitmap_uncheck = wx.Bitmap(opj(bitmapDir+ "notchecked.ico"), wx.BITMAP_TYPE_ICO)
        bitmap_flag = wx.Bitmap(opj(bitmapDir+ "flagged.ico"), wx.BITMAP_TYPE_ICO)
        bitmap_unflag = wx.Bitmap(opj(bitmapDir+ "notflagged.ico"), wx.BITMAP_TYPE_ICO)

        self.bitmap_check = wx.StaticBitmap(self, -1, bitmap_check)
        self.bitmap_uncheck = wx.StaticBitmap(self, -1, bitmap_uncheck)
        self.bitmap_flag = wx.StaticBitmap(self, -1, bitmap_flag)
        self.bitmap_unflag = wx.StaticBitmap(self, -1, bitmap_unflag)

        self.okbutton = wx.Button(self, -1, "Ok")
        self.cancelbutton = wx.Button(self, -1, "Cancel")

        self.parent = parent

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.OnOk, self.okbutton)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, self.cancelbutton)
        self.Bind(wx.EVT_LISTBOX, self.OnListBox, self.listicons)


    def __set_properties(self):

        self.SetTitle("Check/Radio Icon Selector")
        self.listicons.SetSelection(0)
        self.okbutton.SetDefault()


    def __do_layout(self):

        mainsizer = wx.BoxSizer(wx.VERTICAL)
        bottomsizer = wx.BoxSizer(wx.HORIZONTAL)
        topsizer = wx.BoxSizer(wx.HORIZONTAL)
        rightsizer = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        label_1 = wx.StaticText(self, -1, "Please Choose One Of These Sets Of Icons:")
        label_1.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        mainsizer.Add(label_1, 0, wx.ALL|wx.ADJUST_MINSIZE, 10)
        topsizer.Add(self.listicons, 0, wx.ALL|wx.EXPAND|wx.ADJUST_MINSIZE, 5)
        label_2 = wx.StaticText(self, -1, "Checked")
        sizer_1.Add(label_2, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 10)
        sizer_1.Add((20, 20), 1, wx.ALIGN_RIGHT|wx.ADJUST_MINSIZE, 0)
        sizer_1.Add(self.bitmap_check, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 10)
        rightsizer.Add(sizer_1, 0, wx.EXPAND, 0)
        label_3 = wx.StaticText(self, -1, "Not Checked")
        sizer_2.Add(label_3, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 10)
        sizer_2.Add((20, 20), 1, wx.ADJUST_MINSIZE, 0)
        sizer_2.Add(self.bitmap_uncheck, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 10)
        rightsizer.Add(sizer_2, 0, wx.EXPAND, 0)
        label_4 = wx.StaticText(self, -1, "Flagged")
        sizer_3.Add(label_4, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 10)
        sizer_3.Add((20, 20), 1, wx.ADJUST_MINSIZE, 0)
        sizer_3.Add(self.bitmap_flag, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 10)
        rightsizer.Add(sizer_3, 0, wx.EXPAND, 0)
        label_5 = wx.StaticText(self, -1, "Not Flagged")
        sizer_4.Add(label_5, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 10)
        sizer_4.Add((20, 20), 1, wx.ADJUST_MINSIZE, 0)
        sizer_4.Add(self.bitmap_unflag, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 10)
        rightsizer.Add(sizer_4, 0, wx.EXPAND, 0)

        topsizer.Add(rightsizer, 0, wx.ALL|wx.EXPAND, 5)
        mainsizer.Add(topsizer, 1, wx.EXPAND, 0)
        bottomsizer.Add(self.okbutton, 0, wx.ALL|wx.ADJUST_MINSIZE, 20)
        bottomsizer.Add((20, 20), 1, wx.ADJUST_MINSIZE, 0)
        bottomsizer.Add(self.cancelbutton, 0, wx.ALL|wx.ADJUST_MINSIZE, 20)
        mainsizer.Add(bottomsizer, 0, wx.EXPAND, 0)
        self.SetAutoLayout(True)
        self.SetSizer(mainsizer)
        mainsizer.Fit(self)
        mainsizer.SetSizeHints(self)
        self.Layout()


    def OnListBox(self, event):

        selection = self.listicons.GetSelection()

        if selection == 0:
            bitmap_check = opj(bitmapDir + "checked.ico")
            bitmap_uncheck = opj(bitmapDir + "notchecked.ico")
            bitmap_flag = opj(bitmapDir + "flagged.ico")
            bitmap_unflag = opj(bitmapDir + "notflagged.ico")
        else:
            bitmap_check = opj(bitmapDir + "aquachecked.ico")
            bitmap_uncheck = opj(bitmapDir + "aquanotchecked.ico")
            bitmap_flag = opj(bitmapDir + "aquaflagged.ico")
            bitmap_unflag = opj(bitmapDir + "aquanotflagged.ico")

        bitmap_check = wx.Bitmap(bitmap_check, wx.BITMAP_TYPE_ICO)
        bitmap_uncheck = wx.Bitmap(bitmap_uncheck, wx.BITMAP_TYPE_ICO)
        bitmap_flag = wx.Bitmap(bitmap_flag, wx.BITMAP_TYPE_ICO)
        bitmap_unflag = wx.Bitmap(bitmap_unflag, wx.BITMAP_TYPE_ICO)

        self.bitmap_uncheck.SetBitmap(bitmap_uncheck)
        self.bitmap_check.SetBitmap(bitmap_check)
        self.bitmap_unflag.SetBitmap(bitmap_unflag)
        self.bitmap_flag.SetBitmap(bitmap_flag)

        self.bitmap_check.Refresh()
        self.bitmap_uncheck.Refresh()
        self.bitmap_flag.Refresh()
        self.bitmap_unflag.Refresh()

        event.Skip()


    def OnOk(self, event):

        selection = self.listicons.GetSelection()
        self.parent.SetCheckRadio(selection)
        self.Destroy()
        event.Skip()


    def OnCancel(self, event):

        self.Destroy()
        event.Skip()


#---------------------------------------------------------------------------
# Just A Dialog To Select Tree Items Icons
#---------------------------------------------------------------------------
class TreeIcons(wx.Dialog):

    def __init__(self, parent=None, id=-1, title="", pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE, oldpen=None,
                 bitmaps=None):

        wx.Dialog.__init__(self, parent, id, title, pos, size, style)

        self.bitmaps = [None, None, None, None]
        empty = wx.Bitmap(16, 16)
        self.parent = parent

        self.bitmaps[0] = wx.StaticBitmap(self, -1, empty)
        self.combonormal = wx.ComboBox(self, -1, choices=ArtIDs, style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.bitmaps[1] = wx.StaticBitmap(self, -1, empty)
        self.comboselected = wx.ComboBox(self, -1, choices=ArtIDs, style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.bitmaps[2] = wx.StaticBitmap(self, -1, empty)
        self.comboexpanded = wx.ComboBox(self, -1, choices=ArtIDs, style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.bitmaps[3] = wx.StaticBitmap(self, -1, empty)
        self.comboselectedexpanded = wx.ComboBox(self, -1, choices=ArtIDs, style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.okbutton = wx.Button(self, -1, "Ok")
        self.cancelbutton = wx.Button(self, -1, "Cancel")

        self.combonormal.SetSelection(bitmaps[0] >= 0 and bitmaps[0]+1 or 0)
        self.comboselected.SetSelection(bitmaps[1] >= 0 and bitmaps[1]+1 or 0)
        self.comboexpanded.SetSelection(bitmaps[2] >= 0 and bitmaps[2]+1 or 0)
        self.comboselectedexpanded.SetSelection(bitmaps[3] >= 0 and bitmaps[3]+1 or 0)

        self.GetBitmaps(bitmaps)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_COMBOBOX, self.OnComboNormal, self.combonormal)
        self.Bind(wx.EVT_COMBOBOX, self.OnComboSelected, self.comboselected)
        self.Bind(wx.EVT_COMBOBOX, self.OnComboExpanded, self.comboexpanded)
        self.Bind(wx.EVT_COMBOBOX, self.OnComboSelectedExpanded, self.comboselectedexpanded)
        self.Bind(wx.EVT_BUTTON, self.OnOk, self.okbutton)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, self.cancelbutton)


    def __set_properties(self):

        self.SetTitle("Item Icon Selector")
        self.okbutton.SetDefault()


    def __do_layout(self):

        mainsizer = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        gridsizer = wx.FlexGridSizer(cols=3, hgap=5, vgap=5)
        label_1 = wx.StaticText(self, -1, "Please Choose The Icons For This Item (All Are Optional):")
        label_1.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        mainsizer.Add(label_1, 0, wx.ALL|wx.ADJUST_MINSIZE, 10)
        label_2 = wx.StaticText(self, -1, "TreeIcon_Normal:")
        gridsizer.Add(label_2, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 5)
        gridsizer.Add(self.bitmaps[0], 0, wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 5)
        gridsizer.Add(self.combonormal, 0, wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        label_3 = wx.StaticText(self, -1, "TreeIcon_Selected:")
        gridsizer.Add(label_3, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 5)
        gridsizer.Add(self.bitmaps[1], 0, wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 5)
        gridsizer.Add(self.comboselected, 0, wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        label_4 = wx.StaticText(self, -1, "TreeIcon_Expanded:")
        gridsizer.Add(label_4, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 5)
        gridsizer.Add(self.bitmaps[2], 0, wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 5)
        gridsizer.Add(self.comboexpanded, 0, wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        label_5 = wx.StaticText(self, -1, "TreeIcon_SelectedExpanded:")
        gridsizer.Add(label_5, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 5)
        gridsizer.Add(self.bitmaps[3], 0, wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 5)
        gridsizer.Add(self.comboselectedexpanded, 0, wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        gridsizer.AddGrowableCol(0)
        gridsizer.AddGrowableCol(1)
        gridsizer.AddGrowableCol(2)
        mainsizer.Add(gridsizer, 0, wx.ALL|wx.EXPAND, 5)
        sizer_2.Add(self.okbutton, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 20)
        sizer_2.Add((20, 20), 1, wx.ADJUST_MINSIZE, 0)
        sizer_2.Add(self.cancelbutton, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 20)
        mainsizer.Add(sizer_2, 1, wx.EXPAND, 0)
        self.SetAutoLayout(True)
        self.SetSizer(mainsizer)
        mainsizer.Fit(self)
        mainsizer.SetSizeHints(self)
        self.Layout()
        self.Centre()


    def OnComboNormal(self, event):

        input = event.GetSelection()
        self.GetBitmap(input, 0)
        event.Skip()


    def OnComboSelected(self, event):

        input = event.GetSelection()
        self.GetBitmap(input, 1)
        event.Skip()


    def OnComboExpanded(self, event):

        input = event.GetSelection()
        self.GetBitmap(input, 2)
        event.Skip()


    def OnComboSelectedExpanded(self, event):

        input = event.GetSelection()
        self.GetBitmap(input, 3)
        event.Skip()


    def OnOk(self, event):

        bitmaps = [-1, -1, -1, -1]
        normal = self.combonormal.GetSelection()
        selected = self.comboselected.GetSelection()
        expanded = self.comboexpanded.GetSelection()
        selexp = self.comboselectedexpanded.GetSelection()

        bitmaps = [(normal > 0 and normal or -1), (selected > 0 and selected or -1),
                   (expanded > 0 and expanded or -1), (selexp > 0 and selexp or -1)]

        newbitmaps = []

        for bmp in bitmaps:
            if bmp > 0:
                newbitmaps.append(bmp-1)
            else:
                newbitmaps.append(bmp)

        self.parent.SetNewIcons(newbitmaps)

        self.Destroy()
        event.Skip()


    def OnCancel(self, event):

        self.Destroy()
        event.Skip()


    def GetBitmap(self, input, which):

        if input == 0:
            bmp = wx.Bitmap(16,16)
            self.ClearBmp(bmp)
        elif input > 36:
            bmp = GetSmilesBitmap()
        else:
            bmp = wx.ArtProvider.GetBitmap(eval(ArtIDs[input]), wx.ART_OTHER, (16,16))
            if not bmp.Ok():
                bmp = wx.Bitmap(16,16)
                self.ClearBmp(bmp)

        self.bitmaps[which].SetBitmap(bmp)
        self.bitmaps[which].Refresh()


    def GetBitmaps(self, bitmaps):

        output = []

        for count, input in enumerate(bitmaps):
            if input < 0:
                bmp = wx.Bitmap(16,16)
                self.ClearBmp(bmp)
            elif input > 35:
                bmp = GetSmilesBitmap()
            else:
                bmp = wx.ArtProvider.GetBitmap(eval(ArtIDs[input+1]), wx.ART_OTHER, (16,16))
                if not bmp.Ok():
                    bmp = wx.Bitmap(16,16)
                    self.ClearBmp(bmp)

            self.bitmaps[count].SetBitmap(bmp)


    def ClearBmp(self, bmp):

        dc = wx.MemoryDC()
        dc.SelectObject(bmp)
        dc.SetBackground(wx.Brush("white"))
        dc.Clear()


#---------------------------------------------------------------------------
# Custom Renderer for the column headers
#---------------------------------------------------------------------------
class HyperTreeHeaderRenderer(object):
    """
    Draws the column headers as a solid color (self.color)
    """

    def __init__(self, parent):
        self.color = wx.Colour(150,150,150)

    def DrawTextFormatted(self, dc, text, rect):
        """
        Draws the item text, correctly formatted.

        :param `dc`: an instance of `wx.DC`;
        :param `text`: the item text;
        :param `rect`: the item client rectangle.
        """

        # determine if the string can fit inside the current width
        w, h, dummy = dc.GetFullMultiLineTextExtent(text)
        width = rect.width

        if w <= width:

            dc.DrawLabel(text, rect, wx.ALIGN_CENTER_VERTICAL)

        else:

            # determine the base width
            ellipsis = "..."
            base_w, h = dc.GetTextExtent(ellipsis)

            # continue until we have enough space or only one character left

            newText = text.split("\n")
            theText = ""

            for text in newText:

                lenText = len(text)
                drawntext = text
                w, dummy = dc.GetTextExtent(text)

                while lenText > 1:

                    if w + base_w <= width:
                        break

                    w_c, h_c = dc.GetTextExtent(drawntext[-1])
                    drawntext = drawntext[0:-1]
                    lenText -= 1
                    w -= w_c

                # if still not enough space, remove ellipsis characters
                while len(ellipsis) > 0 and w + base_w > width:
                    ellipsis = ellipsis[0:-1]
                    base_w, h = dc.GetTextExtent(ellipsis)

                theText += drawntext + ellipsis + "\n"

            theText = theText.rstrip()
            dc.DrawLabel(theText, rect, wx.ALIGN_CENTER_VERTICAL)



    def DrawHeaderButton(self, dc, rect, flags=0, params=None):

        if params != None:
            text_align = params.m_labelAlignment
            bitmap     = params.m_labelBitmap
            text_color = params.m_labelColour
            text_font  = params.m_labelFont
            text       = params.m_labelText

        color = self.color

        if flags & wx.CONTROL_DISABLED:
            color = wx.Colour(wx.WHITE)
        elif flags & wx.CONTROL_SELECTED:
            color = wx.Colour(wx.BLUE)
        if flags & wx.CONTROL_PRESSED:
            self._pressed = True
            color = cutils.AdjustColour(color,-30)
        elif flags & wx.CONTROL_CURRENT:
            self._hover = True
            color = cutils.AdjustColour(color,50)

        # Draw a solid background in self.color
        dc.SetBrush(wx.Brush(color, wx.BRUSHSTYLE_SOLID))
        dc.SetBackgroundMode(wx.SOLID)
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.DrawRectangleRect(rect)

        # Draw the column divider on the right
        x = rect.width + rect.x - 2
        dc.SetPen(wx.Pen(cutils.AdjustColour(color,-30)))
        dc.DrawLine(x,2,x,rect.height-2)
        x += 1
        dc.SetPen(wx.Pen(cutils.AdjustColour(color,30)))
        dc.DrawLine(x,2,x,rect.height-2)

        dc.SetBackgroundMode(wx.TRANSPARENT)

        if params == None:
            return

        # We need to draw the text and/or icon bitmap
        dc.SetFont(text_font)
        dc.SetTextForeground(text_color)

        # Determine the width of the text
        wLabel, hLabel, dummy = dc.GetFullMultiLineTextExtent(text)
        wLabel += 4  # 2 pixel margin either side

        # and the width of the icon, if any
        if bitmap:
            wLabel += bitmap.GetWidth() + 2  # 2 is a margin between the image and text

        # ALIGN_LEFT if the label is larger than the available space
        text_align = (wLabel < rect.width and [text_align] or [wx.ALIGN_LEFT])[0]

        x = rect.x + 2

        if text_align == wx.ALIGN_LEFT:
            xAligned = x

        elif text_align == wx.ALIGN_RIGHT:
            xAligned = x + rect.width - wLabel - 1

        elif text_align == wx.ALIGN_CENTER:
            xAligned = x + (rect.width - wLabel)/2

        if bitmap:
            dc.DrawBitmap(bitmap, xAligned + wLabel - bitmap.GetWidth() , 2, True)

        dc.SetClippingRegion(x, 1, rect.width-2, rect.height - 2)
        self.DrawTextFormatted(dc, text, wx.Rect(xAligned+2, 1, rect.width-2, rect.height-2))
        dc.DestroyClippingRegion()




#---------------------------------------------------------------------------
# HyperTreeList Demo Implementation
#---------------------------------------------------------------------------
class HyperTreeListDemo(wx.Frame):

    def __init__(self, parent, log):

        wx.Frame.__init__(self, parent)

        self.SetMinSize((640, 480))
        self.SetIcon(images.Mondrian.GetIcon())
        self.SetTitle("HyperTreeList wxPython Demo ;-)")

        self.CenterOnParent()

        statusbar = self.CreateStatusBar(2)
        statusbar.SetStatusWidths([-2, -1])
        # statusbar fields
        statusbar_fields = [("HyperTreeList Demo, Andrea Gavana @ 08 May 2007"),
                            ("Welcome To wxPython!")]

        for i in range(len(statusbar_fields)):
            statusbar.SetStatusText(statusbar_fields[i], i)

        self.CreateMenuBar()

        self.oldicons = 0

        splitter = wx.SplitterWindow(self, -1, style=wx.CLIP_CHILDREN | wx.SP_LIVE_UPDATE | wx.SP_3D)
        panel = wx.Panel(splitter, -1, style=wx.WANTS_CHARS)

        # Set up a log window
        self.log = log

        sizer = wx.BoxSizer(wx.VERTICAL)
        # Create the HyperTreeList
        self.tree = HyperTreeList(panel, -1, log=self.log)

        sizer.Add(self.tree, 1, wx.EXPAND)
        panel.SetSizer(sizer)
        sizer.Layout()

        self.leftpanel = wx.ScrolledWindow(splitter, -1, style=wx.SUNKEN_BORDER)
        self.PopulateLeftPanel(self.tree.styles, self.tree.events)

        splitter.SplitVertically(self.leftpanel, panel, 300)

        splitter.SetMinimumPaneSize(120)
        self.leftpanel.SetBackgroundColour(wx.WHITE)
        self.leftpanel.SetScrollRate(20, 20)


    def CreateMenuBar(self):

        file_menu = wx.Menu()

        AS_EXIT = wx.NewId()
        file_menu.Append(AS_EXIT, "&Exit")
        self.Bind(wx.EVT_MENU, self.OnClose, id=AS_EXIT)

        help_menu = wx.Menu()

        AS_ABOUT = wx.NewId()
        help_menu.Append(AS_ABOUT, "&About...")
        self.Bind(wx.EVT_MENU, self.OnAbout, id=AS_ABOUT)

        menu_bar = wx.MenuBar()

        menu_bar.Append(file_menu, "&File")
        menu_bar.Append(help_menu, "&Help")

        self.SetMenuBar(menu_bar)


    def OnClose(self, event):

        self.Destroy()


    def OnAbout(self, event):

        msg = "This Is The About Dialog Of The HyperTreeList Demo.\n\n" + \
              "Author: Andrea Gavana @ 08 May 2007\n\n" + \
              "Please Report Any Bug/Requests Of Improvements\n" + \
              "To Me At The Following Adresses:\n\n" + \
              "andrea.gavana@maerskoil.com\n" + "andrea.gavana@gmail.com\n\n" + \
              "Welcome To wxPython " + wx.VERSION_STRING + "!!"

        dlg = wx.MessageDialog(self, msg, "HyperTreeList Demo",
                               wx.OK | wx.ICON_INFORMATION)

        if wx.Platform != '__WXMAC__':
            dlg.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False))

        dlg.ShowModal()
        dlg.Destroy()


    def PopulateLeftPanel(self, styles, events):

        mainsizer = wx.BoxSizer(wx.VERTICAL)
        recreatetree = wx.Button(self.leftpanel, -1, "Recreate HyperTreeList")
        mainsizer.Add(recreatetree, 0, wx.ALL|wx.ALIGN_CENTER, 10)
        recreatetree.Bind(wx.EVT_BUTTON, self.OnRecreateTree)

        staticboxstyles = wx.StaticBox(self.leftpanel, -1, "HyperTreeList Styles")
        stylesizer = wx.StaticBoxSizer(staticboxstyles, wx.VERTICAL)
        staticboxcolumns = wx.StaticBox(self.leftpanel, -1, "HyperTreeList Columns")
        columnssizer = wx.StaticBoxSizer(staticboxcolumns, wx.VERTICAL)
        staticboxevents = wx.StaticBox(self.leftpanel, -1, "HyperTreeList Events")
        eventssizer = wx.StaticBoxSizer(staticboxevents, wx.VERTICAL)
        staticboxcolours = wx.StaticBox(self.leftpanel, -1, "HyperTreeList Images/Colours")
        colourssizer = wx.StaticBoxSizer(staticboxcolours, wx.VERTICAL)
        staticboxthemes = wx.StaticBox(self.leftpanel, -1, "HyperTreeList Themes/Gradients")
        themessizer = wx.StaticBoxSizer(staticboxthemes, wx.VERTICAL)

        self.treestyles = []
        self.treeevents = []

        for count, style in enumerate(styles):

            if count == 0:
                tags = wx.ALL
            else:
                tags = wx.LEFT|wx.RIGHT|wx.BOTTOM

            if style != "TR_DEFAULT_STYLE":
                check = wx.CheckBox(self.leftpanel, -1, style)
                stylesizer.Add(check, 0, tags, 3)

                if style in ["TR_HAS_BUTTONS", "TR_HAS_VARIABLE_ROW_HEIGHT"]:
                    check.SetValue(1)

                if style == "TR_HAS_VARIABLE_ROW_HEIGHT":
                    check.Enable(False)

                check.Bind(wx.EVT_CHECKBOX, self.OnCheckStyle)
                self.treestyles.append(check)

        flexgridcolumn = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
        flexgridcolumn.AddGrowableCol(0)
        label = wx.StaticText(self.leftpanel, -1, "Text Font")
        label.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        self.buttonfont = wx.Button(self.leftpanel, -1, "Choose...")
        self.buttonfont.Bind(wx.EVT_BUTTON, self.OnColumnFont)
        flexgridcolumn.Add(label, 0, wx.ALIGN_CENTER_VERTICAL)
        flexgridcolumn.Add(self.buttonfont, 0)

        label = wx.StaticText(self.leftpanel, -1, "Text Colour")
        label.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        self.columncolour = csel.ColourSelect(self.leftpanel, -1, "Choose...", wx.BLACK)
        self.columncolour.Bind(csel.EVT_COLOURSELECT, self.OnColumnColour)
        flexgridcolumn.Add(label, 0, wx.ALIGN_CENTER_VERTICAL)
        flexgridcolumn.Add(self.columncolour, 0)

        label = wx.StaticText(self.leftpanel, -1, "Alignment")
        label.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        alignment = wx.Choice(self.leftpanel, -1, choices=["wx.LEFT", "wx.CENTER", "wx.RIGHT"])
        alignment.Bind(wx.EVT_CHOICE, self.OnColumnAlignment)
        flexgridcolumn.Add(label, 0, wx.ALIGN_CENTER_VERTICAL)
        flexgridcolumn.Add(alignment, 0)

        label = wx.StaticText(self.leftpanel, -1, "Width Options")
        label.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        widthoptions = wx.Choice(self.leftpanel, -1, choices=["USEHEADER", "AUTOSIZE"])
        widthoptions.Bind(wx.EVT_CHOICE, self.OnColumnWidth)
        flexgridcolumn.Add(label, 0, wx.ALIGN_CENTER_VERTICAL)
        flexgridcolumn.Add(widthoptions, 0)

        columnimages = wx.CheckBox(self.leftpanel, -1, "Images On Columns", style=wx.ALIGN_RIGHT)
        columnimages.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        columnimages.Bind(wx.EVT_CHECKBOX, self.OnColumnImages)
        flexgridcolumn.Add(columnimages, 0, wx.ALIGN_CENTER_VERTICAL)
        flexgridcolumn.Add((20,20), 0)

        columnimages = wx.CheckBox(self.leftpanel, -1, "Custom Renderer", style=wx.ALIGN_RIGHT)
        columnimages.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        columnimages.Bind(wx.EVT_CHECKBOX, self.OnCustomRenderer)
        flexgridcolumn.Add(columnimages, 0, wx.ALIGN_CENTER_VERTICAL)
        flexgridcolumn.Add((20,20), 0)

        columnssizer.Add(flexgridcolumn, 1, wx.EXPAND)

        for count, event in enumerate(events):

            if count == 0:
                tags = wx.ALL
            else:
                tags = wx.LEFT|wx.RIGHT|wx.BOTTOM

            if count not in [6, 17, 22, 23]:
                check = wx.CheckBox(self.leftpanel, -1, event)
                eventssizer.Add(check, 0, tags, 3)

                if event in ["EVT_TREE_ITEM_EXPANDED", "EVT_TREE_ITEM_COLLAPSED",
                             "EVT_TREE_SEL_CHANGED", "EVT_TREE_SEL_CHANGING"]:

                    check.SetValue(1)

                check.Bind(wx.EVT_CHECKBOX, self.OnCheckEvent)
                self.treeevents.append(check)

        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self.leftpanel, -1, "Connection Pen")
        font = label.GetFont()
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        label.SetFont(font)
        buttonconnection = wx.Button(self.leftpanel, -1, "Choose...")
        buttonconnection.Bind(wx.EVT_BUTTON, self.OnButtonConnection)
        sizer1.Add(label, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        sizer1.Add((1,0), 1, wx.EXPAND)
        sizer1.Add(buttonconnection, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_RIGHT, 5)

        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self.leftpanel, -1, "Border Pen")
        font = label.GetFont()
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        label.SetFont(font)
        buttonborder = wx.Button(self.leftpanel, -1, "Choose...")
        buttonborder.Bind(wx.EVT_BUTTON, self.OnButtonBorder)
        sizer2.Add(label, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.ALIGN_CENTER, 5)
        sizer2.Add((1,0), 1, wx.EXPAND)
        sizer2.Add(buttonborder, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_RIGHT, 5)

        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self.leftpanel, -1, "Tree Buttons")
        font = label.GetFont()
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        label.SetFont(font)
        buttontree = wx.Button(self.leftpanel, -1, "Choose...")
        buttontree.Bind(wx.EVT_BUTTON, self.OnButtonTree)
        sizer3.Add(label, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.ALIGN_CENTER, 5)
        sizer3.Add((1,0), 1, wx.EXPAND)
        sizer3.Add(buttontree, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_RIGHT, 5)

        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self.leftpanel, -1, "Check/Radio Buttons")
        font = label.GetFont()
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        label.SetFont(font)
        buttoncr = wx.Button(self.leftpanel, -1, "Choose...")
        buttoncr.Bind(wx.EVT_BUTTON, self.OnButtonCheckRadio)
        sizer4.Add(label, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.ALIGN_CENTER, 5)
        sizer4.Add((1,0), 1, wx.EXPAND)
        sizer4.Add(buttoncr, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_RIGHT, 5)

        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        radioimage = wx.RadioButton(self.leftpanel, -1, "Image Background", style=wx.RB_GROUP)
        radioimage.Bind(wx.EVT_RADIOBUTTON, self.OnBackgroundImage)
        self.imagebutton = wx.Button(self.leftpanel, -1, "Choose...")
        self.imagebutton.Bind(wx.EVT_BUTTON, self.OnChooseImage)
        sizer5.Add(radioimage, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        sizer5.Add((1,0), 1, wx.EXPAND)
        sizer5.Add(self.imagebutton, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_RIGHT, 5)

        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        radiobackground = wx.RadioButton(self.leftpanel, -1, "Background Colour")
        radiobackground.Bind(wx.EVT_RADIOBUTTON, self.OnBackgroundColour)
        self.backbutton = csel.ColourSelect(self.leftpanel, -1, "Choose...", wx.WHITE)
        self.backbutton.Bind(csel.EVT_COLOURSELECT, self.OnChooseBackground)
        sizer6.Add(radiobackground, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.ALIGN_CENTER, 5)
        sizer6.Add((1,0), 1, wx.EXPAND)
        sizer6.Add(self.backbutton, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.ALIGN_CENTER, 5)

        colourssizer.Add(sizer1, 0, wx.EXPAND)
        colourssizer.Add(sizer2, 0, wx.EXPAND)
        colourssizer.Add(sizer3, 0, wx.EXPAND)
        colourssizer.Add(sizer4, 0, wx.EXPAND)
        colourssizer.Add(sizer5, 0, wx.EXPAND)
        colourssizer.Add(sizer6, 0, wx.EXPAND)

        sizera = wx.BoxSizer(wx.HORIZONTAL)
        self.checknormal = wx.CheckBox(self.leftpanel, -1, "Standard Colours")
        self.focus = csel.ColourSelect(self.leftpanel, -1, "Focus",
                                       self.tree.GetHilightFocusColour())
        self.unfocus = csel.ColourSelect(self.leftpanel, -1, "Non-Focus",
                                         self.tree.GetHilightNonFocusColour())
        self.checknormal.Bind(wx.EVT_CHECKBOX, self.OnCheckNormal)
        self.focus.Bind(csel.EVT_COLOURSELECT, self.OnFocusColour)
        self.unfocus.Bind(csel.EVT_COLOURSELECT, self.OnNonFocusColour)
        sizera1 = wx.BoxSizer(wx.VERTICAL)
        sizera1.Add(self.focus, 0, wx.BOTTOM, 2)
        sizera1.Add(self.unfocus, 0)
        sizera.Add(self.checknormal, 0, wx.ALL, 3)
        sizera.Add((1, 0), 1, wx.EXPAND)
        sizera.Add(sizera1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 3)

        sizerb = wx.BoxSizer(wx.VERTICAL)
        self.checkgradient = wx.CheckBox(self.leftpanel, -1, "Gradient Theme")
        self.checkgradient.Bind(wx.EVT_CHECKBOX, self.OnCheckGradient)
        sizerb1 = wx.BoxSizer(wx.HORIZONTAL)
        sizerb1.Add((10, 0))
        self.radiohorizontal = wx.RadioButton(self.leftpanel, -1, "Horizontal", style=wx.RB_GROUP)
        self.radiohorizontal.Bind(wx.EVT_RADIOBUTTON, self.OnHorizontal)
        sizerb1.Add(self.radiohorizontal, 0, wx.TOP|wx.BOTTOM, 3)
        sizerb2 = wx.BoxSizer(wx.HORIZONTAL)
        sizerb2.Add((10, 0))
        self.radiovertical = wx.RadioButton(self.leftpanel, -1, "Vertical")
        self.radiovertical.Bind(wx.EVT_RADIOBUTTON, self.OnVertical)
        sizerb2.Add(self.radiovertical, 0, wx.BOTTOM, 3)
        sizerb3 = wx.BoxSizer(wx.HORIZONTAL)
        self.firstcolour = csel.ColourSelect(self.leftpanel, -1, "First Colour",
                                             self.tree.GetFirstGradientColour())
        self.secondcolour = csel.ColourSelect(self.leftpanel, -1, "Second Colour",
                                              self.tree.GetSecondGradientColour())
        self.firstcolour.Bind(csel.EVT_COLOURSELECT, self.OnFirstColour)
        self.secondcolour.Bind(csel.EVT_COLOURSELECT, self.OnSecondColour)
        sizerb3.Add(self.firstcolour, 0, wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER_HORIZONTAL, 3)
        sizerb3.Add(self.secondcolour, 0, wx.LEFT|wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER_HORIZONTAL, 3)
        sizerb.Add(self.checkgradient, 0, wx.ALL, 3)
        sizerb.Add(sizerb1, 0)
        sizerb.Add(sizerb2, 0)
        sizerb.Add(sizerb3, 0, wx.ALIGN_CENTER)

        self.checkvista = wx.CheckBox(self.leftpanel, -1, "Windows Vista Theme")
        self.checkvista.Bind(wx.EVT_CHECKBOX, self.OnVista)

        themessizer.Add(sizera, 0, wx.EXPAND)
        themessizer.Add(sizerb, 0, wx.EXPAND)
        themessizer.Add((0, 5))
        themessizer.Add(self.checkvista, 0, wx.EXPAND|wx.ALL, 3)

        mainsizer.Add(stylesizer, 0, wx.EXPAND|wx.ALL, 5)
        mainsizer.Add(columnssizer, 0, wx.EXPAND|wx.ALL, 5)
        mainsizer.Add(colourssizer, 0, wx.EXPAND|wx.ALL, 5)
        mainsizer.Add(themessizer, 0, wx.EXPAND|wx.ALL, 5)
        mainsizer.Add(eventssizer, 0, wx.EXPAND|wx.ALL, 5)

        self.leftpanel.SetSizer(mainsizer)
        mainsizer.Layout()

        radiobackground.SetValue(1)
        self.checknormal.SetValue(1)
        self.radiohorizontal.Enable(False)
        self.radiovertical.Enable(False)
        self.firstcolour.Enable(False)
        self.secondcolour.Enable(False)
        self.imagebutton.Enable(False)


    def OnRecreateTree(self, event):

        panelparent = self.tree.GetParent()
        panelsizer = panelparent.GetSizer()
        panelparent.Freeze()

        panelsizer.Detach(self.tree)
        self.tree.Destroy()
        del self.tree
        self.tree = HyperTreeList(panelparent, -1, log=self.log)
        panelsizer.Add(self.tree, 1, wx.EXPAND)
        panelsizer.Layout()

        panelparent.Thaw()


    def OnCheckStyle(self, event):

        self.tree.ChangeStyle(self.treestyles)
        event.Skip()


    def OnCheckEvent(self, event):

        obj = event.GetEventObject()
        self.tree.BindEvents(obj)

        event.Skip()


    def OnButtonConnection(self, event):

        pen = self.tree.GetConnectionPen()
        dlg = PenDialog(self, -1, oldpen=pen, pentype=0)

        dlg.ShowModal()

        event.Skip()


    def OnColumnFont(self, event):

        font = self.tree.GetColumn(0).GetFont()

        data = wx.FontData()
        data.SetInitialFont(font)
        dlg = wx.FontDialog(self, data)

        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetFontData()
            font = data.GetChosenFont()
            for i in range(0, self.tree.GetMainWindow().GetColumnCount()):
                self.tree.SetColumnFont(i, font)

        dlg.Destroy()
        event.Skip()


    def OnColumnColour(self, event):

        col1 = event.GetValue()
        for i in range(0, self.tree.GetMainWindow().GetColumnCount()):
            self.tree.SetColumnColour(i, col1)

        event.Skip()


    def OnColumnAlignment(self, event):

        selection = event.GetSelection()
        if selection == 0:
            alignment = wx.ALIGN_LEFT
        elif selection == 1:
            alignment = wx.ALIGN_CENTER
        else:
            alignment = wx.ALIGN_RIGHT

        for i in range(1, self.tree.GetMainWindow().GetColumnCount()):
            self.tree.SetColumnAlignment(i, alignment)

        event.Skip()


    def OnColumnImages(self, event):

        for i in range(self.tree.GetMainWindow().GetColumnCount()):
            randimage = random.randint(1, len(ArtIDs))
            img = (event.IsChecked() and [randimage] or [-1])[0]
            self.tree.SetColumnImage(i, img)

        event.Skip()

    def OnCustomRenderer(self, event):

        if event.IsChecked():
            renderer = HyperTreeHeaderRenderer(self)
            renderer.color = wx.Colour(211,227,247)
            renderer.text_color = wx.Colour(30,30,30)
            self.tree.SetHeaderCustomRenderer(renderer)
        else:
            renderer = None
            self.tree.SetHeaderCustomRenderer(renderer)

        self.Refresh()

        event.Skip()



    def OnColumnWidth(self, event):

        selection = event.GetSelection()
        if selection == 0:    # wx.LIST_AUTOSIZE_USEHEADER
            choice = wx.LIST_AUTOSIZE_USEHEADER
        else:
            choice = wx.LIST_AUTOSIZE

        for i in range(self.tree.GetMainWindow().GetColumnCount()):
            self.tree.SetColumnWidth(i, choice)

        event.Skip()


    def SetConnectionPen(self, pen):

        self.tree.SetConnectionPen(pen)


    def OnButtonBorder(self, event):

        pen = self.tree.GetBorderPen()
        dlg = PenDialog(self, -1, oldpen=pen, pentype=1)

        dlg.ShowModal()
        event.Skip()


    def SetBorderPen(self, pen):

        self.tree.SetBorderPen(pen)


    def OnButtonTree(self, event):

        dlg = TreeDialog(self, -1, oldicons=self.oldicons)
        dlg.ShowModal()

        event.Skip()


    def OnButtonCheckRadio(self, event):

        dlg = CheckDialog(self, -1)
        dlg.ShowModal()

        event.Skip()


    def SetTreeButtons(self, selection):

        bitmap_plus = opj(bitmapDir + "plus" + str(selection+1) + ".ico")
        bitmap_minus = opj(bitmapDir + "minus" + str(selection+1) + ".ico")

        bitmap = wx.Bitmap(bitmap_plus, wx.BITMAP_TYPE_ICO)
        width = bitmap.GetWidth()

        il = wx.ImageList(width, width)

        il.Add(wx.Bitmap(bitmap_plus, wx.BITMAP_TYPE_ICO))
        il.Add(wx.Bitmap(bitmap_plus, wx.BITMAP_TYPE_ICO))
        il.Add(wx.Bitmap(bitmap_minus, wx.BITMAP_TYPE_ICO))
        il.Add(wx.Bitmap(bitmap_minus, wx.BITMAP_TYPE_ICO))

        self.il = il
        self.tree.SetButtonsImageList(il)


    def SetCheckRadio(self, selection):

        if selection == 0:
            self.tree.SetImageListCheck(13, 13)
        else:
            bitmap_check = opj(bitmapDir + "aquachecked.ico")
            bitmap_uncheck = opj(bitmapDir + "aquanotchecked.ico")
            bitmap_flag = opj(bitmapDir + "aquaflagged.ico")
            bitmap_unflag = opj(bitmapDir + "aquanotflagged.ico")

            il = wx.ImageList(16, 16)

            il.Add(wx.Bitmap(bitmap_check, wx.BITMAP_TYPE_ICO))
            il.Add(wx.Bitmap(bitmap_uncheck, wx.BITMAP_TYPE_ICO))
            il.Add(wx.Bitmap(bitmap_flag, wx.BITMAP_TYPE_ICO))
            il.Add(wx.Bitmap(bitmap_unflag, wx.BITMAP_TYPE_ICO))
            self.tree.SetImageListCheck(16, 16, il)


    def OnBackgroundImage(self, event):

        if hasattr(self, "backgroundimage"):
            self.tree.SetBackgroundImage(self.backgroundimage)

        self.backbutton.Enable(False)
        self.imagebutton.Enable(True)

        event.Skip()


    def OnChooseImage(self, event):

        wildcard = "JPEG Files (*.jpg)|*.jpg|"     \
                   "Bitmap Files (*.bmp)|*.bmp|" \
                   "PNG Files (*.png)|*.png|"    \
                   "Icon Files (*.ico)|*.ico|"        \
                   "GIF Files (*.gif)|*.gif|"        \
                   "All files (*.*)|*.*"

        dlg = wx.FileDialog(self, "Choose An Image File", ".", "", wildcard, wx.FD_OPEN)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
        else:
            dlg.Destroy()
            return

        dlg.Destroy()
        bitmap = wx.Bitmap(path, wx.BITMAP_TYPE_ANY)
        self.tree.SetBackgroundImage(bitmap)
        self.backgroundimage = bitmap

        event.Skip()


    def OnBackgroundColour(self, event):

        self.imagebutton.Enable(False)
        self.backbutton.Enable(True)
        self.tree.SetBackgroundImage(None)

        event.Skip()


    def OnChooseBackground(self, event):

        col1 = event.GetValue()
        self.tree.SetBackgroundColour(col1)
        event.Skip()


    def OnCheckNormal(self, event):

        self.radiohorizontal.Enable(False)
        self.radiovertical.Enable(False)
        self.firstcolour.Enable(False)
        self.secondcolour.Enable(False)
        self.focus.Enable(True)
        self.unfocus.Enable(True)
        self.checkgradient.SetValue(0)
        self.checkvista.SetValue(0)
        self.tree.EnableSelectionGradient(False)
        self.tree.EnableSelectionVista(False)
        event.Skip()


    def OnFocusColour(self, event):

        col1 = event.GetValue()
        self.tree.SetHilightFocusColour(col1)
        event.Skip()


    def OnNonFocusColour(self, event):

        col1 = event.GetValue()
        self.tree.SetHilightNonFocusColour(col1)
        event.Skip()


    def OnCheckGradient(self, event):

        self.radiohorizontal.Enable(True)
        self.radiovertical.Enable(True)
        self.firstcolour.Enable(True)
        self.secondcolour.Enable(True)
        self.checknormal.SetValue(0)
        self.checkvista.SetValue(0)
        self.focus.Enable(False)
        self.unfocus.Enable(False)
        self.tree.SetGradientStyle(self.radiovertical.GetValue())
        self.tree.EnableSelectionVista(False)
        self.tree.EnableSelectionGradient(True)

        event.Skip()


    def OnHorizontal(self, event):

        self.tree.SetGradientStyle(self.radiovertical.GetValue())
        event.Skip()


    def OnVertical(self, event):

        self.tree.SetGradientStyle(self.radiovertical.GetValue())
        event.Skip()


    def OnFirstColour(self, event):

        col1 = event.GetValue()
        self.tree.SetFirstGradientColour(wx.Colour(col1[0], col1[1], col1[2]))
        event.Skip()


    def OnSecondColour(self, event):

        col1 = event.GetValue()
        self.tree.SetSecondGradientColour(wx.Colour(col1[0], col1[1], col1[2]))
        event.Skip()


    def OnVista(self, event):

        self.radiohorizontal.Enable(False)
        self.radiovertical.Enable(False)
        self.firstcolour.Enable(False)
        self.secondcolour.Enable(False)
        self.checknormal.SetValue(0)
        self.checkgradient.SetValue(0)
        self.focus.Enable(False)
        self.unfocus.Enable(False)
        self.tree.EnableSelectionGradient(False)
        self.tree.EnableSelectionVista(True)

        event.Skip()


#---------------------------------------------------------------------------
# HyperTreeList Implementation
#---------------------------------------------------------------------------
class HyperTreeList(HTL.HyperTreeList):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize,
                 style=wx.SUNKEN_BORDER,
                 agwStyle=wx.TR_HAS_BUTTONS | wx.TR_HAS_VARIABLE_ROW_HEIGHT,
                 log=None):

        HTL.HyperTreeList.__init__(self, parent, id, pos, size, style, agwStyle)

        alldata = dir(HTL)

        treestyles = []
        events = []
        for data in alldata:
            if data.startswith("TR_"):
                treestyles.append(data)
            elif data.startswith("EVT_"):
                events.append(data)

        events = events + [i for i in dir(wx) if i.startswith("EVT_TREE_")]
        for evt in ["EVT_TREE_GET_INFO", "EVT_TREE_SET_INFO", "EVT_TREE_ITEM_MIDDLE_CLICK",
                    "EVT_TREE_STATE_IMAGE_CLICK"]:
            events.remove(evt)

        treestyles = treestyles + [i for i in dir(wx) if i.startswith("TR_")]
        treeset = {}
        treestyles = [treeset.setdefault(e,e) for e in treestyles if e not in treeset]

        treestyles.sort()

        self.events = events
        self.styles = treestyles
        self.item = None

        il = wx.ImageList(16, 16)

        for items in ArtIDs[1:-1]:
            bmp = wx.ArtProvider.GetBitmap(eval(items), wx.ART_TOOLBAR, (16, 16))
            il.Add(bmp)

        smileidx = il.Add(images.Smiles.GetBitmap())
        numicons = il.GetImageCount()

        self.AssignImageList(il)
        self.count = 0
        self.log = log

        # NOTE:  For some reason tree items have to have a data object in
        #        order to be sorted.  Since our compare just uses the labels
        #        we don't need any real data, so we'll just use None below for
        #        the item data.

        # create some columns
        self.AddColumn("Main column")
        self.AddColumn("Column 1")
        self.AddColumn("Column 2")
        self.SetMainColumn(0) # the one with the tree in it...
        self.SetColumnWidth(0, 175)

        self.root = self.AddRoot("The Root Item")

        if not(self.GetAGWWindowStyleFlag() & wx.TR_HIDE_ROOT):
            self.SetPyData(self.root, None)
            self.SetItemImage(self.root, 24, which=wx.TreeItemIcon_Normal)
            self.SetItemImage(self.root, 13, which=wx.TreeItemIcon_Expanded)
            self.SetItemText(self.root, "col 1 root", 1)
            self.SetItemText(self.root, "col 2 root", 2)

        textctrl = wx.TextCtrl(self.GetMainWindow(), -1, "I Am A Simple\nMultiline wx.TexCtrl", style=wx.TE_MULTILINE)
        self.gauge = wx.Gauge(self.GetMainWindow(), -1, 50, style=wx.GA_HORIZONTAL|wx.GA_SMOOTH)
        self.gauge.SetValue(0)
        combobox = wx.ComboBox(self.GetMainWindow(), -1, choices=["That", "Was", "A", "Nice", "Holiday!"], style=wx.CB_READONLY|wx.CB_DROPDOWN)
        button1 = wx.Button(self.GetMainWindow(), -1, "wxPython")
        button1.SetSize(button1.GetBestSize())
        button2 = wx.Button(self.GetMainWindow(), -1, "Rules!")
        button2.SetSize(button2.GetBestSize())
        listctrl = ListCtrl.TestListCtrlPanel(self.GetMainWindow(), self.log)
        listctrl.SetSize((500, 200))

        textctrl.Bind(wx.EVT_CHAR, self.OnTextCtrl)
        combobox.Bind(wx.EVT_COMBOBOX, self.OnComboBox)

        for x in range(15):
            txt = "Item %d" % x
            if x == 1:
                child = self.AppendItem(self.root, txt + "\nHello World\nHappy wxPython-ing!")
                self.SetItemBold(child, True)
            else:
                child = self.AppendItem(self.root, txt)

            self.SetPyData(child, None)
            self.SetItemText(child, txt + " (c1)", 1)
            self.SetItemText(child, txt + " (c2)", 2)
            self.SetItemImage(child, 24, which=wx.TreeItemIcon_Normal)
            self.SetItemImage(child, 13, which=wx.TreeItemIcon_Expanded)

            for y in range(5):
                txt = "item %d-%s" % (x, chr(ord("a")+y))
                if y == 0 and x == 1:
                    last = self.AppendItem(child, txt, ct_type=2, wnd=self.gauge)
                elif y == 1 and x == 2:
                    last = self.AppendItem(child, txt, ct_type=1, wnd=textctrl)
                    if random.randint(0, 3) == 1:
                        self.SetItem3State(last, True)
                elif 2 < y < 4:
                    last = self.AppendItem(child, txt)
                elif y == 4 and x == 1:
                    last = self.AppendItem(child, txt, wnd=combobox)
                else:
                    last = self.AppendItem(child, txt, ct_type=2)

                self.SetPyData(last, None)
                self.SetItemText(last, txt + " (c1)", 1)
                self.SetItemText(last, txt + " (c2)", 2)
                self.SetItemImage(last, 24, which=wx.TreeItemIcon_Normal)
                self.SetItemImage(last, 13, which=wx.TreeItemIcon_Expanded)

                if y == 3 and x == 0:
                    self.SetItemWindow(last, button1, 1)
                    self.SetItemWindow(last, button2, 2)

                for z in range(5):
                    txt = "item %d-%s-%d" % (x, chr(ord("a")+y), z)
                    if z > 2:
                        item = self.AppendItem(last, txt, ct_type=1)
                        if random.randint(0, 3) == 1:
                            self.SetItem3State(item, True)
                    elif 0 < z <= 2:
                        item = self.AppendItem(last, txt, ct_type=2)
                    elif z == 0:
                        item = self.AppendItem(last, txt)

                    self.SetPyData(item, None)

                    if x == 0 and y == 0 and z == 0:
                        self.SetItemText(item, "", 1)
                        self.SetItemText(item, txt + " (c2)", 2)
                        self.SetItemWindow(item, self.CreateTreeCtrl(), 1)
                    elif x == 0 and y == 0 and z == 1:
                        self.SetItemText(item, txt + " (c1)", 1)
                        self.SetItemText(item, "", 2)
                        self.SetItemWindow(item, listctrl, 2)
                    else:
                        self.SetItemText(item, txt + " (c1)", 1)
                        self.SetItemText(item, txt + " (c2)", 2)
                        if z == 0:
                            self.SetItemHyperText(item, True)

                    self.SetItemImage(item, 28, which=wx.TreeItemIcon_Normal)
                    self.SetItemImage(item, numicons-1, which=wx.TreeItemIcon_Selected)

        self.GetMainWindow().Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClick)
        self.Bind(wx.EVT_IDLE, self.OnIdle)

        self.eventdict = {'EVT_TREE_BEGIN_DRAG': self.OnBeginDrag, 'EVT_TREE_BEGIN_LABEL_EDIT': self.OnBeginEdit,
                          'EVT_TREE_BEGIN_RDRAG': self.OnBeginRDrag, 'EVT_TREE_DELETE_ITEM': self.OnDeleteItem,
                          'EVT_TREE_END_DRAG': self.OnEndDrag, 'EVT_TREE_END_LABEL_EDIT': self.OnEndEdit,
                          'EVT_TREE_ITEM_ACTIVATED': self.OnActivate, 'EVT_TREE_ITEM_CHECKED': self.OnItemCheck,
                          'EVT_TREE_ITEM_CHECKING': self.OnItemChecking, 'EVT_TREE_ITEM_COLLAPSED': self.OnItemCollapsed,
                          'EVT_TREE_ITEM_COLLAPSING': self.OnItemCollapsing, 'EVT_TREE_ITEM_EXPANDED': self.OnItemExpanded,
                          'EVT_TREE_ITEM_EXPANDING': self.OnItemExpanding, 'EVT_TREE_ITEM_GETTOOLTIP': self.OnToolTip,
                          'EVT_TREE_ITEM_MENU': self.OnItemMenu, 'EVT_TREE_ITEM_RIGHT_CLICK': self.OnRightDown,
                          'EVT_TREE_KEY_DOWN': self.OnKey, 'EVT_TREE_SEL_CHANGED': self.OnSelChanged,
                          'EVT_TREE_SEL_CHANGING': self.OnSelChanging, "EVT_TREE_ITEM_HYPERLINK": self.OnHyperLink}

        mainframe = wx.GetTopLevelParent(self)

        if not hasattr(mainframe, "leftpanel"):
            self.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnItemExpanded)
            self.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnItemCollapsed)
            self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged)
            self.Bind(wx.EVT_TREE_SEL_CHANGING, self.OnSelChanging)
            self.GetMainWindow().Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
            self.GetMainWindow().Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
        else:
            for combos in mainframe.treeevents:
                self.BindEvents(combos)

        if hasattr(mainframe, "leftpanel"):
            self.ChangeStyle(mainframe.treestyles)

        if not(self.GetAGWWindowStyleFlag() & wx.TR_HIDE_ROOT):
            self.SelectItem(self.root)
            self.Expand(self.root)


    def CreateTreeCtrl(self):

        tree = wx.TreeCtrl(self.GetMainWindow(), -1, wx.Point(0, 0), wx.Size(160, 200),
                           wx.TR_DEFAULT_STYLE)

        items = []

        imglist = wx.ImageList(16, 16, True, 2)
        imglist.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, wx.Size(16,16)))
        imglist.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, wx.Size(16,16)))
        tree.AssignImageList(imglist)

        root = tree.AddRoot("HyperTreeList :-D", image=0)

        items.append(tree.AppendItem(root, "Item 1", 0))
        items.append(tree.AppendItem(root, "Item 2", 0))
        items.append(tree.AppendItem(root, "Item 3", 0))
        items.append(tree.AppendItem(root, "Item 4", 0))
        items.append(tree.AppendItem(root, "Item 5", 0))

        for ii in range(len(items)):

            id = items[ii]
            tree.AppendItem(id, "Subitem 1", 1)
            tree.AppendItem(id, "Subitem 2", 1)
            tree.AppendItem(id, "Subitem 3", 1)
            tree.AppendItem(id, "Subitem 4", 1)
            tree.AppendItem(id, "Subitem 5", 1)

        tree.Expand(root)
        tree.Expand(items[1])
        tree.Expand(items[3])
        tree.SelectItem(root)

        return tree


    def BindEvents(self, choice, recreate=False):

        value = choice.GetValue()
        text = choice.GetLabel()

        evt = "wx." + text
        binder = self.eventdict[text]

        if value == 1:
            if evt == "wx.EVT_TREE_BEGIN_RDRAG":
                self.GetMainWindow().Bind(wx.EVT_RIGHT_DOWN, None)
                self.GetMainWindow().Bind(wx.EVT_RIGHT_UP, None)
            try:
                self.Bind(eval(evt), binder)
            except:
                self.Bind(eval("HTL." + text), binder)
        else:
            try:
                self.Bind(eval(evt), None)
            except:
                self.Bind(eval("HTL." + text), None)

            if evt == "wx.EVT_TREE_BEGIN_RDRAG":
                self.GetMainWindow().Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
                self.GetMainWindow().Bind(wx.EVT_RIGHT_UP, self.OnRightUp)


    def ChangeStyle(self, combos):

        style = 0
        for combo in combos:
            if combo.GetValue() == 1:
                if combo.GetLabel() == "TR_VIRTUAL":
                    style = style | HTL.TR_VIRTUAL
                else:
                    try:
                        style = style | eval("wx." + combo.GetLabel())
                    except:
                        style = style | eval("HTL." + combo.GetLabel())

        if self.GetAGWWindowStyleFlag() != style:
            self.SetAGWWindowStyleFlag(style)


    def OnCompareItems(self, item1, item2):

        t1 = self.GetItemText(item1)
        t2 = self.GetItemText(item2)

        self.log.write('compare: ' + t1 + ' <> ' + t2 + "\n")

        if t1 < t2:
            return -1
        if t1 == t2:
            return 0

        return 1


    def OnIdle(self, event):

        if self.gauge:

            try:
                if self.gauge.IsEnabled() and self.gauge.IsShown():
                    self.count = self.count + 1

                    if self.count >= 50:
                        self.count = 0

                    self.gauge.SetValue(self.count)

            except:

                self.gauge = None

        event.Skip()


    def OnRightDown(self, event):

        pt = event.GetPosition()
        item, flags, column = self.HitTest(pt)

        if item:
            self.item = item
            self.log.write("OnRightClick: %s, %s, %s\n" % (self.GetItemText(item), type(item), item.__class__))
            self.SelectItem(item)


    def OnRightUp(self, event):

        item = self.item

        if not item:
            event.Skip()
            return

        if not self.IsItemEnabled(item):
            event.Skip()
            return

        # Item Text Appearance
        ishtml = self.IsItemHyperText(item)
        back = self.GetItemBackgroundColour(item)
        fore = self.GetItemTextColour(item)
        isbold = self.IsBold(item)
        font = self.GetItemFont(item)

        # Icons On Item
        normal = self.GetItemImage(item, wx.TreeItemIcon_Normal)
        selected = self.GetItemImage(item, wx.TreeItemIcon_Selected)
        expanded = self.GetItemImage(item, wx.TreeItemIcon_Expanded)
        selexp = self.GetItemImage(item, wx.TreeItemIcon_SelectedExpanded)

        # Enabling/Disabling Windows Associated To An Item
        haswin = self.GetItemWindow(item)

        # Enabling/Disabling Items
        enabled = self.IsItemEnabled(item)

        # Generic Item's Info
        children = self.GetChildrenCount(item)
        itemtype = self.GetItemType(item)
        text = self.GetItemText(item)
        pydata = self.GetPyData(item)

        self.current = item
        self.itemdict = {"ishtml": ishtml, "back": back, "fore": fore, "isbold": isbold,
                         "font": font, "normal": normal, "selected": selected, "expanded": expanded,
                         "selexp": selexp, "haswin": haswin, "children": children,
                         "itemtype": itemtype, "text": text, "pydata": pydata, "enabled": enabled}

        menu = wx.Menu()

        item2 = menu.Append(wx.ID_ANY, "Modify Item Text Colour")
        menu.AppendSeparator()
        if isbold:
            strs = "Make Item Text Not Bold"
        else:
            strs = "Make Item Text Bold"
        item3 = menu.Append(wx.ID_ANY, strs)
        item4 = menu.Append(wx.ID_ANY, "Change Item Font")
        item13 = menu.Append(wx.ID_ANY, "Change Item Background Colour")
        menu.AppendSeparator()
        if ishtml:
            strs = "Set Item As Non-Hyperlink"
        else:
            strs = "Set Item As Hyperlink"
        item5 = menu.Append(wx.ID_ANY, strs)
        menu.AppendSeparator()

        item7 = menu.Append(wx.ID_ANY, "Disable Item")

        menu.AppendSeparator()
        item8 = menu.Append(wx.ID_ANY, "Change Item Icons")
        menu.AppendSeparator()
        item9 = menu.Append(wx.ID_ANY, "Get Other Information For This Item")
        menu.AppendSeparator()

        item10 = menu.Append(wx.ID_ANY, "Delete Item")
        if item == self.GetRootItem():
            item10.Enable(False)
        item11 = menu.Append(wx.ID_ANY, "Prepend An Item")
        item12 = menu.Append(wx.ID_ANY, "Append An Item")

        self.Bind(wx.EVT_MENU, self.OnItemForeground, item2)
        self.Bind(wx.EVT_MENU, self.OnItemBold, item3)
        self.Bind(wx.EVT_MENU, self.OnItemFont, item4)
        self.Bind(wx.EVT_MENU, self.OnItemHyperText, item5)
        self.Bind(wx.EVT_MENU, self.OnDisableItem, item7)
        self.Bind(wx.EVT_MENU, self.OnItemIcons, item8)
        self.Bind(wx.EVT_MENU, self.OnItemInfo, item9)
        self.Bind(wx.EVT_MENU, self.OnItemDelete, item10)
        self.Bind(wx.EVT_MENU, self.OnItemPrepend, item11)
        self.Bind(wx.EVT_MENU, self.OnItemAppend, item12)
        self.Bind(wx.EVT_MENU, self.OnItemBackground, item13)

        self.PopupMenu(menu)
        menu.Destroy()
        event.Skip()


    def OnItemForeground(self, event):

        colourdata = wx.ColourData()
        colourdata.SetColour(self.itemdict["fore"])
        dlg = wx.ColourDialog(self, colourdata)

        dlg.GetColourData().SetChooseFull(True)

        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetColourData()
            col1 = data.GetColour().Get()
            self.SetItemTextColour(self.current, col1)
        dlg.Destroy()
        event.Skip()


    def OnItemBold(self, event):

        self.SetItemBold(self.current, not self.itemdict["isbold"])
        event.Skip()


    def OnItemFont(self, event):

        data = wx.FontData()
        font = self.itemdict["font"]

        if font is None:
            font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)

        data.SetInitialFont(font)

        dlg = wx.FontDialog(self, data)

        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetFontData()
            font = data.GetChosenFont()
            self.SetItemFont(self.current, font)

        dlg.Destroy()
        event.Skip()


    def OnItemHyperText(self, event):

        self.SetItemHyperText(self.current, not self.itemdict["ishtml"])
        event.Skip()


    def OnDisableItem(self, event):

        self.EnableItem(self.current, False)
        event.Skip()


    def OnItemIcons(self, event):

        bitmaps = [self.itemdict["normal"], self.itemdict["selected"],
                   self.itemdict["expanded"], self.itemdict["selexp"]]

        wx.BeginBusyCursor()
        dlg = TreeIcons(self, -1, bitmaps=bitmaps)
        wx.EndBusyCursor()
        dlg.ShowModal()
        event.Skip()


    def SetNewIcons(self, bitmaps):

        self.SetItemImage(self.current, bitmaps[0], which=wx.TreeItemIcon_Normal)
        self.SetItemImage(self.current, bitmaps[1], which=wx.TreeItemIcon_Selected)
        self.SetItemImage(self.current, bitmaps[2], which=wx.TreeItemIcon_Expanded)
        self.SetItemImage(self.current, bitmaps[3], which=wx.TreeItemIcon_SelectedExpanded)


    def OnItemInfo(self, event):

        itemtext = self.itemdict["text"]
        numchildren = str(self.itemdict["children"])
        itemtype = self.itemdict["itemtype"]
        pydata = repr(type(self.itemdict["pydata"]))

        if itemtype == 0:
            itemtype = "Normal"
        elif itemtype == 1:
            itemtype = "CheckBox"
        else:
            itemtype = "RadioButton"

        strs = "Information On Selected Item:\n\n" + "Text: " + itemtext + "\n" \
               "Number Of Children: " + numchildren + "\n" \
               "Item Type: " + itemtype + "\n" \
               "Item Data Type: " + pydata + "\n"

        dlg = wx.MessageDialog(self, strs, "HyperTreeListDemo Info", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

        event.Skip()


    def OnItemDelete(self, event):

        strs = "Are You Sure You Want To Delete Item " + self.GetItemText(self.current) + "?"
        dlg = wx.MessageDialog(None, strs, 'Deleting Item', wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_QUESTION)

        if dlg.ShowModal() in [wx.ID_NO, wx.ID_CANCEL]:
            dlg.Destroy()
            return

        dlg.Destroy()

        self.DeleteChildren(self.current)
        self.Delete(self.current)
        self.current = None

        event.Skip()


    def OnItemPrepend(self, event):

        dlg = wx.TextEntryDialog(self, "Please Enter The New Item Name", 'Item Naming', 'Python')

        if dlg.ShowModal() == wx.ID_OK:
            newname = dlg.GetValue()
            newitem = self.PrependItem(self.current, newname)
            self.EnsureVisible(newitem)

        dlg.Destroy()
        event.Skip()


    def OnItemAppend(self, event):

        dlg = wx.TextEntryDialog(self, "Please Enter The New Item Name", 'Item Naming', 'Python')

        if dlg.ShowModal() == wx.ID_OK:
            newname = dlg.GetValue()
            newitem = self.AppendItem(self.current, newname)
            self.EnsureVisible(newitem)

        dlg.Destroy()
        event.Skip()


    def OnItemBackground(self, event):

        colourdata = wx.ColourData()
        colourdata.SetColour(self.itemdict["back"])
        dlg = wx.ColourDialog(self, colourdata)

        dlg.GetColourData().SetChooseFull(True)

        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetColourData()
            col1 = data.GetColour().Get()
            self.SetItemBackgroundColour(self.current, col1)

        dlg.Destroy()
        event.Skip()


    def OnBeginEdit(self, event):

        self.log.write("OnBeginEdit\n")
        # show how to prevent edit...
        item = event.GetItem()
        if item and self.GetItemText(item) == "The Root Item":
            wx.Bell()
            self.log.write("You can't edit this one...\n")

            # Lets just see what's visible of its children
            cookie = 0
            root = event.GetItem()
            (child, cookie) = self.GetFirstChild(root)

            while child:
                self.log.write("Child [%s] visible = %d\n" % (self.GetItemText(child), self.IsVisible(child)))
                (child, cookie) = self.GetNextChild(root, cookie)

            event.Veto()


    def OnEndEdit(self, event):

        self.log.write("OnEndEdit: %s %s\n" %(event.IsEditCancelled(), event.GetLabel()))
        # show how to reject edit, we'll not allow any digits
        for x in event.GetLabel():
            if x in string.digits:
                self.log.write("You can't enter digits...\n")
                event.Veto()
                return


    def OnLeftDClick(self, event):

        pt = event.GetPosition()
        item, flags, column = self.HitTest(pt)
        if item and (flags & wx.TREE_HITTEST_ONITEMLABEL):
            if self.GetAGWWindowStyleFlag() & wx.TR_EDIT_LABELS:
                self.log.write("OnLeftDClick: %s (manually starting label edit)\n"% self.GetItemText(item))
                self.EditLabel(item)
            else:
                self.log.write("OnLeftDClick: Cannot Start Manual Editing, Missing Style TR_EDIT_LABELS\n")

        event.Skip()


    def OnItemExpanded(self, event):

        item = event.GetItem()
        if item:
            self.log.write("OnItemExpanded: %s\n" % self.GetItemText(item))


    def OnItemExpanding(self, event):

        item = event.GetItem()
        if item:
            self.log.write("OnItemExpanding: %s\n" % self.GetItemText(item))

        event.Skip()


    def OnItemCollapsed(self, event):

        item = event.GetItem()
        if item:
            self.log.write("OnItemCollapsed: %s" % self.GetItemText(item))


    def OnItemCollapsing(self, event):

        item = event.GetItem()
        if item:
            self.log.write("OnItemCollapsing: %s\n" % self.GetItemText(item))

        event.Skip()


    def OnSelChanged(self, event):

        self.item = event.GetItem()
        if self.item:
            self.log.write("OnSelChanged: %s" % self.GetItemText(self.item))
            if wx.Platform == '__WXMSW__':
                self.log.write(", BoundingRect: %s\n" % self.GetBoundingRect(self.item, True))
            else:
                self.log.write("\n")

        event.Skip()


    def OnSelChanging(self, event):

        item = event.GetItem()
        olditem = event.GetOldItem()

        if item:
            if not olditem:
                olditemtext = "None"
            else:
                olditemtext = self.GetItemText(olditem)
            self.log.write("OnSelChanging: From %s To %s\n" %(olditemtext, self.GetItemText(item)))

        event.Skip()


    def OnBeginDrag(self, event):

        self.item = event.GetItem()
        if self.item:
            self.log.write("Beginning Drag...\n")

            event.Allow()


    def OnBeginRDrag(self, event):

        self.item = event.GetItem()
        if self.item:
            self.log.write("Beginning Right Drag...\n")

            event.Allow()


    def OnEndDrag(self, event):

        self.item = event.GetItem()
        if self.item:
            self.log.write("Ending Drag!\n")

        event.Skip()


    def OnDeleteItem(self, event):

        item = event.GetItem()

        if not item:
            return

        self.log.write("Deleting Item: %s\n" % self.GetItemText(item))
        event.Skip()


    def OnItemCheck(self, event):

        item = event.GetItem()
        self.log.write("Item " + self.GetItemText(item) + " Has Been Cheched!\n")
        event.Skip()


    def OnItemChecking(self, event):

        item = event.GetItem()
        self.log.write("Item " + self.GetItemText(item) + " Is Being Checked...\n")
        event.Skip()


    def OnToolTip(self, event):

        item = event.GetItem()
        if item:
            event.SetToolTip(wx.ToolTip(self.GetItemText(item)))


    def OnItemMenu(self, event):

        item = event.GetItem()
        if item:
            self.log.write("OnItemMenu: %s\n" % self.GetItemText(item))

        event.Skip()


    def OnKey(self, event):

        keycode = event.GetKeyCode()
        keyname = keyMap.get(keycode, None)

        if keycode == wx.WXK_BACK:
            self.log.write("OnKeyDown: HAHAHAHA! I Vetoed Your Backspace! HAHAHAHA\n")
            return

        if keyname is None:
            if "unicode" in wx.PlatformInfo:
                keycode = event.GetUnicodeKey()
                if keycode <= 127:
                    keycode = event.GetKeyCode()
                keyname = "\"" + unichr(event.GetUnicodeKey()) + "\""
                if keycode < 27:
                    keyname = "Ctrl-%s" % chr(ord('A') + keycode-1)

            elif keycode < 256:
                if keycode == 0:
                    keyname = "NUL"
                elif keycode < 27:
                    keyname = "Ctrl-%s" % chr(ord('A') + keycode-1)
                else:
                    keyname = "\"%s\"" % chr(keycode)
            else:
                keyname = "unknown (%s)" % keycode

        self.log.write("OnKeyDown: You Pressed '" + keyname + "'\n")

        event.Skip()


    def OnActivate(self, event):

        if self.item:
            self.log.write("OnActivate: %s\n" % self.GetItemText(self.item))

        event.Skip()


    def OnHyperLink(self, event):

        item = event.GetItem()
        if item:
            self.log.write("OnHyperLink: %s\n" % self.GetItemText(self.item))


    def OnTextCtrl(self, event):

        char = chr(event.GetKeyCode())
        self.log.write("EDITING THE TEXTCTRL: You Wrote '" + char + \
                       "' (KeyCode = " + str(event.GetKeyCode()) + ")\n")
        event.Skip()


    def OnComboBox(self, event):

        selection = event.GetEventObject().GetValue()
        self.log.write("CHOICE FROM COMBOBOX: You Chose '" + selection + "'\n")
        event.Skip()


#---------------------------------------------------------------------------


class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        b = wx.Button(self, -1, " Test HyperTreeList ", (50,50))
        self.Bind(wx.EVT_BUTTON, self.OnButton, b)


    def OnButton(self, evt):
        self.win = HyperTreeListDemo(self, self.log)
        self.win.Show(True)

#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------


overview = HTL.__doc__


if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

