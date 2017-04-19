import unittest
from unittests import wtc
import wx
import wx.lib.masked as m

#---------------------------------------------------------------------------

class MaskedComboBoxTests(wtc.WidgetTestCase):

    def test_ComboBoxCtors(self):
        c = m.ComboBox(self.frame, value='value', choices="one two three four".split())
        c = m.ComboBox(self.frame, -1, 'value', wx.Point(10,10), wx.Size(80,-1),
                      "one two three four".split(), 0)
        c = m.ComboBox(self.frame, -1, "", (10,10), (80,-1), "one two three four".split(), 0)

        self.assertTrue(c.GetCount() == 4)

    #def test_ComboBoxDefaultCtor(self):
        #c = m.PreMaskedComboBox(self.frame)
        #c.Create(self.frame, value="value", choices="one two three four".split())


#---------------------------------------------------------------------------

class MaskedTextCtrlTests(wtc.WidgetTestCase):

    def test_textctrlCtor(self):
        t = m.TextCtrl(self.frame)
        t = m.TextCtrl(self.frame, -1, "Hello")
        t = m.TextCtrl(self.frame, style=wx.TE_READONLY)
        t = m.TextCtrl(self.frame, style=wx.TE_PASSWORD)
        t = m.TextCtrl(self.frame, style=wx.TE_MULTILINE)


    #def test_textctrlDefaultCtor(self):
        #t = m.TextCtrl()
        #t.Create(self.frame)


    def test_textctrlProperties(self):
        t = m.TextCtrl(self.frame)

        t.DefaultStyle
        t.NumberOfLines
        t.Hint
        t.InsertionPoint
        t.LastPosition
        t.Margins
        t.StringSelection
        t.Value


#---------------------------------------------------------------------------


class MaskedNumCtrlTests(wtc.WidgetTestCase):

    def test_numctrlCtor(self):
        t1 = m.NumCtrl(self.frame)
        t2 = m.NumCtrl(self.frame, -1, "10")
        t3 = m.NumCtrl(self.frame, value='32',style=wx.TE_READONLY, min=32, max=72)
        t3.ChangeValue("16")
        self.assertTrue(not t3.IsValid())

    #def test_numctrlDefaultCtor(self):
        #t = m.TextCtrl()
        #t.Create(self.frame)


    def test_numctrlProperties(self):
        t = m.NumCtrl(self.frame)

        t.DefaultStyle
        t.NumberOfLines
        t.Hint
        t.InsertionPoint
        t.LastPosition
        t.Margins
        t.StringSelection
        t.Value


#---------------------------------------------------------------------------


class MaskedTimeCtrlTests(wtc.WidgetTestCase):

    def test_timectrlCtor(self):
        t = m.TimeCtrl(self.frame)
        t = m.TimeCtrl(self.frame, -1, "18:00:00")
        t = m.TimeCtrl(self.frame, style=wx.TE_READONLY)


    #def test_numctrlDefaultCtor(self):
        #t = m.TextCtrl()
        #t.Create(self.frame)

    def test_timectrlIsValid(self):
        t = m.TimeCtrl(self.frame, -1, "18:25:18")

        theTime = t.GetValue(as_wxDateTime=True)
        self.assertEqual(theTime.hour, 18, "Hour: %s instead of '18'" % theTime.hour)
        self.assertEqual(theTime.minute, 25, "Minutes: %s instead of '18'" % theTime.minute)
        self.assertEqual(theTime.second, 18, "Seconds: %s instead of '18'" % theTime.second)

        self.assertEqual(t.IsInBounds(), True)
        self.assertEqual(t.GetCtrlParameter('validBackgroundColour'), t.GetBackgroundColour())

    def test_timectrlProperties(self):
        t = m.TimeCtrl(self.frame)

        t.DefaultStyle
        t.NumberOfLines
        t.Hint
        t.InsertionPoint
        t.LastPosition
        t.Margins
        t.StringSelection
        t.Value


#---------------------------------------------------------------------------

class MaskedIpAddrCtrlTests(wtc.WidgetTestCase):

    def test_ipaddrctrlCtor(self):
        t = m.IpAddrCtrl(self.frame)
        t = m.IpAddrCtrl(self.frame, -1, "128.000.000.000")
        t = m.IpAddrCtrl(self.frame, style=wx.TE_READONLY)


    #def test_ipaddrctrlDefaultCtor(self):
        #t = m.IpAddrCtrl()
        #t.Create(self.frame)


    def test_ipaddrctrlProperties(self):
        t = m.IpAddrCtrl(self.frame)

        t.DefaultStyle
        t.NumberOfLines
        t.Hint
        t.InsertionPoint
        t.LastPosition
        t.Margins
        t.StringSelection
        t.Value


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
