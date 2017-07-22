#----------------------------------------------------------------------
# Name:        wx.lib.dialogs
# Purpose:     ScrolledMessageDialog, MultipleChoiceDialog and
#              function wrappers for the common dialogs by Kevin Altis.
#
# Author:      Various
#
# Created:     3-January-2002
# Copyright:   (c) 2002-2017 by Total Control Software
# Licence:     wxWindows license
# Tags:        phoenix-port
#----------------------------------------------------------------------
# 12/01/2003 - Jeff Grimmett (grimmtooth@softhome.net)
#
# o Updated for 2.5 compatibility.
#
# 12/18/2003 - Jeff Grimmett (grimmtooth@softhome.net)
#
# o wxScrolledMessageDialog -> ScrolledMessageDialog
# o wxMultipleChoiceDialog -> MultipleChoiceDialog
#

import  wx
import  wx.lib.layoutf as layoutf

#----------------------------------------------------------------------

class ScrolledMessageDialog(wx.Dialog):
    def __init__(self, parent, msg, caption,
                 pos=wx.DefaultPosition, size=(500,300),
                 style=wx.DEFAULT_DIALOG_STYLE):
        wx.Dialog.__init__(self, parent, -1, caption, pos, size, style)
        x, y = pos
        if x == -1 and y == -1:
            self.CenterOnScreen(wx.BOTH)

        self.text = text = wx.TextCtrl(self, -1, msg,
                                       style=wx.TE_MULTILINE | wx.TE_READONLY)

        ok = wx.Button(self, wx.ID_OK, "OK")
        ok.SetDefault()
        lc = layoutf.Layoutf('t=t5#1;b=t5#2;l=l5#1;r=r5#1', (self,ok))
        text.SetConstraints(lc)

        lc = layoutf.Layoutf('b=b5#1;x%w50#1;w!80;h*', (self,))
        ok.SetConstraints(lc)
        self.SetAutoLayout(1)
        self.Layout()


class MultipleChoiceDialog(wx.Dialog):
    def __init__(self, parent, msg, title, lst, pos = wx.DefaultPosition,
                 size = (200,200), style = wx.DEFAULT_DIALOG_STYLE):
        wx.Dialog.__init__(self, parent, -1, title, pos, size, style)

        x, y = pos
        if x == -1 and y == -1:
            self.CenterOnScreen(wx.BOTH)

        stat = wx.StaticText(self, -1, msg)
        self.lbox = wx.ListBox(self, 100, wx.DefaultPosition, wx.DefaultSize,
                               lst, wx.LB_MULTIPLE)

        ok = wx.Button(self, wx.ID_OK, "OK")
        ok.SetDefault()
        cancel = wx.Button(self, wx.ID_CANCEL, "Cancel")

        dlgsizer = wx.BoxSizer(wx.VERTICAL)
        dlgsizer.Add(stat, 0, wx.ALL, 4)
        dlgsizer.Add(self.lbox, 1, wx.EXPAND | wx.ALL, 4)

        btnsizer = wx.StdDialogButtonSizer()
        btnsizer.AddButton(ok)
        btnsizer.AddButton(cancel)
        btnsizer.Realize()

        dlgsizer.Add(btnsizer, 0, wx.ALL | wx.ALIGN_RIGHT, 4)

        self.SetSizer(dlgsizer)

        self.lst = lst
        self.Layout()

    def GetValue(self):
        return self.lbox.GetSelections()

    def GetValueString(self):
        sel = self.lbox.GetSelections()
        val = [ self.lst[i] for i in sel ]
        return tuple(val)


#----------------------------------------------------------------------
"""
function wrappers for wxPython system dialogs
Author: Kevin Altis
Date:   2003-1-2
Rev:    3

This is the third refactor of the PythonCard dialog.py module
for inclusion in the main wxPython distribution. There are a number of
design decisions and subsequent code refactoring to be done, so I'm
releasing this just to get some feedback.

rev 3:
- result dictionary replaced by DialogResults class instance
- should message arg be replaced with msg? most wxWindows dialogs
  seem to use the abbreviation?

rev 2:
- All dialog classes have been replaced by function wrappers
- Changed arg lists to more closely match wxWindows docs and wx.lib.dialogs
- changed 'returned' value to the actual button id the user clicked on
- added a returnedString value for the string version of the return value
- reworked colorDialog and fontDialog so you can pass in just a color or font
    for the most common usage case
- probably need to use colour instead of color to match the English English
    spelling in wxWindows (sigh)
- I still think we could lose the parent arg and just always use None
"""

