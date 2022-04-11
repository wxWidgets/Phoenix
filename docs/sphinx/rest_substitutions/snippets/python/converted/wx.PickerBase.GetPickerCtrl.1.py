
                if wx.Platform == '__WXMSW__':
                    # wxMSW is one of the platforms where the generic implementation
                    # of wx.FilePickerCtrl is used...

                    pButt = myFilePickerCtrl.GetPickerCtrl()

                    if pButt is not None:
                        pButt.SetLabel('Custom browse string')

