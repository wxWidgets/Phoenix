"""

:copyright: Copyright since 2006 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE.txt for details.

"""

from pubsub import setuparg1
from pubsub.py2and3 import print_

import console_senders as senders
import console_listeners


def run():
    print_('Using "arg1" messaging protocol of pubsub v3')

    senders.doSomething1()
    senders.doSomething2()


if __name__ == '__main__':
    run()
