
            dt = wx.DateTimeFromDMY(8, 5, 1977)
            y = dt.GetYear()
            epoch = (y > 0 and ["AD"] or ["BC"])[0]
            print "The year is %d%s"%(wx.DateTime.ConvertYearToBC(y), epoch)
