
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

PyAssertionError = wx.wxAssertionError  # an alias for compatibility with Classic

#----------------------------------------------------------------------------
