"""

:copyright: Copyright 2006-2009 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE.txt for details.


"""

import unittest

from unittests import wtc



#---------------------------------------------------------------------------


class lib_pubsub_Notify2_1(wtc.PubsubTestCase):


    def test1_SubscribeNotify(self):
        from wx.lib.pubsub.utils.notification import useNotifyByPubsubMessage

        useNotifyByPubsubMessage()

        class MyListener:
            countSub = 0
            countUnsub = 0
            def listenerSub(self, msgTopic=self.pub.AUTO_TOPIC, listener=None,
                            topic=None, newSub=None):
                self.assertEqual(msgTopic.getName(), 'pubsub.subscribe' )
                assert topic.getName() in ('pubsub.unsubscribe', 'testSubscribeNotify')
                if newSub:
                    self.countSub += 1
            def listenerUnsub(self, msgTopic=self.pub.AUTO_TOPIC, topic=None,
                              listener=None, listenerRaw=None):
                assert topic.getName() in ('testSubscribeNotify', 'pubsub.subscribe' )
                self.assertEqual(msgTopic.getName(), 'pubsub.unsubscribe' )
                if listener is not None:
                    self.countUnsub += 1
            def listenerTest(self):
                raise NotImplementedError # should never get here

        self.pub.setNotificationFlags(subscribe=True, unsubscribe=True)
        self.pub.getDefaultTopicMgr().getOrCreateTopic('testSubscribeNotify')
        tmp = MyListener()
        tmp.assertEqual = self.assertEqual

        self.pub.subscribe(tmp.listenerSub, 'pubsub.subscribe')
        self.assertEqual(tmp.countSub, 0)   # don't notify of self subscription
        self.assertEqual(tmp.countUnsub, 0)
        sl, ok = self.pub.subscribe(tmp.listenerUnsub, 'pubsub.unsubscribe')
        assert ok
        self.assertEqual(tmp.countSub, 1)
        self.assertEqual(tmp.countUnsub, 0)

        self.pub.subscribe(tmp.listenerTest, 'testSubscribeNotify')
        self.assertEqual(tmp.countUnsub, 0)
        self.pub.unsubscribe(tmp.listenerTest, 'testSubscribeNotify')
        self.assertEqual(tmp.countUnsub, 1)

        self.pub.unsubscribe(tmp.listenerSub,   'pubsub.subscribe')
        self.assertEqual(tmp.countSub, 2)
        self.assertEqual(tmp.countUnsub, 2)
        self.pub.unsubscribe(tmp.listenerUnsub, 'pubsub.unsubscribe')
        self.assertEqual(tmp.countSub, 2)
        self.assertEqual(tmp.countUnsub, 2) # don't notify of self unsubscription



#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
