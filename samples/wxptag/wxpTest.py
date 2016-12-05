import sys, os
import wx
import wx.html
import wx.lib.wxpTag

class HtmlWindow(wx.html.HtmlWindow):
    def __init__(self, parent, id, size=(600,400)):
        wx.html.HtmlWindow.__init__(self,parent, id, size=size)

class Frame(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, None, title=title, pos=(150,150), size=(600,400))
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        hwin = HtmlWindow(self, -1, size=(600,400))
        name = os.path.join(os.path.dirname(sys.argv[0]), 'widgetTest.html')
        hwin.LoadPage(name)

        hwin.Bind(wx.EVT_BUTTON, self.OnButton, id=wx.ID_OK)


    def OnClose(self, event):
        self.Destroy()

    def OnButton(self, event):
        print('It works!')


app = wx.App()
top = Frame("wxpTest")
top.Show()
app.MainLoop()


