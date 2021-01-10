import wx
import wx.adv

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        self.btn = wx.Button(self, -1, "Notify me of something...!", pos=(50,50))
        self.btn.Bind(wx.EVT_BUTTON, self.OnButton)

    def OnButton(self, event):
        notify = wx.adv.NotificationMessage(
            title="This is a Notification!",
            message="wxPython is awesome. Phoenix is awesomer! Python is awesomest!!\n\n"
                    "The quick brown fox jumped over the lazy dog.",
            parent=None, flags=wx.ICON_INFORMATION)

        # Various options can be set after the message is created if desired.
        # notify.SetFlags(# wx.ICON_INFORMATION
        #                 wx.ICON_WARNING
        #                 # wx.ICON_ERROR
        #                 )
        # notify.SetTitle("Wooot")
        # notify.SetMessage("It's a message!")
        # notify.SetParent(self)

        notify.Show(timeout=5) # 1 for short timeout, 100 for long timeout
        # notify.Close()       # Hides the notification.


def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win


#---------------------------------------------------------------------------


overview = """\
This class allows to show the user a message non intrusively.

Currently it is implemented natively for Windows and GTK and
uses (non-modal) dialogs for the display of the notifications
under the other platforms.

The OS X implementation uses Notification Center to display native
notifications. In order to use actions your notifications must use the
alert style. This can be enabled by the user in system settings or by
setting the NSUserNotificationAlertStyle value in Info.plist to alert.
Please note that the user always has the option to change the notification
style.
"""


if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])


