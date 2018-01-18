
          # Don't try to load the image if it doesn't exist. This avoids the
          # log messages without blocking all the others.
          if os.path.exists('bogus.png'):
              bmp = wx.Bitmap('bogus.png')
          else:
              pass
            # ... do something else here...
