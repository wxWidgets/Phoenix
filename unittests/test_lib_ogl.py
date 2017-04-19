import unittest
from unittests import wtc
import wx

import wx.lib.ogl as ogl


class lib_ogl_Tests(wtc.WidgetTestCase):

    def test_lib_oglCtor(self):
        ogl.OGLInitialize()
        osc = ogl.ShapeCanvas(self.frame)
        self.diagram = ogl.Diagram()
        osc.SetDiagram(self.diagram)
        self.diagram.SetCanvas(osc)

        aShape = ogl.RectangleShape(w=50, h=50)
        aShape.SetCanvas(osc)
        self.diagram.AddShape(aShape)

    def test_lib_oglRectangle(self):
        ogl.OGLInitialize()
        osc = ogl.ShapeCanvas(self.frame)
        self.diagram = ogl.Diagram()
        osc.SetDiagram(self.diagram)
        self.diagram.SetCanvas(osc)

        aShape = ogl.RectangleShape(w=50, h=50)
        aShape.SetCanvas(osc)
        self.diagram.AddShape(aShape)

    def test_lib_oglPolygonShape(self):
        ogl.OGLInitialize()
        osc = ogl.ShapeCanvas(self.frame)
        self.diagram = ogl.Diagram()
        osc.SetDiagram(self.diagram)
        self.diagram.SetCanvas(osc)

        aShape = ogl.PolygonShape()
        w, h = 60, 60
        points = [(0.0, -h/2.0),
                  (w/2.0, 0.0),
                  (0.0, h/2.0),
                  (-w/2.0, 0.0),
                  ]

        aShape.Create(points)
        aShape.SetCanvas(osc)
        self.diagram.AddShape(aShape)

    def test_lib_oglCircle(self):
        ogl.OGLInitialize()
        osc = ogl.ShapeCanvas(self.frame)
        self.diagram = ogl.Diagram()
        osc.SetDiagram(self.diagram)
        self.diagram.SetCanvas(osc)

        aShape = ogl.CircleShape(50)
        aShape.SetCanvas(osc)
        self.diagram.AddShape(aShape)

    def test_lib_oglEllipseShape(self):
        ogl.OGLInitialize()
        osc = ogl.ShapeCanvas(self.frame)
        self.diagram = ogl.Diagram()
        osc.SetDiagram(self.diagram)
        self.diagram.SetCanvas(osc)

        aShape = ogl.EllipseShape(50, 50)
        aShape.SetCanvas(osc)
        self.diagram.AddShape(aShape)

    def test_lib_oglTextShape(self):
        ogl.OGLInitialize()
        osc = ogl.ShapeCanvas(self.frame)
        self.diagram = ogl.Diagram()
        osc.SetDiagram(self.diagram)
        self.diagram.SetCanvas(osc)

        aShape = ogl.TextShape(50, 50)
        aShape.SetCanvas(osc)
        aShape.AddText("Some nice text here")
        self.diagram.AddShape(aShape)

    def test_lib_oglLineShape(self):
        ogl.OGLInitialize()
        osc = ogl.ShapeCanvas(self.frame)
        self.diagram = ogl.Diagram()
        osc.SetDiagram(self.diagram)
        self.diagram.SetCanvas(osc)

        fromShape = ogl.RectangleShape(w=50, h=50)
        fromShape.SetCanvas(osc)
        self.diagram.AddShape(fromShape)

        toShape = ogl.RectangleShape(w=50, h=50)
        toShape.SetCanvas(osc)
        self.diagram.AddShape(toShape)

        lShape = ogl.LineShape()
        lShape.SetCanvas(osc)
        lShape.MakeLineControlPoints(2)
        fromShape.AddLine(lShape, toShape)
        self.diagram.AddShape(lShape)
        lShape.Show(True)

    def test_lib_oglShapeRegion(self):
        ogl.OGLInitialize()
        osc = ogl.ShapeCanvas(self.frame)
        self.diagram = ogl.Diagram()
        osc.SetDiagram(self.diagram)
        self.diagram.SetCanvas(osc)

        aShape = ogl.RectangleShape(w=50, h=50)
        aShape.SetCanvas(osc)
        self.diagram.AddShape(aShape)

        region1 = ogl.ShapeRegion()
        region1.SetText('DividedShape')
        region1.SetProportions(0.0, 0.2)
        region1.SetFormatMode(ogl.FORMAT_CENTRE_HORIZ)
        aShape.AddRegion(region1)

    def test_lib_oglDivisonShape(self):
        ogl.OGLInitialize()
        osc = ogl.ShapeCanvas(self.frame)
        self.diagram = ogl.Diagram()
        osc.SetDiagram(self.diagram)
        self.diagram.SetCanvas(osc)

        aShape = ogl.CompositeShape()
        aShape.SetCanvas(osc)
        self.diagram.AddShape(aShape)

        # create a division in the composite
        aShape.MakeContainer()

        # add a shape to the original division
        shape2 = ogl.RectangleShape(40, 60)
        aShape.GetDivisions()[0].AddChild(shape2)

    def test_lib_oglCompositeShape(self):
        ogl.OGLInitialize()
        osc = ogl.ShapeCanvas(self.frame)
        self.diagram = ogl.Diagram()
        osc.SetDiagram(self.diagram)
        self.diagram.SetCanvas(osc)

        aShape = ogl.CompositeShape()
        aShape.SetCanvas(osc)
        self.diagram.AddShape(aShape)

        constraining_shape = ogl.RectangleShape(120, 100)
        constrained_shape1 = ogl.CircleShape(50)
        constrained_shape2 = ogl.RectangleShape(80, 20)

        aShape.AddChild(constraining_shape)
        aShape.AddChild(constrained_shape1)
        aShape.AddChild(constrained_shape2)

        constraint = ogl.Constraint(ogl.CONSTRAINT_MIDALIGNED_BOTTOM,
                                    constraining_shape,
                                    [constrained_shape1, constrained_shape2])
        aShape.AddConstraint(constraint)
        aShape.Recompute()

    def test_lib_ogl_Constants(self):
        ogl.CONSTRAINT_CENTRED_VERTICALLY
        ogl.CONSTRAINT_CENTRED_HORIZONTALLY
        ogl.CONSTRAINT_CENTRED_BOTH
        ogl.CONSTRAINT_LEFT_OF
        ogl.CONSTRAINT_RIGHT_OF
        ogl.CONSTRAINT_ABOVE
        ogl.CONSTRAINT_BELOW
        ogl.CONSTRAINT_ALIGNED_TOP
        ogl.CONSTRAINT_ALIGNED_BOTTOM
        ogl.CONSTRAINT_ALIGNED_LEFT
        ogl.CONSTRAINT_ALIGNED_RIGHT

        # Like aligned, but with the objects centred on the respective edge
        # of the reference object.
        ogl.CONSTRAINT_MIDALIGNED_TOP
        ogl.CONSTRAINT_MIDALIGNED_BOTTOM
        ogl.CONSTRAINT_MIDALIGNED_LEFT
        ogl.CONSTRAINT_MIDALIGNED_RIGHT

        # from _drawn
        ogl.METAFLAGS_OUTLINE
        ogl.METAFLAGS_ATTACHMENTS

        ogl.DRAWN_ANGLE_0
        ogl.DRAWN_ANGLE_90
        ogl.DRAWN_ANGLE_180
        ogl.DRAWN_ANGLE_270

        # Drawing operations
        ogl.DRAWOP_SET_PEN
        ogl.DRAWOP_SET_BRUSH
        ogl.DRAWOP_SET_FONT
        ogl.DRAWOP_SET_TEXT_COLOUR
        ogl.DRAWOP_SET_BK_COLOUR
        ogl.DRAWOP_SET_BK_MODE
        ogl.DRAWOP_SET_CLIPPING_RECT
        ogl.DRAWOP_DESTROY_CLIPPING_RECT

        ogl.DRAWOP_DRAW_LINE
        ogl.DRAWOP_DRAW_POLYLINE
        ogl.DRAWOP_DRAW_POLYGON
        ogl.DRAWOP_DRAW_RECT
        ogl.DRAWOP_DRAW_ROUNDED_RECT
        ogl.DRAWOP_DRAW_ELLIPSE
        ogl.DRAWOP_DRAW_POINT
        ogl.DRAWOP_DRAW_ARC
        ogl.DRAWOP_DRAW_TEXT
        ogl.DRAWOP_DRAW_SPLINE
        ogl.DRAWOP_DRAW_ELLIPTIC_ARC

        # Line alignment flags
        # Vertical by default
        ogl.LINE_ALIGNMENT_HORIZ
        ogl.LINE_ALIGNMENT_VERT
        ogl.LINE_ALIGNMENT_TO_NEXT_HANDLE
        ogl.LINE_ALIGNMENT_NONE

        # keys
        ogl.KEY_SHIFT
        ogl.KEY_CTRL

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
