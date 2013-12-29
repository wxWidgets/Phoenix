"""
Uses topic definition provider for kwargs messaging protocol. Compare with 
main_arg1.py which shows example using arg1 messaging protocol: 
kwargs protocol provides for message data self-documentation and more 
robustness (pubsub can determine if message data missing or unknown due 
to type, etc).

Experiment by changing arg1_topics.py and looking at the output tree 
in kwargs_topics_out.py.

:copyright: Copyright since 2006 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE.txt for details.
"""

from pubsub import pub
from pubsub.py2and3 import print_

import notifhandle
import exchandle

import kwargs_topics

#***** actual application **********

print_('Using "kwargs" messaging protocol of pubsub v3')

try:
    print_('------- init ----------')

    pub.addTopicDefnProvider( kwargs_topics, pub.TOPIC_TREE_FROM_CLASS )
    pub.setTopicUnspecifiedFatal()

    import kwargs_listeners
    import kwargs_senders as senders

    print_('-----------------------')
    senders.doSomething1()
    senders.doSomething2()

    print_('------- done ----------')

    print_('Exporting topic tree to', kwargs_topics.__name__)
    pub.exportTopicTreeSpec('kwargs_topics_out')

except Exception:
    import traceback
    traceback.print_exc()
    print_(pub.exportTopicTreeSpec())

print_('------ exiting --------')