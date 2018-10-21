# Name:         buttonpanel.py
# Package:      wx.lib.pdfviewer
#
# Purpose:      A button panel class for pdf viewer
#
# Author:       David Hughes     dfh@forestfield.co.uk
# Copyright:    Forestfield Software Ltd
# Licence:      Same as wxPython host

# History:      Created 26 Jun 2009
#
# Tags:         phoenix-port, documented
#
#----------------------------------------------------------------------------
"""
This module provides the :class:`~wx.lib.pdfviewer.buttonpanel.pdfButtonPanel`
which can be used together with the :class:`~wx.lib.pdfviewer.viewer.pdfViewer`.
"""
import sys, os, time

from . import images
import wx
import wx.lib.agw.buttonpanel as bp

class pdfButtonPanel(bp.ButtonPanel):
    """
    :class:`~wx.lib.pdfviewer.buttonpanel.pdfButtonPanel` is derived
    from wx.lib.agw.buttonpanel and provides buttons to manipulate the viewed
    PDF, e.g. zoom, save, print etc.
    """
    def __init__(self, parent, nid, pos, size, style):
        """
        Default class constructor.

        :param wx.Window `parent`: parent window. Must not be ``None``;
        :param integer `nid`: window identifier. A value of -1 indicates a default value;
        :param `pos`: the control position. A value of (-1, -1) indicates a default position,
         chosen by either the windowing system or wxPython, depending on platform;
        :type `pos`: tuple or :class:`wx.Point`
        :param `size`: the control size. A value of (-1, -1) indicates a default size,
         chosen by either the windowing system or wxPython, depending on platform;
        :type `size`: tuple or :class:`wx.Size`
        :param integer `style`: the button style (unused);

        """
        self.viewer = None          # reference to viewer is set by their common parent
        self.numpages = None
        bp.ButtonPanel.__init__(self, parent, nid, "",
                                agwStyle=bp.BP_USE_GRADIENT, alignment=bp.BP_ALIGN_LEFT)
        self.SetProperties()
        self.CreateButtons()

    def CreateButtons(self):
        """
        Add the buttons and other controls to the panel.
        """
        self.disabled_controls = []
        self.pagelabel = wx.StaticText(self, -1, 'Page')
        self.page = wx.TextCtrl(self, -1, size=(30, -1), style=wx.TE_CENTRE|wx.TE_PROCESS_ENTER)
        self.page.Enable(False)
        self.disabled_controls.append(self.page)
        self.page.Bind(wx.EVT_KILL_FOCUS, self.OnPage)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnPage, self.page)
        self.maxlabel = wx.StaticText(self, -1, '          ')
        self.zoom = wx.ComboBox(self, -1, style=wx.CB_DROPDOWN|wx.TE_PROCESS_ENTER)
        self.zoom.Enable(False)
        self.disabled_controls.append(self.zoom)
        self.comboval = (('Actual size', 1.0), ('Fit width', -1), ('Fit page', -2),
                          ('25%', 0.25), ('50%', 0.5), ('75%', 0.75), ('100%', 1.0),
                            ('125%', 1.25), ('150%', 1.5), ('200%', 2.0), ('400%', 4.0),
                            ('800%', 8.0), ('1000%', 10.0))
        for item in self.comboval:
            self.zoom.Append(item[0], item[1])      # string value and client data
        self.Bind(wx.EVT_COMBOBOX, self.OnZoomSet, self.zoom)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnZoomSet, self.zoom)
        panelitems = [
          ('btn', images.PrintIt.GetBitmap(), wx.ITEM_NORMAL, "Print", self.OnPrint),
          ('sep',),
          ('btn', images.SaveIt.GetBitmap(), wx.ITEM_NORMAL, "Save", self.OnSave),
          ('sep',),
          ('btn', images.First.GetBitmap(), wx.ITEM_NORMAL, "First page", self.OnFirst),
          ('btn', images.Prev.GetBitmap(), wx.ITEM_NORMAL, "Previous page", self.OnPrev),
          ('btn', images.Next.GetBitmap(), wx.ITEM_NORMAL, "Next page", self.OnNext),
          ('btn', images.Last.GetBitmap(), wx.ITEM_NORMAL, "Last page", self.OnLast),
          ('Ctrl', self.pagelabel),
          ('ctrl', self.page),
          ('ctrl', self.maxlabel),
          ('sep',),
          ('btn', images.ZoomOut.GetBitmap(), wx.ITEM_NORMAL, "Zoom out", self.OnZoomOut),
          ('btn', images.ZoomIn.GetBitmap(), wx.ITEM_NORMAL, "Zoom in", self.OnZoomIn),
          ('ctrl', self.zoom),
          ('btn', images.Width.GetBitmap(), wx.ITEM_NORMAL, "Fit page width", self.OnWidth),
          ('btn', images.Height.GetBitmap(), wx.ITEM_NORMAL, "Fit page height", self.OnHeight),
          ]

        self.Freeze()
        for item in panelitems:
            if item[0].lower() == 'btn':
                x_type, image, kind, popup, handler = item
                btn = bp.ButtonInfo(self, wx.ID_ANY,image, kind=kind,
                                    shortHelp=popup, longHelp='')
                self.AddButton(btn)
                btn.Enable(False)
                self.disabled_controls.append(btn)
                self.Bind(wx.EVT_BUTTON, handler, id=btn.GetId())
            elif item[0].lower() == 'sep':
                self.AddSeparator()
            elif item[0].lower() == 'space':
                self.AddSpacer(item[1])
            elif item[0].lower() == 'ctrl':
                self.AddControl(item[1])
        self.Thaw()
        self.DoLayout()


    def SetProperties(self):
        """
        Setup the buttonpanel colours, borders etc.
        """
        bpArt = self.GetBPArt()
        bpArt.SetGradientType(bp.BP_GRADIENT_VERTICAL)
        bpArt.SetColor(bp.BP_GRADIENT_COLOUR_FROM, wx.Colour(119, 136, 153)) #light slate
        bpArt.SetColor(bp.BP_GRADIENT_COLOUR_TO, wx.Colour(245, 245, 245))   # white smoke
        bpArt.SetColor(bp.BP_BORDER_COLOUR, wx.Colour(119, 136, 153))
        bpArt.SetColor(bp.BP_BUTTONTEXT_COLOUR, wx.Colour(0,0,0))            # not used
        bpArt.SetColor(bp.BP_SEPARATOR_COLOUR,
                       bp.BrightenColour(wx.Colour(60, 11, 112), 0.85))
        bpArt.SetColor(bp.BP_SELECTION_BRUSH_COLOUR, wx.Colour(225, 225, 255))    # used?
        bpArt.SetColor(bp.BP_SELECTION_PEN_COLOUR,
                               wx.SystemSettings.GetColour(wx.SYS_COLOUR_ACTIVECAPTION))

    def Update(self, pagenum, numpages, zoomscale):
        """
        Called from viewer to initialize and update controls.

        :param integer `pagenum`: the page to show
        :param integer `numpages`: the total pages
        :param integer `zoomscale`: the zoom factor

        :note:
            In the viewer, page range is from 0 to numpages-1, in button controls it
            is from 1 to numpages.

        """
        if self.disabled_controls:
            for item in self.disabled_controls:
                item.Enable(True)
            self.disabled_controls = []
            self.Refresh()

        self.pageno = pagenum + 1
        self.page.ChangeValue('%d' % self.pageno)
        if numpages != self.numpages:
            self.maxlabel.SetLabel('of %d' % numpages)
            self.numpages = numpages
        self.percentzoom = zoomscale * 100
        self.zoom.SetValue('%.0f%%' % self.percentzoom)
        self.zoomtext = self.zoom.GetValue()    # save last good value

    def OnSave(self, event):
        """
        The button handler to save the PDF file.
        """
        self.viewer.Save()

    def OnPrint(self, event):
        """
        The button handler to print the PDF file.
        """
        self.viewer.Print()

    def OnFirst(self, event):
        """
        The button handler to show the first page of the report.
        """
        if self.pageno > 1:
            self.pageno = 1
            self.ChangePage()

    def OnPrev(self, event):
        """
        The button handler to show the previous page of the report.
        """
        if self.pageno > 1:
            self.pageno -= 1
            self.ChangePage()

    def OnNext(self, event):
        """
        The button handler to show the next page of the report.
        """
        if self.pageno < self.numpages:
            self.pageno += 1
            self.ChangePage()

    def OnLast(self, event):
        """
        The button handler to show the last page of the report.
        """
        if self.pageno < self.numpages:
            self.pageno = self.numpages
            self.ChangePage()

    def OnPage(self, event):
        """
        The handler to go to enter page number of the report, if a
        valid number is entered.
        """
        try:
            newpage = int(self.page.GetValue())
            if 1 <= newpage <= self.numpages:
                if newpage != self.pageno:
                    self.pageno = newpage
                    self.ChangePage()
        except ValueError:
            pass
        event.Skip()

    def OnZoomOut(self, event):
        "Decrease page magnification"
        self.viewer.SetZoom(max(0.1, self.percentzoom*0.5/100.0))

    def OnZoomIn(self, event):
        """
        The button handler to zoom in.
        """
        self.viewer.SetZoom(min(self.percentzoom*2/100.0, 10))

    def OnZoomSet(self, event):
        """
        The zoom set handler, either a list selection or a value entered.
        """
        MINZ = 0
        MAXZ = 1000
        newzoom_scale = None
        num =  self.zoom.GetSelection()
        if num >= 0:            # selection from list
            newzoom_scale = self.zoom.GetClientData(num)
        else:                   # combo text
            astring = self.zoom.GetValue().strip().replace('%','')  # ignore percent sign
            try:
                numvalue = float(astring)
                if numvalue < MINZ or numvalue > MAXZ:
                    numvalue = None
            except ValueError:
                numvalue = None
            if numvalue:        # numeric value
                newzoom_scale = numvalue/100.0
            else:               # valid text?
                textvalue = self.zoom.GetValue()
                for k in range(len(self.comboval)):
                    if textvalue.lower() == self.comboval[k][0].lower():
                        newzoom_scale = self.comboval[k][1]
                        break

        if newzoom_scale:
            self.viewer.SetZoom(newzoom_scale)      # will send update to set zoomtext
        else:
            self.zoom.SetValue(self.zoomtext)       # restore last good value
        event.Skip()

    def OnWidth(self, event):
        """
        The button handler to fit display to page width.
        """
        self.viewer.SetZoom(-1)

    def OnHeight(self, event):
        """
        The button handler to fit display to page height.
        """
        self.viewer.SetZoom(-2)

    def ChangePage(self):
        """
        Update viewer with new page number.
        """
        self.viewer.GoPage(self.pageno - 1)

