"""

:copyright: Copyright since 2006 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE.txt for details.

"""

from pubsub import pub

def doSomething1():
    pub.sendMessage('topic_1.subtopic_11',
        msg='message for subtopic 11', msg2='other message', extra=123)


def doSomething2():
    pub.sendMessage('topic_1', msg='message for topic 1')
    pub.sendMessage('topic_2.subtopic_21', msg='message for subtopic 2')


