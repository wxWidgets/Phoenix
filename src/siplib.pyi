#---------------------------------------------------------------------------
# Name:        wx/siplib.pyi
# Purpose:     Partial type stub for the wx.siplib module, which is the sip
#              runtime module that wxPython's wrapper classes are based on
#
# License:     wxWindows License
#---------------------------------------------------------------------------

from typing import Any

class wrappertype(type): ...

class simplewrapper(metaclass=wrappertype): ...

class wrapper(simplewrapper): ...

def __getattr__(name: str) -> Any: ...
