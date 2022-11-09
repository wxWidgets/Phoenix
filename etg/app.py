#---------------------------------------------------------------------------
# Name:        etg/app.py
# Author:      Robin Dunn
#
# Created:     22-Nov-2010
# Copyright:   (c) 2010-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools
from etgtools import PyFunctionDef, PyCodeDef, PyPropertyDef

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "app"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxAppConsole',
           'wxApp',
           ]

OTHERDEPS = [ 'src/app_ex.cpp',   # and some C++ code too
              ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.find('wxDISABLE_DEBUG_SUPPORT').ignore()

    c = module.find('wxAppConsole')
    assert isinstance(c, etgtools.ClassDef)

    etgtools.prependText(c.detailedDoc,
         "Note that it is not intended for this class to be used directly from "
         "Python. It is wrapped just for inheriting its methods in :class:`App`.")

    # There's no need for the command line stuff as Python has its own ways to
    # deal with that
    c.find('argc').ignore()
    c.find('argv').ignore()
    c.find('OnCmdLineError').ignore()
    c.find('OnCmdLineHelp').ignore()
    c.find('OnCmdLineParsed').ignore()
    c.find('OnInitCmdLine').ignore()

    c.find('HandleEvent').ignore()

    # We will use OnAssertFailure, but I don't think we should let it be
    # overridden in Python.
    c.find('OnAssertFailure').ignore()

    # TODO: Decide if these should be visible from Python. They are for
    # dealing with C/C++ exceptions, but perhaps we could also add the ability
    # to deal with unhandled Python exceptions using these (overridable)
    # methods too.
    c.find('OnExceptionInMainLoop').ignore()
    c.find('OnFatalException').ignore()
    c.find('OnUnhandledException').ignore()
    c.find('StoreCurrentException').ignore()
    c.find('RethrowStoredException').ignore()

    # Release the GIL for potentially blocking or long-running functions
    c.find('MainLoop').releaseGIL()
    c.find('ProcessPendingEvents').releaseGIL()
    c.find('Yield').releaseGIL()

    c.addProperty('AppDisplayName GetAppDisplayName SetAppDisplayName')
    c.addProperty('AppName GetAppName SetAppName')
    c.addProperty('ClassName GetClassName SetClassName')
    c.addProperty('VendorDisplayName GetVendorDisplayName SetVendorDisplayName')
    c.addProperty('VendorName GetVendorName SetVendorName')
    c.addProperty('Traits GetTraits')

    #-------------------------------------------------------
    c = module.find('wxApp')

    # Add a new C++ wxPyApp class that adds empty Mac* methods for other
    # platforms, and other goodies, then change the name so SIP will
    # generate code wrapping this class as if it was the wxApp class seen in
    # the DoxyXML.
    c.includeCppCode('src/app_ex.cpp')

    # Now change the class name, ctors and dtor names from wxApp to wxPyApp
    for item in c.allItems():
        if item.name == 'wxApp':
            item.name = 'wxPyApp'
        if item.name == '~wxApp':
            item.name = '~wxPyApp'

    c.find('ProcessMessage').ignore()

    c.addCppMethod('void', 'MacHideApp', '()',
        doc="""\
            Hide all application windows just as the user can do with the
            system Hide command.  Mac only.""",
        body="""\
            #ifdef __WXMAC__
                self->MacHideApp();
            #endif
            """)

    c.addCppMethod('int', 'GetComCtl32Version', '()',
        isStatic=True,
        doc="""\
        Returns 400, 470, 471, etc. for comctl32.dll 4.00, 4.70, 4.71 or 0 if
        it wasn't found at all.  Raises an exception on non-Windows platforms.""",
        body="""\
            #ifdef __WXMSW__
                return wxApp::GetComCtl32Version();
            #else
                wxPyRaiseNotImplemented();
                return 0;
            #endif
            """)


    # Remove the virtualness from these methods
    for m in [ 'GetDisplayMode', 'GetLayoutDirection', 'GetTopWindow', 'IsActive',
               'SafeYield', 'SafeYieldFor', 'SetDisplayMode',
               'SetNativeTheme', ]:
        c.find(m).isVirtual = False

    # Methods we implement in wxPyApp beyond what are in wxApp, plus some
    # overridden virtuals (or at least some that we want the wrapper
    # generator to treat as if they are overridden.)
    #
    # TODO: Add them as etg method objects instead of a WigCode block so the
    # documentation generators will see them too
    c.addItem(etgtools.WigCode("""\
        protected:
        virtual bool TryBefore(wxEvent& event);
        virtual bool TryAfter(wxEvent& event);

        public:
        virtual int  MainLoop() /ReleaseGIL/;
        virtual void OnPreInit();
        virtual bool OnInit();
        virtual bool OnInitGui();
        virtual int  OnRun();
        virtual int  OnExit();

        void         _BootstrapApp();

        static long GetMacAboutMenuItemId();
        static long GetMacPreferencesMenuItemId();
        static long GetMacExitMenuItemId();
        static wxString GetMacHelpMenuTitleName();
        static void SetMacAboutMenuItemId(long val);
        static void SetMacPreferencesMenuItemId(long val);
        static void SetMacExitMenuItemId(long val);
        static void SetMacHelpMenuTitleName(const wxString& val);
        """))


    # Add these methods by creating extractor objects so they can be tweaked
    # like normal, their docs will be able to be generated, etc.
    c.addItem(etgtools.MethodDef(
        protection='public', type='wxAppAssertMode', name='GetAssertMode', argsString='()',
        briefDoc="Returns the current mode for how the application responds to wx asserts.",
        className=c.name))

    m = etgtools.MethodDef(
        protection='public', type='void', name='SetAssertMode', argsString='(wxAppAssertMode mode)',
        briefDoc="""\
        Set the mode indicating how the application responds to wx assertion
        statements. Valid settings are a combination of these flags:

            - wx.APP_ASSERT_SUPPRESS
            - wx.APP_ASSERT_EXCEPTION
            - wx.APP_ASSERT_DIALOG
            - wx.APP_ASSERT_LOG

        The default behavior is to raise a wx.wxAssertionError exception.
        """,
        className=c.name)

    m.addItem(etgtools.ParamDef(type='wxAppAssertMode', name='wxAppAssertMode'))
    c.addItem(m)

    c.addItem(etgtools.MethodDef(
        protection='public', isStatic=True, type='bool', name='IsDisplayAvailable', argsString='()',
        briefDoc="""\
        Returns True if the application is able to connect to the system's
        display, or whatever the equivallent is for the platform.""",
        className=c.name))

    # Release the GIL for potentially blocking or long-running functions
    c.find('SafeYield').releaseGIL()
    c.find('SafeYieldFor').releaseGIL()

    c.addProperty('AssertMode GetAssertMode SetAssertMode')
    c.addProperty('DisplayMode GetDisplayMode SetDisplayMode')
    c.addProperty('ExitOnFrameDelete GetExitOnFrameDelete SetExitOnFrameDelete')
    c.addProperty('LayoutDirection GetLayoutDirection')
    c.addProperty('UseBestVisual GetUseBestVisual SetUseBestVisual')
    c.addProperty('TopWindow GetTopWindow SetTopWindow')

    c.find('GTKSuppressDiagnostics').setCppCode("""\
        #ifdef __WXGTK__
            wxApp::GTKSuppressDiagnostics(flags);
        #endif
        """)

    c.find('GTKAllowDiagnosticsControl').setCppCode("""\
        #ifdef __WXGTK__
            wxApp::GTKAllowDiagnosticsControl();
        #endif
        """)
           
    c.find('GetGUIInstance').ignore()


    #-------------------------------------------------------

    module.find('wxHandleFatalExceptions').setCppCode("""\
        #if wxUSE_ON_FATAL_EXCEPTION
            return wxHandleFatalExceptions(doIt);
        #else
            wxLogInfo("This build of wxWidgets does not support wxHandleFatalExceptions.");
            return false;
        #endif
        """)

    #-------------------------------------------------------

    module.addHeaderCode("""\
        enum wxAppAssertMode {
            wxAPP_ASSERT_SUPPRESS  = 1,
            wxAPP_ASSERT_EXCEPTION = 2,
            wxAPP_ASSERT_DIALOG    = 4,
            wxAPP_ASSERT_LOG       = 8
        };""")
    # add extractor objects for the enum too
    enum = etgtools.EnumDef(name='wxAppAssertMode')
    for eitem in "wxAPP_ASSERT_SUPPRESS wxAPP_ASSERT_EXCEPTION wxAPP_ASSERT_DIALOG wxAPP_ASSERT_LOG".split():
        enum.addItem(etgtools.EnumValueDef(name=eitem))
    module.insertItemBefore(c, enum)

    module.addHeaderCode("""\
        wxAppConsole* wxGetApp();
        """)
    module.find('wxTheApp').ignore()
    f = module.find('wxGetApp')
    f.type = 'wxAppConsole*'
    f.briefDoc = "Returns the current application object."
    f.detailedDoc = []


    module.find('wxYield').releaseGIL()
    module.find('wxSafeYield').releaseGIL()

    module.addPyFunction('YieldIfNeeded', '()',
        doc="Convenience function for wx.GetApp().Yield(True)",
        body="return wx.GetApp().Yield(True)")

    #-------------------------------------------------------

    # Now add extractor objects for the main App class as a Python class,
    # deriving from the wx.PyApp class that we created above. Also define the
    # stdio helper class too.


    module.addPyClass('PyOnDemandOutputWindow', ['object'],
        doc="""\
            A class that can be used for redirecting Python's stdout and
            stderr streams.  It will do nothing until something is wrriten to
            the stream at which point it will create a Frame with a text area
            and write the text there.
            """,
        items=[
            PyFunctionDef('__init__', '(self, title="wxPython: stdout/stderr")',
                body="""\
                    self.frame  = None
                    self.title  = title
                    self.pos    = wx.DefaultPosition
                    self.size   = (450, 300)
                    self.parent = None
                    """),

            PyFunctionDef('SetParent', '(self, parent)',
                doc="""Set the window to be used as the popup Frame's parent.""",
                body="""self.parent = parent"""),

            PyFunctionDef('CreateOutputWindow', '(self, txt)',
                doc="",
                body="""\
                    self.frame = wx.Frame(self.parent, -1, self.title, self.pos, self.size,
                                          style=wx.DEFAULT_FRAME_STYLE)
                    self.text  = wx.TextCtrl(self.frame, -1, "",
                                             style=wx.TE_MULTILINE|wx.TE_READONLY)
                    self.text.AppendText(txt)
                    self.frame.Show(True)
                    self.frame.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
                    """),

            PyFunctionDef('OnCloseWindow', '(self, event)',
                doc="",
                body="""\
                    if self.frame is not None:
                        self.frame.Destroy()
                    self.frame = None
                    self.text  = None
                    self.parent = None
                    """),

            # These methods provide the file-like output behaviour.
            PyFunctionDef('write', '(self, text)',
                doc="""\
                    Create the output window if needed and write the string to it.
                    If not called in the context of the gui thread then CallAfter is
                    used to do the work there.
                    """,
                body="""\
                    if self.frame is None:
                        if not wx.IsMainThread():
                            wx.CallAfter(self.CreateOutputWindow, text)
                        else:
                            self.CreateOutputWindow(text)
                    else:
                        if not wx.IsMainThread():
                            wx.CallAfter(self.text.AppendText, text)
                        else:
                            self.text.AppendText(text)
                     """),

            PyFunctionDef('close', '(self)',
                doc="",
                body="""\
                    if self.frame is not None:
                        wx.CallAfter(self.frame.Close)
                    """),

            PyFunctionDef('flush', '(self)', 'pass'),
            ])


    module.addPyClass('App', ['PyApp'],
        doc="""\
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
            however ``wx.App`` is also usable on its own without derivation.

            :note: In Python the wrapper for the C++ class ``wxApp`` has been renamed tp
                :class:`wx.PyApp`. This ``wx.App`` class derives from ``wx.PyApp``, and is
                responsible for handling the Python-specific needs for bootstrapping the
                wxWidgets library and other Python integration related requirements.
            """,

        items=[
            PyCodeDef('outputWindowClass = PyOnDemandOutputWindow'),

            PyFunctionDef('__init__', '(self, redirect=False, filename=None, useBestVisual=False, clearSigInt=True)',
                doc="""\
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

                    :note: You should override OnInit to do application
                        initialization to ensure that the system, toolkit and
                        wxWidgets are fully initialized.
                    """,
                body="""\
                    PyApp.__init__(self)

                    # make sure we can create a GUI
                    if not self.IsDisplayAvailable():

                        if wx.Port == "__WXMAC__":
                            msg = "This program needs access to the screen. Please run with a\\n" \\
                                  "Framework build of python, and only when you are logged in\\n" \\
                                  "on the main display of your Mac."

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

                    # Use Python's install prefix as the default
                    prefix = _sys.prefix
                    if isinstance(prefix, (bytes, bytearray)):
                        prefix = prefix.decode(_sys.getfilesystemencoding())
                    wx.StandardPaths.Get().SetInstallPrefix(prefix)

                    # Until the new native control for wxMac is up to par, still use the generic one.
                    wx.SystemOptions.SetOption("mac.listctrl.always_use_generic", 1)

                    # This finishes the initialization of wxWindows and then calls
                    # the OnInit that should be present in the derived class
                    self._BootstrapApp()
                    """),

            PyFunctionDef('OnPreInit', '(self)',
                doc="""\
                    Things that must be done after _BootstrapApp has done its thing, but
                    would be nice if they were already done by the time that OnInit is
                    called.  This can be overridden in derived classes, but be sure to call
                    this method from there.
                    """,
                body="""\
                    wx.StockGDI._initStockObjects()
                    self.InitLocale()
                    """),

            PyFunctionDef('__del__', '(self)',
                doc="",
                body="""\
                    # Just in case the MainLoop was overridden without calling RestoreStio
                    self.RestoreStdio()
                    """),

            PyFunctionDef('SetTopWindow', '(self, frame)',
                doc="""\
                    Set the \"main\" top level window, which will be used for the parent of
                    the on-demand output window as well as for dialogs that do not have
                    an explicit parent set.
                    """,
                body="""\
                    if self.stdioWin:
                        self.stdioWin.SetParent(frame)
                    wx.PyApp.SetTopWindow(self, frame)
                    """),

            PyFunctionDef('MainLoop', '(self)',
                doc="""Execute the main GUI event loop""",
                body="""\
                    rv = wx.PyApp.MainLoop(self)
                    self.RestoreStdio()
                    return rv
                    """),

            PyFunctionDef('RedirectStdio', '(self, filename=None)',
                doc="""Redirect sys.stdout and sys.stderr to a file or a popup window.""",
                body="""\
                    if filename:
                        _sys.stdout = _sys.stderr = open(filename, 'a')
                    else:
                        self.stdioWin = self.outputWindowClass()
                        _sys.stdout = _sys.stderr = self.stdioWin
                    """),

            PyFunctionDef('RestoreStdio', '(self)',
                doc="",
                body="""\
                    try:
                        _sys.stdout, _sys.stderr = self.saveStdio
                    except:
                        pass
                    """),

            PyFunctionDef('SetOutputWindowAttributes', '(self, title=None, pos=None, size=None)',
                doc="""\
                    Set the title, position and/or size of the output window if the stdio
                    has been redirected. This should be called before any output would
                    cause the output window to be created.
                    """,
                body="""\
                    if self.stdioWin:
                        if title is not None:
                            self.stdioWin.title = title
                        if pos is not None:
                            self.stdioWin.pos = pos
                        if size is not None:
                            self.stdioWin.size = size
                    """),

            PyFunctionDef('InitLocale', '(self)',
                doc="""\
                    Starting with version 3.8 on Windows, Python is now setting the locale
                    to what is defined by the system as the default locale. This causes
                    problems with wxWidgets which expects to be able to manage the locale
                    via the wx.Locale class, so the locale will be reset here to be the
                    default "C" locale settings.

                    If you have troubles from the default behavior of this method you can
                    override it in a derived class to behave differently. Please report
                    the problem you encountered.
                    """,
                body="""\
                    if _sys.platform.startswith('win') and _sys.version_info > (3,8):
                        import locale
                        locale.setlocale(locale.LC_ALL, "C")
                    """),

            PyFunctionDef('ResetLocale', '(self)',
                doc="""\
                    This method is now a NOP and will be deprecated.
                    """,
                body="""\
                    pass
                    """),

            PyFunctionDef('Get', '()', isStatic=True,
                doc="""\
                    A staticmethod returning the currently active application object.
                    Essentially just a more pythonic version of :meth:`GetApp`.""",
                body="return GetApp()"
                )
            ])



    module.addPyClass('PySimpleApp', ['App'], deprecated="Use :class:`App` instead.",
        doc="""This class is deprecated.  Please use :class:`App` instead.""",
        items=[
            PyFunctionDef('__init__', '(self, *args, **kw)',
                body="App.__init__(self, *args, **kw)")
            ])


    module.find('wxInitialize').ignore()
    module.find('wxUninitialize').ignore()

    for item in module.allItems():
        if item.name == 'wxEntry':
            item.ignore()


    module.find('wxWakeUpIdle').mustHaveApp()


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------

#---------------------------------------------------------------------------


if __name__ == '__main__':
    run()

