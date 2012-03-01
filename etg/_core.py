#---------------------------------------------------------------------------
# Name:        etg/_core.py
# Author:      Robin Dunn
#
# Created:     8-Nov-2010
# Copyright:   (c) 2011 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools
from etgtools import PyFunctionDef, PyCodeDef, PyPropertyDef

PACKAGE   = "wx" 
MODULE    = "_core"
NAME      = "_core"   # Base name of the file to generate to for this script
DOCSTRING = ""

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

INCLUDES = [  'defs',
              'object',
              'wxpy_utils',
              'string',
              'arrays',
              'clntdata',
              'userdata',
              'stockgdi',
              
              'windowid',
              'platinfo',
              'vidmode',
              'display',
              'intl',
              
              'cmndata',
              'gdicmn',
              'geometry',
              'position',

              'stream', 'filesys',

              'colour',
              'image',
              'gdiobj',
              'bitmap',
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
              'graphics',
              
              'accel',
              'log',
              'dataobj',
              'config',
              'variant',
              'tracker',
              'kbdstate',
              'mousestate',
              'tooltip',
              'layout',
              'event',
              'pyevent',
              'utils',
              'process',
              'sizer', 'gbsizer', 'wrapsizer',
              'uiaction', 
              
              'eventfilter',
              'evtloop',
              'apptrait',
              'app',

              # basic windows and stuff
              'timer',
              'window',
              'validate',
              'panel',
              'menu',
              'menuitem',
              'imaglist',
              
              
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
              'srchctrl',
              'radiobox', 
              'radiobut',
              'slider',
              'spinbutt',
              'spinctrl',
              'tglbtn',
              'scrolbar',
              
              # toplevel and dialogs
              'nonownedwnd',
              'toplevel',
              'dialog',
              'dirdlg',
              'filedlg',
              'frame',
              'msgdlg',
              'progdlg',
              'popupwin',
              'tipwin',

              # other window types and stuff
              'stdpaths',
              'snglinst',
              'scrolwin',
              'vscroll',
             
              ]


# Separate the list into those that are generated from ETG scripts and the
# rest. These lists can be used from setup.py for a list of sources and a list
# of additional dependencies when building this extension module
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
    
    module.addHeaderCode("""\
    #if defined(__APPLE__)
        // When it's possible that we're building universal binaries with both
        // 32-bit and 64-bit architectures then these need to be undefed because
        // otherwise the values set by configure could conflict with those set
        // based on runtime flags in Python's headers.  We also do something
        // similar in wx/platform.h so it's okay to undef them now because they
        // will be defined again soon.
        #undef SIZEOF_VOID_P
        #undef SIZEOF_LONG
        #undef SIZEOF_SIZE_T

        // Turn off the warning about converting string literals to char*
        // TODO: fix these the right way...
        #pragma GCC diagnostic ignored "-Wwrite-strings"
    #endif
    #ifdef _MSC_VER
        #pragma warning(disable:4800)
        #pragma warning(disable:4190)
    #endif
    
    #include <wx/wx.h>
    """)
    
    module.addInclude(INCLUDES)
    module.includePyCode('src/core_ex.py', order=10)

    module.addPyFunction('version', '()',
        doc="""Returns a string containing version and port info""",
        body="""\
            if wx.Port == '__WXMSW__':
                port = 'msw'
            elif wx.Port == '__WXMAC__':
                if 'wxOSX-carbon' in wx.PortInfo:
                    port = 'osx-carbon'
                else:
                    port = 'osx-cocoa'
            elif wx.Port == '__WXGTK__':
                port = 'gtk'
                if 'gtk2' in wx.PortInfo:
                    port = 'gtk2'
            else:
                port = '???'
            return "%s %s (phoenix)" % (wx.VERSION_STRING, port)
            """)


    module.addPyFunction('CallAfter', '(callableObj, *args, **kw)', doc="""\
            Call the specified function after the current and pending event
            handlers have been completed.  This is also good for making GUI
            method calls from non-GUI threads.  Any extra positional or
            keyword args are passed on to the callable when it is called.
            
            :see: `CallLater`""",
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


    module.addPyClass('CallLater', ['object'], 
        doc="""\
            A convenience class for `wx.Timer`, that calls the given callable
            object once after the given amount of milliseconds, passing any
            positional or keyword args.  The return value of the callable is
            availbale after it has been run with the `GetResult` method.
            
            If you don't need to get the return value or restart the timer
            then there is no need to hold a reference to this object.  It will
            hold a reference to itself while the timer is running (the timer
            has a reference to self.Notify) but the cycle will be broken when
            the timer completes, automatically cleaning up the wx.CallLater
            object.
            
            :see: `CallAfter`""",
        items = [
            PyFunctionDef('__init__', '(self, millis, callableObj, *args, **kwargs)',
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
            
            PyFunctionDef('Start', '(self, millis=None, *args, **kwargs)', 
                doc="(Re)start the timer",
                body="""\
                    self.hasRun = False
                    if millis is not None:
                        self.millis = millis
                    if args or kwargs:
                        self.SetArgs(*args, **kwargs)
                    self.Stop()
                    self.timer = wx.PyTimer(self.Notify)
                    self.timer.Start(self.millis, wx.TIMER_ONE_SHOT)
                    self.running = True"""),
            PyCodeDef('Restart = Start'),
            
            PyFunctionDef('Stop', '(self)', 
                doc="Stop and destroy the timer.",
                body="""\
                    if self.timer is not None:
                        self.timer.Stop()
                        self.timer = None"""),
            
            PyFunctionDef('GetInterval', '(self)', """\
                if self.timer is not None:
                    return self.timer.GetInterval()
                else:
                    return 0"""),
            
            PyFunctionDef('IsRunning', '(self)', 
                """return self.timer is not None and self.timer.IsRunning()"""),
            
            PyFunctionDef('SetArgs', '(self, *args, **kwargs)', 
                doc="""\
                    (Re)set the args passed to the callable object.  This is
                    useful in conjunction with Restart if you want to schedule a
                    new call to the same callable object but with different
                    parameters.""",
                body="""\
                    self.args = args
                    self.kwargs = kwargs"""),
            
            PyFunctionDef('HasRun', '(self)', 'return self.hasRun'),
            PyFunctionDef('GetResult', '(self)', 'return self.result'),
            
            PyFunctionDef('Notify', '(self)', 
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


    module.addPreInitializerCode("""\
        wxPyPreInit(sipModuleDict);
        """)

    # This code is inserted into the module initialization function
    module.addPostInitializerCode("""\
        wxPyCoreModuleInject(sipModuleDict);
        """)
    # Here is the function it calls
    module.includeCppCode('src/core_ex.cpp')
                      
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    

    
#---------------------------------------------------------------------------

if __name__ == '__main__':
    run()
