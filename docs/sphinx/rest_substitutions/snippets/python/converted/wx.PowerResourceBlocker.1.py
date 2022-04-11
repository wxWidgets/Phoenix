    

        blocker = wx.PowerResourceBlocker(
                wx.POWER_RESOURCE_SYSTEM, "Downloading something important")
    
        if not blocker.IsInEffect():
            # If the resource could not be acquired, tell the user that he has
            # to keep the system alive
            wx.LogMessage("Warning: system may suspend while downloading.")
        
    
        # Run an important download and the system will not suspend while downloading
        for i in range(download.size()):
            download.read_byte()

        del blocker
        # wx.POWER_RESOURCE_SYSTEM automatically released here.

