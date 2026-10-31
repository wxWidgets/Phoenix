import ctypes as ct
from ctypes import wintypes as wt
import sys
import unittest
from unittests import wtc
import wx

if sys.platform == 'win32':
    try:
        import comtypes
        import comtypes.hresult as hr
        import wx.lib.activex as activex
        from wx.siplib import voidptr
    except ImportError:
        comtypes = None
else:
    comtypes = None

#---------------------------------------------------------------------------

@unittest.skipIf(comtypes is None, 'needs comtypes on Windows')
class lib_activex_Tests(wtc.WidgetTestCase):

    def test_lib_activexRealControlTranslateMessage(self):
        ctrl = activex.ActiveXCtrl(self.frame, 'Shell.Explorer.2')
        msg = wt.MSG()
        self.assertFalse(ctrl.MSWTranslateMessage(voidptr(ct.addressof(msg))))

    def test_lib_activexPassesFullPointer(self):
        class FakeIpao(comtypes.COMObject):
            _com_interfaces_ = [activex.IOleInPlaceActiveObject]
            pointers = []

            def TranslateAccelerator(self, lpmsg):
                self.pointers.append(lpmsg)
                return hr.S_OK

        ctrl = activex.ActiveXCtrl(self.frame, 'Shell.Explorer.2')
        realIpao = ctrl.ipao
        fake = FakeIpao()
        ctrl.ipao = fake.QueryInterface(activex.IOleInPlaceActiveObject)
        try:
            pointer = 0x7FFF12345678
            self.assertTrue(ctrl.MSWTranslateMessage(voidptr(pointer)))
            self.assertEqual(fake.pointers, [pointer])
        finally:
            # The fake claims every message, even the ones the test app needs
            ctrl.ipao = realIpao

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
