"""
Uses topic definition provider for arg1 messaging protocol. Compare with 
main_kwargs.py which shows example using kwargs messaging protocol: 
kwargs protocol provides for message data self-documentation and more 
robustness (pubsub can determine if message data missing or unknown due 
to type, etc).

Experiment by changing arg1_topics.py and looking at the output tree 
in arg1_topics_out.py.

:copyright: Copyright since 2006 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE.txt for details.
"""

from pubsub import setuparg1
from pubsub import pub
from pubsub.py2and3 import print_

import notifhandle
import exchandle

import arg1_topics

#***** actual application **********

print_('Using "arg1" messaging protocol of pubsub v3')

try:
    print_('------- init ----------')

    pub.addTopicDefnProvider( arg1_topics, pub.TOPIC_TREE_FROM_CLASS )
    pub.setTopicUnspecifiedFatal()

    import arg1_listeners
    import arg1_senders as senders

    print_('-----------------------')
    senders.doSomething1()
    senders.doSomething2()

    print_('------- done ----------')

    print_('Exporting topic tree to', arg1_topics.__name__)
    pub.exportTopicTreeSpec('arg1_topics_out')

except Exception:
    import traceback
    traceback.print_exc()
    print_(pub.exportTopicTreeSpec())

print_('------ exiting --------')