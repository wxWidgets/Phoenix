import imp_unittest, unittest
import wtc
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

        region1 = ogl.ShapeRegion()
        region1.SetText('DividedShape')
        region1.SetProportions(0.0, 0.2)
        region1.SetFormatMode(ogl.FORMAT_CENTRE_HORIZ)
        aShape.AddRegion(region1)


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
