# Name:          __init__.py
# Package:      wx.lib.pubsub
#
# Purpose:      Pubsub package initialization
#
# Author:       Oliver Schoenborn
# Copyright:    Oliver Schoenborn
# Licence:      BSD, see LICENSE_BSD_Simple.txt for details

# History:      Created 2000/2006
#
# Tags:         phoenix-port, documented
#
#----------------------------------------------------------------------------

"""
**pubsub** is a Python package which provides a publish/subscribe API to facilitate event-based
programming and decoupling of components of an application via the Observer design pattern.

Using the Observer pattern in your application can dramatically simplify its design and improve
testability. Basically you just have some part(s) of your program subscribe to a particular topic
and have some other part(s) of your program publish messages with that topic. All the plumbing
is taken care of by pubsub.

It originated in wxPython around the year 2000 but has been standalone, available on PyPI, since
2006 under the name **PyPubSub** although the code has also been kept in wxPython as wx.lib.pubsub.

To remove the duplication of the pubsub code in both PyPubSub and wx.lib but to maintain backward
compatibility, wxPython 4 simply imports the standalone package into wx.lib.pubsub. Installing
or updating wxPython should now also install PyPubSub but it can be explicitly installed using
``pip install PyPubSub``

The documentation for pubsub is available at https://pypubsub.readthedocs.io/en/v4.0.0/ and the
source code is hosted at https://github.com/schollii/pypubsub
"""

try:
    from pubsub import *
except ImportError:
    msg = "Stand-alone pubsub not found. Use `pip install PyPubSub`"
    raise ImportError(msg)
    
