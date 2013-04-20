"""

:copyright: Copyright 2006-2009 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE.txt for details.


"""

import imp_unittest, unittest
import wtc

from difflib import ndiff, unified_diff, context_diff

# setup notification and logging
from wx.lib.pubsub import pub
from wx.lib.pubsub.utils.notification import useNotifyByWriteFile, INotificationHandler


#---------------------------------------------------------------------------


class lib_pubsub_Notify(wtc.WidgetTestCase):

    
    def captureStdout(self):
        from StringIO import StringIO
        capture = StringIO()
        useNotifyByWriteFile( fileObj = capture )
        return capture


    def testNotifyByPrint(self):
        capture = self.captureStdout()
    
        def listener1(arg1):
            pass
        pub.subscribe(listener1, 'baz')
        pub.sendMessage('baz', arg1=123)
        pub.unsubscribe(listener1, 'baz')
    
        def doa():
            def listener2():
                pass
            pub.subscribe(listener2, 'bar')
        doa()
    
        pub.delTopic('baz')
    
        expect = '''\
PUBSUB: New topic "baz" created
PUBSUB: Subscribed listener "listener1" to topic "baz"
PUBSUB: Start sending message of topic "baz"
PUBSUB: Sending message of topic "baz" to listener listener1
PUBSUB: Done sending message of topic "baz"
PUBSUB: Unsubscribed listener "listener1" from topic "baz"
PUBSUB: New topic "bar" created
PUBSUB: Subscribed listener "listener2" to topic "bar"
PUBSUB: Listener "listener2" of Topic "bar" has died
PUBSUB: Topic "baz" destroyed
    '''
        captured = capture.getvalue()
        # strip as other wise one has \n, at least on windows
        assert captured.strip() == expect.strip(), \
            '\n'.join( unified_diff(expect.splitlines(), captured.splitlines(), n=0) )
    
    
    def testFlagChanges(self):
        savedFlags = pub.getNotificationFlags()
    
        pub.setNotificationFlags(all=True, sendMessage=False, deadListener=False)
        flags = pub.getNotificationFlags()
        assert not flags['sendMessage']
        assert not flags['deadListener']
        assert flags['newTopic']
        assert flags['delTopic']
        assert flags['subscribe']
        assert flags['unsubscribe']
    
        pub.setNotificationFlags(subscribe=False, deadListener=True)
        flags = pub.getNotificationFlags()
        assert not flags['sendMessage']
        assert not flags['subscribe']
        assert flags['newTopic']
        assert flags['delTopic']
        assert flags['deadListener']
        assert flags['unsubscribe']
    
        pub.setNotificationFlags(all=False, subscribe=True, unsubscribe=True)
        flags = pub.getNotificationFlags()
        assert not flags['sendMessage']
        assert not flags['deadListener']
        assert not flags['newTopic']
        assert not flags['delTopic']
        assert flags['subscribe']
        assert flags['unsubscribe']
    
        pub.setNotificationFlags(** savedFlags)
    
        
    def testNotifications(self):
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
        pub.addNotificationHandler(notifiee)
        pub.setNotificationFlags(all=True)
    
        def verify(**ref):
            for key, val in notifiee.counts.iteritems():
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
    
        pub.getOrCreateTopic('newTopic')
        verify(newt=1)
    
        pub.subscribe(testListener, 'newTopic')
        pub.subscribe(testListener2, 'newTopic')
        verify(sub=2)
    
        pub.sendMessage('newTopic')
        verify(send=1)
    
        del testListener
        verify(dead=1)
    
        pub.unsubscribe(testListener2,'newTopic')
        verify(unsub=1)
    
        pub.delTopic('newTopic')
        verify(delt=1)
    

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
