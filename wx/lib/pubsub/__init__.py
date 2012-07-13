'''
The publish-subscribe package is called *pubsub*. It provides the 
following modules:

- ``pub``: pubsub's main module. It provides, first and foremost,   
  functions for sending messages and subscribing listeners. It provides 
  functions and classes for tracking pubsub usage, handling exceptions
  in listeners, specificying topics, and various others. 
- ``utils``: subpackage of utility functions and classes, it provides 
  basic pubsub usage trackers, exception handlers, topic tree printer, 
  and more. These can also serve as examples of how to create your 
  own trackers/handlers/etc. 
  
A few other modules inside pubsub are specific to configuring the pubsub API
and must be used only ONCE in an application:

- ``setupkwargs``: module to setup pubsub to use "kwargs" messaging protocol 
  of the Argspec API. This API and protocol are the default so it is 
  not usually necessary to use setupkwargs. 
- ``setupv1``: (deprecated) module to force pubsub to use the legacy
  "version 1" (aka v1) API. Should only be useful to wxPython users
  for legacy code.
- ``setuparg1``: module to setup pubsub to use "arg1" messaging protocol of 
  the Argspec API. This supports the same messaging semantics as legacy API
  but with the Argspec API, useful when transitioning an application 
  from legacy to Argspec API. 
'''

'''
:copyright: Copyright 2006-2009 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE.txt for details.

Last change info:
- $Date: 2011-11-25 23:30:40 -0500 (Fri, 25 Nov 2011) $
- $Revision: 271 $

'''


__all__ = [
    'pub', 'utils',
    'printImported', 'setupkwargs', 'setuparg1', 'setupv1',
    ]


# set our module search path in globalsettings so setup*.py modules 
# can find and modify
import pubsubconf
pubsubconf.setPubsubInfo(__path__, globals())
del pubsubconf # prevent circular ref


def _tryAutoSetupV1():
    '''This function is called automatically when the pubsub module is 
    imported. It determines if the legacy "version 1" API of pubsub should
    be used automatically, by looking for a module called 'autosetuppubsubv1'
    on the module's search path. If this module is found, setupv1 is imported,
    so your application will get v1 API just by doing "from pubsub import ...". 
    If that module is not found then nothing happens and the function
    returns; in this case a "from pubsub import ..." will get the "default" 
    Argspec API unless you explicitly choose a different one. Note that 
    autosetuppubsubv1 is never actually imported, just searched. '''
    try: 
        import autosetuppubsubv1
        
    except ImportError:
        # nothing to do, will use default API
        pass
        
    else:
        # configure for legacy API
        import setupv1
        assert pub is not None
        assert Publisher is pub.Publisher


_tryAutoSetupV1()
