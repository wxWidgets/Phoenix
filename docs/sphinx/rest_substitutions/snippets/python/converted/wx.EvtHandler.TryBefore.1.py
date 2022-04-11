
    class MyClass(BaseClass):  # something inheriting from wx.EvtHandler

    ...
        def TryBefore(self, event):
            if (self.MyPreProcess(event)):
                return True

            return BaseClass.TryBefore(self, event)

