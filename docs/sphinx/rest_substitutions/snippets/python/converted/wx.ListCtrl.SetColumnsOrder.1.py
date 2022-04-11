
                listCtrl = wx.ListCtrl(parent, style=wx.LC_REPORT)

                for i in range(3):
                    listCtrl.InsertColumn(i, "Column %d"%i)

                order = [2, 0, 1]
                listCtrl.SetColumnsOrder(order)

                # now listCtrl.GetColumnsOrder() will return order and
                # listCtrl.GetColumnIndexFromOrder(n) will return order[n] and
                # listCtrl.GetColumnOrder() will return 1, 2 and 0 for the column 0,
                # 1 and 2 respectively
