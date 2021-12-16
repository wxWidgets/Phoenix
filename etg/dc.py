#---------------------------------------------------------------------------
# Name:        etg/stattext.py
# Author:      Kevin Ollivier
#              Robin Dunn
#
# Created:     26-Aug-2011
# Copyright:   (c) 2011 by Wide Open Technologies
# Copyright:   (c) 2011-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

from textwrap import dedent

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "dc"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxFontMetrics',
           'wxDC',
           'wxDCClipper',
           'wxDCBrushChanger',
           'wxDCPenChanger',
           'wxDCTextColourChanger',
           'wxDCFontChanger',
           'wxDCTextBgColourChanger',
           'wxDCTextBgModeChanger',
           ]

OTHERDEPS = [ 'src/dc_ex.cpp', ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxDC')
    assert isinstance(c, etgtools.ClassDef)
    c.mustHaveApp()

    c.addPrivateCopyCtor()
    c.addPublic()
    tools.removeVirtuals(c)

    c.addDtor('public', True)

    # Keep only the wxSize overloads of these
    c.find('GetSize').findOverload('wxCoord').ignore()
    c.find('GetSizeMM').findOverload('wxCoord').ignore()

    # TODO: needs wxAffineMatrix2D support.
    #c.find('GetTransformMatrix').ignore()
    #c.find('SetTransformMatrix').ignore()

    # remove wxPoint* overloads, we use the wxPointList ones
    c.find('DrawLines').findOverload('wxPoint points').ignore()
    c.find('DrawPolygon').findOverload('wxPoint points').ignore()
    c.find('DrawSpline').findOverload('wxPoint points').ignore()

    # TODO: we'll need a custom method implementation for this since there
    # are multiple array parameters involved...
    c.find('DrawPolyPolygon').ignore()


    # Add output param annotations so the generated docstrings will be correct
    c.find('GetUserScale.x').out = True
    c.find('GetUserScale.y').out = True

    c.find('GetLogicalScale.x').out = True
    c.find('GetLogicalScale.y').out = True

    c.find('GetLogicalOrigin').overloads = []
    c.find('GetLogicalOrigin.x').out = True
    c.find('GetLogicalOrigin.y').out = True

    c.find('GetClippingBox').findOverload('wxRect').ignore()
    c.find('GetClippingBox.x').out = True
    c.find('GetClippingBox.y').out = True
    c.find('GetClippingBox.width').out = True
    c.find('GetClippingBox.height').out = True
    c.addPyMethod('GetClippingRect', '(self)',
        doc="Returns the rectangle surrounding the current clipping region as a wx.Rect.",
        body="""\
            rv, x, y, w, h = self.GetClippingBox()
            return wx.Rect(x,y,w,h)
            """)


    # Deal with the text-extent methods. In Classic we renamed one overloaded
    # method with a "Full" name, and the simpler one was left with the
    # original name.  I think a simpler approach here will be to remove the
    # simple version, rename the Full version as before, and then add a
    # CppMethod to reimplement the simple version.

    for name in ['GetTextExtent', 'GetMultiLineTextExtent']:
        m = c.find(name)
        # if these fail then double-check order of parsed methods, etc.
        assert len(m.overloads) == 1
        assert 'wxCoord' not in m.overloads[0].argsString
        m.overloads = []

    c.find('GetTextExtent').pyName = 'GetFullTextExtent'
    c.find('GetMultiLineTextExtent').pyName = 'GetFullMultiLineTextExtent'

    # Set output parameters
    c.find('GetTextExtent.w').out = True
    c.find('GetTextExtent.h').out = True
    c.find('GetTextExtent.descent').out = True
    c.find('GetTextExtent.externalLeading').out = True

    c.find('GetMultiLineTextExtent.w').out = True
    c.find('GetMultiLineTextExtent.h').out = True
    c.find('GetMultiLineTextExtent.heightLine').out = True


    # Update the docs to remove references to overloading, pointer values, etc.
    m = c.find('GetTextExtent')
    m.briefDoc = "Gets the dimensions of the string as it would be drawn."
    m.detailedDoc = [dedent("""\
        The ``string`` parameter is the string to measure.  The return value
        is a tuple of integer values consisting of ``widget``, ``height``,
        ``decent`` and ``externalLeading``. The ``descent`` is the dimension
        from the baseline of the font to the bottom of the descender, and
        ``externalLeading`` is any extra vertical space added to the font by the
        font designer (usually is zero).

        If the optional parameter ``font`` is specified and valid, then it is
        used for the text extent calculation. Otherwise the currently selected
        font is.

        .. seealso:: :class:`wx.Font`, :meth:`~wx.DC.SetFont`,
           :meth:`~wx.DC.GetPartialTextExtents, :meth:`~wx.DC.GetMultiLineTextExtent`
        """)]

    m = c.find('GetMultiLineTextExtent')
    m.briefDoc = "Gets the dimensions of the string as it would be drawn."
    m.detailedDoc = [dedent("""\
        The ``string`` parameter is the string to measure.  The return value
        is a tuple of integer values consisting of ``widget``, ``height`` and
        ``heightLine``.  The ``heightLine`` is the the height of a single line.

        If the optional parameter ``font`` is specified and valid, then it is
        used for the text extent calculation. Otherwise the currently selected
        font is.

        .. note:: This function works with both single-line and multi-line strings.

        .. seealso:: :class:`wx.Font`, :meth:`~wx.DC.SetFont`,
           :meth:`~wx.DC.GetPartialTextExtents, :meth:`~wx.DC.GetTextExtent`
        """)]

    # Now add the simpler versions of the extent methods
    c.addCppMethod('wxSize*', 'GetTextExtent', '(const wxString& st)', isConst=True,
        doc=dedent("""\
            Return the dimensions of the given string's text extent using the
            currently selected font.

            :param st: The string to be measured

            .. seealso:: :meth:`~wx.DC.GetFullTextExtent`
            """),
        body="""\
            return new wxSize(self->GetTextExtent(*st));
            """,
        overloadOkay=False, factory=True)

    c.addCppMethod('wxSize*', 'GetMultiLineTextExtent', '(const wxString& st)', isConst=True,
        doc=dedent("""\
            Return the dimensions of the given string's text extent using the
            currently selected font, taking into account multiple lines if
            present in the string.

            :param st: The string to be measured

            .. seealso:: :meth:`~wx.DC.GetFullMultiLineTextExtent`
            """),
        body="""\
            return new wxSize(self->GetMultiLineTextExtent(*st));
            """,
        overloadOkay=False, factory=True)




    # Add some alternate implementations for other DC methods, in order to
    # avoid using parameters as return values, etc. as well as Classic
    # compatibility.
    c.find('GetPixel').ignore()
    c.addCppMethod('wxColour*', 'GetPixel', '(wxCoord x, wxCoord y)',
        doc="""\
            Gets the colour at the specified location on the DC.

            This method isn't available for ``wx.PostScriptDC`` or ``wx.MetafileDC`` nor
            for any DC in wxOSX port, and simply returns ``wx.NullColour`` there.

            .. note:: Setting a pixel can be done using DrawPoint().

            .. note:: This method shouldn't be used with ``wx.PaintDC`` as accessing the
                      DC while drawing can result in unexpected results, notably in wxGTK.
            """,
        body="""\
            wxColour* col = new wxColour;
            self->GetPixel(x, y, col);
            return col;
            """,
        factory=True)

    # Return the rect instead of using an output parameter
    m = c.find('DrawLabel').findOverload('rectBounding')
    m.type = 'wxRect*'
    m.find('rectBounding').ignore()
    m.factory = True  # a new instance of wxRect is being created
    m.setCppCode("""\
        wxRect rv;
        self->DrawLabel(*text, *bitmap, *rect, alignment, indexAccel, &rv);
        return new wxRect(rv);
        """)
    c.addPyCode('DC.DrawImageLabel = wx.deprecated(DC.DrawLabel, "Use DrawLabel instead.")')


    # Return the array instead of using an output parameter
    m = c.find('GetPartialTextExtents')
    m.type = 'wxArrayInt*'
    m.find('widths').ignore()
    m.factory = True  # a new instance is being created
    m.setCppCode("""\
        wxArrayInt rval;
        self->GetPartialTextExtents(*text, rval);
        return new wxArrayInt(rval);
        """)


    c.addCppMethod('int', '__nonzero__', '()', "return self->IsOk();")
    c.addCppMethod('int', '__bool__', '()', "return self->IsOk();")

    c.addPyMethod('GetBoundingBox', '(self)', doc="""\
        GetBoundingBox() -> (x1,y1, x2,y2)\n
        Returns the min and max points used in drawing commands so far.""",
        body="return (self.MinX(), self.MinY(), self.MaxX(), self.MaxY())")


    m = c.find('GetHandle')
    m.type = 'wxUIntPtr*'
    m.setCppCode("return new wxUIntPtr((wxUIntPtr)self->GetHandle());")


    c.addCppMethod('long', 'GetHDC', '()', """\
        #ifdef __WXMSW__
            return HandleToLong(self->GetHandle());
        #else
            wxPyRaiseNotImplemented();
            return 0;
        #endif""")
    c.addCppMethod('wxUIntPtr*', 'GetCGContext', '()', """\
        #ifdef __WXMAC__
            return new wxUIntPtr((wxUIntPtr)self->GetHandle());
        #else
            wxPyRaiseNotImplemented();
            return NULL;
        #endif""")
    c.addCppMethod('wxUIntPtr*', 'GetGdkDrawable', '()', """\
        #ifdef __WXGTK__
            return new wxUIntPtr((wxUIntPtr)self->GetHandle());
        #else
            wxPyRaiseNotImplemented();
            return NULL;
        #endif""")

    c.addPyCode('DC.GetHDC = wx.deprecated(DC.GetHDC, "Use GetHandle instead.")')
    c.addPyCode('DC.GetCGContext = wx.deprecated(DC.GetCGContext, "Use GetHandle instead.")')
    c.addPyCode('DC.GetGdkDrawable = wx.deprecated(DC.GetGdkDrawable, "Use GetHandle instead.")')

    # context manager methods
    c.addPyMethod('__enter__', '(self)', 'return self')
    c.addPyMethod('__exit__', '(self, exc_type, exc_val, exc_tb)', 'self.Destroy()')


    # This file contains implementations of functions for quickly drawing
    # lists of items on the DC. They are called from the CppMethods defined
    # below, which in turn are called from the PyMethods below that.
    c.includeCppCode('src/dc_ex.cpp')

    c.addCppMethod('PyObject*', '_DrawPointList', '(PyObject* pyCoords, PyObject* pyPens, PyObject* pyBrushes)',
        body="return wxPyDrawXXXList(*self, wxPyDrawXXXPoint, pyCoords, pyPens, pyBrushes);")

    c.addCppMethod('PyObject*', '_DrawLineList', '(PyObject* pyCoords, PyObject* pyPens, PyObject* pyBrushes)',
        body="return wxPyDrawXXXList(*self, wxPyDrawXXXLine, pyCoords, pyPens, pyBrushes);")

    c.addCppMethod('PyObject*', '_DrawRectangleList', '(PyObject* pyCoords, PyObject* pyPens, PyObject* pyBrushes)',
        body="return wxPyDrawXXXList(*self, wxPyDrawXXXRectangle, pyCoords, pyPens, pyBrushes);")

    c.addCppMethod('PyObject*', '_DrawEllipseList', '(PyObject* pyCoords, PyObject* pyPens, PyObject* pyBrushes)',
        body="return wxPyDrawXXXList(*self, wxPyDrawXXXEllipse, pyCoords, pyPens, pyBrushes);")

    c.addCppMethod('PyObject*', '_DrawPolygonList', '(PyObject* pyCoords, PyObject* pyPens, PyObject* pyBrushes)',
        body="return wxPyDrawXXXList(*self, wxPyDrawXXXPolygon, pyCoords, pyPens, pyBrushes);")

    c.addCppMethod('PyObject*', '_DrawTextList',
        '(PyObject* textList, PyObject* pyPoints, PyObject* foregroundList, PyObject* backgroundList)',
        body="return wxPyDrawTextList(*self, textList, pyPoints, foregroundList, backgroundList);")

    c.addCppMethod('PyObject*', '_DrawLinesFromBuffer',
        '(PyObject* pyBuff)',
        body="return wxPyDrawLinesFromBuffer(*self, pyBuff);")

    c.addPyMethod('DrawPointList', '(self, points, pens=None)',
        doc="""\
            Draw a list of points as quickly as possible.

            :param points: A sequence of 2-element sequences representing
                           each point to draw, (x,y).
            :param pens:   If None, then the current pen is used.  If a single
                           pen then it will be used for all points.  If a list of
                           pens then there should be one for each point in points.
            """,
        body="""\
            if pens is None:
                pens = []
            elif isinstance(pens, wx.Pen):
                pens = [pens]
            elif len(pens) != len(points):
                raise ValueError('points and pens must have same length')
            return self._DrawPointList(points, pens, [])
            """)

    c.addPyMethod('DrawLineList', '(self, lines, pens=None)',
        doc="""\
            Draw a list of lines as quickly as possible.

            :param lines: A sequence of 4-element sequences representing
                          each line to draw, (x1,y1, x2,y2).
            :param pens:  If None, then the current pen is used.  If a
                          single pen then it will be used for all lines.  If
                          a list of pens then there should be one for each line
                          in lines.
            """,
        body="""\
            if pens is None:
                pens = []
            elif isinstance(pens, wx.Pen):
                pens = [pens]
            elif len(pens) != len(lines):
                raise ValueError('lines and pens must have same length')
            return self._DrawLineList(lines, pens, [])
            """)

    c.addPyMethod('DrawRectangleList', '(self, rectangles, pens=None, brushes=None)',
        doc="""\
            Draw a list of rectangles as quickly as possible.

            :param rectangles: A sequence of 4-element sequences representing
                               each rectangle to draw, (x,y, w,h).
            :param pens:       If None, then the current pen is used.  If a
                               single pen then it will be used for all rectangles.
                               If a list of pens then there should be one for each
                               rectangle in rectangles.
            :param brushes:    A brush or brushes to be used to fill the rectagles,
                               with similar semantics as the pens parameter.
            """,
        body="""\
            if pens is None:
                pens = []
            elif isinstance(pens, wx.Pen):
                pens = [pens]
            elif len(pens) != len(rectangles):
                raise ValueError('rectangles and pens must have same length')
            if brushes is None:
                brushes = []
            elif isinstance(brushes, wx.Brush):
                brushes = [brushes]
            elif len(brushes) != len(rectangles):
                raise ValueError('rectangles and brushes must have same length')
            return self._DrawRectangleList(rectangles, pens, brushes)
            """)

    c.addPyMethod('DrawEllipseList', '(self, ellipses, pens=None, brushes=None)',
        doc="""\
            Draw a list of ellipses as quickly as possible.

            :param ellipses: A sequence of 4-element sequences representing
                             each ellipse to draw, (x,y, w,h).
            :param pens:     If None, then the current pen is used.  If a
                             single pen then it will be used for all ellipses.
                             If a list of pens then there should be one for each
                             ellipse in ellipses.
            :param brushes:  A brush or brushes to be used to fill the ellipses,
                             with similar semantics as the pens parameter.
            """,
        body="""\
            if pens is None:
                pens = []
            elif isinstance(pens, wx.Pen):
                pens = [pens]
            elif len(pens) != len(ellipses):
                raise ValueError('ellipses and pens must have same length')
            if brushes is None:
                brushes = []
            elif isinstance(brushes, wx.Brush):
                brushes = [brushes]
            elif len(brushes) != len(ellipses):
                raise ValueError('ellipses and brushes must have same length')
            return self._DrawEllipseList(ellipses, pens, brushes)
            """)

    c.addPyMethod('DrawPolygonList', '(self, polygons, pens=None, brushes=None)',
        doc="""\
            Draw a list of polygons, each of which is a list of points.

            :param polygons: A sequence of sequences of sequences.
                             [[(x1,y1),(x2,y2),(x3,y3)...], [(x1,y1),(x2,y2),(x3,y3)...]]

            :param pens:     If None, then the current pen is used.  If a
                             single pen then it will be used for all polygons.
                             If a list of pens then there should be one for each
                             polygon.
            :param brushes:  A brush or brushes to be used to fill the polygons,
                             with similar semantics as the pens parameter.
            """,
        body="""\
            if pens is None:
                pens = []
            elif isinstance(pens, wx.Pen):
                pens = [pens]
            elif len(pens) != len(polygons):
                raise ValueError('polygons and pens must have same length')
            if brushes is None:
                brushes = []
            elif isinstance(brushes, wx.Brush):
                brushes = [brushes]
            elif len(brushes) != len(polygons):
                raise ValueError('polygons and brushes must have same length')
            return self._DrawPolygonList(polygons, pens, brushes)
            """)

    c.addPyMethod('DrawTextList', '(self, textList, coords, foregrounds=None, backgrounds=None)',
        doc="""\
            Draw a list of strings using a list of coordinants for positioning each string.

            :param textList:    A list of strings
            :param coords:      A list of (x,y) positions
            :param foregrounds: A list of `wx.Colour` objects to use for the
                                foregrounds of the strings.
            :param backgrounds: A list of `wx.Colour` objects to use for the
                                backgrounds of the strings.

            NOTE: Make sure you set background mode to wx.Solid (DC.SetBackgroundMode)
                  If you want backgrounds to do anything.
            """,
        body="""\
            if type(textList) == type(''):
                textList = [textList]
            elif len(textList) != len(coords):
                raise ValueError('textlist and coords must have same length')
            if foregrounds is None:
                foregrounds = []
            elif isinstance(foregrounds, wx.Colour):
                foregrounds = [foregrounds]
            elif len(foregrounds) != len(coords):
                raise ValueError('foregrounds and coords must have same length')
            if backgrounds is None:
                backgrounds = []
            elif isinstance(backgrounds, wx.Colour):
                backgrounds = [backgrounds]
            elif len(backgrounds) != len(coords):
                raise ValueError('backgrounds and coords must have same length')
            return  self._DrawTextList(textList, coords, foregrounds, backgrounds)
            """)


    c.addPyMethod('DrawLinesFromBuffer', '(self, pyBuff)',
        doc="""\
            Implementation of DrawLines that can use numpy arrays, or anything else that uses the
            python buffer protocol directly without any element conversion.  This provides a 
            significant performance increase over the standard DrawLines function.
            
            The pyBuff argument needs to provide an array of C integers organized as 
            x, y point pairs.  The size of a C integer is platform dependent.
            With numpy, the intc data type will provide the appropriate element size.

            If called with an object that doesn't support
            the python buffer protocol, or if the underlying element size does not
            match the size of a C integer, a TypeError exception is raised.  If 
            the buffer provided has float data with the same element size as a 
            C integer, no error will be raised, but the lines will not be drawn
            in the appropriate places.

            :param pyBuff:    A python buffer containing integer pairs
            """,
        body="""\
            return  self._DrawLinesFromBuffer(pyBuff)
            """)


    #-----------------------------------------------------------------
    c = module.find('wxDCClipper')
    assert isinstance(c, etgtools.ClassDef)
    c.addPrivateCopyCtor()
    # context manager methods
    c.addPyMethod('__enter__', '(self)', 'return self')
    c.addPyMethod('__exit__', '(self, exc_type, exc_val, exc_tb)', 'return False')


    #-----------------------------------------------------------------
    c = module.find('wxDCBrushChanger')
    assert isinstance(c, etgtools.ClassDef)
    c.addPrivateCopyCtor()
    # context manager methods
    c.addPyMethod('__enter__', '(self)', 'return self')
    c.addPyMethod('__exit__', '(self, exc_type, exc_val, exc_tb)', 'return False')


    #-----------------------------------------------------------------
    c = module.find('wxDCPenChanger')
    assert isinstance(c, etgtools.ClassDef)
    c.addPrivateCopyCtor()
    # context manager methods
    c.addPyMethod('__enter__', '(self)', 'return self')
    c.addPyMethod('__exit__', '(self, exc_type, exc_val, exc_tb)', 'return False')


    #-----------------------------------------------------------------
    c = module.find('wxDCTextColourChanger')
    assert isinstance(c, etgtools.ClassDef)
    c.addPrivateCopyCtor()
    # context manager methods
    c.addPyMethod('__enter__', '(self)', 'return self')
    c.addPyMethod('__exit__', '(self, exc_type, exc_val, exc_tb)', 'return False')


    #-----------------------------------------------------------------
    c = module.find('wxDCFontChanger')
    assert isinstance(c, etgtools.ClassDef)
    c.addPrivateCopyCtor()
    # context manager methods
    c.addPyMethod('__enter__', '(self)', 'return self')
    c.addPyMethod('__exit__', '(self, exc_type, exc_val, exc_tb)', 'return False')


    #-----------------------------------------------------------------
    c = module.find('wxDCTextBgColourChanger')
    assert isinstance(c, etgtools.ClassDef)
    c.addPrivateCopyCtor()
    # context manager methods
    c.addPyMethod('__enter__', '(self)', 'return self')
    c.addPyMethod('__exit__', '(self, exc_type, exc_val, exc_tb)', 'return False')


    #-----------------------------------------------------------------
    c = module.find('wxDCTextBgModeChanger')
    assert isinstance(c, etgtools.ClassDef)
    c.addPrivateCopyCtor()
    # context manager methods
    c.addPyMethod('__enter__', '(self)', 'return self')
    c.addPyMethod('__exit__', '(self, exc_type, exc_val, exc_tb)', 'return False')


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

