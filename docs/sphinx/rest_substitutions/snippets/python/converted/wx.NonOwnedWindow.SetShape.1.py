
                size = self.GetSize()

                path = wx.GraphicsRenderer.GetDefaultRenderer().CreatePath()
                path.AddCircle(size.x/2, size.y/2, 30)

                self.SetShape(path)
