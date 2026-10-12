#---------------------------------------------------------------------------
# Name:        wx/lib/newevent.pyi
# Purpose:     Type stub for wx.lib.newevent
#
# License:     wxWindows License
#---------------------------------------------------------------------------

from typing import Any, Tuple, Type

import wx

# The event classes are made when NewEvent and NewCommandEvent are called, so
# these stand in for them. Their instances have attributes for the keyword
# arguments they are created with.

class _PyEvent(wx.PyEvent):
    def __init__(self, **kw: Any) -> None: ...
    def __getattr__(self, name: str) -> Any: ...

class _PyCommandEvent(wx.PyCommandEvent):
    def __init__(self, id: int, **kw: Any) -> None: ...
    def __getattr__(self, name: str) -> Any: ...

def NewEvent() -> Tuple[Type[_PyEvent], wx.PyEventBinder[_PyEvent]]: ...
def NewCommandEvent() -> Tuple[Type[_PyCommandEvent], wx.PyEventBinder[_PyCommandEvent]]: ...
