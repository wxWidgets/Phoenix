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


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
