
            dt = wx.DateTime() # Uninitialized datetime
            bDate = "25/12/2012"

            if not dt.ParseFormat(bDate, "%d-%m-%Y"):
                # This datetime format is wrong on purpose
                print "Wrong format"

            elif dt.ParseFormat(bDate, "%d/%m/%Y"):
                # This is correct
                print "Format OK!", dt

