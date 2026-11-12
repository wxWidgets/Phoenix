import unittest
from unittests import wtc
import wx
import wx.lib.masked as m

#---------------------------------------------------------------------------

def typeOverSelection(ctrl, selected, char, removeFirst):
    """
    Select the text selected and type char over it. With removeFirst, the
    selected text is removed before EVT_CHAR, like the native control does in
    wxGTK.
    """
    start = wx.TextEntry.GetValue(ctrl).index(selected)
    end = start + len(selected)
    ctrl._SetSelection(start, end)
    down = wx.KeyEvent(wx.wxEVT_KEY_DOWN)
    down.SetKeyCode(ord(char.upper()))
    ctrl._OnKeyDown(down)
    if removeFirst:
        wx.TextEntry.Remove(ctrl, start, end)
    evt = wx.KeyEvent(wx.wxEVT_CHAR)
    evt.SetKeyCode(ord(char))
    evt.SetUnicodeKey(ord(char))
    ctrl._OnChar(evt)

#---------------------------------------------------------------------------

class MaskedComboBoxTests(wtc.WidgetTestCase):

    def test_ComboBoxTypeOverSelection(self):
        for removeFirst in (False, True):
            c = m.ComboBox(self.frame, mask='###', choices=['123', '456'],
                           value='123')
            typeOverSelection(c, '12', '9', removeFirst)
            self.myYield()
            self.assertEqual(c.GetValue(), '9 3')

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

    def test_textctrlAutoComplete(self):
        t = m.TextCtrl(self.frame)
        choices = ['apple', 'banana', 'blueberry', 'cherry']
        self.assertEqual(t._autoComplete(1, choices, 'b', False, None), (1, True))
        self.assertEqual(t._autoComplete(-1, choices, 'b', False, None), (2, True))
        self.assertEqual(t._autoComplete(1, choices, 'b', False, 1), (2, True))
        self.assertEqual(t._autoComplete(-1, choices, 'b', False, 2), (1, True))


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

    def test_numctrlAllowNoneWithFraction(self):
        t = m.NumCtrl(self.frame, allowNone=True, fractionWidth=2)
        t.SetValue(None)
        self.assertIsNone(t.GetValue())
        t.SetValue(1.5)
        self.assertEqual(t.GetValue(), 1.5)
        t.Clear()
        self.assertIsNone(t.GetValue())
        t.SetValue(0)
        self.assertEqual(t.GetValue(), 0.0)

        t = m.NumCtrl(self.frame, fractionWidth=2)
        t.Clear()
        self.assertEqual(t.GetValue(), 0.0)

    def test_numctrlAllowNoneLimited(self):
        for kw in ({}, {'fractionWidth': 1}):
            t = m.NumCtrl(self.frame, value=None, allowNone=True, min=1, max=100,
                          limited=True, **kw)
            self.assertIsNone(t.GetValue())
            t.SetValue(50)
            self.assertEqual(t.GetValue(), 50)
            t.SetValue(None)
            self.assertIsNone(t.GetValue())

    def test_numctrlTypeOverSelection(self):
        for removeFirst in (False, True):
            t = m.NumCtrl(self.frame, value=123)
            typeOverSelection(t, '23', '5', removeFirst)
            self.myYield()
            self.assertEqual(t.GetValue(), 15)

            t = m.NumCtrl(self.frame, value=1234.5, fractionWidth=2)
            typeOverSelection(t, '23', '9', removeFirst)
            self.myYield()
            self.assertEqual(t.GetValue(), 194.5)


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


class TimeCtrlTests(wtc.WidgetTestCase):

    def test_timectrlInvalidString(self):
        t = m.TimeCtrl(self.frame)
        with self.assertRaises(ValueError):
            t.GetWxDateTime('not a time')

    def test_timectrlSetParametersKeepsValue(self):
        t = m.TimeCtrl(self.frame, value='14:34:56')
        t.SetParameters(format='24HHMMSS')
        self.assertEqual(t.GetValue(), '14:34:56')

    def test_timectrlSetTimeSpan(self):
        t = m.TimeCtrl(self.frame, fmt24hr=True)
        t.SetValue(wx.TimeSpan(13, 45, 30))
        self.assertEqual(t.GetValue(), '13:45:30')


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
