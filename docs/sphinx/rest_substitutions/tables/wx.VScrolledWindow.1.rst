======================================= ==============================================================================================================================================================================================================================================================================
`GetFirstVisibleLine()`                 Deprecated for :meth:`~wx.VarVScrollHelper.GetVisibleRowsBegin`
`GetLastVisibleLine()`                  Deprecated for :meth:`~wx.VarVScrollHelper.GetVisibleRowsEnd` This function originally had a slight design flaw in that it was possible to return ``sys.maxint-1``   (ie: a large positive number) if the scroll position was 0 and the first line wasn't completely visible.
`GetLineCount()`                        Deprecated for :meth:`~wx.VarVScrollHelper.GetRowCount`
`HitTest(x, y)`
`HitTest(pt)`                           Deprecated for :meth:`~wx.VarScrollHelperBase.VirtualHitTest`.
`OnGetLineHeight(line)`                 Deprecated for :meth:`~wx.VarVScrollHelper.OnGetRowHeight`
`OnGetLinesHint(lineMin, lineMax)`      Deprecated for :meth:`~wx.VarVScrollHelper.OnGetRowsHeightHint`
`RefreshLine(line)`                     Deprecated for :meth:`~wx.VarVScrollHelper.RefreshRow`
`RefreshLines(from_, to_)`              Deprecated for :meth:`~wx.VarVScrollHelper.RefreshRows`
`ScrollLines(lines)`                    Deprecated for :meth:`~wx.VarVScrollHelper.ScrollRows`
`ScrollPages(pages)`                    Deprecated for :meth:`~wx.VarVScrollHelper.ScrollRowPages`
`ScrollToLine(line)`                    Deprecated for :meth:`~wx.VarVScrollHelper.ScrollToRow`
`SetLineCount(count)`                   Deprecated for :meth:`~wx.VarVScrollHelper.SetRowCount`
======================================= ==============================================================================================================================================================================================================================================================================

|

