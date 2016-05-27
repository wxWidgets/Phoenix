#!/usr/bin/env python

import wx

import os
import sys
import random

try:
    dirName = os.path.dirname(os.path.abspath(__file__))
except:
    dirName = os.path.dirname(os.path.abspath(sys.argv[0]))

sys.path.append(os.path.split(dirName)[0])

try:
    from agw import genericmessagedialog as GMD
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.genericmessagedialog as GMD

import images


_msg = "This is the about dialog of GenericMessageDialog demo.\n\n" + \
       "Author: Andrea Gavana @ 07 Oct 2008\n\n" + \
       "Please report any bugs/requests of improvements\n" + \
       "to me at the following addresses:\n\n" + \
       "andrea.gavana@gmail.com\n" + "andrea.gavana@maerskoil.com\n\n" + \
       "Welcome to wxPython " + wx.VERSION_STRING + "!!"


ART_ICONS = []
for d in dir(wx):
    if d.startswith('ART_'):
        if not eval('wx.%s'%d).endswith(b'_C'):
            ART_ICONS.append(eval('wx.%s'%d))


class GenericMessageDialogDemo(wx.Panel):

    def __init__(self, parent, log):

        wx.Panel.__init__(self, parent)

        self.log = log

        self.mainPanel = wx.Panel(self)
        self.buttonSizer_staticbox = wx.StaticBox(self.mainPanel, -1, "Buttons Styles")
        self.ok = wx.CheckBox(self.mainPanel, -1, "wx.OK")
        self.yes_no = wx.CheckBox(self.mainPanel, -1, "wx.YES_NO")
        self.cancel = wx.CheckBox(self.mainPanel, -1, "wx.CANCEL")
        self.yes = wx.CheckBox(self.mainPanel, -1, "wx.YES")
        self.no = wx.CheckBox(self.mainPanel, -1, "wx.NO")
        self.no_default = wx.CheckBox(self.mainPanel, -1, "wx.NO_DEFAULT")
        self.help = wx.CheckBox(self.mainPanel, -1, "wx.HELP")
        self.dialogStyles = wx.RadioBox(self.mainPanel, -1, "Dialog Styles",
                                        choices=["wx.ICON_INFORMATION", "wx.ICON_WARNING",
                                                 "wx.ICON_EXCLAMATION", "wx.ICON_ERROR",
                                                 "wx.ICON_QUESTION"],
                                        majorDimension=5, style=wx.RA_SPECIFY_ROWS)
        self.buttonKinds = wx.RadioBox(self.mainPanel, -1, "Button Kind",
                                        choices=["Themed buttons", "AquaButtons",
                                                 "GradientButtons"],
                                        majorDimension=3, style=wx.RA_SPECIFY_ROWS)

        self.useExtended = wx.CheckBox(self.mainPanel, -1, "Add extended message")
        self.customIcons = wx.CheckBox(self.mainPanel, -1, "Use custom icons")

        self.showDialog = wx.Button(self.mainPanel, -1, "Show GenericMessageDialog")

        self.SetProperties()
        self.DoLayout()

        self.Bind(wx.EVT_BUTTON, self.OnShowDialog, self.showDialog)
        self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox)


    def SetProperties(self):

        self.ok.SetValue(1)
        self.dialogStyles.SetSelection(0)
        self.showDialog.SetDefault()


    def DoLayout(self):

        frameSizer = wx.BoxSizer(wx.VERTICAL)
        panelSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonSizer = wx.StaticBoxSizer(self.buttonSizer_staticbox, wx.VERTICAL)

        buttonSizer.Add(self.ok, 0, wx.LEFT|wx.RIGHT|wx.TOP, 5)
        buttonSizer.Add((0, 2), 0, 0, 0)
        buttonSizer.Add(self.yes_no, 0, wx.LEFT|wx.RIGHT, 5)
        buttonSizer.Add((0, 2), 0, 0, 0)
        buttonSizer.Add(self.cancel, 0, wx.LEFT|wx.RIGHT, 5)
        buttonSizer.Add((0, 2), 0, 0, 0)
        buttonSizer.Add(self.yes, 0, wx.LEFT|wx.RIGHT, 5)
        buttonSizer.Add((0, 2), 0, 0, 0)
        buttonSizer.Add(self.no, 0, wx.LEFT|wx.RIGHT, 5)
        buttonSizer.Add((0, 2), 0, 0, 0)
        buttonSizer.Add(self.no_default, 0, wx.LEFT|wx.RIGHT, 5)
        buttonSizer.Add((0, 2), 0, 0, 0)
        buttonSizer.Add(self.help, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        mainSizer.Add(buttonSizer, 0, wx.ALL, 5)
        mainSizer.Add(self.buttonKinds, 0, wx.ALL, 5)
        mainSizer.Add(self.dialogStyles, 0, wx.ALL, 5)
        mainSizer.Add((10, 0), 0, 0, 0)
        mainSizer.Add(self.showDialog, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10)
        mainSizer.Add((10, 0), 0, 0, 0)

        panelSizer.Add(mainSizer, 1, wx.EXPAND)
        panelSizer.Add(self.useExtended, 0, wx.ALL, 15)
        panelSizer.Add(self.customIcons, 0, wx.LEFT|wx.RIGHT, 15)
        panelSizer.Add((0, 0), 1, wx.ALL, 10)

        self.mainPanel.SetSizer(panelSizer)

        frameSizer.Add(self.mainPanel, 1, wx.EXPAND)
        self.SetSizer(frameSizer)
        frameSizer.Layout()


    def OnCheckBox(self, event):

        obj = event.GetEventObject()

        if obj in [self.useExtended, self.customIcons]:
            event.Skip()
            return

        widgets = [self.yes, self.yes_no, self.no, self.no_default]
        if not event.IsChecked():
            return

        if obj == self.ok:
            for checks in widgets:
                checks.SetValue(0)
        elif obj in widgets:
            self.ok.SetValue(0)


    def OnShowDialog(self, event):

        btnStyle = 0
        for child in self.mainPanel.GetChildren():
            if isinstance(child, wx.CheckBox) and child not in [self.useExtended, self.customIcons]:
                if child.GetValue():
                    btnStyle |= eval(child.GetLabel())

        dlgStyle = eval(self.dialogStyles.GetStringSelection())
        buttonKind = self.buttonKinds.GetSelection()

        if buttonKind == 1:
            # Aquabuttons
            dlgStyle += GMD.GMD_USE_AQUABUTTONS
        elif buttonKind == 2:
            # GradientButtons
            dlgStyle += GMD.GMD_USE_GRADIENTBUTTONS

        if self.useExtended:
            extended = _msg
            message = "This is the main message!"
        else:
            extended = ""
            message = _msg

        dlg = GMD.GenericMessageDialog(self, message,
                                       "A Nice Message Box",
                                       btnStyle | dlgStyle)

        if self.customIcons.GetValue():
            b1, b2, b3 = [random.randint(0, len(ART_ICONS)-1) for i in range(3)]
            b4, b5 = [random.randint(0, len(ART_ICONS)-1) for i in range(2)]

            yes    = wx.ArtProvider.GetBitmap(ART_ICONS[b1], wx.ART_OTHER, (16, 16))
            no     = wx.ArtProvider.GetBitmap(ART_ICONS[b2], wx.ART_OTHER, (16, 16))
            cancel = wx.ArtProvider.GetBitmap(ART_ICONS[b3], wx.ART_OTHER, (16, 16))
            ok     = wx.ArtProvider.GetBitmap(ART_ICONS[b4], wx.ART_OTHER, (16, 16))
            help   = wx.ArtProvider.GetBitmap(ART_ICONS[b5], wx.ART_OTHER, (16, 16))

            dlg.SetYesNoCancelBitmaps(yes, no, cancel)
            dlg.SetOKBitmap(ok)
            dlg.SetHelpBitmap(help)

        dlg.SetExtendedMessage(extended)
        dlg.SetIcon(images.Mondrian.GetIcon())
        dlg.ShowModal()
        dlg.Destroy()


#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = GenericMessageDialogDemo(nb, log)
    return win

#----------------------------------------------------------------------

overview = GMD.__doc__

if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])


