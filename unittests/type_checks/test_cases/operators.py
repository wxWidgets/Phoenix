import wx


# The arguments of operator methods can only be given by position, like at
# runtime
def operators(a: wx.Point, b: wx.Point) -> None:
    a.__eq__(b)
    a == (1, 2)
    a.__eq__(other=b)  # type: ignore[call-arg]  # ty: ignore[positional-only-parameter-as-kwarg]
