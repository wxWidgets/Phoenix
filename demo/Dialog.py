#!/usr/bin/env python

import wx

#---------------------------------------------------------------------------
# Create and set a help provider.  Normally you would do this in
# the app's OnInit as it must be done before any SetHelpText calls.
provider = wx.SimpleHelpProvider()
wx.HelpProvider.Set(provider)

#---------------------------------------------------------------------------

class TestDialog(wx.Dialog):
    def __init__(
            self, parent, id, title, size=wx.DefaultSize, pos=wx.DefaultPosition,
            style=wx.DEFAULT_DIALOG_STYLE, name='dialog'
            ):

        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI object using the Create
        # method.
        wx.Dialog.__init__(self)
        self.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        self.Create(parent, id, title, pos, size, style, name)

        # Now continue with the normal construction of the dialog
        # contents
        sizer = wx.BoxSizer(wx.VERTICAL)

        label = wx.StaticText(self, -1, "This is a wx.Dialog")
        label.SetHelpText("This is the help text for the label")
        sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, -1, "Field #1:")
        label.SetHelpText("This is the help text for the label")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        text = wx.TextCtrl(self, -1, "", size=(80,-1))
        text.SetHelpText("Here's some help text for field #1")
        box.Add(text, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, -1, "Field #2:")
        label.SetHelpText("This is the help text for the label")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        text = wx.TextCtrl(self, -1, "", size=(80,-1))
        text.SetHelpText("Here's some help text for field #2")
        box.Add(text, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)

        btnsizer = wx.StdDialogButtonSizer()

        if wx.Platform != "__WXMSW__":
            btn = wx.ContextHelpButton(self)
            btnsizer.AddButton(btn)

        btn = wx.Button(self, wx.ID_OK)
        btn.SetHelpText("The OK button completes the dialog")
        btn.SetDefault()
        btnsizer.AddButton(btn)

        btn = wx.Button(self, wx.ID_CANCEL)
        btn.SetHelpText("The Cancel button cancels the dialog. (Cool, huh?)")
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)

#---------------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        b = wx.Button(self, -1, "Create and Show a custom Dialog", (50,50))
        self.Bind(wx.EVT_BUTTON, self.OnButton, b)

        b = wx.Button(self, -1, "Show dialog with ShowWindowModal", (50, 140))
        self.Bind(wx.EVT_BUTTON, self.OnShowWindowModal, b)
        self.Bind(wx.EVT_WINDOW_MODAL_DIALOG_CLOSED, self.OnWindowModalDialogClosed)


    def OnButton(self, evt):
        dlg = TestDialog(self, -1, "Sample Dialog", size=(350, 200),
                         style=wx.DEFAULT_DIALOG_STYLE,
                         )
        dlg.CenterOnScreen()

        # this does not return until the dialog is closed.
        val = dlg.ShowModal()

        if val == wx.ID_OK:
            self.log.WriteText("You pressed OK\n")
        else:
            self.log.WriteText("You pressed Cancel\n")

        dlg.Destroy()


    def OnShowWindowModal(self, evt):
        dlg = TestDialog(self, -1, "Sample Dialog", size=(350, 200),
                         style=wx.DEFAULT_DIALOG_STYLE)
        dlg.ShowWindowModal()


    def OnWindowModalDialogClosed(self, evt):
        dialog = evt.GetDialog()
        val = evt.GetReturnCode()
        try:
            btnTxt = { wx.ID_OK : "OK",
                       wx.ID_CANCEL: "Cancel" }[val]
        except KeyError:
            btnTxt = '<unknown>'

        wx.MessageBox("You closed the window-modal dialog with the %s button" % btnTxt)

        dialog.Destroy()

#---------------------------------------------------------------------------


def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win


#---------------------------------------------------------------------------


overview = """\
wxPython offers quite a few general purpose dialogs for useful data input from
the user; they are all based on the wx.Dialog class, which you can also subclass
to create custom dialogs to suit your needs.

The Dialog class, in addition to dialog-like behaviors, also supports the full
wxWindows layout featureset, which means that you can incorporate sizers or
layout constraints as needed to achieve the look and feel desired. It even supports
context-sensitive help, which is illustrated in this example.

The example is very simple; in real world situations, a dialog that had input
fields such as this would no doubt be required to deliver those values back to
the calling function. The Dialog class supports data retrieval in this manner.
<b>However, the data must be retrieved prior to the dialog being destroyed.</b>
The example shown here is <i>modal</i>; non-modal dialogs are possible as well.

See the documentation for the <code>Dialog</code> class for more details.

"""

if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

