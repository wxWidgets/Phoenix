import unittest
from unittests import wtc
import wx
import wx.adv
import os

pngFile = os.path.join(os.path.dirname(__file__), 'wizard.png')

#---------------------------------------------------------------------------

class MySimpleWizPage(wx.adv.WizardPageSimple):
    def __init__(self, parent, title):
        wx.adv.WizardPageSimple.__init__(self, parent)
        st = wx.StaticText(self, label='Wizard Page: %s' % title)
        st.SetFont(wx.FFont(24, wx.FONTFAMILY_SWISS))
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(st, 0, wx.ALIGN_CENTER)
        sizer.Add(wx.StaticLine(self), 0, wx.EXPAND)
        self.SetSizer(sizer)



class wizard_Tests(wtc.WidgetTestCase):

    def test_wizard1(self):
        wx.adv.WIZARD_EX_HELPBUTTON
        wx.adv.WIZARD_VALIGN_TOP
        wx.adv.WIZARD_VALIGN_CENTRE
        wx.adv.WIZARD_VALIGN_BOTTOM
        wx.adv.WIZARD_HALIGN_LEFT
        wx.adv.WIZARD_HALIGN_CENTRE
        wx.adv.WIZARD_HALIGN_RIGHT
        wx.adv.WIZARD_TILE

    def test_wizard2(self):
        # Create the wizard
        bmp = wx.BitmapBundle(wx.Bitmap(pngFile))
        wiz = wx.adv.Wizard(self.frame, title="Test Wizard 2", bitmap=bmp)

        # create the pages
        pages = []
        for i in range(5):
            pages.append(MySimpleWizPage(wiz, str(i+1)))

        # set the next/prev pages
        for idx, p in enumerate(pages):
            p.SetNext(pages[idx+1] if idx < len(pages)-1 else None)
            p.SetPrev(pages[idx-1] if idx > 0 else None)

        wiz.FitToPage(pages[0])
        wx.CallLater(100, self._autoPilot, wiz)
        wiz.RunWizard(pages[0])
        wiz.Destroy()

    def test_wizard3(self):
        # Same as above but use the Chain function to connect the pages
        bmp = wx.BitmapBundle(wx.Bitmap(pngFile))
        wiz = wx.adv.Wizard(self.frame, title="Test Wizard 2", bitmap=bmp)

        pages = []
        for i in range(5):
            pages.append(MySimpleWizPage(wiz, str(i+1)))

        wx.adv.WizardPageSimple.Chain(pages[0], pages[1])
        wx.adv.WizardPageSimple.Chain(pages[1], pages[2])
        wx.adv.WizardPageSimple.Chain(pages[2], pages[3])
        wx.adv.WizardPageSimple.Chain(pages[3], pages[4])

        wiz.FitToPage(pages[0])
        wx.CallLater(100, self._autoPilot, wiz)
        wiz.RunWizard(pages[0])
        wiz.Destroy()


    def test_wizard4(self):
        # Create the wizard
        bmp = wx.BitmapBundle(wx.Bitmap(pngFile))
        wiz = wx.adv.Wizard(self.frame, title="Test Wizard 2", bitmap=bmp)

        # create the pages
        pages = []
        for i in range(5):
            pages.append(MySimpleWizPage(wiz, str(i+1)))

        # set the next/prev pages
        for idx, p in enumerate(pages):
            p.SetNext(pages[idx+1] if idx < len(pages)-1 else None)
            p.SetPrev(pages[idx-1] if idx > 0 else None)

        wiz.FitToPage(pages[0])
        wx.CallLater(100, self._autoPilot, wiz)

        # Simply test if these new methods exist
        wiz.ShowPage(pages[2])
        wiz.IsRunning()

        wiz.RunWizard(pages[0])
        wiz.Destroy()


    def _autoPilot(self, wiz):
        # simulate clicking the next button until the wizard closes
        if not wiz or not wiz.GetCurrentPage():
            return

        # There seems to be a problem with stacking CallLaters while running
        # the unittests, so for now just cancel and return.
        wiz.EndModal(wx.ID_CANCEL)
        return

        #btn = wiz.FindWindowById(wx.ID_FORWARD)
        #evt = wx.CommandEvent(wx.EVT_BUTTON.typeId, wx.ID_FORWARD)
        #evt.SetEventObject(btn)
        #wx.PostEvent(btn, evt)
        #wx.CallLater(100, self._autoPilot, wiz)

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
