# This class is used by test_xrc7() in test_xrc.py
import wx


class MyCustomPanel(wx.Panel):
    def __init__(self):
        wx.Panel.__init__(self)
        # the Create step is done by XRC.
        self.Bind(wx.EVT_WINDOW_CREATE, self.OnCreate)
        self.Bind(wx.EVT_SIZE, self.OnSize)


    def OnCreate(self, evt):
        # This is the little bit of customization that we do for this
        # silly example.  It could just as easily have been done in
        # the resource.  We do it in the EVT_WINDOW_CREATE handler
        # because the window doesn't really exist yet in the __init__.
        if self is evt.GetEventObject():
            t = wx.StaticText(self, -1, "MyCustomPanel")
            f = t.GetFont()
            f.SetWeight(wx.BOLD)
            f.SetPointSize(f.GetPointSize()+2)
            t.SetFont(f)
            self.t = t
            # On OSX the EVT_SIZE happens before EVT_WINDOW_CREATE !?!
            # so give it another kick
            wx.CallAfter(self.OnSize, None)
        evt.Skip()

    def OnSize(self, evt):
        if hasattr(self, 't'):
            sz = self.GetSize()
            w, h = self.t.GetTextExtent(self.t.GetLabel())
            self.t.SetPosition(((sz.width-w)//2, (sz.height-h)//2))

