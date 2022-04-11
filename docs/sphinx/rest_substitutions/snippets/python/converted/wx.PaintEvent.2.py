
        # Called when window needs to be repainted.
        def OnPaint(self, event):

            dc = wx.PaintDC(self)

            # Find out where the window is scrolled to
            vbX, vbY = self.GetViewStart()

            # get the update rect list
            upd = wx.RegionIterator(self.GetUpdateRegion())

            while upd.HaveRects():

                rect = upd.GetRect()

                # Repaint this rectangle
                PaintRectangle(rect, dc)

                upd.Next()

