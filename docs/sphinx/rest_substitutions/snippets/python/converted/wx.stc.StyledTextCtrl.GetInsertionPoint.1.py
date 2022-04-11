
            def GetCurrentChar(self, text_ctrl):

                pos = text_ctrl.GetInsertionPoint()
                if pos == text_ctrl.GetLastPosition():
                    return ''

                return text_ctrl.GetRange(pos, pos + 1)

