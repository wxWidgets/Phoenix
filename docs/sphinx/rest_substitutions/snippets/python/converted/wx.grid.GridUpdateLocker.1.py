
    def GridLocker(self):

        self.grid = wx.grid.Grid(self, -1)

        noUpdates = wx.grid.GridUpdateLocker(self.grid)
        self.grid.AppendColumn()
        # ... many other operations with self.grid ...
        self.grid.AppendRow()

        # destructor called, grid refreshed
