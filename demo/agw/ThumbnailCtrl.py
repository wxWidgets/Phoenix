import wx
import os

import sys

try:
    dirName = os.path.dirname(os.path.abspath(__file__))
except:
    dirName = os.path.dirname(os.path.abspath(sys.argv[0]))

sys.path.append(os.path.split(dirName)[0])

try:
    from agw import thumbnailctrl as TC
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.thumbnailctrl as TC

import images


class ThumbnailCtrlDemo(wx.Frame):

    def __init__(self, parent, log):

        wx.Frame.__init__(self, parent)

        self.SetIcon(images.Mondrian.GetIcon())
        self.SetTitle("ThumbnailCtrl wxPython Demo ;-)")

        self.statusbar = self.CreateStatusBar(2, wx.ST_SIZEGRIP)
        self.statusbar.SetStatusWidths([-2, -1])
        # statusbar fields
        statusbar_fields = [("ThumbnailCtrl Demo, Andrea Gavana @ 10 Dec 2005"),
                            ("Welcome To wxPython!")]

        for i in range(len(statusbar_fields)):
            self.statusbar.SetStatusText(statusbar_fields[i], i)

        self.SetMenuBar(self.CreateMenuBar())
        
        splitter = wx.SplitterWindow(self, -1, style=wx.CLIP_CHILDREN |
                                     wx.SP_3D | wx.WANTS_CHARS | wx.SP_LIVE_UPDATE)
        self.panel = wx.Panel(splitter, -1)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        scroll = TC.ThumbnailCtrl(splitter, -1, imagehandler=TC.NativeImageHandler)
        
        scroll.ShowFileNames()
        if os.path.isdir("../bitmaps"):
            scroll.ShowDir(os.path.normpath(os.getcwd() + "/../bitmaps"))
        else:
            scroll.ShowDir(os.getcwd())

        self.TC = scroll
        self.log = log
        
        self.thumbsizer_staticbox = wx.StaticBox(self.panel, -1, "Thumb Style")
        self.customsizer_staticbox = wx.StaticBox(self.panel, -1, "Thumb Customization")
        self.optionsizer_staticbox = wx.StaticBox(self.panel, -1, "More Options")
        self.dirsizer_staticbox = wx.StaticBox(self.panel, -1, "Directory Selection")
        self.dirbutton = wx.Button(self.panel, -1, "Change Directory")
        self.radiostyle1 = wx.RadioButton(self.panel, -1, "THUMB_OUTLINE_NONE", style=wx.RB_GROUP)
        self.radiostyle2 = wx.RadioButton(self.panel, -1, "THUMB_OUTLINE_FULL")
        self.radiostyle3 = wx.RadioButton(self.panel, -1, "THUMB_OUTLINE_RECT")
        self.radiostyle4 = wx.RadioButton(self.panel, -1, "THUMB_OUTLINE_IMAGE")
        self.highlight = wx.CheckBox(self.panel, -1, "Highlight on pointing")
        self.showfiles = wx.CheckBox(self.panel, -1, "Show file names")
        self.enabledragging = wx.CheckBox(self.panel, -1, "Enable drag and drop")
        self.setpopup = wx.CheckBox(self.panel, -1, "Set popup menu on thumbs")
        self.setgpopup = wx.CheckBox(self.panel, -1, "Set global popup menu")
        self.showcombo = wx.CheckBox(self.panel, -1, "Show folder combobox")
        self.enabletooltip = wx.CheckBox(self.panel, -1, "Enable thumb tooltips")
        self.textzoom = wx.TextCtrl(self.panel, -1, "1.4")
        self.zoombutton = wx.Button(self.panel, -1, "Set zoom factor")
        self.fontbutton = wx.Button(self.panel, -1, "Set caption font")
        self.colourbutton = wx.Button(self.panel, -1, "Set selection colour")

        self.radios = [self.radiostyle1, self.radiostyle2, self.radiostyle3,
                       self.radiostyle4]
        self.thumbstyles = ["THUMB_OUTLINE_NONE", "THUMB_OUTLINE_FULL", "THUMB_OUTLINE_RECT",
                            "THUMB_OUTLINE_IMAGE"]
        
        self.SetProperties()
        self.DoLayout()

        self.panel.SetSizer(sizer)
        sizer.Layout()
    
        self.Bind(wx.EVT_RADIOBUTTON, self.OnChangeOutline, self.radiostyle1)
        self.Bind(wx.EVT_RADIOBUTTON, self.OnChangeOutline, self.radiostyle2)
        self.Bind(wx.EVT_RADIOBUTTON, self.OnChangeOutline, self.radiostyle3)
        self.Bind(wx.EVT_RADIOBUTTON, self.OnChangeOutline, self.radiostyle4)
        self.Bind(wx.EVT_CHECKBOX, self.OnHighlight, self.highlight)
        self.Bind(wx.EVT_CHECKBOX, self.OnShowFiles, self.showfiles)
        self.Bind(wx.EVT_CHECKBOX, self.OnEnableDragging, self.enabledragging)
        self.Bind(wx.EVT_CHECKBOX, self.OnSetPopup, self.setpopup)
        self.Bind(wx.EVT_CHECKBOX, self.OnSetGlobalPopup, self.setgpopup)
        self.Bind(wx.EVT_CHECKBOX, self.OnShowComboBox, self.showcombo)
        self.Bind(wx.EVT_CHECKBOX, self.OnEnableToolTips, self.enabletooltip)
        self.Bind(wx.EVT_BUTTON, self.OnSetZoom, self.zoombutton)
        self.Bind(wx.EVT_BUTTON, self.OnSetFont, self.fontbutton)
        self.Bind(wx.EVT_BUTTON, self.OnSetColour, self.colourbutton)
        self.Bind(wx.EVT_BUTTON, self.OnSetDirectory, self.dirbutton)

        self.TC.Bind(TC.EVT_THUMBNAILS_SEL_CHANGED, self.OnSelChanged)
        self.TC.Bind(TC.EVT_THUMBNAILS_POINTED, self.OnPointed)
        self.TC.Bind(TC.EVT_THUMBNAILS_DCLICK, self.OnDClick)
        
        splitter.SplitVertically(scroll, self.panel, 180)

        splitter.SetMinimumPaneSize(140)        
        self.SetMinSize((700, 590))
        self.CenterOnScreen()

        
    def SetProperties(self):

        self.radiostyle4.SetValue(1)
        self.showfiles.SetValue(1)
        boldFont = wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, "")
        self.zoombutton.SetFont(boldFont)
        self.fontbutton.SetFont(boldFont)
        self.dirbutton.SetFont(boldFont)
        self.colourbutton.SetFont(boldFont)


    def DoLayout(self):
        
        splitsizer = wx.BoxSizer(wx.VERTICAL)
        optionsizer = wx.StaticBoxSizer(self.optionsizer_staticbox, wx.VERTICAL)
        zoomsizer = wx.BoxSizer(wx.HORIZONTAL)
        customsizer = wx.StaticBoxSizer(self.customsizer_staticbox, wx.VERTICAL)
        thumbsizer = wx.StaticBoxSizer(self.thumbsizer_staticbox, wx.VERTICAL)
        radiosizer = wx.BoxSizer(wx.VERTICAL)
        dirsizer = wx.StaticBoxSizer(self.dirsizer_staticbox, wx.HORIZONTAL)
        dirsizer.Add(self.dirbutton, 0, wx.LEFT|wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 3)
        splitsizer.Add(dirsizer, 0, wx.EXPAND|wx.TOP|wx.LEFT, 5)
        radiosizer.Add(self.radiostyle1, 0, wx.LEFT|wx.TOP|wx.ADJUST_MINSIZE, 3)
        radiosizer.Add(self.radiostyle2, 0, wx.LEFT|wx.TOP|wx.ADJUST_MINSIZE, 3)
        radiosizer.Add(self.radiostyle3, 0, wx.LEFT|wx.TOP|wx.ADJUST_MINSIZE, 3)
        radiosizer.Add(self.radiostyle4, 0, wx.LEFT|wx.TOP|wx.BOTTOM|wx.ADJUST_MINSIZE, 3)
        thumbsizer.Add(radiosizer, 1, wx.EXPAND, 0)
        splitsizer.Add(thumbsizer, 0, wx.TOP|wx.EXPAND|wx.LEFT, 5)
        customsizer.Add(self.highlight, 0, wx.LEFT|wx.TOP|wx.BOTTOM|wx.ADJUST_MINSIZE, 3)
        customsizer.Add(self.showfiles, 0, wx.LEFT|wx.BOTTOM|wx.ADJUST_MINSIZE, 3)
        customsizer.Add(self.enabledragging, 0, wx.LEFT|wx.BOTTOM|wx.ADJUST_MINSIZE, 3)
        customsizer.Add(self.setpopup, 0, wx.LEFT|wx.BOTTOM|wx.ADJUST_MINSIZE, 3)
        customsizer.Add(self.setgpopup, 0, wx.LEFT|wx.BOTTOM|wx.ADJUST_MINSIZE, 3)
        customsizer.Add(self.showcombo, 0, wx.LEFT|wx.BOTTOM|wx.ADJUST_MINSIZE, 3)
        customsizer.Add(self.enabletooltip, 0, wx.LEFT|wx.BOTTOM|wx.ADJUST_MINSIZE, 3)
        splitsizer.Add(customsizer, 0, wx.TOP|wx.EXPAND|wx.LEFT, 5)
        zoomsizer.Add(self.textzoom, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 3)
        zoomsizer.Add(self.zoombutton, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 3)
        optionsizer.Add(zoomsizer, 1, wx.EXPAND, 0)
        optionsizer.Add(self.fontbutton, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 3)
        optionsizer.Add(self.colourbutton, 0, wx.TOP|wx.LEFT|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 3)
        splitsizer.Add(optionsizer, 0, wx.EXPAND | wx.TOP|wx.LEFT, 5)
        self.panel.SetAutoLayout(True)
        self.panel.SetSizer(splitsizer)
        splitsizer.Fit(self.panel)
        

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

        return menu_bar        


    def OnClose(self, event):
        
        self.Destroy()


    def OnAbout(self, event):

        msg = "This Is The About Dialog Of The ThumbnailCtrl Demo.\n\n" + \
              "Author: Andrea Gavana @ 10 Dec 2005\n\n" + \
              "Please Report Any Bug/Requests Of Improvements\n" + \
              "To Me At The Following Adresses:\n\n" + \
              "andrea.gavana@agip.it\n" + "andrea_gavana@tin.it\n\n" + \
              "Welcome To wxPython " + wx.VERSION_STRING + "!!"
              
        dlg = wx.MessageDialog(self, msg, "ThumbnailCtrl Demo",
                               wx.OK | wx.ICON_INFORMATION)
        
        dlg.SetFont(wx.Font(8, wx.NORMAL, wx.NORMAL, wx.NORMAL, False))
        dlg.ShowModal()
        dlg.Destroy()


    def OnSetDirectory(self, event):

        dlg = wx.DirDialog(self, "Choose a directory with images:",
                           defaultPath=os.getcwd(),
                           style=wx.DD_DEFAULT_STYLE|wx.DD_NEW_DIR_BUTTON)

        # If the user selects OK, then we process the dialog's data.
        # This is done by getting the path data from the dialog - BEFORE
        # we destroy it. 
        if dlg.ShowModal() == wx.ID_OK:
            self.TC.ShowDir(dlg.GetPath())
            self.log.write("OnSetDirectory: directory changed to: %s\n"%dlg.GetPath())

        # Only destroy a dialog after you're done with it.
        dlg.Destroy()
        
        
    def OnChangeOutline(self, event): # wxGlade: MyFrame.<event_handler>

        radio = event.GetEventObject()
        pos = self.radios.index(radio)

        if pos == 0:
            self.TC.SetThumbOutline(TC.THUMB_OUTLINE_NONE)
        elif pos == 1:
            self.TC.SetThumbOutline(TC.THUMB_OUTLINE_FULL)
        elif pos == 2:
            self.TC.SetThumbOutline(TC.THUMB_OUTLINE_RECT)
        elif pos == 3:
            self.TC.SetThumbOutline(TC.THUMB_OUTLINE_IMAGE)

        self.TC.Refresh()
        
        self.log.write("OnChangeOutline: Outline changed to: %s\n"%self.thumbstyles[pos])
        event.Skip()


    def OnHighlight(self, event): # wxGlade: MyFrame.<event_handler>

        if self.highlight.GetValue() == 1:
            self.TC.SetHighlightPointed(True)
            self.log.write("OnHighlight: Highlight thumbs on pointing\n")
        else:
            self.TC.SetHighlightPointed(False)
            self.log.write("OnHighlight: Don't Highlight thumbs on pointing\n")
            
        event.Skip()


    def OnShowFiles(self, event): # wxGlade: MyFrame.<event_handler>

        if self.showfiles.GetValue() == 1:
            self.TC.ShowFileNames(True)
            self.log.write("OnShowFiles: Thumbs file names shown\n")
        else:
            self.TC.ShowFileNames(False)
            self.log.write("OnShowFiles: Thumbs file names not shown\n")

        self.TC.Refresh()
        
        event.Skip()


    def OnEnableDragging(self, event):

        if self.enabledragging.GetValue() == 1:
            self.TC.EnableDragging(True)
            self.log.write("OnEnableDragging: Thumbs drag and drop enabled\n")
        else:
            self.TC.EnableDragging(False)
            self.log.write("OnEnableDragging: Thumbs drag and drop disabled\n")

        self.TC.Refresh()
        
        event.Skip()
        

    def OnSetPopup(self, event): # wxGlade: MyFrame.<event_handler>

        if self.setpopup.GetValue() == 1:
            menu = self.CreatePopups()
            self.TC.SetPopupMenu(menu)
            self.log.write("OnSetPopup: Popups enabled on thumbs\n")
        else:
            self.TC.SetPopupMenu(None)
            self.log.write("OnSetPopup: Popups disabled on thumbs\n")
        
        event.Skip()


    def OnSetGlobalPopup(self, event):

        if self.setgpopup.GetValue() == 1:
            menu = self.CreateGlobalPopups()
            self.TC.SetGlobalPopupMenu(menu)
            self.log.write("OnSetGlobalPopup: Popups enabled globally (no selection needed)\n")
        else:
            self.TC.SetGlobalPopupMenu(None)
            self.log.write("OnSetGlobalPopup: Popups disabled globally (no selection needed)\n")
            
        event.Skip()


    def OnShowComboBox(self, event):

        if self.showcombo.GetValue() == 1:
            self.log.write("OnShowComboBox: Directory comboBox shown\n")
            self.TC.ShowComboBox(True)
        else:
            self.log.write("OnShowComboBox: Directory comboBox hidden\n")
            self.TC.ShowComboBox(False)

        event.Skip()


    def OnEnableToolTips(self, event):

        if self.enabletooltip.GetValue() == 1:
            self.log.write("OnEnableToolTips: File information on tooltips enabled\n")
            self.TC.EnableToolTips(True)
        else:
            self.log.write("OnEnableToolTips: File information on tooltips disabled\n")
            self.TC.EnableToolTips(False)

        event.Skip()
        
        
    def OnSetZoom(self, event): # wxGlade: MyFrame.<event_handler>

        val = self.textzoom.GetValue().strip()

        try:
            val = float(val)
        except:
            errstr = "Error: a float value is required."
            dlg = wx.MessageDialog(self, errstr, "ThumbnailCtrlDemo Error",
                                   wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            self.textzoom.SetValue("1.4")
            return


        if val < 1.0:
            errstr = "Error: zoom factor must be grater than 1.0."
            dlg = wx.MessageDialog(self, errstr, "ThumbnailCtrlDemo Error",
                                   wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            self.textzoom.SetValue("1.4")
            return

        self.TC.SetZoomFactor(val)
        
        event.Skip()


    def OnSelChanged(self, event):

        self.log.write("OnSelChanged: Thumb selected: %s\n"%str(self.TC.GetSelection()))
        event.Skip()


    def OnPointed(self, event):

        self.log.write("OnPointed: Thumb pointed: %s\n"%self.TC.GetPointed())
        event.Skip()


    def OnDClick(self, event):

        self.log.write("OnDClick: Thumb double-clicked: %s\n"%self.TC.GetSelection())
        event.Skip()
        

    def OnSetFont(self, event): # wxGlade: MyFrame.<event_handler>

        data = wx.FontData()
        data.EnableEffects(True)
        data.SetInitialFont(self.TC.GetCaptionFont())

        dlg = wx.FontDialog(self, data)
        
        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetFontData()
            font = data.GetChosenFont()
            self.TC.SetCaptionFont(font)
            self.TC.Refresh()
            self.log.write("OnSetFont: Caption font changed\n")
            
        # Don't destroy the dialog until you get everything you need from the
        # dialog!
        dlg.Destroy()        
        event.Skip()


    def OnSetColour(self, event):

        dlg = wx.ColourDialog(self)

        # Ensure the full colour dialog is displayed, 
        # not the abbreviated version.
        dlg.GetColourData().SetChooseFull(True)

        if dlg.ShowModal() == wx.ID_OK:

            # If the user selected OK, then the dialog's wx.ColourData will
            # contain valid information. Fetch the data ...
            data = dlg.GetColourData()

            # ... then do something with it. The actual colour data will be
            # returned as a three-tuple (r, g, b) in this particular case.
            colour = data.GetColour().Get()
            colour = wx.Colour(colour[0], colour[1], colour[2])
            self.TC.SetSelectionColour(colour)
            self.TC.Refresh()

        # Once the dialog is destroyed, Mr. wx.ColourData is no longer your
        # friend. Don't use it again!
        dlg.Destroy()
        

    def CreatePopups(self):

        if not hasattr(self, "popupID1"):
            self.popupID1 = wx.NewId()
            self.popupID2 = wx.NewId()
            self.popupID3 = wx.NewId()
            self.popupID4 = wx.NewId()
            self.popupID5 = wx.NewId()
            self.popupID6 = wx.NewId()
            self.popupID7 = wx.NewId()
            self.popupID8 = wx.NewId()
            self.popupID9 = wx.NewId()
            self.popupID10 = wx.NewId()
            self.popupID11 = wx.NewId()
            self.popupID12 = wx.NewId()

            self.Bind(wx.EVT_MENU, self.OnPopupOne, id=self.popupID1)
            self.Bind(wx.EVT_MENU, self.OnPopupTwo, id=self.popupID2)
            self.Bind(wx.EVT_MENU, self.OnPopupThree, id=self.popupID3)
            self.Bind(wx.EVT_MENU, self.OnPopupFour, id=self.popupID4)
            self.Bind(wx.EVT_MENU, self.OnPopupFive, id=self.popupID5)
            self.Bind(wx.EVT_MENU, self.OnPopupSix, id=self.popupID6)
            self.Bind(wx.EVT_MENU, self.OnPopupSeven, id=self.popupID7)
            self.Bind(wx.EVT_MENU, self.OnPopupEight, id=self.popupID8)
            self.Bind(wx.EVT_MENU, self.OnPopupNine, id=self.popupID9)
            
        menu = wx.Menu()
        item = wx.MenuItem(menu, self.popupID1, "One")
        img = images.Mondrian.GetImage()
        img.Rescale(16, 16)
        bmp = img.ConvertToBitmap()
        item.SetBitmap(bmp)
        menu.AppendItem(item)
        
        # add some other items
        menu.Append(self.popupID2, "Two")
        menu.Append(self.popupID3, "Three")
        menu.Append(self.popupID4, "Four")
        menu.Append(self.popupID5, "Five")
        menu.Append(self.popupID6, "Six")
        # make a submenu
        sm = wx.Menu()
        sm.Append(self.popupID8, "Sub Item 1")
        sm.Append(self.popupID9, "Sub Item 1")
        menu.AppendMenu(self.popupID7, "Test Submenu", sm)

        return menu


    def CreateGlobalPopups(self):

        if not hasattr(self, "popupID10"):
            self.popupID10 = wx.NewId()
            self.popupID11 = wx.NewId()
            self.popupID12 = wx.NewId()

        self.Bind(wx.EVT_MENU, self.OnPopupTen, id=self.popupID10)
        self.Bind(wx.EVT_MENU, self.OnPopupEleven, id=self.popupID11)
        self.Bind(wx.EVT_MENU, self.OnPopupTwelve, id=self.popupID12)
        
        menu = wx.Menu()
        item = wx.MenuItem(menu, self.popupID10, "Select all")
        menu.AppendItem(item)
        menu.AppendSeparator()

        item = wx.MenuItem(menu, self.popupID11, "Say Hello!")
        img = images.Mondrian.GetImage()
        img.Rescale(16, 16)
        bmp = img.ConvertToBitmap()
        item.SetBitmap(bmp)
        menu.AppendItem(item)
        menu.AppendSeparator()
        
        menu.Append(self.popupID12, "Get thumbs count")

        return menu
    

    def OnPopupOne(self, event):
        self.log.write("OnPopupMenu: Popup One\n")


    def OnPopupTwo(self, event):
        self.log.write("OnPopupMenu: Popup Two\n")


    def OnPopupThree(self, event):
        self.log.write("OnPopupMenu: Popup Three\n")


    def OnPopupFour(self, event):
        self.log.write("OnPopupMenu: Popup Four\n")


    def OnPopupFive(self, event):
        self.log.write("OnPopupMenu: Popup Five\n")


    def OnPopupSix(self, event):
        self.log.write("OnPopupMenu: Popup Six\n")


    def OnPopupSeven(self, event):
        self.log.write("OnPopupMenu: Popup Seven\n")


    def OnPopupEight(self, event):
        self.log.write("OnPopupMenu: Popup Eight\n")


    def OnPopupNine(self, event):
        self.log.write("OnPopupMenu: Popup Nine\n")
        

    def OnPopupTen(self, event):

        items = self.TC.GetItemCount()

        for ii in xrange(items):
            self.TC.SetSelection(ii)

        self.log.write("OnGlobalPopupMenu: all thumbs selected\n")
        
        event.Skip()


    def OnPopupEleven(self, event):

        self.log.write("OnGlobalPopupMenu: say hello message...\n")
        
        msgstr = "Info: let's say hello to wxPython! "
        dlg = wx.MessageDialog(self, msgstr, "ThumbnailCtrlDemo Info",
                               wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

        event.Skip()


    def OnPopupTwelve(self, event):

        items = self.TC.GetItemCount()
        self.log.write("OnGlobalPopupMenu: number of thumbs: %d\n"%items)
        
        msgstr = "Info: number of thumbs: %d"%items
        dlg = wx.MessageDialog(self, msgstr, "ThumbnailCtrlDemo Info",
                               wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

        event.Skip()
        
        

#---------------------------------------------------------------------------


class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        b = wx.Button(self, -1, " Test ThumbnailCtrl ", (50,50))
        self.Bind(wx.EVT_BUTTON, self.OnButton, b)


    def OnButton(self, evt):
        self.win = ThumbnailCtrlDemo(self, self.log)
        self.win.Show(True)

#----------------------------------------------------------------------

def runTest(frame, nb, log):

    try:
        import PIL.Image
        win = TestPanel(nb, log)
        return win

    except ImportError:

        from Main import MessagePanel
        win = MessagePanel(nb, 'This demo requires PIL (Python Imaging Library).',
                           'Sorry', wx.ICON_WARNING)
        return win

#----------------------------------------------------------------------


overview = TC.__doc__


if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])


