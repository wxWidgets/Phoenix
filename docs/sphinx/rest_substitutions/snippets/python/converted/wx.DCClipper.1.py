
        def MyFunction(dc):

            clip = wx.DCClipper(dc, rect)
            # ... drawing functions here are affected by clipping rect ...


        def OtherFunction():

            dc = wx.DC()
            MyFunction(dc)
            # ... drawing functions here are not affected by clipping rect ...

