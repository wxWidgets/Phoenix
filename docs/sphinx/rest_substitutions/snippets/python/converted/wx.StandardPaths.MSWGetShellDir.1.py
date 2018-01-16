
            if wx.Platform == '__WXMSW__':
                # get the location of files waiting to be burned on a CD
                cdburnArea = wx.StandardPaths.MSWGetShellDir(CSIDL_CDBURN_AREA)

            # endif __WXMSW__