class DialogResults:
    def __init__(self, returned):
        self.returned = returned
        self.accepted = returned in (wx.ID_OK, wx.ID_YES)
        self.returnedString = returnedString(returned)

    def __repr__(self):
        return str(self.__dict__)

def returnedString(ret):
    if ret == wx.ID_OK:
        return "Ok"
    elif ret == wx.ID_CANCEL:
        return "Cancel"
    elif ret == wx.ID_YES:
        return "Yes"
    elif ret == wx.ID_NO:
        return "No"


## findDialog was created before wxPython got a Find/Replace dialog
## but it may be instructive as to how a function wrapper can
## be added for your own custom dialogs
## this dialog is always modal, while wxFindReplaceDialog is
## modeless and so doesn't lend itself to a function wrapper
def findDialog(parent=None, searchText='', wholeWordsOnly=0, caseSensitive=0):
    dlg = wx.Dialog(parent, -1, "Find", wx.DefaultPosition, (380, 120))

    wx.StaticText(dlg, -1, 'Find what:', (7, 10))
    wSearchText = wx.TextCtrl(dlg, -1, searchText, (80, 7), (195, -1))
    wSearchText.SetValue(searchText)
    wx.Button(dlg, wx.ID_OK, "Find Next", (285, 5), wx.DefaultSize).SetDefault()
    wx.Button(dlg, wx.ID_CANCEL, "Cancel", (285, 35), wx.DefaultSize)

    wWholeWord = wx.CheckBox(dlg, -1, 'Match whole word only',
                            (7, 35), wx.DefaultSize, wx.NO_BORDER)

    if wholeWordsOnly:
        wWholeWord.SetValue(1)

    wCase = wx.CheckBox(dlg, -1, 'Match case', (7, 55), wx.DefaultSize, wx.NO_BORDER)

    if caseSensitive:
        wCase.SetValue(1)

    wSearchText.SetSelection(0, len(wSearchText.GetValue()))
    wSearchText.SetFocus()

    result = DialogResults(dlg.ShowModal())
    result.searchText = wSearchText.GetValue()
    result.wholeWordsOnly = wWholeWord.GetValue()
    result.caseSensitive = wCase.GetValue()
    dlg.Destroy()
    return result


def colorDialog(parent=None, colorData=None, color=None):
    if colorData:
        dialog = wx.ColourDialog(parent, colorData)
    else:
        dialog = wx.ColourDialog(parent)
        dialog.GetColourData().SetChooseFull(1)

    if color is not None:
        dialog.GetColourData().SetColour(color)

    result = DialogResults(dialog.ShowModal())
    result.colorData = dialog.GetColourData()
    result.color = result.colorData.GetColour().Get()
    dialog.Destroy()
    return result


## it is easier to just duplicate the code than
## try and replace color with colour in the result
def colourDialog(parent=None, colourData=None, colour=None):
    if colourData:
        dialog = wx.ColourDialog(parent, colourData)
    else:
        dialog = wx.ColourDialog(parent)
        dialog.GetColourData().SetChooseFull(1)

    if colour is not None:
        dialog.GetColourData().SetColour(color)

    result = DialogResults(dialog.ShowModal())
    result.colourData = dialog.GetColourData()
    result.colour = result.colourData.GetColour().Get()
    dialog.Destroy()
    return result


def fontDialog(parent=None, fontData=None, font=None):
    if fontData is None:
        fontData = wx.FontData()
        fontData.SetColour(wx.BLACK)
        fontData.SetInitialFont(wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT))

    if font is not None:
        fontData.SetInitialFont(font)

    dialog = wx.FontDialog(parent, fontData)
    result = DialogResults(dialog.ShowModal())

    if result.accepted:
        fontData = dialog.GetFontData()
        result.fontData = fontData
        result.color = fontData.GetColour().Get()
        result.colour = result.color
        result.font = fontData.GetChosenFont()
    else:
        result.color = None
        result.colour = None
        result.font = None

    dialog.Destroy()
    return result


def textEntryDialog(parent=None, message='', title='', defaultText='',
                    style=wx.OK | wx.CANCEL):
    dialog = wx.TextEntryDialog(parent, message, title, defaultText, style)
    result = DialogResults(dialog.ShowModal())
    result.text = dialog.GetValue()
    dialog.Destroy()
    return result


def messageDialog(parent=None, message='', title='Message box',
                  aStyle = wx.OK | wx.CANCEL | wx.CENTRE,
                  pos=wx.DefaultPosition):
    dialog = wx.MessageDialog(parent, message, title, aStyle, pos)
    result = DialogResults(dialog.ShowModal())
    dialog.Destroy()
    return result


