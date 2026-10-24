import unittest
from unittests import wtc
import wx

import wx.lib.analogclock as ac
from wx.lib.analogclock.setup import Setup
from wx.lib.analogclock.lib_setup import fontselect

#---------------------------------------------------------------------------

class lib_analogclock_Tests(wtc.WidgetTestCase):

    def test_lib_analogclockCtor(self):
        clock = ac.AnalogClock(self.frame)

    def test_lib_analogclockSetupStaticBoxChildren(self):
        clock = ac.AnalogClock(self.frame)
        dlg = Setup(clock)
        # Let the dialog's deferred UpdateControls run before it's destroyed,
        # otherwise it fails later and leaves the busy cursor on.
        self.myYield()
        self.checkStaticBoxSizers(dlg)
        dlg.Destroy()

    def test_lib_analogclockSetupFontSelect(self):
        clock = ac.AnalogClock(self.frame)
        dlg = Setup(clock)
        ticksPage = dlg.nb.GetPage(2)
        hoursGroup = ticksPage.GetChildren()[0]

        font = wx.Font(wx.FontInfo(20).Bold())
        fs = hoursGroup.ft
        wx.PostEvent(fs.parent, fontselect.FontSelectEvent(id=fs.GetId(), obj=fs, val=font))
        self.myYield()

        tickFont = clock.GetTickFont(ac.HOUR)[0]
        self.assertEqual(tickFont.GetPointSize(), 20)
        self.assertEqual(tickFont.GetWeight(), wx.FONTWEIGHT_BOLD)
        dlg.Destroy()

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
