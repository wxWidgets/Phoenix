import unittest
from unittests import wtc
import wx

import wx.lib.docview as docview
import wx.lib.pydocview as pydocview

#---------------------------------------------------------------------------

class lib_pydocview_Tests(wtc.WidgetTestCase):

    def test_lib_pydocviewServicesAreEvtHandlers(self):
        for serviceClass in (pydocview.DocService, pydocview.DocOptionsService,
                             pydocview.AboutService, pydocview.FilePropertiesService,
                             pydocview.WindowMenuService):
            service = serviceClass()
            self.assertTrue(service.GetEvtHandlerEnabled())
            service.Destroy()

    def test_lib_pydocviewOptionsSupportedModes(self):
        service = pydocview.DocOptionsService(showGeneralOptions=False)
        self.assertEqual(service.GetSupportedModes(), docview.DOC_SDI | docview.DOC_MDI)
        service.SetSupportedModes(docview.DOC_SDI)
        self.assertEqual(service.GetSupportedModes(), docview.DOC_SDI)
        service.Destroy()

    def test_lib_pydocviewScaleIcon(self):
        icon = pydocview._ScaleIcon(wx.Icon(wx.Bitmap(32, 32)), 16)
        self.assertEqual(icon.GetSize(), wx.Size(16, 16))

    def test_lib_pydocviewChopPath(self):
        service = pydocview.FilePropertiesService()
        self.assertEqual(service.chopPath('/abc/def/ghi', length=8), '/abc/def\n/ghi')
        service.Destroy()

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
