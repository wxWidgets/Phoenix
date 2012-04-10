    
        class MyWidget(wx.Window):

            def __init__(self, parent):    

                pre = wx.PreWindow() # Use Pre- constructor here!
            
                # Do this first:
                self.SetBackgroundStyle(wx.BG_STYLE_TRANSPARENT)

                # And really create the window afterwards:
                pre.Create(parent)
                self.PostCreate(pre)

        
                    
                
