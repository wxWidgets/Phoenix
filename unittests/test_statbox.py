import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class statbox_Tests(wtc.WidgetTestCase):

    def test_statboxCtor(self):
        s = wx.StaticBox(self.frame, label='StaticBox')

    def test_statboxDefaultCtor(self):
        s = wx.StaticBox()
        s.Create(self.frame, label='StaticBox')

    def test_statboxGetBordersForSizer(self):
        s = wx.StaticBox(self.frame, label='StaticBox')
        topBorder, otherBorder = s.GetBordersForSizer()
        assert isinstance(topBorder, int)
        assert isinstance(otherBorder, int)
        assert topBorder >= 0
        assert otherBorder >= 0

    @unittest.skipIf(not wx.HAS_WINDOW_LABEL_IN_STATIC_BOX, 'window labels are not supported')
    def test_statboxWindowLabel(self):
        cb = wx.CheckBox(self.frame, label='CheckBox')
        s = wx.StaticBox(self.frame, wx.ID_ANY, cb)
        assert isinstance(s, wx.StaticBox)
        s.Enable(False)
        assert cb.IsEnabled()

    @unittest.skipIf(not wx.HAS_WINDOW_LABEL_IN_STATIC_BOX, 'window labels are not supported')
    def test_statboxWindowLabelCreate(self):
        cb = wx.CheckBox(self.frame, label='CheckBox')
        s = wx.StaticBox()
        assert s.Create(self.frame, wx.ID_ANY, cb)

    @unittest.skipIf(not wx.HAS_WINDOW_LABEL_IN_STATIC_BOX, 'window labels are not supported')
    def test_statboxWindowLabelSubclass(self):
        class MyStaticBox(wx.StaticBox):
            pass
        cb = wx.CheckBox(self.frame, label='CheckBox')
        s = MyStaticBox(self.frame, wx.ID_ANY, cb)
        assert isinstance(s, MyStaticBox)

    @unittest.skipIf(wx.HAS_WINDOW_LABEL_IN_STATIC_BOX, 'window labels are supported')
    def test_statboxWindowLabelNotImplemented(self):
        cb = wx.CheckBox(self.frame, label='CheckBox')
        with self.assertRaises(NotImplementedError):
            wx.StaticBox(self.frame, wx.ID_ANY, cb)
        with self.assertRaises(NotImplementedError):
            wx.StaticBox().Create(self.frame, wx.ID_ANY, cb)

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
