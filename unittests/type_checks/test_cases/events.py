import wx
import wx.grid
from typing_extensions import assert_type


def onCommand(event: wx.CommandEvent) -> None: ...
def onSize(event: wx.SizeEvent) -> None: ...
def onEvent(event: wx.Event) -> None: ...


# Event binders know their type of event, so the handlers given to Bind can
# be checked against it
def binding(frame: wx.Frame, button: wx.Button, grid: wx.grid.Grid) -> None:
    assert_type(wx.EVT_SIZE, wx.PyEventBinder[wx.SizeEvent])
    assert_type(wx.grid.EVT_GRID_CELL_LEFT_CLICK, wx.PyEventBinder[wx.grid.GridEvent])
    frame.Bind(wx.EVT_BUTTON, onCommand, button)
    frame.Bind(wx.EVT_MENU, onCommand, id=wx.ID_EXIT)
    frame.Bind(wx.EVT_SIZE, onSize)
    # Handlers for a base class of the event are fine too
    frame.Bind(wx.EVT_SIZE, onEvent)
    frame.Bind(wx.EVT_SIZE, None)
    grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, lambda event: event.GetRow())
    frame.Unbind(wx.EVT_SIZE, handler=onSize)
    frame.Bind(wx.EVT_SIZE, onCommand)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


# Events made with wx.lib.newevent
def newEvents(frame: wx.Frame) -> None:
    from wx.lib.newevent import NewCommandEvent, NewEvent
    MooEvent, EVT_MOO = NewEvent()
    GooEvent, EVT_GOO = NewCommandEvent()
    wx.PostEvent(frame, MooEvent(moo=1))
    wx.PostEvent(frame, GooEvent(wx.ID_ANY, goo=2))
    frame.Bind(EVT_MOO, lambda event: print(event.moo))
    frame.Bind(EVT_GOO, onCommand)
    frame.Bind(EVT_MOO, onCommand)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]
