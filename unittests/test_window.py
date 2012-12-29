import imp_unittest, unittest
import wtc
import wx
import wx.lib.six as six

#---------------------------------------------------------------------------

class WindowTests(wtc.WidgetTestCase):
    
    def test_SimpleWindowCtor(self):
        w = wx.Window(self.frame, -1, (10,10), (50,50), 
                      wx.BORDER_SIMPLE|wx.VSCROLL)
        self.assertTrue(w.GetWindowStyle() == wx.BORDER_SIMPLE|wx.VSCROLL)
        self.assertTrue(w.Parent is self.frame)

    def test_windowHandle(self):
        w = wx.Window(self.frame, -1, (10,10), (50,50))
        hdl = w.GetHandle()
        self.assertTrue(isinstance(hdl, six.integer_types))
        
        
    def test_windowProperties(self):
        w = wx.Window(self.frame, -1, (10,10), (50,50))
        # Just test that these properties exist for now. More tests can be
        # added later to ensure that they work correctly.
        w.AcceleratorTable 
        w.AutoLayout 
        w.BackgroundColour 
        w.BackgroundStyle 
        w.EffectiveMinSize 
        w.BestSize 
        w.BestVirtualSize 
        w.Border 
        w.Caret 
        w.CharHeight 
        w.CharWidth 
        w.Children 
        w.ClientAreaOrigin 
        w.ClientRect 
        w.ClientSize 
        w.Constraints 
        w.ContainingSizer 
        w.Cursor 
        w.DefaultAttributes 
        w.DropTarget 
        w.EventHandler 
        w.ExtraStyle 
        w.Font 
        w.ForegroundColour 
        w.GrandParent 
        w.TopLevelParent 
        w.Handle 
        w.HelpText 
        w.Id 
        w.Label 
        w.LayoutDirection 
        w.MaxHeight 
        w.MaxSize 
        w.MaxWidth 
        w.MinHeight 
        w.MinSize 
        w.MinWidth 
        w.Name 
        w.Parent 
        w.Position 
        w.Rect 
        w.ScreenPosition 
        w.ScreenRect 
        w.Size 
        w.Sizer 
        w.ThemeEnabled 
        w.ToolTip 
        w.UpdateClientRect 
        w.UpdateRegion 
        w.Validator 
        w.VirtualSize 
        w.WindowStyle 
        w.WindowStyleFlag 
        w.WindowVariant 
        w.Shown 
        w.Enabled 
        w.TopLevel 
        w.MinClientSize 
        w.MaxClientSize 


    def test_windowFunctions(self):
        wx.FindWindowById
        wx.FindWindowByName
        wx.FindWindowByLabel
    
        self.assertEqual(wx.FindWindowById(self.frame.GetId()),  self.frame)
        
        
#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
