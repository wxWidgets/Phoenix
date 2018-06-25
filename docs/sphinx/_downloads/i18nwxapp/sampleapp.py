#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The sample I18N application"""

import os

import wx
import wx.lib.sized_controls as sc

class AppI18N(sc.SizedFrame):
    def __init__(self, parent, **kwds):
        """
        A sample application to demonstrate how to enable I18N support
        """
        super(AppI18N, self).__init__(parent, **kwds)
        self.SetTitle(_(u"The I18N sample application"))

        self.createMenu()
        self.createOtherCtrls()

    def createMenu(self):
        menubar = wx.MenuBar()

        # file menu
        fileMenu = wx.Menu()
        closeMenuItem = fileMenu.Append(wx.ID_ANY,
                                        _(u"Close"),
                                        _(u"Close the application"))
        self.Bind(wx.EVT_MENU, self.onClose, closeMenuItem)
        menubar.Append(fileMenu, _(u"&File"))

        # edit menu
        manageMenu = wx.Menu()
        manageSomethingMenuItem = manageMenu.Append(wx.ID_ANY,
                                            _(u"Edit something"),
                                            _(u"Edit an entry of something"))
        self.Bind(wx.EVT_MENU, self.doEditSomething, manageSomethingMenuItem)

        menubar.Append(manageMenu, _(u"&Edit"))

        # help menu
        helpMenu = wx.Menu()
        aboutMenuItem = helpMenu.Append(wx.ID_ANY,
                                        _(u"&About"),
                                        _(u"About the program"))
        self.Bind(wx.EVT_MENU, self.doAboutBox, aboutMenuItem)
        menubar.Append(helpMenu, _(u"&Help"))

        self.SetMenuBar(menubar)

    def createOtherCtrls(self):
        pane = self.GetContentsPane()

        cPane = sc.SizedPanel(pane)
        cPane.SetSizerType("grid", options={"cols": 2})
        st = wx.StaticText(cPane, wx.ID_ANY,
                           _(u"A nice label for the TextCtrl"))
        st.SetSizerProps(valign='center')
        tc = wx.TextCtrl(cPane, wx.ID_ANY)

        searchSt = wx.StaticText(cPane, wx.ID_ANY,
                            _(u"a search control"))
        searchSt.SetSizerProps(valign='center')
        searchC = wx.SearchCtrl(cPane, wx.ID_ANY)

        sline = wx.StaticLine(pane, wx.ID_ANY)
        sline.SetSizerProps(expand=True)
        bPane = sc.SizedPanel(pane)
        fB = wx.Button(bPane, wx.ID_ANY, _(u"Open a file dialog"))
        fB.SetSizerProps(align="center")
        fB.Bind(wx.EVT_BUTTON, self.onFbButton)

    def onFbButton(self, event):
        wildcard = "Python source (*.py)|*.py|"     \
                   "Compiled Python (*.pyc)|*.pyc|" \
                   "SPAM files (*.spam)|*.spam|"    \
                   "Egg file (*.egg)|*.egg|"        \
                   "All files (*.*)|*.*"

        with wx.FileDialog(
            self, message=_(u"Choose a file"),
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard=wildcard,
            style=wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_CHANGE_DIR
            ) as dlg:

            # Show the dialog and retrieve the user response. If it is the
            # OK response,
            # process the data.
            if dlg.ShowModal() == wx.ID_OK:
                # This returns a Python list of files that were selected.
                paths = dlg.GetPaths()

    def onClose(self, event):
        event.Skip()

    def doEditSomething(self, event):
        event.Skip()

    def doAboutBox(self, event):
        event.Skip()

if __name__ == '__main__':
    import app_base as ab
    app = ab.BaseApp(redirect=False)

    frame = AppI18N(None)
    frame.Show()
    app.MainLoop()
