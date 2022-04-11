
            musicCtrl = wx.dataview.DataViewCtrl(self, wx.ID_ANY)
            musicModel = MyMusicModel()
            musicCtrl.AssociateModel(musicModel)
            musicModel.DecRef()  # avoid memory leak !!

            # add columns now
