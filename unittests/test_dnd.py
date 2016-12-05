import unittest
from unittests import wtc
import wx
import os

icoFile = os.path.join(os.path.dirname(__file__), 'mondrian.ico')
curFile = os.path.join(os.path.dirname(__file__), 'horse.cur')

#---------------------------------------------------------------------------

class dnd_Tests(wtc.WidgetTestCase):

    def test_dnd1(self):
        wx.Drag_CopyOnly
        wx.Drag_AllowMove
        wx.Drag_DefaultMove

        wx.DragError
        wx.DragNone
        wx.DragCopy
        wx.DragMove
        wx.DragLink
        wx.DragCancel


    def test_dndDropTarget(self):
        class MyTarget(wx.DropTarget):
            def OnData(self, x, y, defResult):
                self.GetData()
                return defResult

        dt = MyTarget()
        dt.DefaultAction
        self.frame.SetDropTarget(dt)


    def test_dndDropSource(self):
        ds = wx.DropSource(self.frame)
        if 'wxGTK' in wx.PlatformInfo:
            ds.SetIcon(wx.DragCopy, wx.Icon(icoFile))
        else:
            ds.SetCursor(wx.DragCopy, wx.Cursor(curFile, wx.BITMAP_TYPE_CUR))


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
