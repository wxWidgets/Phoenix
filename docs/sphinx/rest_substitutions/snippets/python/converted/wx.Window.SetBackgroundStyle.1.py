
        class MyWidget(wx.Window):

            def __init__(self, parent):

                wx.Window.__init__(self) # Use default constructor here!

                # Do this first:
                self.SetBackgroundStyle(wx.BG_STYLE_TRANSPARENT)

                # And really create the window afterwards:
                self.Create(parent)




