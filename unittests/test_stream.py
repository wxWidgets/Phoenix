import imp_unittest, unittest
import wtc
import wx
import os
from cStringIO import StringIO


pngFile = os.path.join(os.path.dirname(__file__), 'toucan.png')

#---------------------------------------------------------------------------

class stream_Tests(wtc.WidgetTestCase):

    def test_inputStreamParam(self):
        # This tests being able to pass a Python file-like object to a
        # wrapped function expecting a wxInputStream.
        
        # First, load the image data into a StringIO object
        stream = StringIO(open(pngFile, 'rb').read())
        
        # Then use it to create a wx.Image
        img = wx.Image(stream)
        self.assertTrue(img.IsOk())
        
    def test_outputStreamParam(self):
        # This tests being able to pass a Python file-like object to a
        # wrapped function expecting a wxOytputStream.

        image = wx.Image(pngFile)
        stream = StringIO()
        image.SaveFile(stream, wx.BITMAP_TYPE_PNG)
        del image
        
        stream = StringIO(stream.getvalue())        
        image = wx.Image(stream)
        self.assertTrue(image.IsOk())
        
        
        
#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
