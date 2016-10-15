#----------------------------------------------------------------------------
# Name:         NavCanvas.py
# Purpose:      Combines FloatCanvas with Navigation controls
#
# Author:
#
# Created:
# Version:
# Date:
# Licence:
# Tags:         phoenix-port, unittest, documented, py3-port
#----------------------------------------------------------------------------
"""
Combines :class:`~lib.floatcanvas.FloatCanvas.FloatCanvas` with Navigation
controls onto a :class:`Panel`


In the following very simple sample ``self`` is a frame, but it could be another
container type control::

    from wx.lib.floatcanvas import NavCanvas, FloatCanvas

    #Add the Canvas
    self.Canvas = NavCanvas.NavCanvas(self, -1,
                                 size=(500, 500),
                                 ProjectionFun=None,
                                 Debug=0,
                                 BackgroundColor="White",
                                 ).Canvas

    # add a circle
    cir = FloatCanvas.Circle((10, 10), 100)
    self.Canvas.AddObject(cir)

    # add a rectangle
    rect = FloatCanvas.Rectangle((110, 10), (100, 100), FillColor='Red')
    self.Canvas.AddObject(rect)

    self.Canvas.Draw()


Many samples are available in the `wxPhoenix/samples/floatcanvas` folder.


"""

import wx
from . import FloatCanvas, Resources, GUIMode

class NavCanvas(wx.Panel):
    """
    :class:`~lib.floatcanvas.NavCanvas.NavCanvas` encloses a
    :class:`~lib.floatcanvas.FloatCanvas.FloatCanvas` in a :class:`Panel` and
    adds a Navigation toolbar.

    """

    def __init__(self,
                 parent,
                 id = wx.ID_ANY,
                 size = wx.DefaultSize,
                 **kwargs):
        """
        Default class constructor.

        :param wx.Window `parent`: parent window. Must not be ``None``;
        :param integer `id`: window identifier. A value of -1 indicates a default value;
        :param `size`: a tuple or :class:`wx.Size`
        :param `**kwargs`: will be passed on to :class:`~lib.floatcanvas.FloatCanvas.FloatCanvas`
        """
        wx.Panel.__init__(self, parent, id, size=size)

        self.Modes = [("Pointer",  GUIMode.GUIMouse(),   Resources.getPointerBitmap()),
                      ("Zoom In",  GUIMode.GUIZoomIn(),  Resources.getMagPlusBitmap()),
                      ("Zoom Out", GUIMode.GUIZoomOut(), Resources.getMagMinusBitmap()),
                      ("Pan",      GUIMode.GUIMove(),    Resources.getHandBitmap()),
                      ]

        self.BuildToolbar()
        ## Create the vertical sizer for the toolbar and Panel
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.ToolBar, 0, wx.ALL | wx.ALIGN_LEFT | wx.GROW, 4)

        self.Canvas = FloatCanvas.FloatCanvas(self, **kwargs)
        box.Add(self.Canvas, 1, wx.GROW)

        self.SetSizerAndFit(box)

        # default to first mode
        #self.ToolBar.ToggleTool(self.PointerTool.GetId(), True)
        self.Canvas.SetMode(self.Modes[0][1])

        return None

    def BuildToolbar(self):
        """
        Build the default tool bar, can be over-ridden in a subclass to add
        extra tools etc.
        """
        tb = wx.ToolBar(self)
        self.ToolBar = tb
        tb.SetToolBitmapSize((24,24))
        self.AddToolbarModeButtons(tb, self.Modes)
        self.AddToolbarZoomButton(tb)
        tb.Realize()
        ## fixme: remove this when the bug is fixed!
        #wx.CallAfter(self.HideShowHack) # this required on wxPython 2.8.3 on OS-X

    def AddToolbarModeButtons(self, tb, Modes):
        """
        Add the mode buttons to the tool bar.

        :param ToolBar `tb`: the toolbar instance
        :param list `Modes`: a list of modes to add, out of the box valid modes
         are subclassed from :class:`~lib.floatcanvas.GUIMode.GUIBase` or modes
         can also be user defined.

        """
        self.ModesDict = {}
        for Mode in Modes:
            tool = tb.AddTool(wx.ID_ANY, label=Mode[0],
                              shortHelp=Mode[0], bitmap=Mode[2],
                              kind=wx.ITEM_RADIO)
            self.Bind(wx.EVT_TOOL, self.SetMode, tool)
            self.ModesDict[tool.GetId()]=Mode[1]
        #self.ZoomOutTool = tb.AddRadioTool(wx.ID_ANY, bitmap=Resources.getMagMinusBitmap(), shortHelp = "Zoom Out")
        #self.Bind(wx.EVT_TOOL, lambda evt : self.SetMode(Mode=self.GUIZoomOut), self.ZoomOutTool)

    def AddToolbarZoomButton(self, tb):
        """
        Add the zoom button to the tool bar.

        :param ToolBar `tb`: the toolbar instance

        """
        tb.AddSeparator()

        self.ZoomButton = wx.Button(tb, label="Zoom To Fit")
        tb.AddControl(self.ZoomButton)
        self.ZoomButton.Bind(wx.EVT_BUTTON, self.ZoomToFit)


    def HideShowHack(self):
        ##fixme: remove this when the bug is fixed!
        """
        Hack to hide and show button on toolbar to get around OS-X bug on
        wxPython2.8 on OS-X
        """
        self.ZoomButton.Hide()
        self.ZoomButton.Show()

    def SetMode(self, event):
        """Event handler to set the mode."""
        Mode = self.ModesDict[event.GetId()]
        self.Canvas.SetMode(Mode)

    def ZoomToFit(self, event):
        """Event handler to zoom to fit."""
        self.Canvas.ZoomToBB()
        self.Canvas.SetFocus() # Otherwise the focus stays on the Button, and wheel events are lost.

