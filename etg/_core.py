#---------------------------------------------------------------------------
# Name:        etg/_core.py
# Author:      Robin Dunn
#
# Created:     8-Nov-2010
# Copyright:   (c) 2010-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools
from etgtools import PyFunctionDef, PyCodeDef, PyPropertyDef

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "_core"   # Base name of the file to generate to for this script
DOCSTRING = """\
The classes in this module are the most commonly used classes for wxPython,
which is why they have been made visible in the core `wx` namespace.
Everything you need for building typical GUI applications is here.
"""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ ]



# The list of other ETG scripts and back-end generator modules that are
# included as part of this module. These items are in their own etg scripts
# for easier maintainability, but their class and function definitions are
# intended to be part of this module, not their own module. This also makes it
# easier to promote one of these to module status later if desired, simply
# remove it from this list of Includes, and change the MODULE value in the
# promoted script to be the same as its NAME.

INCLUDES = [  # base and core stuff
              'wacky_ints',
              'defs',
              'debug',
              'object',
              'wxpy_api',
              'arrayholder',
              'string',
              'filename',
              'arrays',
              'clntdata',
              'clntdatactnr',
              'userdata',
              'wxpybuffer',
              'msgdlg_btnlabel',
              'wxvector',

              'stockgdi',
              'longlong',
              'wxdatetime',
              'stopwatch',

              'windowid',
              'platinfo',
              'vidmode',
              'display',
              'intl',
              'translation',

              'cmndata',
              'gdicmn',
              'geometry',
              'affinematrix2d',
              'position',
              'colour',

              'stream',
              'filesys',

              # GDI and graphics
              'image',
              'gdiobj',
              'bitmap',
              'bmpbndl',
              'icon', 'iconloc', 'iconbndl',
              'font',
              'fontutil',
              'pen',
              'brush',
              'cursor',
              'region',
              'dc',
              'dcclient',
              'dcmemory',
              'dcbuffer',
              'dcscreen',
              'dcgraph',
              'dcmirror',
              'dcprint',
              'dcps',
              'dcsvg',
              'metafile',
              'graphics',
              'imaglist',
              'overlay',
              'palette',
              'renderer',
              'rawbmp',

              # more core
              'access',
              'accel',
              'log',
              'dataobj',
              'dnd',
              'clipbrd',
              'config',
              'variant',
              'tracker',
              'kbdstate',
              'mousestate',
              'tooltip',
              'layout',
              'event',
              'pyevent',
              'sizer', 'gbsizer', 'wrapsizer',
              'stdpaths',

              'eventfilter',
              'evtloop',
              'apptrait',
              'app',

              # basic windows and stuff
              'timer',
              'window',
              'validate',
              'panel',
              'menuitem',
              'menu',
              'scrolwin',
              'vscroll',

              # controls
              'control',
              'ctrlsub',
              'statbmp',
              'stattext',
              'statbox',
              'statusbar',
              'choice',
              'anybutton',
              'button',
              'bmpbuttn',
              'withimage',
              'bookctrl',
              'notebook',
              'splitter',
              'collpane',
              'statline',
              'textcompleter',
              'textentry',
              'textctrl',
              'combobox',
              'checkbox',
              'listbox',
              'checklst',
              'gauge',
              'headercol',
              'headerctrl',
              'srchctrl',
              'radiobox',
              'radiobut',
              'slider',
              'spinbutt',
              'spinctrl',
              'tglbtn',
              'scrolbar',
              'toolbar',
              'infobar',
              'listctrl',
              'treeitemdata',
              'treectrl',
              'pickers',
              'filectrl',
              'combo',
              'choicebk',
              'listbook',
              'toolbook',
              'treebook',
              'simplebook',
              'vlbox',
              'activityindicator',
              'collheaderctrl',

              # toplevel and dialogs
              'nonownedwnd',
              'toplevel',
              'dialog',
              'dirdlg',
              'dirctrl',
              'filedlg',
              'filedlgcustomize',
              'frame',
              'msgdlg',
              'richmsgdlg',
              'progdlg',
              'popupwin',
              'tipwin',
              'colordlg',
              'choicdlg',
              'fdrepdlg',
              'mdi',
              'fontdlg',
              'rearrangectrl',
              'minifram',
              'textdlg',
              'numdlg',

              # misc
              'power',
              'utils',
              'process',
              'uiaction',
              'snglinst',
              'help',
              'cshelp',
              'settings',
              'sysopt',
              'artprov',
              'dragimag',
              'printfw',
              'printdlg',
              'mimetype',
              'busyinfo',
              'caret',
              'fontenum',
              'fontmap',
              'mousemanager',
              'filehistory',
              'cmdproc',
              'fswatcher',
              'preferences',
              'modalhook',
              'unichar',
              'stockitem',
              ]


