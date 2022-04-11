
    # Markup renderer that removes bgcolor attributes when in selection
    class DataViewMarkupRenderer(wx.dataview.DataViewTextRenderer):

        def __init__(self):
            super(DataViewMarkupRenderer, self).__init__()
            self.EnableMarkup()
            self.SetValueAdjuster(DataViewMarkupRenderer._Adjuster())

        class _Adjuster(wx.dataview.DataViewValueAdjuster):
            def MakeHighlighted(self, value):
                pos = value.find(" bgcolor=\"")
                if pos != -1:
                    pos2 = s.find('"', pos + 10)
                    value = value[:pos] + value[pos2+1:]
                return value
