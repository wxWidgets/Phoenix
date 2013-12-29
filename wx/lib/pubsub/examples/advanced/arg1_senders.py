"""

:copyright: Copyright since 2006 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE.txt for details.

"""

from pubsub import pub


def doSomething1():
    pub.sendMessage('topic_1.subtopic_11', ('message for subtopic 11', 'other message', 123))


def doSomething2():
    pub.sendMessage('topic_1', 'message for topic 1')
    pub.sendMessage('topic_2.subtopic_21', 'message for subtopic 2')


