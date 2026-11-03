import unittest
from unittests import wtc
import wx
import wx.adv

#---------------------------------------------------------------------------

class notifmsg_Tests(wtc.WidgetTestCase):

    def test_notifmsg1(self):
        nf = wx.adv.NotificationMessage("The Title", "This is the message")
        nf.Show()
        self.waitFor(300)
        nf.Close()

    def test_notifmsgBinders(self):
        binders = [
            (wx.adv.EVT_NOTIFICATION_MESSAGE_CLICK, wx.adv.wxEVT_NOTIFICATION_MESSAGE_CLICK),
            (wx.adv.EVT_NOTIFICATION_MESSAGE_DISMISSED, wx.adv.wxEVT_NOTIFICATION_MESSAGE_DISMISSED),
            (wx.adv.EVT_NOTIFICATION_MESSAGE_ACTION, wx.adv.wxEVT_NOTIFICATION_MESSAGE_ACTION),
        ]
        for binder, evtType in binders:
            self.assertIsInstance(binder, wx.PyEventBinder)
            self.assertEqual(binder.typeId, evtType)

    # The native implementations only send these events in response to the
    # user or the OS, so simulate them by processing the events directly.
    def test_notifmsgEvents(self):
        nf = wx.adv.NotificationMessage("The Title", "This is the message")
        byUser = int(wx.adv.NotificationMessage.DismissalReason.ByUser)
        received = []
        nf.Bind(wx.adv.EVT_NOTIFICATION_MESSAGE_CLICK,
                lambda evt: received.append(('click', evt.GetId())))
        nf.Bind(wx.adv.EVT_NOTIFICATION_MESSAGE_DISMISSED,
                lambda evt: received.append(('dismissed', evt.GetInt())))
        nf.Bind(wx.adv.EVT_NOTIFICATION_MESSAGE_ACTION,
                lambda evt: received.append(('action', evt.GetId())), id=1001)

        nf.ProcessEvent(wx.CommandEvent(wx.adv.wxEVT_NOTIFICATION_MESSAGE_CLICK))
        evt = wx.CommandEvent(wx.adv.wxEVT_NOTIFICATION_MESSAGE_DISMISSED)
        evt.SetInt(byUser)
        nf.ProcessEvent(evt)
        nf.ProcessEvent(wx.CommandEvent(wx.adv.wxEVT_NOTIFICATION_MESSAGE_ACTION, 1002))
        nf.ProcessEvent(wx.CommandEvent(wx.adv.wxEVT_NOTIFICATION_MESSAGE_ACTION, 1001))

        self.assertEqual(received, [
            ('click', 0),
            ('dismissed', byUser),
            ('action', 1001),
        ])


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
