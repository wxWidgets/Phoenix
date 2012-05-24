import imp_unittest, unittest
import wtc
import wx
import os
if wtc.isPython3():
    from io import BytesIO as FileLikeObject
else:
    from cStringIO import StringIO as FileLikeObject


pngFile = os.path.join(os.path.dirname(__file__), 'toucan.png')

#---------------------------------------------------------------------------

class stream_Tests(wtc.WidgetTestCase):

    def test_inputStreamParam(self):
        # This tests being able to pass a Python file-like object to a
        # wrapped function expecting a wxInputStream.
        
        # First, load the image data into a StringIO object
        f = open(pngFile, 'rb')
        stream = FileLikeObject(f.read())
        f.close()
        
        # Then use it to create a wx.Image
        img = wx.Image(stream)
        self.assertTrue(img.IsOk())
        
    def test_outputStreamParam(self):
        # This tests being able to pass a Python file-like object to a
        # wrapped function expecting a wxOutputStream.

        image = wx.Image(pngFile)
        stream = FileLikeObject()
        image.SaveFile(stream, wx.BITMAP_TYPE_PNG)
        del image
        
        stream = FileLikeObject(stream.getvalue())        
        image = wx.Image(stream)
        self.assertTrue(image.IsOk())
        
        
        
#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
