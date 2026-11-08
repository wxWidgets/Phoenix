
        comboCtrl = wx.ComboCtrl(self, wx.ID_ANY, "")

        popupCtrl = ListCtrlComboPopup()

        # It is important to call SetPopupControl() as soon as possible
        comboCtrl.SetPopupControl(popupCtrl)

        # Populate using the AddItem method of the ListCtrlComboPopup class
        popupCtrl.AddItem("First Item")
        popupCtrl.AddItem("Second Item")
        popupCtrl.AddItem("Third Item")
