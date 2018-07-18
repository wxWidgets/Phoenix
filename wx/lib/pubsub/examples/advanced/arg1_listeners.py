"""

:copyright: Copyright since 2006 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE.txt for details.
"""

from pubsub import pub
from pubsub.py2and3 import print_

# ------------ create some listeners --------------

class Listener:
    def onTopic11(self, msg):
        data = msg.data
        print_('Method Listener.onTopic11 received: ', repr(data))

    def onTopic1(self, msg, topic=pub.AUTO_TOPIC):
        info = 'Method Listener.onTopic1 received "%s" message: %s'
        print_(info % (topic.getName(), repr(msg.data)))

    def __call__(self, msg):
        print_('Listener instance received: ', msg.data)

listenerObj = Listener()


def listenerFn(msg):
    data = msg.data
    print_('Function listenerFn received: ', repr(data))

# ------------ subscribe listeners ------------------

pub.subscribe(listenerObj, pub.ALL_TOPICS) # via its __call__

pub.subscribe(listenerFn, 'topic_1.subtopic_11')
pub.subscribe(listenerObj.onTopic11, 'topic_1.subtopic_11')

pub.subscribe(listenerObj.onTopic1, 'topic_1')

