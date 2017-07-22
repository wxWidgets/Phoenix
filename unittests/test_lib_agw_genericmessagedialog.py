import unittest
from unittests import wtc
import wx

import wx.lib.agw.genericmessagedialog as GMD

#---------------------------------------------------------------------------

class lib_agw_genericmessagedialog_Tests(wtc.WidgetTestCase):

    def test_lib_agw_genericmessagedialogCtor(self):
        dlg = GMD.GenericMessageDialog(self.frame, 'Hello World', 'A Nice Message Box',
                                       agwStyle=wx.ICON_INFORMATION|wx.OK)

    def test_lib_agw_genericmessagedialogMethods(self):
        dlg = GMD.GenericMessageDialog(self.frame, 'Hello World', 'A Nice Message Box',
                                       agwStyle=wx.ICON_INFORMATION|wx.OK)

        # Test custom and default button labels
        for kind in ['OK', 'Yes', 'No', 'Help', 'Cancel']:
            default = 'GetDefault%sLabel()'%kind
            custom  = 'GetCustom%sLabel()'%kind

            self.assertEqual(eval('dlg.%s'%default), eval('dlg.%s'%custom))

        self.assertTrue(not dlg.HasCustomBitmaps())
        self.assertTrue(not dlg.GetExtendedMessage())

        dlg.SetExtendedMessage('An extended message')
        self.assertEqual(dlg.GetFullMessage(), '%s\n\n%s'%(dlg.GetMessage(), dlg.GetExtendedMessage()))


    def test_lib_agw_genericmessagedialogConstantsExist(self):
        GMD.BUTTON_SIZER_FLAGS
        GMD.GMD_DEFAULT
        GMD.GMD_USE_AQUABUTTONS
        GMD.GMD_USE_GRADIENTBUTTONS


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
