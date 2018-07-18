"""

:copyright: Copyright since 2006 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE.txt for details.

"""

from pubsub import pub
from pubsub.py2and3 import print_


def doSomething1():
    print_('--- SENDING topic1.subtopic11 message ---')
    pub.sendMessage('topic1.subtopic11', msg='message for 11', extra=123)
    print_('---- SENT topic1.subtopic11 message ----')

def doSomething2():
    print_('--- SENDING topic1 message ---')
    pub.sendMessage('topic1', msg='message for 1')
    print_('---- SENT topic1 message ----')


