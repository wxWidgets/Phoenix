"""

:copyright: Copyright since 2006 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE.txt for details.
"""

from pubsub import pub
from pubsub.py2and3 import print_


# create one special notification handler that ignores all except
# one type of notification
class MyPubsubExcHandler(pub.IListenerExcHandler):

    def __call__(self, listenerID):
        print_('Exception raised in listener %s during sendMessage()' % listenerID)
        print_(TracebackInfo())


pub.setListenerExcHandler( MyPubsubExcHandler() )

