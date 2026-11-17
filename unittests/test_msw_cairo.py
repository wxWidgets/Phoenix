import ctypes
import os
import tempfile
import unittest
import wx

# The Windows builds bundle libcairo-2.dll in the wx package when wx is built
# with cairo support, which is when it has a cairo renderer.
cairoDll = os.path.join(os.path.dirname(wx.__file__), 'libcairo-2.dll')
haveCairo = ('wxMSW' in wx.PlatformInfo
             and wx.GraphicsRenderer.GetCairoRenderer() is not None)

CAIRO_FORMAT_ARGB32 = 0
CAIRO_STATUS_SUCCESS = 0

#---------------------------------------------------------------------------

@unittest.skipIf(not haveCairo, 'needs wxMSW built with cairo')
class msw_cairo_Tests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.cairo = cairo = ctypes.CDLL(cairoDll)

        p = ctypes.c_void_p
        d = ctypes.c_double
        for name, restype, argtypes in [
                ('cairo_version_string', ctypes.c_char_p, []),
                ('cairo_status_to_string', ctypes.c_char_p, [ctypes.c_int]),
                ('cairo_image_surface_create', p, [ctypes.c_int, ctypes.c_int, ctypes.c_int]),
                ('cairo_image_surface_get_data', ctypes.POINTER(ctypes.c_uint32), [p]),
                ('cairo_pdf_surface_create', p, [ctypes.c_char_p, d, d]),
                ('cairo_surface_flush', None, [p]),
                ('cairo_surface_finish', None, [p]),
                ('cairo_surface_status', ctypes.c_int, [p]),
                ('cairo_surface_destroy', None, [p]),
                ('cairo_create', p, [p]),
                ('cairo_status', ctypes.c_int, [p]),
                ('cairo_destroy', None, [p]),
                ('cairo_set_source_rgb', None, [p, d, d, d]),
                ('cairo_paint', None, [p]),
                ('cairo_rectangle', None, [p, d, d, d, d]),
                ('cairo_fill', None, [p]),
                ('cairo_move_to', None, [p, d, d]),
                ('cairo_select_font_face', None, [p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int]),
                ('cairo_set_font_size', None, [p, d]),
                ('cairo_show_text', None, [p, ctypes.c_char_p]),
                ('cairo_show_page', None, [p]),
                ]:
            func = getattr(cairo, name)
            func.restype = restype
            func.argtypes = argtypes

    def assertStatus(self, status):
        self.assertEqual(status, CAIRO_STATUS_SUCCESS,
                         self.cairo.cairo_status_to_string(status).decode())

    def test_mswCairoVersion(self):
        version = self.cairo.cairo_version_string().decode()
        self.assertTrue(version.startswith('1.'), version)

    def test_mswCairoImageSurface(self):
        cairo = self.cairo
        surface = cairo.cairo_image_surface_create(CAIRO_FORMAT_ARGB32, 4, 4)
        cr = cairo.cairo_create(surface)
        cairo.cairo_set_source_rgb(cr, 1, 0, 0)
        cairo.cairo_paint(cr)
        self.assertStatus(cairo.cairo_status(cr))
        cairo.cairo_destroy(cr)

        cairo.cairo_surface_flush(surface)
        self.assertStatus(cairo.cairo_surface_status(surface))
        self.assertEqual(cairo.cairo_image_surface_get_data(surface)[0], 0xFFFF0000)
        cairo.cairo_surface_destroy(surface)

    # https://github.com/wxWidgets/Phoenix/issues/3035
    def test_mswCairoPdfSurface(self):
        cairo = self.cairo
        with tempfile.TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, 'test.pdf')
            surface = cairo.cairo_pdf_surface_create(filename.encode(), 200, 200)
            cr = cairo.cairo_create(surface)
            cairo.cairo_set_source_rgb(cr, 1, 0, 0)
            cairo.cairo_rectangle(cr, 10, 10, 100, 100)
            cairo.cairo_fill(cr)
            cairo.cairo_set_source_rgb(cr, 0, 0, 0)
            cairo.cairo_select_font_face(cr, b'Arial', 0, 0)
            cairo.cairo_set_font_size(cr, 20)
            cairo.cairo_move_to(cr, 10, 150)
            cairo.cairo_show_text(cr, b'wxPython')
            cairo.cairo_show_page(cr)
            self.assertStatus(cairo.cairo_status(cr))
            cairo.cairo_destroy(cr)

            cairo.cairo_surface_finish(surface)
            self.assertStatus(cairo.cairo_surface_status(surface))
            cairo.cairo_surface_destroy(surface)

            with open(filename, 'rb') as f:
                data = f.read()
        self.assertTrue(data.startswith(b'%PDF-'))
        self.assertIn(b'%%EOF', data[-32:])

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
