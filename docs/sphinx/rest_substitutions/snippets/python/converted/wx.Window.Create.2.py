
    # Suppose we have this factory function in another module.
    def MyCreateWindowObjectFunction()
        return MyCustomClassDerivingFromWindow()


    # Then we can create a window of MyCustomClassDerivingFromWindow
    # class without really knowing about this type, as we would have
    # to do if we wanted to use the non-default constructor, like this:

    # First create the object using the factory function.
    window = MyCreateWindowObjectFunction()

    # And now create the underlying window, perhaps after doing
    # some other stuff first.
    window.Create(parent, wx.ID_ANY, ...)
