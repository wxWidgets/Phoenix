
          # There will normally be a log message if a non-existent file is
          # loaded into a wx.Bitmap.  It can be suppressed with wx.LogNull
          noLog = wx.LogNull()
          bmp = wx.Bitmap('bogus.png')
          # when noLog is destroyed the old log sink is restored
          del noLog
