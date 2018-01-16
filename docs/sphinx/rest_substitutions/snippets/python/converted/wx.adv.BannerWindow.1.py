
        class MyFrame(wx.Frame):

            def __init__(self, parent):

                # ... create the frame itself ...
                wx.Frame.__init__(self, parent)

                # Create and initialize the banner.
                banner = wx.adv.BannerWindow(self, wx.TOP)
                banner.SetText("Welcome to my wonderful program",
                               "  Before doing anything else, you need to connect to "
                               "the online server.\n"
                               "  Please enter your credentials in the controls below.")

                # And position it along the left edge of the window.
                sizer = wx.BoxSizer(wx.VERTICAL)
                sizer.Add(banner, wx.SizerFlags().Expand())

                # ... add the rest of the window contents to the same sizer ...

                self.SetSizerAndFit(sizer)

