import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class srchctrl_Tests(wtc.WidgetTestCase):

    def test_srchctrlCtor(self):
        t = wx.SearchCtrl(self.frame)

    def test_srchctrlDefaultCtor(self):
        t = wx.SearchCtrl()
        t.Create(self.frame)

    def test_srchctrlProperties(self):
        t = wx.SearchCtrl(self.frame)
        t.Menu
        t.SearchButtonVisible
        t.CancelButtonVisible
        t.DescriptiveText

        # these are grafted-on methods, just make sure that they are there
        t.SetSearchBitmap
        t.SetSearchMenuBitmap
        t.SetCancelBitmap

    def test_srchctrlEventBinding(self):
        t = wx.SearchCtrl(self.frame)
        self.frame.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, lambda e: None, t)
        self.frame.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, lambda e: None, t)


    def test_srchctrlGetSetValue(self):
        t = wx.SearchCtrl(self.frame)
        t.SetValue('Hello')
        self.assertEqual(t.GetValue(), 'Hello')
        self.assertEqual(t.Value, 'Hello')


    def test_srchctrlHasTextCtrlMethods(self):
        # Just ensure that the common TextCtrl methods are present. This is
        # done because although the C++ class either derives from wxTextCtrl
        # or from wxTextCtrlIface, we have to kludge it up a bit since the
        # actual class hierarchies are different between platforms. See
        # etg/srchctrl.py for details.

        t = wx.SearchCtrl(self.frame)
        t.Cut
        t.CanCut
        t.IsEditable
        t.HitTest
        t.AppendText
        t.WriteText
        t.ChangeValue



#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
