
            class MyEventLoop(wx.EventLoopBase):

                def RunMyLoop(self):

                    loop = MyEventLoop()
                    activate = wx.EventLoopActivator(loop)

                 # other code...

                 # the previously active event loop restored here
