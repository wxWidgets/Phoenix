
    class MyClass(public BaseClass): # something inheriting from wx.EvtHandler

    ...
        def TryAfter(self, event):
            if (BaseClass.TryAfter(self, event))
                return True

            return self.MyPostProcess(event)

