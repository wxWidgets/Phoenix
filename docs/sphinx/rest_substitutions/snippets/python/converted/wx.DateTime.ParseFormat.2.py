
            dt = wx.DateTime() # Uninitialized datetime
            bDate = "25/12/2012"

            if  dt.ParseFormat(bDate, "%d-%m-%Y") == -1:
                # This datetime format is wrong on purpose
                print "Wrong format"

            elif dt.ParseFormat(bDate, "%d/%m/%Y") >= 0:
                # This is correct
                print "Format OK!", dt

