import wx
import wx.grid

class TestFrame(wx.Frame):
    def __init__(self, *args, **kw):
        wx.Frame.__init__(self, *args, **kw)
        self.grid = wx.grid.Grid(self)
        self.grid.CreateGrid(25, 25)
        
        
app = wx.App()
frm = TestFrame(None, title="Simple Test Grid")
frm.Show()
app.MainLoop()

