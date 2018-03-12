"""
Pubsub package initialization.

:copyright: Copyright since 2006 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE_BSD_Simple.txt for details.
"""

# Import pubsub (Version 4.0.0) from site-packages/pubsub

# Import all items from the pubsub package so they appear
# in the wx.lib.pubsub package namespace. This to maintain
# its appearance as wx.lib.pubsub where it was originally
# created but subsequently published as a stand-alone package
# that is currently sourced from https://github.com/schollii/pypubsub

try:
    from pubsub import *
except ImportError:
    msg = "Stand-alone pubsub not found. Use pip install Pypubsub"
    raise ImportError(msg)
    