## KEA: alerts are common, so I'm providing a class rather than
## requiring the user code to set up the right icons and buttons
## the with messageDialog function
def alertDialog(parent=None, message='', title='Alert', pos=wx.DefaultPosition):
    return messageDialog(parent, message, title, wx.ICON_EXCLAMATION | wx.OK, pos)


def scrolledMessageDialog(parent=None, message='', title='', pos=wx.DefaultPosition,
                          size=(500,300)):

    dialog = ScrolledMessageDialog(parent, message, title, pos, size)
    result = DialogResults(dialog.ShowModal())
    dialog.Destroy()
    return result


def fileDialog(parent=None, title='Open', directory='', filename='', wildcard='*.*',
               style=wx.FD_OPEN | wx.FD_MULTIPLE):

    dialog = wx.FileDialog(parent, title, directory, filename, wildcard, style)
    result = DialogResults(dialog.ShowModal())
    if result.accepted:
        result.paths = dialog.GetPaths()
    else:
        result.paths = None
    dialog.Destroy()
    return result


## openFileDialog and saveFileDialog are convenience functions
## they represent the most common usages of the fileDialog
## with the most common style options
def openFileDialog(parent=None, title='Open', directory='', filename='',
                   wildcard='All Files (*.*)|*.*',
                   style=wx.FD_OPEN | wx.FD_MULTIPLE):
    return fileDialog(parent, title, directory, filename, wildcard, style)


def saveFileDialog(parent=None, title='Save', directory='', filename='',
                   wildcard='All Files (*.*)|*.*',
                   style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT):
    return fileDialog(parent, title, directory, filename, wildcard, style)


def dirDialog(parent=None, message='Choose a directory', path='', style=0,
              pos=wx.DefaultPosition, size=wx.DefaultSize):

    dialog = wx.DirDialog(parent, message, path, style, pos, size)
    result = DialogResults(dialog.ShowModal())
    if result.accepted:
        result.path = dialog.GetPath()
    else:
        result.path = None
    dialog.Destroy()
    return result

directoryDialog = dirDialog


def singleChoiceDialog(parent=None, message='', title='', lst=[],
                       style=wx.OK | wx.CANCEL | wx.CENTRE):
    dialog = wx.SingleChoiceDialog(parent, message, title, list(lst), style | wx.DEFAULT_DIALOG_STYLE)
    result = DialogResults(dialog.ShowModal())
    result.selection = dialog.GetStringSelection()
    dialog.Destroy()
    return result


def multipleChoiceDialog(parent=None, message='', title='', lst=[],
                         pos=wx.DefaultPosition, size=wx.DefaultSize):

    dialog = wx.MultiChoiceDialog(parent, message, title, lst,
                                  wx.CHOICEDLG_STYLE, pos)
    result = DialogResults(dialog.ShowModal())
    result.selection = tuple([lst[i] for i in dialog.GetSelections()])
    dialog.Destroy()
    return result



#---------------------------------------------------------------------------

try:
    wx.CANCEL_DEFAULT
    wx.OK_DEFAULT
except AttributeError:
    wx.CANCEL_DEFAULT = 0
    wx.OK_DEFAULT = 0



