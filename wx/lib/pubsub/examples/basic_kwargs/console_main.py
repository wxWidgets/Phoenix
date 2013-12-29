"""

:copyright: Copyright since 2006 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE.txt for details.

"""

import console_listeners
import console_senders as senders

from pubsub.py2and3 import print_

def run():
    print_('Using "kwargs" messaging protocol of pubsub v3')

    senders.doSomething1()
    senders.doSomething2()


if __name__ == '__main__':
    run()
    