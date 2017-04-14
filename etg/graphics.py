#---------------------------------------------------------------------------
# Name:        etg/graphics.py
# Author:      Kevin Ollivier
#              Robin Dunn
#
# Created:     10-Sept-2011
# Copyright:   (c) 2011 by Kevin Ollivier
# Copyright:   (c) 2011-2017 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "graphics"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [
            'wxGraphicsObject',
            'wxGraphicsBitmap',
            'wxGraphicsBrush',
            'wxGraphicsFont',
            'wxGraphicsPen',
            'wxGraphicsContext',
            'wxGraphicsGradientStop',
            'wxGraphicsGradientStops',
            'wxGraphicsMatrix',
            'wxGraphicsPath',
            'wxGraphicsRenderer',
        ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode('#include <wx/gdicmn.h>')

    def markFactories(klass):
        for func in klass.allItems():
            if isinstance(func, etgtools.FunctionDef) \
               and func.name.startswith('Create') \
               and '*' in func.type:
                func.factory = True

    #---------------------------------------------
    c = module.find('wxGraphicsObject')
    assert isinstance(c, etgtools.ClassDef)
    c.mustHaveApp()
    c.addCppMethod('bool', 'IsOk', '()', 'return !self->IsNull();')
    c.addCppMethod('int', '__nonzero__', '()', "return !self->IsNull();")


    #---------------------------------------------
    c = module.find('wxGraphicsContext')
    assert isinstance(c, etgtools.ClassDef)
    markFactories(c)
    tools.removeVirtuals(c)
    c.abstract = True
    c.mustHaveApp()


    # Ensure that the target DC or image lives as long as the GC does. NOTE:
    # Since the Creates are static methods there is no self to associate the
    # extra reference with, but since they are factories then that extra
    # reference will be held by the return value of the factory instead.
    for m in c.find('Create').all():
        for p in m.items:
            if 'DC' in p.name or p.name == 'image':
                p.keepReference = True


    # FIXME: Handle wxEnhMetaFileDC?
    c.find('Create').findOverload('wxEnhMetaFileDC').ignore()

    c.find('GetSize.width').out = True
    c.find('GetSize.height').out = True
    c.find('GetDPI.dpiX').out = True
    c.find('GetDPI.dpiY').out = True

    m = c.find('GetPartialTextExtents')
    m.find('widths').ignore()
    m.type = 'wxArrayDouble*'
    m.factory = True  # a new instance is being created
    m.setCppCode("""\
        wxArrayDouble rval;
        self->GetPartialTextExtents(*text, rval);
        return new wxArrayDouble(rval);
        """)

    m = c.find('GetTextExtent')
    m.pyName = 'GetFullTextExtent'
    m.find('width').out = True
    m.find('height').out = True
    m.find('descent').out = True
    m.find('externalLeading').out = True

    c.addCppMethod('PyObject*', 'GetTextExtent', '(const wxString& text)',
        pyArgsString="(text) -> (width, height)",
        doc="Gets the dimensions of the string using the currently selected font.",
        body="""\
        wxDouble width = 0.0, height = 0.0;
        self->GetTextExtent(*text, &width, &height, NULL, NULL);
        return sipBuildResult(0, "(dd)", width, height);
        """)

    c.addPyCode("GraphicsContext.DrawRotatedText = wx.deprecated(GraphicsContext.DrawText, 'Use DrawText instead.')")


    c.addCppCode(tools.ObjArrayHelperTemplate('wxPoint2D', 'sipType_wxPoint2DDouble',
                    "Expected a sequence of length-2 sequences or wx.Point2D objects."))

    # we'll reimplement this overload as StrokeLineSegments
    c.find('StrokeLines').findOverload('beginPoints').ignore()
    c.addCppMethod('void', 'StrokeLineSegments', '(PyObject* beginPoints, PyObject* endPoints)',
        pyArgsString="(beginPoint2Ds, endPoint2Ds)",
        doc="Stroke disconnected lines from begin to end points.",
        body="""\
        size_t c1, c2, count;
        wxPoint2D* beginP = wxPoint2D_array_helper(beginPoints, &c1);
        wxPoint2D* endP =   wxPoint2D_array_helper(endPoints, &c2);

        if ( beginP != NULL && endP != NULL ) {
            count = wxMin(c1, c2);
            self->StrokeLines(count, beginP, endP);
        }
        delete [] beginP;
        delete [] endP;
        """)

    # Also reimplement the main StrokeLines method to reuse the same helper
    # function as StrokLineSegments
    m = c.find('StrokeLines').findOverload('points').ignore()
    c.addCppMethod('void', 'StrokeLines', '(PyObject* points)',
        pyArgsString="(point2Ds)",
        doc="Stroke lines conencting all the points.",
        body="""\
        size_t count;
        wxPoint2D* ptsArray = wxPoint2D_array_helper(points, &count);

        if ( ptsArray != NULL ) {
            self->StrokeLines(count, ptsArray);
            delete [] ptsArray;
        }
        """)

    # and once more for DrawLines
    m = c.find('DrawLines').ignore()
    c.addCppMethod('void', 'DrawLines', '(PyObject* points, wxPolygonFillMode fillStyle = wxODDEVEN_RULE)',
        pyArgsString="(point2Ds, fillStyle=ODDEVEN_RULE)",
        doc="Draws a polygon.",
        body="""\
        size_t count;
        wxPoint2D* ptsArray = wxPoint2D_array_helper(points, &count);

        if ( ptsArray != NULL ) {
            self->DrawLines(count, ptsArray, fillStyle);
            delete [] ptsArray;
        }
        """)

    #---------------------------------------------
    c = module.find('wxGraphicsPath')
    tools.removeVirtuals(c)
    c.find('GetBox').findOverload('wxDouble *x, wxDouble *y').ignore()
    c.find('GetCurrentPoint').findOverload('wxDouble *x, wxDouble *y').ignore()
    c.mustHaveApp()


    #---------------------------------------------
    c = module.find('wxGraphicsRenderer')
    tools.removeVirtuals(c)
    markFactories(c)
    c.abstract = True

    for m in c.find('CreateContext').all():
        for p in m.items:
            if 'DC' in p.name or p.name == 'image':
                p.keepReference = True
    c.find('CreateContextFromImage.image').keepReference = True

    # FIXME: Handle wxEnhMetaFileDC?
    c.find('CreateContext').findOverload('wxEnhMetaFileDC').ignore()


    #---------------------------------------------
    c = module.find('wxGraphicsMatrix')
    tools.removeVirtuals(c)
    c.mustHaveApp()

    c.find('Concat').overloads = []
    c.find('IsEqual').overloads = []

    c.find('Get.a').out = True
    c.find('Get.b').out = True
    c.find('Get.c').out = True
    c.find('Get.d').out = True
    c.find('Get.tx').out = True
    c.find('Get.ty').out = True

    c.find('TransformDistance.dx').inOut = True
    c.find('TransformDistance.dy').inOut = True

    c.find('TransformPoint.x').inOut = True
    c.find('TransformPoint.y').inOut = True


    #---------------------------------------------
    c = module.find('wxGraphicsGradientStops')
    c.addCppMethod('SIP_SSIZE_T', '__len__', '()', body="return (SIP_SSIZE_T)self->GetCount();")
    c.addCppMethod('wxGraphicsGradientStop*', '__getitem__', '(ulong n)',
                   pyArgsString='(n)',
                   body="return new wxGraphicsGradientStop(self->Item(n));",
                   factory=True)


    #---------------------------------------------
    # Use the pyNames we set for these classes in geometry.py so the old
    # names do not show up in the docstrings, etc.
    tools.changeTypeNames(module, 'wxPoint2DDouble', 'wxPoint2D')
    tools.changeTypeNames(module, 'wxRect2DDouble', 'wxRect2D')


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

