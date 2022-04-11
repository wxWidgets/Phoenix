#---------------------------------------------------------------------------
# Name:        etg/pseudodc.py
# Author:      Robin Dunn
#
# Created:     26-Jul-2016
# Copyright:   (c) 2016-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools
from etgtools.extractors import ClassDef, MethodDef, ParamDef


PACKAGE   = "wx"
MODULE    = "_adv"
NAME      = "pseudodc"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ ]

OTHERDEPS = [ 'src/pseudodc.h',
              'src/pseudodc.cpp',
              ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    # The PseudoDC class is not in wxWidgets, so there is no Doxygen XML for
    # them. That means we'll have to construct the extractor objects here,
    # from scratch.

    module.addHeaderCode('#include "pseudodc.h"')
    module.includeCppCode('src/pseudodc.cpp')



    cls = ClassDef(name='wxPseudoDC', bases=['wxObject'],
        briefDoc="""\
            A PseudoDC is an object that can be used much like real
            :class:`wx.DC`, however it provides some additional features for
            object recording and manipulation beyond what a ``wx.DC`` can
            provide.

            All commands issued to the ``PseudoDC`` are stored in a list.  You
            can then play these commands back to a real DC object as often as
            needed, using the :meth:`DrawToDC` method or one of the similar
            methods.  Commands in the command list can be tagged by an ID. You
            can use this ID to clear the operations associated with a single
            ID, redraw the objects associated with that ID, grey them, adjust
            their position, etc.
            """,
        items=[
            # ----------------------------------------------
            # Constructor and Destructor

            MethodDef(name='wxPseudoDC', isCtor=True, items=[],
                briefDoc="""\
                    Constructs a new Pseudo device context for recording and
                    replaying DC operations."""),

            MethodDef(name='~wxPseudoDC', isDtor=True),


            # ----------------------------------------------
            # PseudoDC-specific functionality

            MethodDef(type='void', name='RemoveAll', items=[],
                briefDoc="Removes all objects and operations from the recorded list."),

            MethodDef(type='int', name='GetLen', items=[],
                briefDoc="Returns the number of operations in the recorded list."),

            MethodDef(type='void', name='SetId',
                items=[ParamDef(type='int', name='id')],
                briefDoc="Sets the id to be associated with subsequent operations."),

            MethodDef(type='void', name='ClearId',
                items=[ParamDef(type='int', name='id')],
                briefDoc="Removes all operations associated with id so the object can be redrawn."),

            MethodDef(type='void', name='RemoveId',
                items=[ParamDef(type='int', name='id')],
                briefDoc="Remove the object node (and all operations) associated with an id."),

            MethodDef(type='void', name='TranslateId',
                items=[ParamDef(type='int', name='id'),
                       ParamDef(type='wxCoord', name='dx'),
                       ParamDef(type='wxCoord', name='dy'),
                       ],
                briefDoc="Translate the position of the operations of tag `id` by (`dx`, `dy`)."),

            MethodDef(type='void', name='SetIdGreyedOut',
                items=[ParamDef(type='int', name='id'),
                       ParamDef(type='bool', name='greyout'),
                       ],
                briefDoc="Set whether the set of objects with tag `id` are drawn greyed out or not."),

            MethodDef(type='bool', name='GetIdGreyedOut',
                items=[ParamDef(type='int', name='id')],
                briefDoc="Get whether the set of objects with tag `id` are drawn greyed out or not."),


            MethodDef(type='PyObject*', name='FindObjects',
                items=[ ParamDef(type='wxCoord', name='x'),
                        ParamDef(type='wxCoord', name='y'),
                        ParamDef(type='wxCoord', name='radius', default='1'),
                        ParamDef(type='const wxColour &', name='bg', default='*wxWHITE'),
                        ],
                briefDoc="""\
                    Returns a list of all the id's that draw a pixel with
                    color not equal to bg within radius of (x,y). Returns an
                    empty list if nothing is found.  The list is in reverse
                    drawing order so list[0] is the top id."""),


            MethodDef(type='PyObject*', name='FindObjectsByBBox',
                items=[ ParamDef(type='wxCoord', name='x'),
                        ParamDef(type='wxCoord', name='y')],
                briefDoc="""\
                    Returns a list of all the id's whose bounding boxes include (x,y).
                    Returns an empty list if nothing is found.  The list is in
                    reverse drawing order so list[0] is the top id."""),


            MethodDef(type='void', name='DrawIdToDC',
                items=[ ParamDef(type='int', name='id'),
                        ParamDef(type='wxDC *', name='dc')],
                briefDoc="Draw recorded operations tagged with id to dc."),


            MethodDef(type='void', name='SetIdBounds',
                items=[ ParamDef(type='int', name='id'),
                        ParamDef(type='wxRect &', name='rect')],
                briefDoc="""\
                    Set the bounding rect of a given object.
                    This will create an object node if one doesn't exist."""),


            MethodDef(type='wxRect', name='GetIdBounds',
                items=[ParamDef(type='int', name='id')],
                briefDoc="""\
                    Returns the bounding rectangle previously set with `SetIdBounds`.
                    If no bounds have been set, it returns wx.Rect(0,0,0,0)."""),


            MethodDef(type='void', name='DrawToDCClipped',
                items=[ ParamDef(type='wxDC *', name='dc'),
                        ParamDef(type='const wxRect &', name='rect')],
                briefDoc="""\
                    Draws the recorded operations to dc,
                    unless the operation is known to be outside of rect."""),

            MethodDef(type='void', name='DrawToDCClippedRgn',
                      items=[ParamDef(type='wxDC *', name='dc'),
                             ParamDef(type='const wxRegion &', name='region')],
                      briefDoc="""\
                    Draws the recorded operations to dc,
                    unless the operation is known to be outside the given region."""),

            MethodDef(type='void', name='DrawToDC',
                      items=[ParamDef(type='wxDC *', name='dc')],
                      briefDoc="Draws the recorded operations to dc."),


            #----------------------------------------------
            # Methods which mirror the wxDC API


            MethodDef(type='void', name='FloodFill',
                items=[ ParamDef(type='wxCoord', name='x'),
                        ParamDef(type='wxCoord', name='y'),
                        ParamDef(type='const wxColour &', name='col'),
                        ParamDef(type='wxFloodFillStyle', name='style', default='wxFLOOD_SURFACE')],
                briefDoc="""\
                    Flood fills the device context starting from the given point,
                    using the current brush colour, and using a style:

                        - ``wx.FLOOD_SURFACE``: the flooding occurs until a colour other than the given colour is encountered.

                        - ``wx.FLOOD_BORDER``: the area to be flooded is bounded by the given colour.
                    """,
                overloads=[
                    MethodDef(type='void', name='FloodFill',
                        items=[ ParamDef(type='const wxPoint &', name='pt'),
                                ParamDef(type='const wxColour &', name='col'),
                                ParamDef(type='wxFloodFillStyle', name='style', default='wxFLOOD_SURFACE')]),
                ]),


            MethodDef(type='void', name='DrawLine',
                items=[ ParamDef(type='wxCoord', name='x1'),
                        ParamDef(type='wxCoord', name='y1'),
                        ParamDef(type='wxCoord', name='x2'),
                        ParamDef(type='wxCoord', name='y2')],
                briefDoc="""\
                    Draws a line from the first point to the second.
                    The current pen is used for drawing the line. Note that
                    the second point is *not* part of the line and is not
                    drawn by this function (this is consistent with the
                    behaviour of many other toolkits).
                    """,
                overloads=[
                    MethodDef(type='void', name='DrawLine',
                        items=[ ParamDef(type='const wxPoint &', name='pt1'),
                                ParamDef(type='const wxPoint &', name='pt2')])
                ]),

            MethodDef(type='void', name='CrossHair',
                items=[ ParamDef(type='wxCoord', name='x'),
                        ParamDef(type='wxCoord', name='y')],
                briefDoc="""\
                    Displays a cross hair using the current pen. This is a
                    vertical and horizontal line the height and width of the
                    window, centred on the given point.""",
                overloads=[
                    MethodDef(type='void', name='CrossHair',
                        items=[ ParamDef(type='const wxPoint &', name='pt') ])
                ]),


            MethodDef(type='void', name='DrawArc',
                items=[ ParamDef(type='wxCoord', name='x1'),
                        ParamDef(type='wxCoord', name='y1'),
                        ParamDef(type='wxCoord', name='x2'),
                        ParamDef(type='wxCoord', name='y2'),
                        ParamDef(type='wxCoord', name='xc'),
                        ParamDef(type='wxCoord', name='yc'),],
                briefDoc="""\
                    Draws an arc of a circle, centred on the *center* point
                    (xc, yc), from the first point to the second. The current
                    pen is used for the outline and the current brush for
                    filling the shape.

                    The arc is drawn in an anticlockwise direction from the
                    start point to the end point.
                    """,
                overload=[
                    MethodDef(type='void', name='DrawArc',
                              items=[ParamDef(type='wxCoord', name='x1'),
                                     ParamDef(type='wxCoord', name='xc'),
                                     ParamDef(type='wxCoord', name='yc'), ]),
                    ]),


            MethodDef(type='void', name='DrawCheckMark',
                items=[ ParamDef(type='wxCoord', name='x'),
                        ParamDef(type='wxCoord', name='y'),
                        ParamDef(type='wxCoord', name='width'),
                        ParamDef(type='wxCoord', name='height')],
                briefDoc="Draws a check mark inside the given rectangle",
                overloads=[
                    MethodDef(type='void', name='DrawCheckMark',
                        items=[ ParamDef(type='const wxRect &', name='rect') ])
                    ]),


            MethodDef(type='void', name='DrawEllipticArc',
                items=[ ParamDef(type='wxCoord', name='x'),
                        ParamDef(type='wxCoord', name='y'),
                        ParamDef(type='wxCoord', name='w'),
                        ParamDef(type='wxCoord', name='h'),
                        ParamDef(type='double', name='start'),
                        ParamDef(type='double', name='end')],
                briefDoc="""\
                    Draws an arc of an ellipse, with the given rectangle
                    defining the bounds of the ellipse. The current pen is
                    used for drawing the arc and the current brush is used for
                    drawing the pie.

                    The *start* and *end* parameters specify the start and end
                    of the arc relative to the three-o'clock position from the
                    center of the rectangle. Angles are specified in degrees
                    (360 is a complete circle). Positive values mean
                    counter-clockwise motion. If start is equal to end, a
                    complete ellipse will be drawn.""",
                overloads=[
                    MethodDef(type='void', name='DrawEllipticArc',
                        items=[ ParamDef(type='const wxPoint &', name='pt'),
                                ParamDef(type='const wxSize &', name='sz'),
                                ParamDef(type='double', name='start'),
                                ParamDef(type='double', name='end')])
                    ]),


            MethodDef(type='void', name='DrawPoint',
                items=[ParamDef(type='wxCoord', name='x'),
                       ParamDef(type='wxCoord', name='y')],
                briefDoc="Draws a point using the current pen.",
                overloads=[
                    MethodDef(type='void', name='DrawPoint',
                        items=[ParamDef(type='const wxPoint &', name='pt') ])
                ]),


            MethodDef(type='void', name='DrawRectangle',
                items=[ ParamDef(type='wxCoord', name='x'),
                        ParamDef(type='wxCoord', name='y'),
                        ParamDef(type='wxCoord', name='width'),
                        ParamDef(type='wxCoord', name='height') ],
                briefDoc="""\
                    Draws a rectangle with the given top left corner, and with
                    the given size. The current pen is used for the outline
                    and the current brush for filling the shape.
                    """,
                overloads=[
                    MethodDef(type='void', name='DrawRectangle',
                        items=[ ParamDef(type='const wxRect &', name='rect') ]),
                    MethodDef(type='void', name='DrawRectangle',
                        items=[ ParamDef(type='const wxPoint &', name='pt'),
                                ParamDef(type='const wxSize &', name='sz') ])
                ]),




            MethodDef(type='void', name='DrawRoundedRectangle',
                items=[ ParamDef(type='wxCoord', name='x'),
                        ParamDef(type='wxCoord', name='y'),
                        ParamDef(type='wxCoord', name='width'),
                        ParamDef(type='wxCoord', name='height'),
                        ParamDef(type='double', name='radius')],
                briefDoc="""\
                    Draws a rectangle with the given top left corner, and with
                    the given size. The current pen is used for the outline
                    and the current brush for filling the shape.
                    """,
                overloads=[
                    MethodDef(type='void', name='DrawRoundedRectangle',
                        items=[ ParamDef(type='const wxRect &', name='rect'),
                                ParamDef(type='double', name='radius') ]),
                    MethodDef(type='void', name='DrawRoundedRectangle',
                        items=[ ParamDef(type='const wxPoint &', name='pt'),
                                ParamDef(type='const wxSize &', name='sz'),
                                ParamDef(type='double', name='radius') ])
                ]),


            MethodDef(type='void', name='DrawCircle',
                items=[ ParamDef(type='wxCoord', name='x'),
                        ParamDef(type='wxCoord', name='y'),
                        ParamDef(type='wxCoord', name='radius'),],
                briefDoc="""\
                    Draws a circle with the given center point and radius.
                    The current pen is used for the outline and the current
                    brush for filling the shape.

                    :see: `DrawEllipse`
                    """,
                overloads=[
                    MethodDef(type='void', name='DrawCircle',
                        items=[ ParamDef(type='const wxPoint &', name='pt'),
                                ParamDef(type='wxCoord', name='radius') ]),
                    ]),


            MethodDef(type='void', name='DrawEllipse',
                items=[ ParamDef(type='wxCoord', name='x'),
                        ParamDef(type='wxCoord', name='y'),
                        ParamDef(type='wxCoord', name='width'),
                        ParamDef(type='wxCoord', name='height')],
                briefDoc="""\
                    Draws an ellipse contained in the specified rectangle. The current pen
                    is used for the outline and the current brush for filling the shape.", "

                    :see: `DrawCircle`
                    """,
                overloads=[
                    MethodDef(type='void', name='DrawEllipse',
                        items=[ ParamDef(type='const wxRect &', name='rect') ]),
                    MethodDef(type='void', name='DrawEllipse',
                        items=[ ParamDef(type='const wxPoint &', name='pt'),
                                ParamDef(type='const wxSize &', name='sz') ])
                ]),


            MethodDef(type='void', name='DrawIcon',
                items=[ ParamDef(type='const wxIcon &', name='icon'),
                        ParamDef(type='wxCoord', name='x'),
                        ParamDef(type='wxCoord', name='y')
                        ],
                briefDoc="Draw an icon on the display at the given position.",
                overloads=[
                    MethodDef(type='void', name='DrawIcon',
                              items=[ ParamDef(type='const wxIcon &', name='icon'),
                                      ParamDef(type='const wxPoint &', name='pt') ])
                                     ]),


            MethodDef(type='void', name='DrawBitmap',
                items=[ ParamDef(type='const wxBitmap &', name='bmp'),
                        ParamDef(type='wxCoord', name='x'),
                        ParamDef(type='wxCoord', name='y'),
                        ParamDef(type='bool', name='useMask', default='false') ],
                briefDoc="""\
                    Draw a bitmap on the device context at the specified
                    point. If *useMask* is true and the bitmap has a
                    transparency mask, (or alpha channel on the platforms that
                    support it) then the bitmap will be drawn transparently.

                    When drawing a mono-bitmap, the current text foreground
                    colour will be used to draw the foreground of the bitmap
                    (all bits set to 1), and the current text background
                    colour to draw the background (all bits set to 0).

                    :see: `SetTextForeground`, `SetTextBackground` and `wx.MemoryDC`
                    """,
                overloads=[
                    MethodDef(type='void', name='DrawBitmap',
                        items=[ ParamDef(type='const wxBitmap &', name='bmp'),
                                ParamDef(type='const wxPoint &', name='pt'),
                                ParamDef(type='bool', name='useMask', default='false') ])
                    ]),


            MethodDef(type='void', name='DrawText',
                items=[ ParamDef(type='const wxString &', name='text'),
                        ParamDef(type='wxCoord', name='x'),
                        ParamDef(type='wxCoord', name='y') ],
                briefDoc="""\
                    Draws a text string at the specified point, using the
                    current text font, and the current text foreground and
                    background colours.

                    The coordinates refer to the top-left corner of the
                    rectangle bounding the string. See `wx.DC.GetTextExtent`
                    for how to get the dimensions of a text string, which can
                    be used to position the text more precisely, (you will
                    need to use a real DC with GetTextExtent as wx.PseudoDC
                    does not implement it.)

                    **NOTE**: under wxGTK the current logical function is used
                    *by this function but it is ignored by wxMSW. Thus, you
                    *should avoid using logical functions with this function
                    *in portable programs.", "

                    :see: `DrawRotatedText`
                    """,
                overloads=[
                    MethodDef(type='void', name='DrawText',
                        items=[ ParamDef(type='const wxString &', name='text'),
                                ParamDef(type='const wxPoint &', name='pt') ])
                    ]),


            MethodDef(type='void', name='DrawRotatedText',
                items=[ ParamDef(type='const wxString &', name='text'),
                        ParamDef(type='wxCoord', name='x'),
                        ParamDef(type='wxCoord', name='y'),
                        ParamDef(type='double', name='angle') ],
                briefDoc="Draws the text rotated by *angle* degrees, if supported by the platform.",
                overloads=[
                    MethodDef(type='void', name='DrawRotatedText',
                        items=[ ParamDef(type='const wxString &', name='text'),
                                ParamDef(type='const wxPoint &', name='pt'),
                                ParamDef(type='double', name='angle') ])
                    ]),


            MethodDef(type='void', name='DrawLabel',
                items=[ ParamDef(type='const wxString &', name='text'),
                        ParamDef(type='const wxRect &', name='rect'),
                        ParamDef(type='int', name='alignment', default='wxALIGN_LEFT|wxALIGN_TOP'),
                        ParamDef(type='int', name='indexAccel', default='-1'),
                        ],
                briefDoc="""\
                    Draw *text* within the specified rectangle, abiding by the
                    alignment flags.  Will additionally emphasize the
                    character at *indexAccel* if it is not -1.
                    """,
                overloads=[
                    MethodDef(type='void', name='DrawLabel',
                    items=[ ParamDef(type='const wxString &', name='text'),
                            ParamDef(type='const wxBitmap &', name='image'),
                            ParamDef(type='const wxRect &', name='rect'),
                            ParamDef(type='int', name='alignment', default='wxALIGN_LEFT|wxALIGN_TOP'),
                            ParamDef(type='int', name='indexAccel', default='-1'),
                            ],
                briefDoc="""\
                    Draw *text* and an image (which may be ``wx.NullBitmap`` to skip
                    drawing it) within the specified rectangle, abiding by the alignment
                    flags.  Will additionally emphasize the character at *indexAccel* if
                    it is not -1.
                    """)]
                ),



            MethodDef(type='void', name='Clear',
                items=[],
                briefDoc="Clears the device context using the current background brush.",
                overloads=[]),


            MethodDef(type='void', name='SetFont',
                items=[ ParamDef(type='const wxFont &', name='font') ],
                briefDoc="""\
                    Sets the current font for the DC. It must be a valid font, in
                    particular you should not pass ``wx.NullFont`` to this method.

                    :see: `wx.Font`
                    """,
                overloads=[]),

            MethodDef(type='void', name='SetPen',
                items=[ParamDef(type='const wxPen &', name='pen')],
                briefDoc="""\
                    Sets the current pen for the DC.

                    If the argument is ``wx.NullPen``, the current pen is selected out of the
                    device context, and the original pen restored.

                    :see: `wx.Pen`
                    """,
                overloads=[]),


            MethodDef(type='void', name='SetBrush',
                items=[ParamDef(type='const wxBrush &', name='brush')],
                briefDoc="""\
                    Sets the current brush for the DC.

                    If the argument is ``wx.NullBrush``, the current brush is selected out
                    of the device context, and the original brush restored, allowing the
                    current brush to be destroyed safely.

                    :see: `wx.Brush`
                    """,
                overloads=[]),


            MethodDef(type='void', name='SetBackground',
                items=[ ParamDef(type='const wxBrush &', name='brush') ],
                briefDoc="Sets the current background brush for the DC.",
                overloads=[]),


            MethodDef(type='void', name='SetBackgroundMode',
                items=[ ParamDef(type='int', name='mode') ],
                briefDoc="""\
                    The *mode* parameter may be one of ``wx.SOLID`` and
                    ``wx.TRANSPARENT``. This setting determines whether text
                    will be drawn with a background colour or not.
                    """,
                overloads=[]),


            MethodDef(type='void', name='SetTextForeground',
                items=[ ParamDef(type='const wxColour &', name='colour') ],
                briefDoc="Sets the current text foreground colour for the DC.",
                overloads=[]),


            MethodDef(type='void', name='SetTextBackground',
                items=[ ParamDef(type='const wxColour&', name='colour') ],
                briefDoc="Sets the current text background colour for the DC.",
                overloads=[]),


            MethodDef(type='void', name='SetLogicalFunction',
                items=[ ParamDef(type='wxRasterOperationMode', name='function') ],
                briefDoc="""\
                    Sets the current logical function for the device context. This
                    determines how a source pixel (from a pen or brush colour, combines
                    with a destination pixel in the current device context.

                    The possible values and their meaning in terms of source and
                    destination pixel values are defined in the :ref:`wx.RasterOperationMode`
                    enumeration.

                    The default is wx.COPY, which simply draws with the current
                    colour. The others combine the current colour and the background using
                    a logical operation. wx.INVERT is commonly used for drawing rubber
                    bands or moving outlines, since drawing twice reverts to the original
                    colour.
                    """,
                overloads=[]),


            MethodDef(type='void', name='DrawLines',
                items=[ ParamDef(type='const wxPointList *', name='points'),
                        ParamDef(type='wxCoord', name='xoffset', default='0'),
                        ParamDef(type='wxCoord', name='yoffset', default='0')],
                briefDoc="""\
                    Draws lines using a sequence of `wx.Point` objects, adding the
                    optional offset coordinate. The current pen is used for drawing the
                    lines.
                    """,
                overloads=[]),


            MethodDef(type='void', name='DrawPolygon',
                items=[ ParamDef(type='const wxPointList *', name='points'),
                        ParamDef(type='wxCoord', name='xoffset', default='0'),
                        ParamDef(type='wxCoord', name='yoffset', default='0'),
                        ParamDef(type='wxPolygonFillMode', name='fillStyle', default='wxODDEVEN_RULE'),
                        ],
                briefDoc="""\
                    Draws a filled polygon using a sequence of `wx.Point` objects, adding
                    the optional offset coordinate.  The last argument specifies the fill
                    rule: ``wx.ODDEVEN_RULE`` (the default) or ``wx.WINDING_RULE``.

                    The current pen is used for drawing the outline, and the current brush
                    for filling the shape. Using a transparent brush suppresses
                    filling. Note that wxWidgets automatically closes the first and last
                    points.
                    """,
                overloads=[]),


            MethodDef(type='void', name='DrawSpline',
                items=[ ParamDef(type='const wxPointList *', name='points') ],
                briefDoc="""\
                    Draws a spline between all given control points, (a list of `wx.Point`
                    objects) using the current pen. The spline is drawn using a series of
                    lines, using an algorithm taken from the X drawing program 'XFIG'.
                    """,
                overloads=[]),

        ])

    # add deprecation warnings for the old method names
    cls.addPyCode("""\
        PseudoDC.BeginDrawing = wx.deprecated(lambda *args: None, 'BeginDrawing has been removed.')
        PseudoDC.EndDrawing = wx.deprecated(lambda *args: None, 'EndDrawing has been removed.')
        PseudoDC.FloodFillPoint = wx.deprecated(PseudoDC.FloodFill, 'Use FloodFill instead.')
        PseudoDC.DrawLinePoint = wx.deprecated(PseudoDC.DrawLine, 'Use DrawLine instead.')
        PseudoDC.CrossHairPoint = wx.deprecated(PseudoDC.CrossHair, 'Use CrossHair instead.')
        PseudoDC.DrawArcPoint = wx.deprecated(PseudoDC.DrawArc, 'Use DrawArc instead.')
        PseudoDC.DrawCheckMarkRect = wx.deprecated(PseudoDC.DrawCheckMark, 'Use DrawArc instead.')
        PseudoDC.DrawEllipticArcPointSize = wx.deprecated(PseudoDC.DrawEllipticArc, 'Use DrawEllipticArc instead.')
        PseudoDC.DrawPointPoint = wx.deprecated(PseudoDC.DrawPoint, 'Use DrawPoint instead.')
        PseudoDC.DrawRectangleRect = wx.deprecated(PseudoDC.DrawRectangle, 'Use DrawRectangle instead.')
        PseudoDC.DrawRectanglePointSize = wx.deprecated(PseudoDC.DrawRectangle, 'Use DrawRectangle instead.')
        PseudoDC.DrawRoundedRectangleRect = wx.deprecated(PseudoDC.DrawRoundedRectangle, 'Use DrawRectangle instead.')
        PseudoDC.DrawRoundedRectanglePointSize = wx.deprecated(PseudoDC.DrawRoundedRectangle, 'Use DrawRectangle instead.')
        PseudoDC.DrawCirclePoint = wx.deprecated(PseudoDC.DrawCircle, 'Use DrawCircle instead.')
        PseudoDC.DrawEllipseRect = wx.deprecated(PseudoDC.DrawEllipse, 'Use DrawEllipse instead.')
        PseudoDC.DrawEllipsePointSize = wx.deprecated(PseudoDC.DrawEllipse, 'Use DrawEllipse instead.')
        PseudoDC.DrawIconPoint = wx.deprecated(PseudoDC.DrawIcon, 'Use DrawIcon instead.')
        PseudoDC.DrawBitmapPoint = wx.deprecated(PseudoDC.DrawBitmap, 'Use DrawBitmap instead.')
        PseudoDC.DrawTextPoint = wx.deprecated(PseudoDC.DrawText, 'Use DrawText instead.')
        PseudoDC.DrawRotatedTextPoint = wx.deprecated(PseudoDC.DrawRotatedText, 'Use DrawRotatedText instead.')
        PseudoDC.DrawImageLabel = wx.deprecated(PseudoDC.DrawLabel, 'Use DrawLabel instead.')
        """)



    # Other stuff not wrapped yet
    # // Figure out a good typemap for this...
    # //        Convert the first 3 args from a sequence of sequences?
    # //     void DrawPolyPolygon(int n, int count[], wxPoint points[],
    # //                           wxCoord xoffset = 0, wxCoord yoffset = 0,
    # //                           int fillStyle = wxODDEVEN_RULE);
    #
    #
    # DocDeclStr(
    #     virtual void , SetPalette(const wxPalette& palette),
    #     "If this is a window DC or memory DC, assigns the given palette to the
    #     window or bitmap associated with the DC. If the argument is
    #     ``wx.NullPalette``, the current palette is selected out of the device
    #     context, and the original palette restored.", "
    #
    #     :see: `wx.Palette`");


    module.addItem(cls)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

