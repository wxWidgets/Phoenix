"""

:copyright: Copyright 2006-2009 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE.txt for details.


"""

import unittest

from unittests import wtc



#---------------------------------------------------------------------------


class lib_pubsub_Notify2_2(wtc.PubsubTestCase):

    def test2_SendNotify(self):
        from wx.lib.pubsub.utils.notification import useNotifyByPubsubMessage

        useNotifyByPubsubMessage()

        # trap the pubsub.sendMessage topic:
        class SendHandler:
            def __init__(self):
                self.pre = self.post = 0

            def __call__(self, topic=None, stage=None, listener=None,
                         msgTopic=self.pub.AUTO_TOPIC):
                if stage == 'pre':
                    self.pre += 1
                else:
                    self.post += 1
                self.assertEqual(msgTopic.getName(), 'pubsub.sendMessage')
                self.assertEqual(topic.getName(), 'testSendNotify')

        sh = SendHandler()
        sh.assertEqual = self.assertEqual

        self.pub.subscribe(sh, 'pubsub.sendMessage')
        self.pub.setNotificationFlags(sendMessage=True)

        # generate a message that will cause pubsub.sendMessage to be generated too
        assert sh.pre == 0
        assert sh.post == 0
        self.pub.getDefaultTopicMgr().getOrCreateTopic('testSendNotify')
        self.pub.sendMessage('testSendNotify')
        assert sh.pre == 1
        assert sh.post == 1



#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
