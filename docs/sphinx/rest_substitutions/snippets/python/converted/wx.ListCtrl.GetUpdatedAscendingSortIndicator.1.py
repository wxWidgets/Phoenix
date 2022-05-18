
    def OnColClick(self, event):
        col = event.GetColumn()
        if col == -1:
            return # clicked outside any column.

        ascending = self.GetUpdatedAscendingSortIndicator(col)
        self.SortItems(self.MyCompareFunction, ascending)
        self.ShowSortIndicator(col, ascending)
