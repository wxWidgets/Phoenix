
        class MyFrame(wx.Frame):

            def __init__(self, parent):

                wx.Frame.__init__(self, parent, title='InfoBar!')

                self.infoBar = wx.InfoBar(self)

                sizer = wx.BoxSizer(wx.VERTICAL)
                sizer.Add(self.infoBar, wx.SizerFlags().Expand())

                # ... add other frame controls to the sizer ...
                self.SetSizer(sizer)


            def SomeMethod(self):

                self.infoBar.ShowMessage("Something happened", wx.ICON_INFORMATION)

