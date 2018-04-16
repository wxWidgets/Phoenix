
          class MyProvider(wx.ArtProvider):

               def CreateBitmap(self, id, client, size):

                   # Your implementation of CreateBitmap here
                   pass


               # optionally override this one as well
               def CreateIconBundle(self, id, client):

                   # Your implementation of CreateIconBundle here
                   pass


          # Later on...
          wx.ArtProvider.Push(MyProvider())
