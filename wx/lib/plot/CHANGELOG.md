# wx.lib.plot Changelog

This is a log of the changes made to this package in reverse chronological
order.

Attempts were made to maintain previous contributors' attributions, but some
things may have been lost in transition. If a mistake is found, please
submit a PR to correct it.

The `wx.lib.plot` code used to be a module. Conversion to a package began
on 2016-07-05 and finished on [insert date here].


## 2016-07-05 (Start) - Douglas Thor (doug.thor@gmail.com) (PR #)
+ Converted module to package.
+ Separated out changelog and readme to separate files.
+ Changed cursors to use the built-ins rather than PyEmbeddedImage.
+ Moved PlotCanvas class to separate plotcanvas.py module
+ Moved demo to examples/demo; added simple_example.py
+ package now callable via `python -m wx.lib.plot`: runs demo.
+ Moved PendingDeprecation, TempSytle to utils.py
+ Renamed `BoxPlot` to `PolyBoxPlot`.


## 2016-06-14 (Start) - Douglas Thor (doug.thor@gmail.com) (PR #98)
+ Refactored PolyBars and PolyHistogram to PolyBarsBase class
+ Replaced `SaveBrush` et. al., with more generic `TempStyle` combination
  Context Manager and Decorator.
+ Removed `eval` in PolyMarkers._drawmarkers
+ Refactored EnableAxes, EnableAxesValues, and EnableTicks, as they all used
  the same core logic.
+ Replaced some instances of dc.DrawText with dc.DrawTextList
+ Various cleanups of math, line character limits, and PEP8-ing
+ Updated/Added a bunch of Sphinx-compatible documentation
+ NaN is now handled (ignored) in BoxPlot.


## 2016-05-27 - Douglas Thor (doug.thor@gmail.com) (PR #91)
+ Added PolyBars and PolyHistogram classes
+ General Cleanup
+ Added demos for PolyBars and PolyHistogram
+ updated plotNN menu items status-bar text to be descriptive.
+ increased default size of demo
+ updated xSpec and ySpec to accept a list or tuple of (min, max) values.


## 2015-08-20 - Douglas Thor (doug.thor@gmail.com) (PR #26)
+ Implemented a drawstyle option to PolyLine that mimics matplotlib's
  Line2dD.drawstyle option.
+ Added significant customization options to PlotCanvas
  - Gridlines, Axes, Centerline, diagonal, and ticks can now have
    their Pen (color, width, and linestyle) set independently.
  - Ticks, Axes, and AxesValues can now be turned on/off for each side.
+ Added properties to replace getters/setters.
+ All getters and setters now have deprecation warnings
+ Fixed python3 FutureWarning for instances of 'x == None' (replaced with
  'x is None')
+ Documentation updates
+ Added Box Plot
+ Added context manager and decorator that gets and resets the pen before
  and after a function call
+ updated demo for new features
+ Most items are now allow custom pens (color, width, linestyle)
+ Added 'drawstyle' option to PolyLine that mimics MatPlotLib's
  Line2dD.drawstyle option.


## 2009-06-22 - Florian Hoech (florian.hoech@gmx.de)
+ Fixed exception when drawing empty plots on Mac OS X
+ Fixed exception when trying to draw point labels on Mac OS X (Mac OS X
  point label drawing code is still slow and only supports wx.COPY)
+ Moved label positions away from axis lines a bit
+ Added PolySpline class and modified demo 1 and 2 to use it
+ Added center and diagonal lines option (Set/GetEnableCenterLines,
  Set/GetEnableDiagonals)
+ Added anti-aliasing option with optional high-resolution mode
  (Set/GetEnableAntiAliasing, Set/GetEnableHiRes) and demo
+ Added option to specify exact number of tick marks to use for each axis
  (SetXSpec(<number>, SetYSpec(<number>) -- work like 'min', but with
  <number> tick marks)
+ Added support for background and foreground colours (enabled via
  SetBackgroundColour/SetForegroundColour on a PlotCanvas instance)
+ Changed PlotCanvas printing initialization from occurring in __init__ to
  occur on access. This will postpone any IPP and / or CUPS warnings
  which appear on stderr on some Linux systems until printing
  functionality is actually used.


## 2004-08-15 - Gordon Williams (g_will@cyberus.ca)
+ Imported modules given leading underscore to name.
+ Added Cursor Line Tracking and User Point Labels.
+ Demo for Cursor Line Tracking and Point Labels.
+ Size of plot preview frame adjusted to show page better.
+ Added helper functions PositionUserToScreen and PositionScreenToUser
  in PlotCanvas.
+ Added functions GetClosestPoints (all curves) and GetClosestPoint (only
  closest curve) can be in either user coords or screen coords.


## 2004-08-06 - Gordon Williams (g_will@cyberus.ca)
+ Added bar graph demo
+ Modified line end shape from round to square.
+ Removed FloatDCWrapper for conversion to ints and ints in arguments


## 2003-12-18 - Jeff Grimmett (grimmtooth@softhome.net)
+ wxScrolledMessageDialog -> ScrolledMessageDialog


## 2003-12-15 - Jeff Grimmett (grimmtooth@softhome.net)
+ 2.5 compatibility update.
+ Renamed to plot.py in the wx.lib directory.
+ Reworked test frame to work with wx demo framework. This saves a bit
  of tedious cut and paste, and the test app is excellent.


## 2003-02-?? - Gordon Williams (g_will@cyberus.ca)
+ More style options
+ Zooming using mouse "rubber band"
+ Scroll left, right
+ Grid(graticule)
+ Printing, preview, and page set up (margins)
+ Axis and title labels
+ Cursor xy axis values
+ Doc strings and lots of comments
+ Optimizations for large number of points
+ Legends
+ Did a lot of work here to speed markers up. Only a factor of 4
  improvement though. Lines are much faster than markers, especially
  filled markers.  Stay away from circles and triangles unless you
  only have a few thousand points.

  ```
  +--------------------------------------------+
  | Times for 25,000 points                    |
  +============================================+
  | Line                             | 0.078 s |
  +----------------------------------+---------+
  | Markers: Square                  | 0.22 s  |
  +----------------------------------+---------+
  | Markers: dot                     | 0.10    |
  +----------------------------------+---------+
  | Markers: circle                  | 0.87    |
  +----------------------------------+---------+
  | Markers: cross, plus             | 0.28    |
  +----------------------------------+---------+
  | Markers: triangle, triangle_down | 0.90    |
  +----------------------------------+---------+
  ```
+ Thanks to Chris Barker for getting this version working on Linux.
