import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class clipbrd_Tests(wtc.WidgetTestCase):

    def test_clipbrd0(self):
        wx.wxEVT_CLIPBOARD_CHANGED
        wx.EVT_CLIPBOARD_CHANGED


    def test_clipbrd1(self):
        # copy
        data1 = wx.TextDataObject('This is some data.')
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(data1)
            wx.TheClipboard.Close()

        # paste
        data2 = wx.TextDataObject()
        if wx.TheClipboard.Open():
            wx.TheClipboard.GetData(data2)
            wx.TheClipboard.Close()

        self.assertEqual(data2.GetText(), 'This is some data.')
        self.assertEqual(data2.Text, 'This is some data.')


    def test_clpbrd2(self):
        # same, but with the context manager

        # copy
        data1 = wx.TextDataObject('This is some data.')
        with wx.TheClipboard as cb:
            cb.SetData(data1)

        # paste
        data2 = wx.TextDataObject()
        with wx.TheClipboard as cb:
            wx.TheClipboard.GetData(data2)

        self.assertEqual(data2.GetText(), 'This is some data.')
        self.assertEqual(data2.Text, 'This is some data.')

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
