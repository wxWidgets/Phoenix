
# A little trick to make 'wx' be a reference to this module so wx.Names can
# be used in the python code here.
import sys as _sys
wx = _sys.modules[__name__]
 

# Load version numbers from __version__...  Ensure that major and minor
# versions are the same for both wxPython and wxWidgets.
from __version__ import *
import _core
__version__ = VERSION_STRING
assert MAJOR_VERSION == _core.MAJOR_VERSION, "wxPython/wxWidgets version mismatch"
assert MINOR_VERSION == _core.MINOR_VERSION, "wxPython/wxWidgets version mismatch"
if RELEASE_NUMBER != _core.RELEASE_NUMBER:
    import warnings
    warnings.warn("wxPython/wxWidgets release number mismatch")
del _core


def version():
    """Returns a string containing version and port info"""
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
         
                       
import warnings
class wxPyDeprecationWarning(DeprecationWarning):
    pass
warnings.simplefilter('default', wxPyDeprecationWarning)
del warnings

def deprecated(item, msg=''):
    """
    Create a delegating wrapper that raises a deprecation warning.  Can be
    used with callable objects (functions, methods, classes) or with
    properties.
    """
    import warnings
    if isinstance(item, type):
        # It is a class.  Make a subclass that raises a warning.
        class DeprecatedClassProxy(item):
            def __init__(*args, **kw):
                warnings.warn("Using deprecated class. %s" % msg,
                          wxPyDeprecationWarning, stacklevel=2)
                item.__init__(*args, **kw)
        DeprecatedClassProxy.__name__ = item.__name__
        return DeprecatedClassProxy
    
    elif callable(item):
        # wrap a new function around the callable
        def deprecated_func(*args, **kw):
            warnings.warn("Call to deprecated item '%s'. %s" % (item.__name__, msg),
                          wxPyDeprecationWarning, stacklevel=2)
            return item(*args, **kw)
        deprecated_func.__name__ = item.__name__
        deprecated_func.__doc__ = item.__doc__
        if hasattr(item, '__dict__'):
            deprecated_func.__dict__.update(item.__dict__)
        return deprecated_func
        
    elif hasattr(item, '__get__'):
        # it should be a property if there is a getter
        class DepGetProp(object):
            def __init__(self,item, msg):
                self.item = item
                self.msg = msg
            def __get__(self, inst, klass):
                warnings.warn("Accessing deprecated property. %s" % msg,
                              wxPyDeprecationWarning, stacklevel=2)
                return self.item.__get__(inst, klass)
        class DepGetSetProp(DepGetProp):
            def __set__(self, inst, val):
                warnings.warn("Accessing deprecated property. %s" % msg,
                              wxPyDeprecationWarning, stacklevel=2)
                return self.item.__set__(inst, val)
        class DepGetSetDelProp(DepGetSetProp):
            def __delete__(self, inst):
                warnings.warn("Accessing deprecated property. %s" % msg,
                              wxPyDeprecationWarning, stacklevel=2)
                return self.item.__delete__(inst)
        
        if hasattr(item, '__set__') and hasattr(item, '__delete__'):
            return DepGetSetDelProp(item, msg)
        elif hasattr(item, '__set__'):
            return DepGetSetProp(item, msg)
        else:
            return DepGetProp(item, msg)
    else:
        raise TypeError, "unsupported type %s" % type(item)
                   

#----------------------------------------------------------------------------

def CallAfter(callableObj, *args, **kw):
    """
    Call the specified function after the current and pending event
    handlers have been completed.  This is also good for making GUI
    method calls from non-GUI threads.  Any extra positional or
    keyword args are passed on to the callable when it is called.

    :see: `wx.CallLater`
    """
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
    wx.PostEvent(app, evt)

#----------------------------------------------------------------------------


class CallLater(object):
    """
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
    
    :see: `wx.CallAfter`
    """
    def __init__(self, millis, callableObj, *args, **kwargs):
        assert callable(callableObj), "callableObj is not callable"
        self.millis = millis
        self.callable = callableObj
        self.SetArgs(*args, **kwargs)
        self.runCount = 0
        self.running = False
        self.hasRun = False
        self.result = None
        self.timer = None
        self.Start()

    def __del__(self):
        self.Stop()


    def Start(self, millis=None, *args, **kwargs):
        """
        (Re)start the timer
        """
        self.hasRun = False
        if millis is not None:
            self.millis = millis
        if args or kwargs:
            self.SetArgs(*args, **kwargs)
        self.Stop()
        self.timer = wx.PyTimer(self.Notify)
        self.timer.Start(self.millis, wx.TIMER_ONE_SHOT)
        self.running = True
    Restart = Start


    def Stop(self):
        """
        Stop and destroy the timer.
        """
        if self.timer is not None:
            self.timer.Stop()
            self.timer = None


    def GetInterval(self):
        if self.timer is not None:
            return self.timer.GetInterval()
        else:
            return 0


    def IsRunning(self):
        return self.timer is not None and self.timer.IsRunning()


    def SetArgs(self, *args, **kwargs):
        """
        (Re)set the args passed to the callable object.  This is
        useful in conjunction with Restart if you want to schedule a
        new call to the same callable object but with different
        parameters.
        """
        self.args = args
        self.kwargs = kwargs


    def HasRun(self):
        return self.hasRun

    def GetResult(self):
        return self.result

    def Notify(self):
        """
        The timer has expired so call the callable.
        """
        if self.callable and getattr(self.callable, 'im_self', True):
            self.runCount += 1
            self.running = False
            self.result = self.callable(*self.args, **self.kwargs)
        self.hasRun = True
        if not self.running:
            # if it wasn't restarted, then cleanup
            wx.CallAfter(self.Stop)

    Interval = property(GetInterval)
    Result = property(GetResult)

#----------------------------------------------------------------------------

PyAssertionError = wx.wxAssertionError  # an alias for compatibility with Classic

#----------------------------------------------------------------------------
