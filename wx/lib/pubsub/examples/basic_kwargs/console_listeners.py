"""

:copyright: Copyright since 2006 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE.txt for details.

"""

from pubsub import pub
from pubsub.py2and3 import print_

# ------------ create some listeners --------------

class Listener:
    def onTopic11(self, msg, extra=None):
        print_('Method Listener.onTopic11 received: ', repr(msg), repr(extra))

    def onTopic1(self, msg, topic=pub.AUTO_TOPIC):
        info = 'Method Listener.onTopic1 received "%s" message: %s'
        print_(info % (topic.getName(), repr(msg)))

    def __call__(self, **kwargs):
        print_('Listener instance received: ', kwargs)

listenerObj = Listener()


def listenerFn(msg, extra=None):
    print_('Function listenerFn received: ', repr(msg), repr(extra))

# ------------ subscribe listeners ------------------

pub.subscribe(listenerObj, pub.ALL_TOPICS) # via its __call__

pub.subscribe(listenerFn, 'topic1.subtopic11')
pub.subscribe(listenerObj.onTopic11, 'topic1.subtopic11')

pub.subscribe(listenerObj.onTopic1, 'topic1')

