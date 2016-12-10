import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class log_Tests(wtc.WidgetTestCase):

    def test_log(self):

        class MyLog(wx.Log):
            def __init__(self):
                wx.Log.__init__(self)
                self.messageLogged = False
                self.messages = list()

            def DoLogText(self, message):
                self.messageLogged = True
                self.messages.append(message)

        log = MyLog()
        old = wx.Log.SetActiveTarget(log)
        wx.LogMessage("This is a test")
        self.assertTrue(log.messageLogged)

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
