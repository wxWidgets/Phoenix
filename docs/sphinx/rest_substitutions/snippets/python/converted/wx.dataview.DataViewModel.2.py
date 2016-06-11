    
            musicCtrl = wx.dataview.DataViewCtrl(self, wx.ID_ANY)
            musicModel = MyMusicModel()
            musicCtrl.AssociateModel(musicModel.get())
    
            # add columns now
