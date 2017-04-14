import unittest
import wx


#---------------------------------------------------------------------------

class Events(unittest.TestCase):

    # Test the constructors to make sure the classes are not abstract, except
    # for wx.Event

    def test_Event_ctor(self):
        with self.assertRaises(TypeError):
            # it's an abstract class, so it can't be instantiated
            evt = wx.Event()

    def test_CommandEvent_ctor(self):
        evt = wx.CommandEvent()

    def test_ActivateEvent_ctor(self):
        evt = wx.ActivateEvent()

    def test_ChildFocusEvent_ctor(self):
        evt = wx.ChildFocusEvent()

    def test_ClipboardTextEvent_ctor(self):
        evt = wx.ClipboardTextEvent()

    def test_CloseEvent_ctor(self):
        evt = wx.CloseEvent()

    def test_ContextMenuEvent_ctor(self):
        evt = wx.ContextMenuEvent()

    def test_DisplayChangedEvent_ctor(self):
        evt = wx.DisplayChangedEvent()

    def test_DropFilesEvent_ctor(self):
        evt = wx.DropFilesEvent()

    def test_EraseEvent_ctor(self):
        evt = wx.EraseEvent()

    def test_FocusEvent_ctor(self):
        evt = wx.FocusEvent()

    def test_HelpEvent_ctor(self):
        app = wx.App()
        evt = wx.HelpEvent()

    def test_IconizeEvent_ctor(self):
        evt = wx.IconizeEvent()

    def test_IdleEvent_ctor(self):
        evt = wx.IdleEvent()

    def test_InitDialogEvent_ctor(self):
        evt = wx.InitDialogEvent()

    def test_JoystickEvent_ctor(self):
        evt = wx.JoystickEvent()

    def test_KeyEvent_ctor(self):
        evt = wx.KeyEvent()

    def test_KeyEvent_GetUnicodeKey(self):
        evt = wx.KeyEvent()
        unikey = evt.GetUnicodeKey()
        self.assertTrue(isinstance(unikey, int))

    def test_MaximizeEvent_ctor(self):
        evt = wx.MaximizeEvent()

    def test_MenuEvent_ctor(self):
        evt = wx.MenuEvent()

    def test_MouseCaptureChangedEvent_ctor(self):
        evt = wx.MouseCaptureChangedEvent()

    def test_MouseCaptureLostEvent_ctor(self):
        evt = wx.MouseCaptureLostEvent()

    def test_MouseEvent_ctor(self):
        evt = wx.MouseEvent()

    def test_MoveEvent_ctor(self):
        evt = wx.MoveEvent((1,1))

    def test_NavigationKeyEvent_ctor(self):
        evt = wx.NavigationKeyEvent()

    def test_NotifyEvent_ctor(self):
        evt = wx.NotifyEvent()

    def test_PaintEvent_ctor(self):
        evt = wx.PaintEvent()

    def test_PaletteChangedEvent_ctor(self):
        evt = wx.PaletteChangedEvent()

    def test_QueryNewPaletteEvent_ctor(self):
        evt = wx.QueryNewPaletteEvent()

    def test_ScrollEvent_ctor(self):
        evt = wx.ScrollEvent()

    def test_ScrollWinEvent_ctor(self):
        evt = wx.ScrollWinEvent()

    def test_SetCursorEvent_ctor(self):
        evt = wx.SetCursorEvent()

    def test_ShowEvent_ctor(self):
        evt = wx.ShowEvent()

    def test_SizeEvent_ctor(self):
        evt = wx.SizeEvent((1,1))

    def test_SysColourChangedEvent_ctor(self):
        evt = wx.SysColourChangedEvent()

    def test_UpdateUIEvent_ctor(self):
        evt = wx.UpdateUIEvent()

    def test_WindowCreateEvent_ctor(self):
        evt = wx.WindowCreateEvent()

    def test_WindowDestroyEvent_ctor(self):
        evt = wx.WindowDestroyEvent()


    def test_eventBinding(self):
        class Frame(wx.Frame):
            def __init__(self, *args, **kw):
                wx.Frame.__init__(self, *args, **kw)
                self.Bind(wx.EVT_SIZE, self.OnSize)
                self.gotEvent = False
            def OnSize(self, evt):
                self.gotEvent = True
                evt.EventObject.Close()
        app = wx.App()
        frm = Frame(None)
        frm.Show()
        frm.SetSize((200,100))
        #app.MainLoop()
        self.assertTrue(frm.gotEvent)


    def test_DropFilesEvent_tweaks(self):
        evt = wx.DropFilesEvent(123, 'one two three four five'.split())
        self.assertTrue(evt.NumberOfFiles == 5)
        f = evt.Files
        self.assertTrue(isinstance(f, list))
        self.assertTrue(len(f) == 5)


    def test_EventCategory(self):
        wx.EVT_CATEGORY_UI
        wx.EVT_CATEGORY_USER_INPUT
        wx.EVT_CATEGORY_SOCKET
        wx.EVT_CATEGORY_TIMER
        wx.EVT_CATEGORY_THREAD
        wx.EVT_CATEGORY_ALL


    def test_evtHandlerSubclass(self):
        class MyEvtHandler(wx.EvtHandler):
            def __init__(self, **kwds):
                super(MyEvtHandler, self).__init__()  #**kwds)

        eh = MyEvtHandler()
        eh.Destroy()


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
