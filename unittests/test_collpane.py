import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class CollapsiblePaneTests(wtc.WidgetTestCase):

    def test_CollPaneCtors(self):
        c = wx.CollapsiblePane(self.frame, label='label')
        c = wx.CollapsiblePane(self.frame, -1, 'label', (12, 34), (45, 67))

        c.Collapse()
        c.Expand()
        c.IsCollapsed()
        c.IsExpanded()


    def test_CollPaneDefaultCtor(self):
        c = wx.CollapsiblePane()
        c.Create(self.frame)


    def test_CollPaneProperties(self):
        c = wx.CollapsiblePane(self.frame)

        # do the properties exist?
        c.Pane


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