# Separate the list into those that are generated from ETG scripts and the
# rest. These lists can be used from the build scripts to get a list of
# sources and/or additional dependencies when building this extension module.
ETGFILES = ['etg/%s.py' % NAME] + tools.getEtgFiles(INCLUDES)
DEPENDS = tools.getNonEtgFiles(INCLUDES)
OTHERDEPS = [ 'src/core_ex.py',
              'src/core_ex.cpp' ]


#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    module.check4unittest = False

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode('#include <wxPython/wxpy_api.h>')

    module.addInclude(INCLUDES)
    module.includePyCode('src/core_ex.py', order=10)

    module.addPyFunction('version', '()',
        doc="""Returns a string containing version and port info""",
        body="""\
            if wx.Port == '__WXMSW__':
                port = 'msw'
            elif wx.Port == '__WXMAC__':
                if 'wxOSX-carbon' in wx.PlatformInfo:
                    port = 'osx-carbon'
                else:
                    port = 'osx-cocoa'
            elif wx.Port == '__WXGTK__':
                port = 'gtk'
                if 'gtk2' in wx.PlatformInfo:
                    port = 'gtk2'
                elif 'gtk3' in wx.PlatformInfo:
                    port = 'gtk3'
            else:
                port = '???'
            return "%s %s (phoenix) %s" % (wx.VERSION_STRING, port, wx.wxWidgets_version)
            """)


    module.addPyCode('import typing', order=10)
    module.addPyCode("""\
        _T = typing.TypeVar('_T')
        try:
            _P = typing.ParamSpec('_P')
        except AttributeError:
            import typing_extensions
            _P = typing_extensions.ParamSpec('_P')
        """)
    module.addPyFunction('CallAfter', '(callableObj: typing.Callable[_P, _T], *args: _P.args, **kw: _P.kwargs) -> None', doc="""\
            Call the specified function after the current and pending event
            handlers have been completed.  This is also good for making GUI
            method calls from non-GUI threads.  Any extra positional or
            keyword args are passed on to the callable when it is called.

            :param PyObject callableObj: the callable object
            :param args: arguments to be passed to the callable object
            :param kw: keywords to be passed to the callable object

            .. seealso::
                :ref:`wx.CallLater`

            """,
        body="""\
            assert callable(callableObj), "callableObj is not callable"
            app = wx.GetApp()
            assert app is not None, 'No wx.App created yet'

            if not hasattr(app, "_CallAfterId"):
                app._CallAfterId = wx.NewEventType()
                app.Connect(-1, -1, app._CallAfterId,
                            lambda event: event.callable(*event.args, **event.kw) )
            evt = wx.PyEvent()
            evt.SetEventType(app._CallAfterId)
            evt.callable = callableObj
            evt.args = args
            evt.kw = kw
            wx.PostEvent(app, evt)""")


    module.addPyClass('CallLater', ['typing.Generic[_P, _T]'],
        doc="""\
            A convenience class for :class:`wx.Timer`, that calls the given callable
            object once after the given amount of milliseconds, passing any
            positional or keyword args.  The return value of the callable is
            available after it has been run with the :meth:`~wx.CallLater.GetResult`
            method.

            If you don't need to get the return value or restart the timer
            then there is no need to hold a reference to this object. CallLater
            maintains references to its instances while they are running. When they
            finish, the internal reference is deleted and the GC is free to collect
            naturally.

            .. seealso::
                :func:`wx.CallAfter`

            """,
        items = [
            PyCodeDef('__instances = {}'),
            PyFunctionDef('__init__', '(self, millis, callableObj: typing.Callable[_P, _T], *args: _P.args, **kwargs: _P.kwargs) -> None',
                doc="""\
                    Constructs a new :class:`wx.CallLater` object.

                    :param int millis: number of milliseconds to delay until calling the callable object
                    :param PyObject callableObj: the callable object
                    :param args: arguments to be passed to the callable object
                    :param kw: keyword arguments to be passed to the callable object
                """,

                body="""\
                    assert callable(callableObj), "callableObj is not callable"
                    self.millis = millis
                    self.callable = callableObj
                    self.SetArgs(*args, **kwargs)
                    self.runCount = 0
                    self.running = False
                    self.hasRun = False
                    self.result = None
                    self.timer = None
                    self.Start()"""),

            PyFunctionDef('__del__', '(self)', 'self.Stop()'),

            PyFunctionDef('Start', '(self, millis: typing.Optional[int]=None, *args: _P.args, **kwargs: _P.kwargs) -> None',
                doc="""\
                    (Re)start the timer

                    :param int millis: number of milli seconds
                    :param args: arguments to be passed to the callable object
                    :param kw: keywords to be passed to the callable object

                    """,
                body="""\
                    self.hasRun = False
                    if millis is not None:
                        self.millis = millis
                    if args or kwargs:
                        self.SetArgs(*args, **kwargs)
                    self.Stop()
                    CallLater.__instances[self] = "value irrelevant"  # Maintain a reference to avoid GC
                    self.timer = wx.PyTimer(self.Notify)
                    self.timer.Start(self.millis, wx.TIMER_ONE_SHOT)
                    self.running = True"""),
            PyCodeDef('Restart = Start'),

            PyFunctionDef('Stop', '(self) -> None',
                doc="Stop and destroy the timer.",
                body="""\
                    if self in CallLater.__instances:
                        del CallLater.__instances[self]
                    if self.timer is not None:
                        self.timer.Stop()
                        self.timer = None"""),

            PyFunctionDef('GetInterval', '(self) -> int', """\
                if self.timer is not None:
                    return self.timer.GetInterval()
                else:
                    return 0"""),

            PyFunctionDef('IsRunning', '(self) -> bool',
                """return self.timer is not None and self.timer.IsRunning()"""),

            PyFunctionDef('SetArgs', '(self, *args: _P.args, **kwargs: _P.kwargs) -> None',
                doc="""\
                    (Re)set the args passed to the callable object.  This is
                    useful in conjunction with :meth:`Start` if
                    you want to schedule a new call to the same callable
                    object but with different parameters.

                    :param args: arguments to be passed to the callable object
                    :param kw: keywords to be passed to the callable object

                    """,
                body="""\
                    self.args = args
                    self.kwargs = kwargs"""),

            PyFunctionDef('HasRun', '(self) -> bool', 'return self.hasRun',
                doc="""\
                    Returns whether or not the callable has run.

                    :rtype: bool

                    """),

            PyFunctionDef('GetResult', '(self) -> _T', 'return self.result',
                doc="""\
                    Returns the value of the callable.

                    :rtype: a Python object
                    :return: result from callable
                    """),

            PyFunctionDef('Notify', '(self) -> None',
                doc="The timer has expired so call the callable.",
                body="""\
                    if self.callable and getattr(self.callable, 'im_self', True):
                        self.runCount += 1
                        self.running = False
                        self.result = self.callable(*self.args, **self.kwargs)
                    self.hasRun = True
                    if not self.running:
                        # if it wasn't restarted, then cleanup
                        wx.CallAfter(self.Stop)"""),

            PyPropertyDef('Interval', 'GetInterval'),
            PyPropertyDef('Result', 'GetResult'),
            ])

    module.addPyCode("FutureCall = deprecated(CallLater, 'Use CallLater instead.')")

    module.addPyCode("""\
        def GetDefaultPyEncoding() -> str:
            return "utf-8"
        GetDefaultPyEncoding = deprecated(GetDefaultPyEncoding, msg="wxPython now always uses utf-8")
        """)

    module.addCppFunction('bool', 'IsMainThread', '()',
        doc="Returns ``True`` if the current thread is what wx considers the GUI thread.",
        body="return wxThread::IsMain();")


    module.addInitializerCode("""\
        wxPyPreInit(sipModuleDict);
        """)

    # This code is inserted into the module initialization function
    module.addPostInitializerCode("""\
        wxPyCoreModuleInject(sipModuleDict);
        """)
    # Here is the function it calls
    module.includeCppCode('src/core_ex.cpp')
    module.addItem(etgtools.WigCode("void _wxPyCleanup();"))


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)



#---------------------------------------------------------------------------

if __name__ == '__main__':
    run()
