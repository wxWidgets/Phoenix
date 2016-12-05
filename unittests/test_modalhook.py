import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class modalhook_Tests(wtc.WidgetTestCase):

    def test_modalhook1(self):
        class MyModalDialogHook(wx.ModalDialogHook):
            def __init__(self):
                wx.ModalDialogHook.__init__(self)
                self.counter = 0

            def Enter(self, dialog):
                self.counter += 1
                return wx.ID_OK

            def Exit(self, dialog):
                self.counter += 1  # not called because Enter didn't return wx.ID_NONE

        myHook = MyModalDialogHook()
        myHook.Register()

        wx.MessageBox("This should be auto-dismissed...", style=wx.OK|wx.CANCEL)
        self.assertEqual(myHook.counter, 1)

        myHook.Unregister()


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
