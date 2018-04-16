
            def OnEvent(self, event):

                dc = wx.ClientDC(self)
                self.DoPrepareDC(dc)

                dc.SetPen(wx.BLACK_PEN)

                x, y = event.GetPosition()

                if (xpos > -1 and ypos > -1 and event.Dragging()):
                    dc.DrawLine(xpos, ypos, x, y)

                xpos = x
                ypos = y

