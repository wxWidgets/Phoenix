import unittest
from unittests import wtc
import wx
import wx.glcanvas

#---------------------------------------------------------------------------

class glcanvas_Tests(wtc.WidgetTestCase):

    def test_glcanvas1(self):
        wx.glcanvas.WX_GL_RGBA
        wx.glcanvas.WX_GL_BUFFER_SIZE
        wx.glcanvas.WX_GL_LEVEL
        wx.glcanvas.WX_GL_DOUBLEBUFFER
        wx.glcanvas.WX_GL_STEREO
        wx.glcanvas.WX_GL_AUX_BUFFERS
        wx.glcanvas.WX_GL_MIN_RED
        wx.glcanvas.WX_GL_MIN_GREEN
        wx.glcanvas.WX_GL_MIN_BLUE
        wx.glcanvas.WX_GL_MIN_ALPHA
        wx.glcanvas.WX_GL_DEPTH_SIZE
        wx.glcanvas.WX_GL_STENCIL_SIZE
        wx.glcanvas.WX_GL_MIN_ACCUM_RED
        wx.glcanvas.WX_GL_MIN_ACCUM_GREEN
        wx.glcanvas.WX_GL_MIN_ACCUM_BLUE
        wx.glcanvas.WX_GL_MIN_ACCUM_ALPHA
        wx.glcanvas.WX_GL_SAMPLE_BUFFERS
        wx.glcanvas.WX_GL_SAMPLES


    def test_glcanvas2(self):
        cvs = wx.glcanvas.GLCanvas(self.frame)
        ctx = wx.glcanvas.GLContext(cvs)


    def test_glcanvas3(self):
        attribs = [wx.glcanvas.WX_GL_DEPTH_SIZE, 24,
                   wx.glcanvas.WX_GL_DOUBLEBUFFER,
                   0]
        cvs = wx.glcanvas.GLCanvas(self.frame, attribList=attribs)


    def test_glcanvas4(self):
        attribs = [wx.glcanvas.WX_GL_DEPTH_SIZE, 32,
                   wx.glcanvas.WX_GL_DOUBLEBUFFER,
                   0]
        wx.glcanvas.GLCanvas.IsDisplaySupported(attribs)


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
