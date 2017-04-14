#!/usr/bin/env python

import wx
import wx.lib.colourselect as csel
import random

import os
import sys

try:
    dirName = os.path.dirname(os.path.abspath(__file__))
except:
    dirName = os.path.dirname(os.path.abspath(sys.argv[0]))

bitmapDir = os.path.join(dirName, 'bitmaps')
sys.path.append(os.path.split(dirName)[0])

try:
    from agw import labelbook as LB
    from agw.fmresources import *
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.labelbook as LB
    from wx.lib.agw.fmresources import *

import images

_pageTexts = ["Hello", "From", "wxPython", "LabelBook", "Demo"]
_pageIcons = ["roll.png", "charge.png", "add.png", "decrypted.png", "news.png"]
_pageColours = [wx.RED, wx.GREEN, wx.WHITE, wx.BLUE, "Pink"]

#----------------------------------------------------------------------
class SamplePane(wx.Panel):
    """
    Just a simple test window to put into the LabelBook.
    """
    def __init__(self, parent, colour, label):

        wx.Panel.__init__(self, parent, style=0)#wx.BORDER_SUNKEN)
        self.SetBackgroundColour(wx.Colour(255,255,255))

        label = label + "\nEnjoy the LabelBook && FlatImageBook demo!"
        static = wx.StaticText(self, -1, label, pos=(10, 10))

#----------------------------------------------------------------------

