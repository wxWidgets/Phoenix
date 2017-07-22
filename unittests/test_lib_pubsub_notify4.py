"""

:copyright: Copyright 2006-2009 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE.txt for details.


"""

import unittest
from unittests import wtc

import six
from difflib import ndiff, unified_diff, context_diff


#---------------------------------------------------------------------------



class lib_pubsub_NotifyN(wtc.PubsubTestCase):

    def testNotifications(self):
        from wx.lib.pubsub.utils.notification import INotificationHandler

        class Handler(INotificationHandler):
            def __init__(self):
                self.resetCounts()
            def resetCounts(self):
                self.counts = dict(send=0, sub=0, unsub=0, delt=0, newt=0, dead=0, all=0)
            def notifySubscribe(self, pubListener, topicObj, newSub):
                self.counts['sub'] += 1
            def notifyUnsubscribe(self, pubListener, topicObj):
                self.counts['unsub'] += 1
            def notifyDeadListener(self, pubListener, topicObj):
                self.counts['dead'] += 1
            def notifySend(self, stage, topicObj, pubListener=None):
                if stage == 'pre': self.counts['send'] += 1
            def notifyNewTopic(self, topicObj, description, required, argsDocs):
                self.counts['newt'] += 1
            def notifyDelTopic(self, topicName):
                self.counts['delt'] += 1

        notifiee = Handler()
        self.pub.addNotificationHandler(notifiee)
        self.pub.setNotificationFlags(all=True)

        def verify(**ref):
            for key, val in six.iteritems(notifiee.counts):
                if key in ref:
                    self.assertEqual(val, ref[key], "\n%s\n%s" % (notifiee.counts, ref) )
                else:
                    self.assertEqual(val, 0, "%s = %s, expected 0" % (key, val))
            notifiee.resetCounts()

        verify()
        def testListener():
            pass
        def testListener2():
            pass

        self.pub.getDefaultTopicMgr().getOrCreateTopic('newTopic')
        verify(newt=1)

        self.pub.subscribe(testListener, 'newTopic')
        self.pub.subscribe(testListener2, 'newTopic')
        verify(sub=2)

        self.pub.sendMessage('newTopic')
        verify(send=1)

        del testListener
        verify(dead=1)

        self.pub.unsubscribe(testListener2,'newTopic')
        verify(unsub=1)

        self.pub.getDefaultTopicMgr().delTopic('newTopic')
        verify(delt=1)


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