class MultiMessageDialog(wx.Dialog):
    """
    A dialog like :class:`wx.MessageDialog`, but with an optional 2nd message string
    that is shown in a scrolled window, and also allows passing in the icon to
    be shown instead of the stock error, question, etc. icons. The btnLabels
    can be used if you'd like to change the stock labels on the buttons, it's
    a dictionary mapping stock IDs to label strings.
    """
    CONTENT_MAX_W = 550
    CONTENT_MAX_H = 350

    def __init__(self, parent, message, caption = "Message Box", msg2="",
                 style = wx.OK | wx.CANCEL, pos = wx.DefaultPosition, icon=None,
                 btnLabels=None):
        if 'wxMac' not in wx.PlatformInfo:
            title = caption  # the caption will be displayed inside the dialog on Macs
        else:
            title = ""

        wx.Dialog.__init__(self, parent, -1, title, pos,
                           style = wx.DEFAULT_DIALOG_STYLE | style & (wx.STAY_ON_TOP | wx.DIALOG_NO_PARENT))

        bitmap = None
        isize = (32,32)

        # was an icon passed to us?
        if icon is not None:
            if isinstance(icon, wx.Icon):
                bitmap = wx.Bitmap()
                bitmap.CopyFromIcon(icon)
            elif isinstance(icon, wx.Image):
                bitmap = wx.Bitmap(icon)
            else:
                assert isinstance(icon, wx.Bitmap)
                bitmap = icon

        else:
            # check for icons in the style flags
            artid = None
            if style & wx.ICON_ERROR or style & wx.ICON_HAND:
                artid = wx.ART_ERROR
            elif style & wx.ICON_EXCLAMATION:
                artid = wx.ART_WARNING
            elif style & wx.ICON_QUESTION:
                artid = wx.ART_QUESTION
            elif style & wx.ICON_INFORMATION:
                artid = wx.ART_INFORMATION

            if artid is not None:
                bitmap = wx.ArtProvider.GetBitmap(artid, wx.ART_MESSAGE_BOX, isize)

        if bitmap:
            bitmap = wx.StaticBitmap(self, -1, bitmap)
        else:
            bitmap = isize # will be a spacer when added to the sizer

        # Sizer to contain the icon, text area and buttons
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(bitmap, 0, wx.TOP|wx.LEFT, 12)
        sizer.Add((10,10))

        # Make the text area
        messageSizer = wx.BoxSizer(wx.VERTICAL)
        if 'wxMac' in wx.PlatformInfo and caption:
            caption = wx.StaticText(self, -1, caption)
            caption.SetFont(wx.Font(18, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
            messageSizer.Add(caption)
            messageSizer.Add((10,10))

        stext = wx.StaticText(self, -1, message)
        #stext.SetLabelMarkup(message)  Wrap() causes all markup to be lost, so don't try to use it yet...
        stext.Wrap(self.CONTENT_MAX_W)
        messageSizer.Add(stext)

        if msg2:
            messageSizer.Add((15,15))
            t = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_RICH|wx.TE_DONTWRAP)
            t.SetValue(msg2)

            # Set size to be used by the sizer based on the message content,
            # with good maximums
            dc = wx.ClientDC(t)
            dc.SetFont(t.GetFont())
            w,h,_ = dc.GetFullMultiLineTextExtent(msg2)
            w = min(self.CONTENT_MAX_W, 10 + w + wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X))
            h = min(self.CONTENT_MAX_H, 10 + h)
            t.SetMinSize((w,h))
            messageSizer.Add(t, 0, wx.EXPAND)

        # Make the buttons
        buttonSizer = self.CreateStdDialogButtonSizer(
            style & (wx.OK | wx.CANCEL | wx.YES_NO | wx.NO_DEFAULT
                     | wx.CANCEL_DEFAULT | wx.YES_DEFAULT | wx.OK_DEFAULT
                     ))
        self.Bind(wx.EVT_BUTTON, self.OnButton)
        if btnLabels:
            for sid, label in btnLabels.iteritems():
                btn = self.FindWindow(sid)
                if btn:
                    btn.SetLabel(label)
        messageSizer.Add(wx.Size(1, 15))
        messageSizer.Add(buttonSizer, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 12)

        sizer.Add(messageSizer, 0, wx.LEFT | wx.RIGHT | wx.TOP, 12)
        self.SetSizer(sizer)
        self.Fit()
        if parent:
            self.CenterOnParent()
        else:
            self.CenterOnScreen()

        for c in self.Children:
            if isinstance(c, wx.Button):
                wx.CallAfter(c.SetFocus)
                break


    def OnButton(self, evt):
        if self.IsModal():
            self.EndModal(evt.EventObject.Id)
        else:
            self.Close()




def MultiMessageBox(message, caption, msg2="", style=wx.OK, parent=None,
                    icon=None, btnLabels=None):
    """
    A function like :class:`wx.MessageBox` which uses :class:`MultiMessageDialog`.
    """
    #if not style & wx.ICON_NONE and not style & wx.ICON_MASK:
    if not style & wx.ICON_MASK:
        if style & wx.YES:
            style |= wx.ICON_QUESTION
        else:
            style |= wx.ICON_INFORMATION

    dlg = MultiMessageDialog(parent, message, caption, msg2, style,
                             icon=icon, btnLabels=btnLabels)
    ans = dlg.ShowModal()
    dlg.Destroy()

    if ans == wx.ID_OK:
        return wx.OK
    elif ans == wx.ID_YES:
        return wx.YES
    elif ans == wx.ID_NO:
        return wx.NO
    elif ans == wx.ID_CANCEL:
        return wx.CANCEL

    print("unexpected return code from MultiMessageDialog??")
    return wx.CANCEL


#---------------------------------------------------------------------------

if __name__ == '__main__':
    app = wx.App()
    MultiMessageBox("Hello World", "howdy", "This is a MultiMessageBox \ntest. With a multi-line message.")
    app.MainLoop()
