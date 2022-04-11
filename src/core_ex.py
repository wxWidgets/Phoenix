import sys as _sys

# Load version numbers from __version__ and some other initialization tasks...
if 'wxEVT_NULL' in dir():
    from wx.__version__ import *
    import wx._core
    __version__ = VERSION_STRING

    # Add the build type to PlatformInfo
    PlatformInfo = PlatformInfo + ('build-type: ' + BUILD_TYPE, )

    # Register a function to be called when Python terminates that will clean
    # up and release all system resources that wxWidgets allocated.
    import atexit
    atexit.register(wx._core._wxPyCleanup)
    del atexit

else:
    Port = ''
    Platform = ''
    PlatformInfo = []

# A little trick to make 'wx' be a reference to this module so wx.Names can
# be used in the python code here.
wx = _sys.modules[__name__]


import warnings
class wxPyDeprecationWarning(DeprecationWarning):
    pass

warnings.simplefilter('default', wxPyDeprecationWarning)
del warnings


def deprecated(item, msg='', useName=False):
    """
    Create a delegating wrapper that raises a deprecation warning.  Can be
    used with callable objects (functions, methods, classes) or with
    properties.
    """
    import warnings

    name = ''
    if useName:
        try:
            name = ' ' + item.__name__
        except AttributeError:
            pass

    if isinstance(item, type):
        # It is a class.  Make a subclass that raises a warning.
        class DeprecatedClassProxy(item):
            def __init__(*args, **kw):
                warnings.warn("Using deprecated class%s. %s" % (name, msg),
                          wxPyDeprecationWarning, stacklevel=2)
                item.__init__(*args, **kw)
        DeprecatedClassProxy.__name__ = item.__name__
        return DeprecatedClassProxy

    elif callable(item):
        # wrap a new function around the callable
        def deprecated_func(*args, **kw):
            warnings.warn("Call to deprecated item%s. %s" % (name, msg),
                          wxPyDeprecationWarning, stacklevel=2)
            if not kw:
                return item(*args)
            return item(*args, **kw)
        deprecated_func.__name__ = item.__name__
        deprecated_func.__doc__ = item.__doc__
        if hasattr(item, '__dict__'):
            deprecated_func.__dict__.update(item.__dict__)
        return deprecated_func

    elif hasattr(item, '__get__'):
        # it should be a property if there is a getter
        class DepGetProp(object):
            def __init__(self, item, msg):
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
        raise TypeError("unsupported type %s" % type(item))


def deprecatedMsg(msg):
    """
    A wrapper for the deprecated decorator that makes it easier to attach a
    custom message to the warning that is raised if the item is used. This
    can also be used in the @decorator role since it returns the real
    decorator when called.
    """
    import functools
    return functools.partial(deprecated, msg=msg, useName=True)

#----------------------------------------------------------------------------

EmptyString = ""

#----------------------------------------------------------------------------
