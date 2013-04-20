"""
Except for one test, this file tests with auto-creation of topics 
disabled, as it is more rigorous for testing purposes. 

:copyright: Copyright 2006-2009 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE.txt for details.


"""

import imp_unittest, unittest
import wtc

from wx.lib.pubsub import pub
from wx.lib.pubsub.utils.notification import IgnoreNotificationsMixin


#---------------------------------------------------------------------------


class lib_pubsub_Except(wtc.WidgetTestCase):


    def testDOAListenerPubsub(self):
        # Verify that a 'temporary' listener (one that will be garbage collected
        # as soon as subscribe() returns because there are no strong references to
        # it) gets immediately unregistered
    
        def listener():
            pass
        class Wrapper:
            def __init__(self, func):
                self.func = func
            def __call__(self):
                pass
    
        pub.subscribe( Wrapper(listener), 'testDOAListenerPubsub')
        assert not pub.getTopic('testDOAListenerPubsub').hasListeners()
        assert pub.isValid(listener, 'testDOAListenerPubsub')
    
        
    def testDeadListener(self):
        # create a listener for listeners that have died
        class DeathListener(IgnoreNotificationsMixin):
            listenerStr = ''
            def notifyDeadListener(self, pubListener, topicObj):
                self.assertEqual(topicObj.getName(), 'sadTopic')
                DeathListener.listenerStr = pubListener.name()
        dl = DeathListener()
        dl.assertEqual = self.assertEqual
        pub.addNotificationHandler(dl)
        pub.setNotificationFlags(deadListener=True)
        
        # define a topic, subscribe to it, and kill its listener:
        class TempListener:
            def __call__(self, **kwargs): 
                pass
            def __del__(self):
                pass #print 'being deleted'
        tempListener = TempListener()
        expectLisrStr, _ = pub.getListenerID(tempListener)
        pub.subscribe(tempListener, 'sadTopic')
        del tempListener
        
        # verify:
        assert DeathListener.listenerStr.startswith(expectLisrStr), \
            '"%s" !~ "%s"' % (DeathListener.listenerStr, expectLisrStr)
    
        pub.addNotificationHandler(None)
        pub.clearNotificationHandlers()
        
    
    def testSubscribe(self):
        topicName = 'testSubscribe'
        def proto(a, b, c=None):
            pass
        pub.getOrCreateTopic(topicName, proto)
    
        def listener(a, b, c=None): pass
        # verify that pub.isValid() works too
        pub.validate(listener, topicName)
        assert pub.isValid(listener, topicName)
    
        self.assertEqual(pub.getTopic(topicName).getNumListeners(), 0)
        self.assertEqual(pub.getAssociatedTopics(listener), [])
        assert not pub.isSubscribed(listener, topicName)
        assert pub.subscribe(listener, topicName)
        assert pub.isSubscribed(listener, topicName)
        def topicNames(listener):
            return [t.getName() for t in pub.getAssociatedTopics(listener)]
        self.assertEqual(topicNames(listener), [topicName])
        # should do nothing if already subscribed:
        assert not pub.subscribe(listener, topicName)[1]
        self.assertEqual(pub.getTopic(topicName).getNumListeners(), 1)
        
        # test pub.getAssociatedTopics()
        pub.subscribe(listener, 'lt2', )
        self.assertEqual(set(topicNames(listener)), 
                         set([topicName,'lt2']))
        pub.subscribe(listener, 'lt1.lst1')
        self.assertEqual(set(topicNames(listener)), 
                      set([topicName,'lt2','lt1.lst1']))
        
        # test ALL_TOPICS
        def listenToAll():
            pass
        pub.subscribe(listenToAll, pub.ALL_TOPICS)
        self.assertEqual(topicNames(listenToAll), [pub.ALL_TOPICS])
        
        
    def testMissingReqdArgs(self):
        def proto(a, b, c=None):
            pass
        pub.getOrCreateTopic('missingReqdArgs', proto)
        self.assertRaises(pub.SenderMissingReqdArgs, pub.sendMessage,
                          'missingReqdArgs', a=1)
    
    
    def testSendTopicWithMessage(self):
        class MyListener:
            def __init__(self):
                self.count = 0
                self.heardTopic = False
                self.listen2Topics = []
            def listen0(self): 
                pass
            def listen1(self, **kwarg): 
                self.count += 1
                self.heardTopic = True
            def listen2(self, msgTopic=pub.AUTO_TOPIC, **kwarg):
                self.listen2Topics.append(msgTopic.getName())
                
        my = MyListener()
        pub.subscribe(my.listen0, 'testSendTopic')
        pub.subscribe(my.listen1, 'testSendTopic')
        pub.subscribe(my.listen2, 'testSendTopic')
    
        pub.sendMessage('testSendTopic')
        self.assertEqual(my.count, 1)
        self.assertEqual(my.heardTopic, True)
    
        pub.subscribe(my.listen0, 'testSendTopic.subtopic')
        pub.subscribe(my.listen1, 'testSendTopic.subtopic')
        pub.subscribe(my.listen2, 'testSendTopic.subtopic')
    
        pub.sendMessage('testSendTopic.subtopic')
        self.assertEqual(my.count, 3)
        self.assertEqual([], [topic for topic in my.listen2Topics 
            if topic not in ('testSendTopic', 'testSendTopic.subtopic')] )
    
    
    def testAcceptAllArgs(self):
        def listen(arg1=None):
            pass
        def listenAllArgs(arg1=None, **kwargs):
            pass
        def listenAllArgs2(arg1=None, msgTopic=pub.AUTO_TOPIC, **kwargs):
            pass
    
        pub.subscribe(listen,  'testAcceptAllArgs')
    
        pub.subscribe(listenAllArgs,  'testAcceptAllArgs')
        pub.subscribe(listenAllArgs2, 'testAcceptAllArgs')
        
        pub.subscribe(listenAllArgs2, 'testAcceptAllArgs.subtopic')
        pub.subscribe(listenAllArgs,  'testAcceptAllArgs.subtopic')
    
    
    def testUnsubAll(self):
        def lisnr1():
            pass 
        def lisnr2():
            pass
        class MyListener:
            def __call__(self):
                pass
            def meth(self):
                pass
            def __hash__(self):
                return 123
        lisnr3 = MyListener()
        lisnr4 = lisnr3.meth
        def lisnrSub(listener=None, topic=None, newSub=None): pass
        pub.subscribe(lisnrSub, 'pubsub.subscribe')
        self.assertEqual(pub.getTopic('pubsub.subscribe').getNumListeners(), 1)
    
        def subAll():
            pub.subscribe(lisnr1, 'testUnsubAll')
            pub.subscribe(lisnr2, 'testUnsubAll')
            pub.subscribe(lisnr3, 'testUnsubAll')
            pub.subscribe(lisnr4, 'testUnsubAll')
            self.assertEqual(pub.getTopic('testUnsubAll').getNumListeners(), 4)
    
        def filter(lisnr):
            passes = str(lisnr).endswith('meth')
            return passes
            
        # test unsub many non-pubsub topic listeners
        subAll()
        pub.unsubAll('testUnsubAll')
        self.assertEqual(pub.getTopic('testUnsubAll').getNumListeners(), 0)
        self.assertEqual(pub.getTopic('pubsub.subscribe').getNumListeners(), 1)
        # now same but with filter:
        subAll()
        unsubed = pub.unsubAll('testUnsubAll', listenerFilter=filter)
        self.assertEqual(pub.getTopic('testUnsubAll').getNumListeners(), 3)
        self.assertEqual(pub.getTopic('pubsub.subscribe').getNumListeners(), 1)
        
        # test unsub all listeners of all topics
        subAll()
        self.assertEqual(pub.getTopic('testUnsubAll').getNumListeners(), 4)
        unsubed = pub.unsubAll(listenerFilter=filter)
        self.assertEqual(unsubed, [lisnr4])
        self.assertEqual(pub.getTopic('testUnsubAll').getNumListeners(), 3)
        self.assertEqual(pub.getTopic('pubsub.subscribe').getNumListeners(), 1)
        unsubed = set( pub.unsubAll() )
        expect = set([lisnr1, lisnrSub, lisnr3, lisnr2])
        # at least all the 'expected' ones were unsub'd; will be others if this
        # test is run after other unit tests in same nosetests run
        assert unsubed >= expect
        
        
    def testSendForUndefinedTopic(self):
        pub.sendMessage('testSendForUndefinedTopic')
        assert pub.getTopic('testSendForUndefinedTopic')
        self.assertEqual(pub.getTopic('testSendForUndefinedTopic').getArgs(),
                         (None, None))
    
        # must also check for subtopics if parents have listeners since
        # filtering of args is affected
        def listener():
            pass
        pub.subscribe(listener, 'testSendForUndefinedTopic')
        pub.sendMessage('testSendForUndefinedTopic.subtopic', msg='something')
        
    def testTopicUnspecifiedError(self):
        self.assertRaises(pub.ListenerSpecIncomplete, pub.setTopicUnspecifiedFatal)
        pub.setTopicUnspecifiedFatal(checkExisting=False)
        def fn():
            pass
        LSI = pub.ListenerSpecIncomplete
        self.assertRaises(LSI, pub.sendMessage, 'testTopicUnspecifiedError')
        self.assertRaises(LSI, pub.subscribe, fn, 'testTopicUnspecifiedError')
        pub.setTopicUnspecifiedFatal(False)
        pub.sendMessage('testTopicUnspecifiedError')
        pub.subscribe(fn, 'testTopicUnspecifiedError')
    
    
    def testArgSpecDerivation(self):
        def ok_0():
            pass
    
        def ok_1(arg1):
            pass
        def err_11(arg1=None):
            pass  # required can't become optional!
        def err_12(arg2):
            pass       # parent's arg1 missing
    
        def ok_2(arg1=None):
            pass
        def ok_21(arg1):
            pass        # optional can become required
        def err_22(arg2):
            pass       # parent's arg1 missing
    
        # with getOrCreateTopic(topic, proto), the 'required args' set
        # is garanteed to be a subset of 'all args'
        pub.getOrCreateTopic('tasd',          ok_0)
        pub.getOrCreateTopic('tasd.t_1',      ok_1)
        self.assertRaises(pub.ListenerSpecInvalid, pub.getOrCreateTopic,
                          'tasd.t_1.t_11',  err_11)
        self.assertRaises(pub.ListenerSpecInvalid, pub.getOrCreateTopic,
                          'tasd.t_1.t_12',  err_12)
        pub.getOrCreateTopic('tasd.t_2',      ok_2)
        pub.getOrCreateTopic('tasd.t_2.t_21', ok_21)
        self.assertRaises(pub.ListenerSpecInvalid, pub.getOrCreateTopic,
                          'tasd.t_2.t_22', err_22)
    
        # with newTopic(), 'required args' specified separately so
        # verify that errors caught
        def check(subName, required=(), **args):
            tName = 'tasd.'+subName
            try:
                pub.newTopic(tName, 'desc', required, **args)
                msg = 'Should have raised pub.ListenerSpecInvalid for %s, %s, %s'
                assert False, msg % (tName, required, args)
            except pub.ListenerSpecInvalid, exc:
                #import traceback
                #traceback.print_exc()
                print 'As expected: ', exc
    
        pub.newTopic('tasd.t_1.t_13', 'desc', ('arg1',), arg1='docs for arg1') # ok_1
        check('t_1.t_14', arg1='docs for arg1')                                # err_11
        check('t_1.t_15', ('arg2',), arg2='docs for arg2')                     # err_12
    
        pub.newTopic('tasd.t_2.t_23', 'desc', ('arg1',), arg1='docs for arg1') # ok_21
        check('t_2.t_24', ('arg2',), arg2='docs for arg2')                     # err_22
    
        # check when no inheritence involved
        # reqd args wrong
        check('t_1.t_16', ('arg1',), arg2='docs for arg2')
        check('t_1.t_17', ('arg2',), arg1='docs for arg1')
        check('t_3',      ('arg1',), arg2='docs for arg2')
    

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()

    