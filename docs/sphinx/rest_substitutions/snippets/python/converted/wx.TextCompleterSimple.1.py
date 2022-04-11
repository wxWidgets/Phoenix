
        class MyTextCompleter(wx.TextCompleterSimple):

            def __init__(self):
                wx.TextCompleterSimple.__init__(self)

            def GetCompletions(self, prefix):
                res = []
                firstWord = prefix.split()[0]

                if firstWord == "white":
                    res.append("white pawn")
                    res.append("white rook")
                elif firstWord == "black":
                    res.append("black king")
                    res.append("black queen")
                else:
                    res.append("white")
                    res.append("black")

                return res


        # Later on...
        text = wx.TextCtrl(parent, wx.ID_ANY, 'My Text')
        text.AutoComplete(MyTextCompleter())

