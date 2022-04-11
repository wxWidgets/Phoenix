
        class MyFrame(wx.Frame):

            def __init__(self, parent):

                wx.Frame.__init__(self, parent)

                self.timer = wx.Timer(self, TIMER_ID)
                self.Bind(wx.EVT_TIMER, self.OnTimer)

                self.timer.Start(1000)    # 1 second interval


            def OnTimer(self, event):

                # do whatever you want to do every second here
                print('Hello')


