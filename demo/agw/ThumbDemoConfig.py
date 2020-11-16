#!/usr/bin/env python

import wx
import os
import images

from wx.lib.agw.scrolledthumbnail import (ScrolledThumbnail,
                                          Thumb,
                                          NativeImageHandler,
                                          EVT_THUMBNAILS_SEL_CHANGED,
                                          EVT_THUMBNAILS_POINTED,
                                          EVT_THUMBNAILS_DCLICK)

class ThumbDemoConfig(wx.Frame):
    """ScrolledThumbnail or ThumbnailCtrl demo common code

    This class contains code common to both the ScrolledThumbnail and
    the ThumbnailCtrl demos.  It is extended by both of these demos to
    address the differences in invoking :class:`ScrolledThumbnail`
    or :class:`ThumbnailCtrl` widgets.

    This class creates a SplitterWindow with the left half containing
    the widget being demoed and the right half containing a number of
    controls which set or change operation of the widget.  In most
    this simply involves passing the user-specified value to the
    widget.

    For information about what setting does, as well as other settings,
    set the documentation for :class:`ScrolledThumbnail` or
    :class:`ThumbnailCtrl`.
    """

    def __init__(self, parent, log, name, about):

        wx.Frame.__init__(self, parent, size=(850,820))
        self.name = name
        self.about = about

        self.SetIcon(images.Mondrian.GetIcon())
        self.SetTitle(self.name + " wxPython Demo ;-)")

        self.statusbar = self.CreateStatusBar(2)
        self.statusbar.SetStatusWidths([-2, -1])
        # statusbar fields
        statusbar_fields = [(self.name + " Demo, Michael Eager @ 10 Nov 2020"),
                            ("Welcome To wxPython!")]

        for i in range(len(statusbar_fields)):
            self.statusbar.SetStatusText(statusbar_fields[i], i)

        self.SetMenuBar(self.CreateMenuBar())

        # Create SplitterWindow with panels for widget and controls.
        self.splitter = wx.SplitterWindow(self, -1, style=wx.CLIP_CHILDREN |
                                     wx.SP_3D | wx.WANTS_CHARS | wx.SP_LIVE_UPDATE)
        self.panel = wx.Panel(self.splitter, -1)

        # Call SetScroll() to create thumbnail widget.
        # This is provided by each of the two demos.
        self.SetScroll()

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
        self.DoComboCheckbox()
        self.enabletooltip = wx.CheckBox(self.panel, -1, "Enable thumb tooltips")
        self.textzoom = wx.TextCtrl(self.panel, -1, "1.4")
        self.zoombutton = wx.Button(self.panel, -1, "Set zoom factor")
        self.textthumbwidth = wx.TextCtrl(self.panel, -1, "96")
        self.textthumbheight = wx.TextCtrl(self.panel, -1, "80")
        self.thumbsizebutton = wx.Button(self.panel, -1, "Set thumbnail size (WxH)")
        self.fontbutton = wx.Button(self.panel, -1, "Set caption font")
        self.colourbutton = wx.Button(self.panel, -1, "Set selection colour")

        self.radios = [self.radiostyle1, self.radiostyle2, self.radiostyle3,
                       self.radiostyle4]
        self.thumbstyles = ["THUMB_OUTLINE_NONE", "THUMB_OUTLINE_FULL", "THUMB_OUTLINE_RECT",
                            "THUMB_OUTLINE_IMAGE"]

        self.SetProperties()
        self.DoLayout()

        self.Bind(wx.EVT_RADIOBUTTON, self.OnChangeOutline, self.radiostyle1)
        self.Bind(wx.EVT_RADIOBUTTON, self.OnChangeOutline, self.radiostyle2)
        self.Bind(wx.EVT_RADIOBUTTON, self.OnChangeOutline, self.radiostyle3)
        self.Bind(wx.EVT_RADIOBUTTON, self.OnChangeOutline, self.radiostyle4)
        self.Bind(wx.EVT_CHECKBOX, self.OnHighlight, self.highlight)
        self.Bind(wx.EVT_CHECKBOX, self.OnShowFiles, self.showfiles)
        self.Bind(wx.EVT_CHECKBOX, self.OnEnableDragging, self.enabledragging)
        self.Bind(wx.EVT_CHECKBOX, self.OnSetPopup, self.setpopup)
        self.Bind(wx.EVT_CHECKBOX, self.OnSetGlobalPopup, self.setgpopup)
        self.DoBindCombo()
        self.Bind(wx.EVT_CHECKBOX, self.OnEnableToolTips, self.enabletooltip)
        self.Bind(wx.EVT_BUTTON, self.OnSetZoom, self.zoombutton)
        self.Bind(wx.EVT_BUTTON, self.OnSetThumbSize, self.thumbsizebutton)
        self.Bind(wx.EVT_BUTTON, self.OnSetFont, self.fontbutton)
        self.Bind(wx.EVT_BUTTON, self.OnSetColour, self.colourbutton)
        self.Bind(wx.EVT_BUTTON, self.OnSetDirectory, self.dirbutton)

        self.scroll.Bind(EVT_THUMBNAILS_SEL_CHANGED, self.OnSelChanged)
        self.scroll.Bind(EVT_THUMBNAILS_POINTED, self.OnPointed)
        self.scroll.Bind(EVT_THUMBNAILS_DCLICK, self.OnDClick)

        # Add thumbnail widget and control panel to SplitterWindow.
        self.splitter.SplitVertically(self.scroll, self.panel, 300)

        self.splitter.SetMinimumPaneSize(140)
        self.CenterOnScreen()


    def SetProperties(self):

        self.radiostyle4.SetValue(1)
        self.showfiles.SetValue(1)


    def DoLayout(self):
        """Layout controls."""

        splitsizer = wx.BoxSizer(wx.VERTICAL)
        optionsizer = wx.StaticBoxSizer(self.optionsizer_staticbox, wx.VERTICAL)
        zoomsizer = wx.BoxSizer(wx.HORIZONTAL)
        thumbsizesizer = wx.BoxSizer(wx.HORIZONTAL)
        customsizer = wx.StaticBoxSizer(self.customsizer_staticbox, wx.VERTICAL)
        thumbsizer = wx.StaticBoxSizer(self.thumbsizer_staticbox, wx.VERTICAL)
        radiosizer = wx.BoxSizer(wx.VERTICAL)
        dirsizer = wx.StaticBoxSizer(self.dirsizer_staticbox, wx.HORIZONTAL)
        dirsizer.Add(self.dirbutton, 0, wx.LEFT|wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 3)
        splitsizer.Add(dirsizer, 0, wx.EXPAND|wx.TOP|wx.LEFT, 5)
        splitsizer.AddSpacer(15)
        radiosizer.Add(self.radiostyle1, 0, wx.LEFT|wx.TOP|wx.ADJUST_MINSIZE, 3)
        radiosizer.Add(self.radiostyle2, 0, wx.LEFT|wx.TOP|wx.ADJUST_MINSIZE, 3)
        radiosizer.Add(self.radiostyle3, 0, wx.LEFT|wx.TOP|wx.ADJUST_MINSIZE, 3)
        radiosizer.Add(self.radiostyle4, 0, wx.LEFT|wx.TOP|wx.BOTTOM|wx.ADJUST_MINSIZE, 3)
        thumbsizer.Add(radiosizer, 1, wx.EXPAND, 0)
        splitsizer.Add(thumbsizer, 0, wx.TOP|wx.EXPAND|wx.LEFT, 5)
        splitsizer.AddSpacer(15)
        customsizer.Add(self.highlight, 0, wx.LEFT|wx.TOP|wx.BOTTOM|wx.ADJUST_MINSIZE, 3)
        customsizer.Add(self.showfiles, 0, wx.LEFT|wx.BOTTOM|wx.ADJUST_MINSIZE, 3)
        customsizer.Add(self.enabledragging, 0, wx.LEFT|wx.BOTTOM|wx.ADJUST_MINSIZE, 3)
        customsizer.Add(self.setpopup, 0, wx.LEFT|wx.BOTTOM|wx.ADJUST_MINSIZE, 3)
        customsizer.Add(self.setgpopup, 0, wx.LEFT|wx.BOTTOM|wx.ADJUST_MINSIZE, 3)
        self.DoAddCombo(customsizer)
        customsizer.Add(self.enabletooltip, 0, wx.LEFT|wx.BOTTOM|wx.ADJUST_MINSIZE, 3)
        splitsizer.Add(customsizer, 0, wx.TOP|wx.EXPAND|wx.LEFT, 5)
        splitsizer.AddSpacer(15)
        zoomsizer.Add(self.textzoom, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 3)
        zoomsizer.Add(self.zoombutton, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 3)
        thumbsizesizer.Add(self.textthumbwidth, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 3)
        thumbsizesizer.Add(self.textthumbheight, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 3)
        thumbsizesizer.Add(self.thumbsizebutton, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 3)
        optionsizer.Add(zoomsizer, 1, wx.EXPAND, 0)
        optionsizer.Add(thumbsizesizer, 1, wx.EXPAND, 0)
        optionsizer.Add(self.fontbutton, 0, wx.ALL|wx.ADJUST_MINSIZE, 3)
        optionsizer.Add(self.colourbutton, 0, wx.TOP|wx.LEFT|wx.ADJUST_MINSIZE, 3)
        splitsizer.Add(optionsizer, 0, wx.EXPAND | wx.TOP|wx.LEFT, 5)
        self.panel.SetSizer(splitsizer)
        splitsizer.Fit(self.panel)


    def CreateMenuBar(self):

        file_menu = wx.Menu()

        AS_EXIT = wx.NewIdRef()
        file_menu.Append(AS_EXIT, "&Exit")
        self.Bind(wx.EVT_MENU, self.OnClose, id=AS_EXIT)

        help_menu = wx.Menu()

        AS_ABOUT = wx.NewIdRef()
        help_menu.Append(AS_ABOUT, "&About...")
        self.Bind(wx.EVT_MENU, self.OnAbout, id=AS_ABOUT)

        menu_bar = wx.MenuBar()

        menu_bar.Append(file_menu, "&File")
        menu_bar.Append(help_menu, "&Help")

        return menu_bar


    def OnClose(self, event):

        self.Destroy()


    def OnAbout(self, event):

        dlg = wx.MessageDialog(self, self.about, self.name + " Demo",
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
            self.ShowDir(dlg.GetPath())
            self.log.write("OnSetDirectory: directory changed to: %s\n"%dlg.GetPath())

        # Only destroy a dialog after you're done with it.
        dlg.Destroy()


    def OnChangeOutline(self, event): # wxGlade: MyFrame.<event_handler>

        radio = event.GetEventObject()
        pos = self.radios.index(radio)

        if pos == 0:
            self.scroll.SetThumbOutline(TC.THUMB_OUTLINE_NONE)
        elif pos == 1:
            self.scroll.SetThumbOutline(TC.THUMB_OUTLINE_FULL)
        elif pos == 2:
            self.scroll.SetThumbOutline(TC.THUMB_OUTLINE_RECT)
        elif pos == 3:
            self.scroll.SetThumbOutline(TC.THUMB_OUTLINE_IMAGE)

        self.scroll.Refresh()

        self.log.write("OnChangeOutline: Outline changed to: %s\n"%self.thumbstyles[pos])
        event.Skip()


    def OnHighlight(self, event): # wxGlade: MyFrame.<event_handler>

        if self.highlight.GetValue() == 1:
            self.scroll.SetHighlightPointed(True)
            self.log.write("OnHighlight: Highlight thumbs on pointing\n")
        else:
            self.scroll.SetHighlightPointed(False)
            self.log.write("OnHighlight: Don't Highlight thumbs on pointing\n")

        event.Skip()


    def OnShowFiles(self, event): # wxGlade: MyFrame.<event_handler>

        if self.showfiles.GetValue() == 1:
            self.scroll.ShowFileNames(True)
            self.log.write("OnShowFiles: Thumbs file names shown\n")
        else:
            self.scroll.ShowFileNames(False)
            self.log.write("OnShowFiles: Thumbs file names not shown\n")

        self.scroll.Refresh()

        event.Skip()


    def OnEnableDragging(self, event):

        if self.enabledragging.GetValue() == 1:
            self.scroll.EnableDragging(True)
            self.log.write("OnEnableDragging: Thumbs drag and drop enabled\n")
        else:
            self.scroll.EnableDragging(False)
            self.log.write("OnEnableDragging: Thumbs drag and drop disabled\n")

        self.scroll.Refresh()

        event.Skip()


    def OnSetPopup(self, event): # wxGlade: MyFrame.<event_handler>

        if self.setpopup.GetValue() == 1:
            menu = self.CreatePopups()
            self.scroll.SetPopupMenu(menu)
            self.log.write("OnSetPopup: Popups enabled on thumbs\n")
        else:
            self.scroll.SetPopupMenu(None)
            self.log.write("OnSetPopup: Popups disabled on thumbs\n")

        event.Skip()


    def OnSetGlobalPopup(self, event):

        if self.setgpopup.GetValue() == 1:
            menu = self.CreateGlobalPopups()
            self.scroll.SetGlobalPopupMenu(menu)
            self.log.write("OnSetGlobalPopup: Popups enabled globally (no selection needed)\n")
        else:
            self.scroll.SetGlobalPopupMenu(None)
            self.log.write("OnSetGlobalPopup: Popups disabled globally (no selection needed)\n")

        event.Skip()


    def OnEnableToolTips(self, event):

        if self.enabletooltip.GetValue() == 1:
            self.log.write("OnEnableToolTips: File information on tooltips enabled\n")
            self.scroll.EnableToolTips(True)
        else:
            self.log.write("OnEnableToolTips: File information on tooltips disabled\n")
            self.scroll.EnableToolTips(False)

        event.Skip()


    def OnSetZoom(self, event): # wxGlade: MyFrame.<event_handler>

        val = self.textzoom.GetValue().strip()

        try:
            val = float(val)
        except:
            errstr = "Error: a float value is required."
            dlg = wx.MessageDialog(self, errstr, self.name + " Error",
                                   wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            self.textzoom.SetValue("1.4")
            return


        if val < 1.0:
            errstr = "Error: zoom factor must be grater than 1.0."
            dlg = wx.MessageDialog(self, errstr, self.name + " Error",
                                   wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            self.textzoom.SetValue("1.4")
            return

        self.scroll.SetZoomFactor(val)

        event.Skip()

    def OnSetThumbSize(self, event):
        try:
            width = int(self.textthumbwidth.GetValue().strip())
            height = int(self.textthumbheight.GetValue().strip())
        except:
            errstr = "Error: thumb size must be integers (min 50x50)."
            dlg = wx.MessageDialog(self, errstr, self.name + " Error",
                                   wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return

        width = max(width, 50)
        height = max(height, 50)
        self.log.write("OnSetThumbSize: (%s, %s)\n" % (width, height))
        self.scroll.SetThumbSize (width, height)

        event.Skip()

    def OnSelChanged(self, event):

        self.log.write("OnSelChanged: Thumb selected: %s\n"%str(self.scroll.GetSelection()))
        event.Skip()


    def OnPointed(self, event):

        self.log.write("OnPointed: Thumb pointed: %s\n"%self.scroll.GetPointed())
        event.Skip()


    def OnDClick(self, event):

        self.log.write("OnDClick: Thumb double-clicked: %s\n"%self.scroll.GetSelection())
        event.Skip()


    def OnSetFont(self, event): # wxGlade: MyFrame.<event_handler>

        data = wx.FontData()
        data.EnableEffects(True)
        data.SetInitialFont(self.scroll.GetCaptionFont())

        dlg = wx.FontDialog(self, data)

        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetFontData()
            font = data.GetChosenFont()
            self.scroll.SetCaptionFont(font)
            self.scroll.Refresh()
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
            self.scroll.SetSelectionColour(colour)
            self.scroll.Refresh()

        # Once the dialog is destroyed, Mr. wx.ColourData is no longer your
        # friend. Don't use it again!
        dlg.Destroy()


    def CreatePopups(self):

        if not hasattr(self, "popupID1"):
            self.popupID1 = wx.NewIdRef()
            self.popupID2 = wx.NewIdRef()
            self.popupID3 = wx.NewIdRef()
            self.popupID4 = wx.NewIdRef()
            self.popupID5 = wx.NewIdRef()
            self.popupID6 = wx.NewIdRef()
            self.popupID7 = wx.NewIdRef()
            self.popupID8 = wx.NewIdRef()
            self.popupID9 = wx.NewIdRef()
            self.popupID10 = wx.NewIdRef()
            self.popupID11 = wx.NewIdRef()
            self.popupID12 = wx.NewIdRef()

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
        menu.Append(item)

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
        menu.Append(self.popupID7, "Test Submenu", sm)

        return menu


    def CreateGlobalPopups(self):

        if not hasattr(self, "popupID10"):
            self.popupID10 = wx.NewIdRef()
            self.popupID11 = wx.NewIdRef()
            self.popupID12 = wx.NewIdRef()

        self.Bind(wx.EVT_MENU, self.OnPopupTen, id=self.popupID10)
        self.Bind(wx.EVT_MENU, self.OnPopupEleven, id=self.popupID11)
        self.Bind(wx.EVT_MENU, self.OnPopupTwelve, id=self.popupID12)

        menu = wx.Menu()
        item = wx.MenuItem(menu, self.popupID10, "Select all")
        menu.Append(item)
        menu.AppendSeparator()

        item = wx.MenuItem(menu, self.popupID11, "Say Hello!")
        img = images.Mondrian.GetImage()
        img.Rescale(16, 16)
        bmp = img.ConvertToBitmap()
        item.SetBitmap(bmp)
        menu.Append(item)
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

        items = self.scroll.GetItemCount()
        self.log.write("Items", items, type(items))

        for ii in range(items):
            self.scroll.SetSelection(ii)

        self.log.write("OnGlobalPopupMenu: all thumbs selected\n")

        event.Skip()


    def OnPopupEleven(self, event):

        self.log.write("OnGlobalPopupMenu: say hello message...\n")

        msgstr = "Info: let's say hello to wxPython! "
        dlg = wx.MessageDialog(self, msgstr, self.name + " Info",
                               wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

        event.Skip()


    def OnPopupTwelve(self, event):

        items = self.scroll.GetItemCount()
        self.log.write("OnGlobalPopupMenu: number of thumbs: %d\n"%items)

        msgstr = "Info: number of thumbs: %d"%items
        dlg = wx.MessageDialog(self, msgstr, self.name + " Info",
                               wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

        event.Skip()


    def DoComboCheckbox(self):
        pass

    def DoBindCombo(self):
        pass

    def DoAddCombo(self, customsizer):
        pass

