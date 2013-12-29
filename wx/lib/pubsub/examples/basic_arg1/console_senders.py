"""

:copyright: Copyright since 2006 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE.txt for details.

"""

from pubsub import pub
from pubsub.py2and3 import print_


def doSomething1():
    print_('--- SENDING topic1.subtopic11 message ---')
    pub.sendMessage('topic1.subtopic11', ('message for 11', 123))
    print_('---- SENT topic1.subtopic11 message ----')

def doSomething2():
    print_('--- SENDING topic1 message ---')
    pub.sendMessage('topic1', ('message for 1',) )
    print_('---- SENT topic1 message ----')