class LabelBookDemo(wx.Frame):

    def __init__(self, parent, log):

        wx.Frame.__init__(self, parent)

        self.initializing = True
        self.book = None
        self._oldTextSize = 1.0

        self.log = log

        self.splitter = wx.SplitterWindow(self, -1, style=wx.SP_3D|wx.SP_BORDER|
                                          wx.SP_LIVE_UPDATE|wx.SP_3DSASH)
        self.mainpanel = wx.Panel(self.splitter, -1)
        self.leftpanel = wx.Panel(self.splitter, -1, style=0)#wx.SUNKEN_BORDER)

        self.sizer_3_staticbox = wx.StaticBox(self.leftpanel, -1, "Book Styles")
        self.sizer_4_staticbox = wx.StaticBox(self.leftpanel, -1, "Colours")

        radioList = ["LabelBook", "FlatImageBook"]
        self.labelbook = wx.RadioBox(self.leftpanel, -1, "Book Type", wx.DefaultPosition,
                                     wx.DefaultSize, radioList, 2, wx.RA_SPECIFY_ROWS)

        radioList = ["Left", "Right", "Top", "Bottom"]
        self.bookdirection = wx.RadioBox(self.leftpanel, -1, "Book Orientation",
                                         wx.DefaultPosition, wx.DefaultSize, radioList,
                                         2, wx.RA_SPECIFY_ROWS)

        self.border = wx.CheckBox(self.leftpanel, -1, "Draw Book Border")
        self.onlytext = wx.CheckBox(self.leftpanel, -1, "Show Only Text")
        self.onlyimages = wx.CheckBox(self.leftpanel, -1, "Show Only Images")
        self.shadow = wx.CheckBox(self.leftpanel, -1, "Draw Shadows")
        self.pin = wx.CheckBox(self.leftpanel, -1, "Use Pin Button")
        self.gradient = wx.CheckBox(self.leftpanel, -1, "Draw Gradient Shading")
        self.web = wx.CheckBox(self.leftpanel, -1, "Web Highlight")
        self.fittext = wx.CheckBox(self.leftpanel, -1, "Fit Label Text")
        self.boldtext = wx.CheckBox(self.leftpanel, -1, "Bold Label Text")
        self.boldselection = wx.CheckBox(self.leftpanel, -1, "Bold Selected Tab")

        self.textsize = wx.TextCtrl(self.leftpanel, -1, "1.0",style=wx.TE_PROCESS_ENTER)
        self.background = csel.ColourSelect(self.leftpanel, -1, "Choose...",
                                            wx.Colour(132, 164, 213), size=(-1, 20))
        self.activetab = csel.ColourSelect(self.leftpanel, -1, "Choose...",
                                           wx.Colour(255, 255, 255), size=(-1, 20))
        self.tabsborder = csel.ColourSelect(self.leftpanel, -1, "Choose...",
                                            wx.Colour(0, 0, 204), size=(-1, 20))
        self.textcolour = csel.ColourSelect(self.leftpanel, -1, "Choose...",
                                            wx.BLACK, size=(-1, 20))
        self.activetextcolour = csel.ColourSelect(self.leftpanel, -1, "Choose...",
                                                  wx.BLACK, size=(-1, 20))
        self.hilite = csel.ColourSelect(self.leftpanel, -1, "Choose...",
                                        wx.Colour(191, 216, 216), size=(-1, 20))

        self.SetProperties()
        self.CreateLabelBook()
        self.DoLayout()

        self.Bind(wx.EVT_RADIOBOX, self.OnBookType, self.labelbook)
        self.Bind(wx.EVT_RADIOBOX, self.OnBookOrientation, self.bookdirection)

        self.Bind(wx.EVT_CHECKBOX, self.OnStyle, self.border)
        self.Bind(wx.EVT_CHECKBOX, self.OnStyle, self.onlytext)
        self.Bind(wx.EVT_CHECKBOX, self.OnStyle, self.onlyimages)
        self.Bind(wx.EVT_CHECKBOX, self.OnStyle, self.shadow)
        self.Bind(wx.EVT_CHECKBOX, self.OnStyle, self.pin)
        self.Bind(wx.EVT_CHECKBOX, self.OnStyle, self.gradient)
        self.Bind(wx.EVT_CHECKBOX, self.OnStyle, self.web)
        self.Bind(wx.EVT_CHECKBOX, self.OnStyle, self.fittext)
        self.Bind(wx.EVT_CHECKBOX, self.OnStyle, self.boldtext)
        self.Bind(wx.EVT_CHECKBOX, self.OnStyle, self.boldselection)
        self.Bind(wx.EVT_TEXT_ENTER,    self.OnStyle, self.textsize)

        self.Bind(csel.EVT_COLOURSELECT, self.OnBookColours, self.background)
        self.Bind(csel.EVT_COLOURSELECT, self.OnBookColours, self.activetab)
        self.Bind(csel.EVT_COLOURSELECT, self.OnBookColours, self.activetextcolour)
        self.Bind(csel.EVT_COLOURSELECT, self.OnBookColours, self.tabsborder)
        self.Bind(csel.EVT_COLOURSELECT, self.OnBookColours, self.textcolour)
        self.Bind(csel.EVT_COLOURSELECT, self.OnBookColours, self.hilite)

        self.Bind(LB.EVT_IMAGENOTEBOOK_PAGE_CHANGING, self.OnPageChanging)
        self.Bind(LB.EVT_IMAGENOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(LB.EVT_IMAGENOTEBOOK_PAGE_CLOSING, self.OnPageClosing)
        self.Bind(LB.EVT_IMAGENOTEBOOK_PAGE_CLOSED, self.OnPageClosed)


        statusbar = self.CreateStatusBar(2)
        statusbar.SetStatusWidths([-2, -1])
        # statusbar fields
        statusbar_fields = [("LabelBook & FlatImageBook wxPython Demo, Andrea Gavana @ 03 Nov 2006"),
                            ("Welcome To wxPython!")]

        for i in range(len(statusbar_fields)):
            statusbar.SetStatusText(statusbar_fields[i], i)

        self.CreateMenu()

        self.SetSize((800,700))

        self.SetIcon(images.Mondrian.GetIcon())
        self.CenterOnScreen()

        self.initializing = False
        self.SendSizeEvent()


    def SetProperties(self):

        self.SetTitle("LabelBook & FlatImageBook wxPython Demo ;-)")
        self.splitter.SetMinimumPaneSize(120)
        self.pin.SetValue(0)
        self.fittext.SetValue(1)
        self.border.SetValue(1)
        self.onlytext.SetValue(1)


    def DoLayout(self):

        mainsizer = wx.BoxSizer(wx.VERTICAL)
        panelsizer = wx.BoxSizer(wx.VERTICAL)
        leftsizer = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.StaticBoxSizer(self.sizer_3_staticbox, wx.VERTICAL)
        sizer_4 = wx.StaticBoxSizer(self.sizer_4_staticbox, wx.VERTICAL)
        gridsizer = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)

        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(self.labelbook, 0, wx.ALL, 3)
        leftsizer.Add(sizer_1, 0, wx.ALL|wx.EXPAND, 5)
        sizer_2.Add(self.bookdirection, 0, wx.ALL, 3)
        leftsizer.Add(sizer_2, 0, wx.ALL|wx.EXPAND, 5)

        sizer_3.Add(self.border, 0, wx.ALL, 3)
        sizer_3.Add(self.onlytext, 0, wx.LEFT|wx.BOTTOM, 3)
        sizer_3.Add(self.onlyimages, 0, wx.LEFT|wx.BOTTOM, 3)
        sizer_3.Add(self.shadow, 0, wx.LEFT|wx.BOTTOM, 3)
        sizer_3.Add(self.pin, 0, wx.LEFT|wx.BOTTOM, 3)
        sizer_3.Add(self.gradient, 0, wx.LEFT|wx.BOTTOM, 3)
        sizer_3.Add(self.web, 0, wx.LEFT|wx.BOTTOM, 3)
        sizer_3.Add(self.fittext, 0, wx.LEFT|wx.BOTTOM, 3)
        sizer_3.Add(self.boldtext, 0, wx.LEFT|wx.BOTTOM, 3)
        sizer_3.Add(self.boldselection, 0, wx.LEFT|wx.BOTTOM, 3)
        leftsizer.Add(sizer_3, 0, wx.ALL|wx.EXPAND, 5)

        lbl = wx.StaticText(self.leftpanel, -1, "Text Font Multiple: ")
        label1 = wx.StaticText(self.leftpanel, -1, "Tab Area Background Colour: ")
        label2 = wx.StaticText(self.leftpanel, -1, "Active Tab Colour: ")
        label3 = wx.StaticText(self.leftpanel, -1, "Tabs Border Colour: ")
        label4 = wx.StaticText(self.leftpanel, -1, "Text Colour: ")
        label5 = wx.StaticText(self.leftpanel, -1, "Active Tab Text Colour: ")
        label6 = wx.StaticText(self.leftpanel, -1, "Tab Highlight Colour: ")

        gridsizer.Add(lbl, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 3)
        gridsizer.Add(self.textsize, 0)
        gridsizer.Add(label1, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 3)
        gridsizer.Add(self.background, 0)
        gridsizer.Add(label2, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 3)
        gridsizer.Add(self.activetab, 0)
        gridsizer.Add(label3, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 3)
        gridsizer.Add(self.tabsborder, 0)
        gridsizer.Add(label4, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 3)
        gridsizer.Add(self.textcolour, 0)
        gridsizer.Add(label5, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 3)
        gridsizer.Add(self.activetextcolour, 0)
        gridsizer.Add(label6, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 3)
        gridsizer.Add(self.hilite, 0)

        sizer_4.Add(gridsizer, 1, wx.EXPAND)
        gridsizer.Layout()
        leftsizer.Add(sizer_4, 0, wx.ALL|wx.EXPAND, 5)

        self.leftpanel.SetSizer(leftsizer)
        leftsizer.Layout()
        leftsizer.SetSizeHints(self.leftpanel)
        leftsizer.Fit(self.leftpanel)

        panelsizer.Add(self.book, 1, wx.EXPAND, 0)
        self.mainpanel.SetSizer(panelsizer)
        panelsizer.Layout()

        self.splitter.SplitVertically(self.leftpanel, self.mainpanel, 200)
        mainsizer.Add(self.splitter, 1, wx.EXPAND, 0)

        self.SetSizer(mainsizer)
        mainsizer.Layout()
        self.Layout()


    def CreateLabelBook(self, btype=0):

        if not self.initializing:
            self.Freeze()
            panelsizer = self.mainpanel.GetSizer()
            panelsizer.Detach(0)
            self.book.Destroy()
        else:
            self.imagelist = self.CreateImageList()

        self.EnableChoices(btype)
        style = self.GetBookStyles()

        if btype == 0: # it is a labelbook:
            self.book = LB.LabelBook(self.mainpanel, -1, agwStyle=style)
            if self.bookdirection.GetSelection() > 1:
                self.bookdirection.SetSelection(0)

            self.SetUserColours()
            self.book.SetFontSizeMultiple(1.0)
            self.book.SetFontBold(False)

        else:
            self.book = LB.FlatImageBook(self.mainpanel, -1, agwStyle=style)

        self.book.AssignImageList(self.imagelist)

        for indx, txts in enumerate(_pageTexts):
            label = "This is panel number %d"%(indx+1)
            self.book.AddPage(SamplePane(self.book, _pageColours[indx], label),
                              txts, True, indx)

        self.book.SetSelection(0)

        if not self.initializing:
            panelsizer.Add(self.book, 1, wx.EXPAND)
            panelsizer.Layout()
            self.GetSizer().Layout()
            self.Layout()
            self.Thaw()

        self.SendSizeEvent()
        #wx.CallAfter(self.book.SetAGWWindowStyleFlag, style)


    def EnableChoices(self, btype):

        self.bookdirection.EnableItem(2, btype)
        self.bookdirection.EnableItem(3, btype)
        self.onlyimages.Enable()
        self.onlytext.Enable()
        self.gradient.Enable(not btype)
        self.web.Enable(not btype)
        self.shadow.Enable(not btype)
        self.background.Enable(not btype)
        self.activetab.Enable(not btype)
        self.activetextcolour.Enable(not btype)
        self.textcolour.Enable(not btype)
        self.hilite.Enable(not btype)
        self.tabsborder.Enable(not btype)
        self.fittext.Enable(not btype)
        self.boldtext.Enable(not btype)


    def GetBookStyles(self):

        style = INB_FIT_BUTTON
        style = self.GetBookOrientation(style)

        if self.onlytext.IsEnabled() and self.onlytext.GetValue():
            style |= INB_SHOW_ONLY_TEXT
        if self.onlyimages.IsEnabled() and self.onlyimages.GetValue():
            style |= INB_SHOW_ONLY_IMAGES
        if self.pin.GetValue():
            style |= INB_USE_PIN_BUTTON
        if self.shadow.GetValue():
            style |= INB_DRAW_SHADOW
        if self.web.GetValue():
            style |= INB_WEB_HILITE
        if self.gradient.GetValue():
            style |= INB_GRADIENT_BACKGROUND
        if self.border.GetValue():
            style |= INB_BORDER
        if self.fittext.IsEnabled() and self.fittext.GetValue():
            style |= INB_FIT_LABELTEXT
        if self.boldselection.IsEnabled() and self.boldselection.GetValue():
            style |= INB_BOLD_TAB_SELECTION

        if self.book:
            self.book.SetFontBold(self.boldtext.GetValue())

        return style


    def CreateImageList(self):

        imagelist = wx.ImageList(32, 32)
        for img in _pageIcons:
            newImg = os.path.join(bitmapDir, "lb%s"%img)
            bmp = wx.Bitmap(newImg, wx.BITMAP_TYPE_PNG)
            imagelist.Add(bmp)

        return imagelist


    def GetBookOrientation(self, style):

        selection = self.bookdirection.GetSelection()
        if selection == 0:
            style |= INB_LEFT
        elif selection == 1:
            style |= INB_RIGHT
        elif selection == 2:
            style |= INB_TOP
        else:
            style |= INB_BOTTOM

        return style


    def OnBookType(self, event):

        self.CreateLabelBook(event.GetInt())
        event.Skip()


    def OnBookOrientation(self, event):

        style = self.GetBookStyles()
        self.book.SetAGWWindowStyleFlag(style)

        event.Skip()


    def OnStyle(self, event):

        style = self.GetBookStyles()
        self.book.SetAGWWindowStyleFlag(style)

        self.book.SetFontSizeMultiple(float(self.textsize.GetValue()))
        if self.textsize.GetValue() != self._oldTextSize:
            self.book.ResizeTabArea()

        self._oldTextSize = self.textsize.GetValue()

        event.Skip()


    def OnBookColours(self, event):

        obj = event.GetId()
        colour = event.GetValue()

        if obj == self.background.GetId():
            self.book.SetColour(INB_TAB_AREA_BACKGROUND_COLOUR, colour)
        elif obj == self.activetab.GetId():
            self.book.SetColour(INB_ACTIVE_TAB_COLOUR, colour)
        elif obj == self.tabsborder.GetId():
            self.book.SetColour(INB_TABS_BORDER_COLOUR, colour)
        elif obj == self.textcolour.GetId():
            self.book.SetColour(INB_TEXT_COLOUR, colour)
        elif obj == self.activetextcolour.GetId():
            self.book.SetColour(INB_ACTIVE_TEXT_COLOUR, colour)
        else:
            self.book.SetColour(INB_HILITE_TAB_COLOUR, colour)

        self.book.Refresh()


    def SetUserColours(self):

        self.book.SetColour(INB_TAB_AREA_BACKGROUND_COLOUR, self.background.GetColour())
        self.book.SetColour(INB_ACTIVE_TAB_COLOUR, self.activetab.GetColour())
        self.book.SetColour(INB_TABS_BORDER_COLOUR, self.tabsborder.GetColour())
        self.book.SetColour(INB_TEXT_COLOUR, self.textcolour.GetColour())
        self.book.SetColour(INB_ACTIVE_TEXT_COLOUR, self.activetextcolour.GetColour())
        self.book.SetColour(INB_HILITE_TAB_COLOUR, self.hilite.GetColour())


    def OnPageChanging(self, event):

        oldsel = event.GetOldSelection()
        newsel = event.GetSelection()
        self.log.write("Page Changing From: " + str(oldsel) + " To: " + str(newsel) + "\n")
        event.Skip()


    def OnPageChanged(self, event):

        newsel = event.GetSelection()
        self.log.write("Page Changed To: " + str(newsel) + "\n")
        event.Skip()


    def OnPageClosing(self, event):

        newsel = event.GetSelection()
        self.log.write("Closing Page: " + str(newsel) + "\n")
        event.Skip()


    def OnPageClosed(self, event):

        newsel = event.GetSelection()
        self.log.write("Closed Page: " + str(newsel) + "\n")
        event.Skip()


    def OnAddPage(self, event):

        pageCount = self.book.GetPageCount()
        indx = random.randint(0, 4)
        label = "This is panel number %d"%(pageCount+1)
        self.book.AddPage(SamplePane(self.book, _pageColours[indx], label),
                          "Added Page", True, indx)


    def OnDeletePage(self, event):

        msg = "Please Enter The Page Number You Want To Remove:"
        dlg = wx.TextEntryDialog(self, msg, "Enter Page")

        if dlg.ShowModal() != wx.ID_OK:
            dlg.Destroy()
            return

        userString = dlg.GetValue()
        dlg.Destroy()

        try:
            page = int(userString)
        except:
            return

        if page < 0 or page > self.book.GetPageCount() - 1:
            return

        self.book.DeletePage(page)


    def OnDeleteAllPages(self, event):

        self.book.DeleteAllPages()


    def CreateMenu(self):

        menuBar = wx.MenuBar(wx.MB_DOCKABLE)
        fileMenu = wx.Menu()
        editMenu = wx.Menu()
        helpMenu = wx.Menu()

        item = wx.MenuItem(fileMenu, wx.ID_ANY, "E&xit")
        self.Bind(wx.EVT_MENU, self.OnQuit, item)
        fileMenu.Append(item)

        item = wx.MenuItem(editMenu, wx.ID_ANY, "Add Page")
        self.Bind(wx.EVT_MENU, self.OnAddPage, item)
        editMenu.Append(item)

        editMenu.AppendSeparator()

        item = wx.MenuItem(editMenu, wx.ID_ANY, "Delete Page")
        self.Bind(wx.EVT_MENU, self.OnDeletePage, item)
        editMenu.Append(item)

        item = wx.MenuItem(editMenu, wx.ID_ANY, "Delete All Pages")
        self.Bind(wx.EVT_MENU, self.OnDeleteAllPages, item)
        editMenu.Append(item)

        item = wx.MenuItem(helpMenu, wx.ID_ANY, "About")
        self.Bind(wx.EVT_MENU, self.OnAbout, item)
        helpMenu.Append(item)

        menuBar.Append(fileMenu, "&File")
        menuBar.Append(editMenu, "&Edit")
        menuBar.Append(helpMenu, "&Help")

        self.SetMenuBar(menuBar)


    def OnQuit(self, event):

        self.Destroy()


    def OnAbout(self, event):

        msg = "This Is The About Dialog Of The LabelBook & FlatImageBook Demo.\n\n" + \
            "Author: Andrea Gavana @ 03 Nov 2006\n\n" + \
            "Please Report Any Bug/Requests Of Improvements\n" + \
            "To Me At The Following Adresses:\n\n" + \
            "andrea.gavana@gmail.com\n" + "andrea.gavana@maerskoil.com\n\n" + \
            "Welcome To wxPython " + wx.VERSION_STRING + "!!"

        dlg = wx.MessageDialog(self, msg, "LabelBook wxPython Demo",
                               wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()


#---------------------------------------------------------------------------


class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        b = wx.Button(self, -1, " Test LabelBook And FlatImageBook ", (50,50))
        self.Bind(wx.EVT_BUTTON, self.OnButton, b)


    def OnButton(self, evt):
        self.win = LabelBookDemo(self, self.log)
        self.win.Show(True)

#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------


overview = LB.__doc__


if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

