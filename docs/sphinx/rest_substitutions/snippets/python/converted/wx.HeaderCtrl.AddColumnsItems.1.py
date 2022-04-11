
            def ColumnItems(self):

                menu = wx.Menu()
                menu.Append(100, "Some custom command")
                menu.AppendSeparator()
                self.AddColumnsItems(menu, 200)
                rc = self.GetPopupMenuSelectionFromUser(menu, pt)

                if rc >= 200:
                    # ... toggle visibility of the column rc-200 ...
                    ToggleVisibility()

