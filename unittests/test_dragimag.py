import unittest
from unittests import wtc
import wx
import os

pngFile = os.path.join(os.path.dirname(__file__), 'toucan.png')
icoFile = os.path.join(os.path.dirname(__file__), 'mondrian.ico')

#---------------------------------------------------------------------------

class dragimag_Tests(wtc.WidgetTestCase):

    def test_dragimag1(self):
        di = wx.DragImage()

    def test_dragimag2(self):
        di = wx.DragImage(wx.Bitmap(pngFile))

    def test_dragimag3(self):
        di = wx.DragImage(wx.Icon(icoFile))

    def test_dragimag4(self):
        di = wx.DragImage("Some draggable text")

    def test_dragimag5(self):
        ctrl = wx.TreeCtrl(self.frame)
        root = ctrl.AddRoot('root item')
        di = wx.DragImage(ctrl, root)

    def test_dragimag6(self):
        ctrl = wx.ListCtrl(self.frame, style=wx.LC_REPORT)
        ctrl.AppendColumn('hello')
        idx = ctrl.InsertItem(0, "a list item")
        di = wx.DragImage(ctrl, idx)


    def test_genericdragimag1(self):
        di = wx.GenericDragImage()

    def test_genericdragimag2(self):
        di = wx.GenericDragImage(wx.Bitmap(pngFile))

    def test_genericdragimag3(self):
        di = wx.GenericDragImage(wx.Icon(icoFile))

    def test_genericdragimag4(self):
        di = wx.GenericDragImage("Some draggable text")

    def test_genericdragimag5(self):
        ctrl = wx.TreeCtrl(self.frame)
        root = ctrl.AddRoot('root item')
        di = wx.GenericDragImage(ctrl, root)

    def test_genericdragimag6(self):
        ctrl = wx.ListCtrl(self.frame, style=wx.LC_REPORT)
        ctrl.AppendColumn('hello')
        idx = ctrl.InsertItem(0, "a list item")
        di = wx.GenericDragImage(ctrl, idx)

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
