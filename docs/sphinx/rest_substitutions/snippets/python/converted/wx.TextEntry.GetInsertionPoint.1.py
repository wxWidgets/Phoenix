
            def GetCurrentChar(textCtrl):

                pos = textCtrl.GetInsertionPoint()

                if pos == textCtrl.GetLastPosition():
                    return ''

                return textCtrl.GetValue()[pos]

