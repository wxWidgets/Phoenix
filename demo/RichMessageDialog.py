#!/usr/bin/env python

import wx


class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        self.bannish = False
        self.annoy = True

        b = wx.Button(self, -1, "Create and Show a wx.RichMessageDialog", (50, 50))
        self.Bind(wx.EVT_BUTTON, self.OnButton, b)

    def OnButton(self, event):
        if self.bannish:
            print("That's rich!")
            return

        def DING():
            """Add some audacity...erm annoyance"""
            wx.Bell()

        event.Skip()
        dlg = wx.RichMessageDialog(self, "Hey You! I'm a rich irritating dialog!")
        dlg.ShowDetailedText(("bla bla bla " * 3) + '\n...\n\n' +
                              "Detailed Text(translated) == Don't show the welcome dialog again"
                              "\n(That almost always seems to popup...)")
        dlg.ShowCheckBox("Bannish me forever")
        dlg.ShowModal()  # return value ignored as we have "Ok" only anyhow

        for i in range(0, 10):
            wx.CallLater(500, DING)

        if dlg.IsCheckBoxChecked():
            # ... make sure we won't show it again the next time ...
            self.bannish = True  # Plonk!
            DING()
        dlg.Destroy()


#---------------------------------------------------------------------------


def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win


#---------------------------------------------------------------------------


overview = """\
A RichMessageDialog...
Extension of MessageDialog with additional functionality.

This class adds the possibility of using a checkbox (that is especially useful
for implementing the "Don't ask me again" kind of dialogs) and an extra explanatory
text which is initially collapsed and not shown to the user but can be expanded to
show more information.

Notice that currently the native dialog is used only under MSW when using Vista or
later Windows version. Elsewhere, or for older versions of Windows, a generic
implementation which is less familiar to the users is used. Because of this it's
recommended to use this class only if you do need its extra functionality and use
MessageDialog which does have native implementation under all platforms otherwise.
However if you do need to put e.g. a checkbox in a dialog, you should definitely
consider using this class instead of using your own custom dialog because it will
have much better appearance at least under recent Windows versions.

To use this class, you need to create the dialog object and call ShowCheckBox and/or
ShowDetailedText to configure its contents. Other than that, it is used in exactly
the same way as MessageDialog and supports all the styles supported by it. In particular,
ShowModal return value is the same as for MessageDialog. The only difference is that you
need to use IsCheckBoxChecked to examine the checkbox value if you had called ShowCheckBox.
"""


if __name__ == '__main__':
    import sys
    import os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])
