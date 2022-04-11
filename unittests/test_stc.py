import unittest
from unittests import wtc
import wx
import wx.stc as stc

text = """\
Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do
eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim
veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea
commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit
esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat
cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est
laborum.
""" * 2

if wx.Platform == '__WXMSW__':
    face1 = 'Arial'
    face2 = 'Times New Roman'
    face3 = 'Courier New'
    pb = 10
else:
    face1 = 'Helvetica'
    face2 = 'Times'
    face3 = 'Courier'
    pb = 12

#---------------------------------------------------------------------------

class stc_Tests(wtc.WidgetTestCase):

    def test_stcCtor(self):
        ed = stc.StyledTextCtrl(self.frame)

    def test_stcDefaultCtor(self):
        ed = stc.StyledTextCtrl()
        ed.Create(self.frame)

    def test_stcStyleTextCtrl1(self):
        ed = stc.StyledTextCtrl(self.frame)
        ed.SetText(text)
        ed.EmptyUndoBuffer()
        ed.GotoPos(0)

        ed.SetMarginType(1, stc.STC_MARGIN_SYMBOL)
        ed.MarkerDefine(0, stc.STC_MARK_ROUNDRECT, "#CCFF00", "RED")
        ed.MarkerDefine(1, stc.STC_MARK_CIRCLE, "FOREST GREEN", "SIENNA")
        ed.MarkerDefine(2, stc.STC_MARK_SHORTARROW, "blue", "blue")
        ed.MarkerDefine(3, stc.STC_MARK_ARROW, "#00FF00", "#00FF00")
        ed.MarkerAdd(1, 0)
        ed.MarkerAdd(2, 1)
        ed.MarkerAdd(3, 2)
        ed.MarkerAdd(4, 3)
        ed.MarkerAdd(5, 0)


    def test_stcStyleTextCtrl2(self):
        ed = stc.StyledTextCtrl(self.frame)
        ed.SetText(text)
        ed.EmptyUndoBuffer()
        ed.GotoPos(0)

        ed.INDICSTYLE00 = 0
        ed.INDICSTYLE01 = 1
        ed.INDICSTYLE02 = 2

        ed.IndicatorSetStyle(ed.INDICSTYLE00, stc.STC_INDIC_SQUIGGLE)
        ed.IndicatorSetForeground(ed.INDICSTYLE00, wx.RED)
        ed.IndicatorSetStyle(ed.INDICSTYLE01, stc.STC_INDIC_DIAGONAL)
        ed.IndicatorSetForeground(ed.INDICSTYLE01, wx.BLUE)
        ed.IndicatorSetStyle(ed.INDICSTYLE02, stc.STC_INDIC_STRIKE)
        ed.IndicatorSetForeground(ed.INDICSTYLE02, wx.RED)

        ed.StartStyling(100)

        ed.SetIndicatorCurrent(ed.INDICSTYLE00)
        ed.IndicatorFillRange(836, 10)
        ed.SetIndicatorCurrent(ed.INDICSTYLE01)
        ed.IndicatorFillRange(846, 8)
        ed.SetIndicatorCurrent(ed.INDICSTYLE02)
        ed.IndicatorFillRange(854, 10)


    def test_stcStyleTextCtrl3(self):
        ed = stc.StyledTextCtrl(self.frame)
        ed.SetText(text)
        ed.EmptyUndoBuffer()
        ed.GotoPos(0)

        ed.StyleSetSpec(stc.STC_STYLE_DEFAULT, "size:%d,face:%s" % (pb, face3))
        ed.StyleClearAll()
        ed.StyleSetSpec(1, "size:%d,bold,face:%s,fore:#0000FF" % (pb, face1))
        ed.StyleSetSpec(2, "face:%s,italic,fore:#FF0000,size:%d" % (face2, pb))
        ed.StyleSetSpec(3, "face:%s,bold,size:%d" % (face2, pb))
        ed.StyleSetSpec(4, "face:%s,size:%d" % (face1, pb-1))
        ed.StyleSetSpec(5, "back:#FFF0F0")

        ed.StartStyling(80)
        ed.SetStyling(6, 1)
        ed.StartStyling(100)
        ed.SetStyling(20, 2)
        ed.StartStyling(180)
        ed.SetStyling(4, 3)
        ed.SetStyling(2, 0)
        ed.SetStyling(10, 4)


    def test_stcStyleTextCtrl5(self):
        ed = stc.StyledTextCtrl(self.frame)
        ed.SetText(text)
        ed.EmptyUndoBuffer()
        ed.GotoPos(0)

        ed.SetMarginType(0, stc.STC_MARGIN_NUMBER)
        ed.SetMarginWidth(0, 22)
        ed.StyleSetSpec(stc.STC_STYLE_LINENUMBER, "size:%d,face:%s" % (pb-2, face1))


    def test_stcStyleTextCtrl6(self):
        ed = stc.StyledTextCtrl(self.frame)
        ed.SetText(text)
        ed.EmptyUndoBuffer()
        ed.GotoPos(10)

        textbytes = ed.GetStyledText(100,150)
        self.assertTrue(isinstance(textbytes, memoryview))

        pointer = ed.GetCharacterPointer()
        self.assertTrue(isinstance(pointer, memoryview))

        line, pos = ed.GetCurLine()
        self.assertTrue(len(line) != 0)
        self.assertTrue(isinstance(pos, int))


    def test_stcStyleTextCtrl8(self):
        ed = stc.StyledTextCtrl(self.frame)
        ed.SetText(text)
        ed.EmptyUndoBuffer()
        ed.GotoPos(10)

        raw = ed.GetLineRaw(5)
        self.assertTrue(isinstance(raw, bytes))

        ed.AddTextRaw(b"some new text")



    def test_stcStyleTextCtrlConstantsExist(self):
        # This is not even close to the full set of constants in the module,
        # but just a represenative few to help ensure that the code
        # generation is continuing to do what it is supposed to be doing.
        stc.STC_P_DEFAULT
        stc.STC_P_DECORATOR
        stc.STC_KEY_DOWN
        stc.STC_MARK_CIRCLE
        stc.STC_MARGIN_NUMBER
        stc.STC_STYLE_BRACELIGHT
        stc.STC_CHARSET_MAC
        stc.STC_INDIC_DIAGONAL
        stc.STC_LEX_PYTHON
        stc.STC_CMD_REDO
        stc.STC_CMD_LINEENDEXTEND
        stc.STC_CMD_PARADOWN


    def test_stcEvent(self):
        evt = stc.StyledTextEvent(stc.wxEVT_STC_CHANGE)

    def test_stcEventConstantsExist(self):
        stc.wxEVT_STC_CHANGE
        stc.wxEVT_STC_STYLENEEDED
        stc.wxEVT_STC_CHARADDED
        stc.wxEVT_STC_SAVEPOINTREACHED
        stc.wxEVT_STC_SAVEPOINTLEFT
        stc.wxEVT_STC_ROMODIFYATTEMPT
        stc.wxEVT_STC_KEY
        stc.wxEVT_STC_DOUBLECLICK
        stc.wxEVT_STC_UPDATEUI
        stc.wxEVT_STC_MODIFIED
        stc.wxEVT_STC_MACRORECORD
        stc.wxEVT_STC_MARGINCLICK
        stc.wxEVT_STC_NEEDSHOWN
        stc.wxEVT_STC_PAINTED
        stc.wxEVT_STC_USERLISTSELECTION
        stc.wxEVT_STC_URIDROPPED
        stc.wxEVT_STC_DWELLSTART
        stc.wxEVT_STC_DWELLEND
        stc.wxEVT_STC_START_DRAG
        stc.wxEVT_STC_DRAG_OVER
        stc.wxEVT_STC_DO_DROP
        stc.wxEVT_STC_ZOOM
        stc.wxEVT_STC_HOTSPOT_CLICK
        stc.wxEVT_STC_HOTSPOT_DCLICK
        stc.wxEVT_STC_HOTSPOT_RELEASE_CLICK
        stc.wxEVT_STC_CALLTIP_CLICK
        stc.wxEVT_STC_AUTOCOMP_SELECTION
        stc.wxEVT_STC_INDICATOR_CLICK
        stc.wxEVT_STC_INDICATOR_RELEASE
        stc.wxEVT_STC_AUTOCOMP_CANCELLED
        stc.wxEVT_STC_AUTOCOMP_CHAR_DELETED
        stc.wxEVT_STC_HOTSPOT_RELEASE_CLICK

    def test_stcEventBinderssExist(self):
        stc.EVT_STC_CHANGE
        stc.EVT_STC_STYLENEEDED
        stc.EVT_STC_CHARADDED
        stc.EVT_STC_SAVEPOINTREACHED
        stc.EVT_STC_SAVEPOINTLEFT
        stc.EVT_STC_ROMODIFYATTEMPT
        stc.EVT_STC_KEY
        stc.EVT_STC_DOUBLECLICK
        stc.EVT_STC_UPDATEUI
        stc.EVT_STC_MODIFIED
        stc.EVT_STC_MACRORECORD
        stc.EVT_STC_MARGINCLICK
        stc.EVT_STC_NEEDSHOWN
        stc.EVT_STC_PAINTED
        stc.EVT_STC_USERLISTSELECTION
        stc.EVT_STC_URIDROPPED
        stc.EVT_STC_DWELLSTART
        stc.EVT_STC_DWELLEND
        stc.EVT_STC_START_DRAG
        stc.EVT_STC_DRAG_OVER
        stc.EVT_STC_DO_DROP
        stc.EVT_STC_ZOOM
        stc.EVT_STC_HOTSPOT_CLICK
        stc.EVT_STC_HOTSPOT_DCLICK
        stc.EVT_STC_HOTSPOT_RELEASE_CLICK
        stc.EVT_STC_CALLTIP_CLICK
        stc.EVT_STC_AUTOCOMP_SELECTION
        stc.EVT_STC_INDICATOR_CLICK
        stc.EVT_STC_INDICATOR_RELEASE
        stc.EVT_STC_AUTOCOMP_CANCELLED
        stc.EVT_STC_AUTOCOMP_CHAR_DELETED


    def test_stcHasTextCtrlMethods(self):
        # Just ensure that the common TextCtrl methods are present. This is
        # done because the C++ class either derives from wxTextEntryBase
        # or from wxTextCtrlIface, but these classes are not part of the API
        # (and thus are not wrapped), so we have to kludge things.
        # See etg/_stc.py for details.

        t = stc.StyledTextCtrl(self.frame)
        t.Cut
        t.CanCut
        t.DiscardEdits
        t.GetDefaultStyle
        t.GetNumberOfLines
        t.GetStyle
        t.IsModified
        t.HitTest
        t.AppendText
        t.WriteText
        t.ChangeValue



#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
