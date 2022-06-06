import unittest
from unittests import wtc
import wx
import os

toolImgFiles = [os.path.join(os.path.dirname(__file__), 'LB01.png'),
                os.path.join(os.path.dirname(__file__), 'LB02.png'),
                os.path.join(os.path.dirname(__file__), 'LB03.png'),
                os.path.join(os.path.dirname(__file__), 'LB04.png'),
                ]

#---------------------------------------------------------------------------

class toolbar_Tests(wtc.WidgetTestCase):

    def test_toolbarStyles(self):
        wx.TOOL_STYLE_BUTTON
        wx.TOOL_STYLE_SEPARATOR
        wx.TOOL_STYLE_CONTROL

        wx.TB_HORIZONTAL
        wx.TB_VERTICAL
        wx.TB_TOP
        wx.TB_LEFT
        wx.TB_BOTTOM
        wx.TB_RIGHT

        wx.TB_FLAT
        wx.TB_DOCKABLE
        wx.TB_NOICONS
        wx.TB_TEXT
        wx.TB_NODIVIDER
        wx.TB_NOALIGN
        wx.TB_HORZ_LAYOUT
        wx.TB_HORZ_TEXT
        wx.TB_NO_TOOLTIPS


    def _populateToolBar(self, tb):
        bmps = [wx.Bitmap(name) for name in toolImgFiles]
        size = bmps[0].GetSize()
        tb.SetToolBitmapSize(size)

        tools = []
        for bmp in bmps:
            tool = tb.AddTool(-1, 'label', wx.BitmapBundle(bmp))
            self.assertTrue(isinstance(tool, wx.ToolBarToolBase))
            tools.append(tool)
        tb.Realize()
        return tools


    def test_toolbar1(self):
        tb = wx.ToolBar(self.frame)
        self._populateToolBar(tb)
        self.frame.SetToolBar(tb)

    def test_toolbar2(self):
        tb = self.frame.CreateToolBar()
        self._populateToolBar(tb)


    def test_toolbarClientData1(self):
        tb = self.frame.CreateToolBar()
        tools = self._populateToolBar(tb)
        # testing client data via the tool object
        tool = tools[0]
        data = "Hobo Joe Is Cool"
        tool.SetClientData(data)
        self.assertEqual(tool.GetClientData(), data)
        self.assertTrue(tool.GetClientData() is data)
        self.assertTrue(tool.ClientData is data)  # property getter
        data = "Hello Phoenix"
        tool.ClientData = data  # testing property setter
        self.assertEqual(tool.GetClientData(), data)


    def test_toolbarClientData2(self):
        tb = self.frame.CreateToolBar()
        assert isinstance(tb, wx.ToolBar)
        tools = self._populateToolBar(tb)
        # testing client data via the toolbar
        toolId = tools[0].GetId()
        data = "Hobo Joe Is Cool"
        tb.SetToolClientData(toolId, data)
        self.assertEqual(tb.GetToolClientData(toolId), data)
        self.assertTrue(tb.GetToolClientData(toolId) is data)


    def test_toolbarTools1(self):
        tb = self.frame.CreateToolBar()
        tools = self._populateToolBar(tb)
        tool = tools[0]

        # Tool properties
        tool.Bitmap
        tool.ClientData
        #tool.Control
        tool.DisabledBitmap
        tool.DropdownMenu
        tool.Id
        tool.Kind
        tool.Label
        tool.LongHelp
        tool.NormalBitmap
        tool.ShortHelp
        tool.Style
        tool.ToolBar


    def test_toolbarTools2(self):
        tb = self.frame.CreateToolBar()
        tools = self._populateToolBar(tb)
        tool = tools[0]
        self.assertEqual(tool.GetToolBar(), tb)

        tool = tb.FindById(tools[1].GetId())
        self.assertEqual(tool.GetToolBar(), tb)


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
