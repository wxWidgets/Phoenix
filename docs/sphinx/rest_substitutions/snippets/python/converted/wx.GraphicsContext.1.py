
        def OnPaint(self, event):

            # Create paint DC
            dc = wx.PaintDC(self)

            # Create graphics context from it
            gc = wx.GraphicsContext.Create(dc)

            if gc:

                # make a path that contains a circle and some lines
                gc.SetPen(wx.RED_PEN)
                path = gc.CreatePath()
                path.AddCircle(50.0, 50.0, 50.0)
                path.MoveToPoint(0.0, 50.0)
                path.AddLineToPoint(100.0, 50.0)
                path.MoveToPoint(50.0, 0.0)
                path.AddLineToPoint(50.0, 100.0)
                path.CloseSubpath()
                path.AddRectangle(25.0, 25.0, 50.0, 50.0)

                gc.StrokePath(path)


