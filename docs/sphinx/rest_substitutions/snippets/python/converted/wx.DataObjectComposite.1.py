
        def MyDropTarget(self):

            dataobj = wx.DataObjectComposite()
            dataobj.Add(wx.BitmapDataObject(), True)
            dataobj.Add(wx.FileDataObject())
            self.SetDataObject(dataobj)


        def OnData(self, x, y, defaultDragResult):

            dragResult = wx.DropTarget.OnData(x, y, defaultDragResult)

            if dragResult == defaultDragResult:
                dataobjComp = self.GetDataObject()

                format = dataObjects.GetReceivedFormat()
                dataobj = dataobjComp.GetObject(format)

                if format.GetType() == wx.DF_BITMAP:
                    dataobjBitmap = dataobj
                    # ... use dataobj.GetBitmap() ...


                elif format.GetType() == wx.DF_FILENAME:
                    dataobjFile = dataobj
                    # ... use dataobj.GetFilenames() ...

                else:
                    raise Exception("unexpected data object format")

            return dragResult

