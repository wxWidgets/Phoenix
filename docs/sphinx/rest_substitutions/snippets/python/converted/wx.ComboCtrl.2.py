
        comboCtrl = wx.ComboCtrl(self, wx.ID_ANY, "")

        popupCtrl = ListViewComboPopup()

        # It is important to call SetPopupControl() as soon as possible
        comboCtrl.SetPopupControl(popupCtrl)

        # Populate using wx.ListView methods
        popupCtrl.InsertItem(popupCtrl.GetItemCount(), "First Item")
        popupCtrl.InsertItem(popupCtrl.GetItemCount(), "Second Item")
        popupCtrl.InsertItem(popupCtrl.GetItemCount(), "Third Item")
