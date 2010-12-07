
class PyOnDemandOutputWindow:
    """
    A class that can be used for redirecting Python's stdout and
    stderr streams.  It will do nothing until something is wrriten to
    the stream at which point it will create a Frame with a text area
    and write the text there.
    """
    def __init__(self, title="wxPython: stdout/stderr"):
        self.frame  = None
        self.title  = title
        self.pos    = wx.DefaultPosition
        self.size   = (450, 300)
        self.parent = None

    def SetParent(self, parent):
        """Set the window to be used as the popup Frame's parent."""
        self.parent = parent


    def CreateOutputWindow(self, st):
        self.frame = wx.Frame(self.parent, -1, self.title, self.pos, self.size,
                              style=wx.DEFAULT_FRAME_STYLE)
        self.text  = wx.TextCtrl(self.frame, -1, "",
                                 style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.text.AppendText(st)
        self.frame.Show(True)
        self.frame.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        

    def OnCloseWindow(self, event):
        if self.frame is not None:
            self.frame.Destroy()
        self.frame = None
        self.text  = None
        self.parent = None


    # These methods provide the file-like output behaviour.
    def write(self, text):
        """
        Create the output window if needed and write the string to it.
        If not called in the context of the gui thread then uses
        CallAfter to do the work there.
        """        
        if self.frame is None:
            if not wx.Thread.IsMain():
                wx.CallAfter(self.CreateOutputWindow, text)
            else:
                self.CreateOutputWindow(text)
        else:
            if not wx.Thread.IsMain():
                wx.CallAfter(self.text.AppendText, text)
            else:
                self.text.AppendText(text)


    def close(self):
        if self.frame is not None:
            wx.CallAfter(self.frame.Close)


    def flush(self):
        pass
    


#----------------------------------------------------------------------

class App(wx.PyApp):
    """
    The ``wx.App`` class represents the application and is used to:

      * bootstrap the wxPython system and initialize the underlying
        gui toolkit
      * set and get application-wide properties
      * implement the native windowing system main message or event loop,
        and to dispatch events to window instances
      * etc.

    Every wx application must have a single ``wx.App`` instance, and all
    creation of UI objects should be delayed until after the ``wx.App`` object
    has been created in order to ensure that the gui platform and wxWidgets
    have been fully initialized.

    Normally you would derive from this class and implement an ``OnInit``
    method that creates a frame and then calls ``self.SetTopWindow(frame)``,
    however ``wx.App`` is also usable on it's own without derivation.
    """
    
    outputWindowClass = PyOnDemandOutputWindow

    def __init__(self,
                 redirect=False,
                 filename=None,
                 useBestVisual=False,
                 clearSigInt=True):
        """
        Construct a ``wx.App`` object.  

        :param redirect: Should ``sys.stdout`` and ``sys.stderr`` be
            redirected?  Defaults to False. If ``filename`` is None
            then output will be redirected to a window that pops up
            as needed.  (You can control what kind of window is created
            for the output by resetting the class variable
            ``outputWindowClass`` to a class of your choosing.)

        :param filename: The name of a file to redirect output to, if
            redirect is True.

        :param useBestVisual: Should the app try to use the best
            available visual provided by the system (only relevant on
            systems that have more than one visual.)  This parameter
            must be used instead of calling `SetUseBestVisual` later
            on because it must be set before the underlying GUI
            toolkit is initialized.

        :param clearSigInt: Should SIGINT be cleared?  This allows the
            app to terminate upon a Ctrl-C in the console like other
            GUI apps will.

        :note: You should override OnInit to do applicaition
            initialization to ensure that the system, toolkit and
            wxWidgets are fully initialized.
        """
        
        wx.PyApp.__init__(self)

        # make sure we can create a GUI
        if not self.IsDisplayAvailable():
            
            if wx.Port == "__WXMAC__":
                msg = """This program needs access to the screen.
Please run with a Framework build of python, and only when you are
logged in on the main display of your Mac."""
                
            elif wx.Port == "__WXGTK__":
                msg ="Unable to access the X Display, is $DISPLAY set properly?"

            else:
                msg = "Unable to create GUI"
                # TODO: more description is needed for wxMSW...

            raise SystemExit(msg)
        
        # This has to be done before OnInit
        self.SetUseBestVisual(useBestVisual)

        # Set the default handler for SIGINT.  This fixes a problem
        # where if Ctrl-C is pressed in the console that started this
        # app then it will not appear to do anything, (not even send
        # KeyboardInterrupt???)  but will later segfault on exit.  By
        # setting the default handler then the app will exit, as
        # expected (depending on platform.)
        if clearSigInt:
            try:
                import signal
                signal.signal(signal.SIGINT, signal.SIG_DFL)
            except:
                pass

        # Save and redirect the stdio to a window?
        self.stdioWin = None
        self.saveStdio = (_sys.stdout, _sys.stderr)
        if redirect:
            self.RedirectStdio(filename)

##        # Use Python's install prefix as the default  
##        wx.StandardPaths.Get().SetInstallPrefix(_sys.prefix)

##        # Until the new native control for wxMac is up to par, still use the generic one.
##        wx.SystemOptions.SetOptionInt("mac.listctrl.always_use_generic", 1)

        # This finishes the initialization of wxWindows and then calls
        # the OnInit that should be present in the derived class
        self._BootstrapApp()


    def OnPreInit(self):
        """
        Things that must be done after _BootstrapApp has done its thing, but
        would be nice if they were already done by the time that OnInit is
        called.
        """
##        wx.StockGDI._initStockObjects()
        

    def __del__(self):
        self.RestoreStdio()  # Just in case the MainLoop was overridden

    def Destroy(self):
##        self.this.own(False)
        wx.PyApp.Destroy(self)

    def SetTopWindow(self, frame):
        """Set the \"main\" top level window"""
        if self.stdioWin:
            self.stdioWin.SetParent(frame)
        wx.PyApp.SetTopWindow(self, frame)


    def MainLoop(self):
        """Execute the main GUI event loop"""
        wx.PyApp.MainLoop(self)
        self.RestoreStdio()


    def RedirectStdio(self, filename=None):
        """Redirect sys.stdout and sys.stderr to a file or a popup window."""
        if filename:
            _sys.stdout = _sys.stderr = open(filename, 'a')
        else:
            self.stdioWin = self.outputWindowClass()
            _sys.stdout = _sys.stderr = self.stdioWin


    def RestoreStdio(self):
        try:
            _sys.stdout, _sys.stderr = self.saveStdio
        except:
            pass


    def SetOutputWindowAttributes(self, title=None, pos=None, size=None):
        """
        Set the title, position and/or size of the output window if the stdio
        has been redirected. This should be called before any output would
        cause the output window to be created.
        """
        if self.stdioWin:
            if title is not None:
                self.stdioWin.title = title
            if pos is not None:
                self.stdioWin.pos = pos
            if size is not None:
                self.stdioWin.size = size
            
#----------------------------------------------------------------------------

@deprecated
class PySimpleApp(App):
    """
    This class is deprecated.  Please use wx.App instead.
    """
    def __init__(self, *args, **kw):
        App.__init__(self, *args, **kw)


## #----------------------------------------------------------------------------
## # DO NOT hold any other references to this object.  This is how we
## # know when to cleanup system resources that wxWidgets is holding.  When
## # the sys module is unloaded, the refcount on sys.__wxPythonCleanup
## # goes to zero and it calls the wx.App_CleanUp function.

## #class __wxPyCleanup:
##     #def __init__(self):
##         #self.cleanup = _core_.App_CleanUp
##     #def __del__(self):
##         #self.cleanup()

## #_sys.__wxPythonCleanup = __wxPyCleanup()
