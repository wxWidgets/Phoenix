"""

:copyright: Copyright 2006-2009 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE.txt for details.


"""

import unittest

from unittests import wtc



#---------------------------------------------------------------------------


class lib_pubsub_Notify2(wtc.PubsubTestCase):

    def test0_NotificationTopics(self):
        from wx.lib.pubsub.utils.notification import useNotifyByPubsubMessage
        topicMgr = self.pub.getDefaultTopicMgr()

        assert not topicMgr.getTopic('pubsub', okIfNone=True)
        useNotifyByPubsubMessage()
        assert topicMgr.getTopic('pubsub')

        assert topicMgr.getTopic('pubsub').hasSubtopic()

        pubsubTopicNames = [obj.getName() for obj in topicMgr.getTopic('pubsub').getSubtopics()]
        self.assertEqual(
            set( pubsubTopicNames ),
            set(['pubsub.sendMessage', 'pubsub.deadListener',
                 'pubsub.subscribe',   'pubsub.unsubscribe',
                 'pubsub.newTopic',    'pubsub.delTopic'])
            )


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
