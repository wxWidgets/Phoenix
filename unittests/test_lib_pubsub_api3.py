"""
Except for one test, this file tests with auto-creation of topics
disabled, as it is more rigorous for testing purposes.

:copyright: Copyright 2006-2009 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE.txt for details.


"""

import unittest
from unittests import wtc

from wx.lib.pubsub.core import getListenerID

#---------------------------------------------------------------------------


class lib_pubsub_Except(wtc.PubsubTestCase):

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

        self.pub.subscribe( Wrapper(listener), 'testDOAListenerPubsub')
        assert not self.pub.getDefaultTopicMgr().getTopic('testDOAListenerPubsub').hasListeners()
        assert self.pub.isValid(listener, 'testDOAListenerPubsub')


    def testDeadListener(self):
        # create a listener for listeners that have died
        from wx.lib.pubsub.utils.notification import IgnoreNotificationsMixin

        class DeathListener(IgnoreNotificationsMixin):
            listenerStr = ''
            def notifyDeadListener(self, pubListener, topicObj):
                self.assertEqual(topicObj.getName(), 'sadTopic')
                DeathListener.listenerStr = pubListener.name()
        dl = DeathListener()
        dl.assertEqual = self.assertEqual
        self.pub.addNotificationHandler(dl)
        self.pub.setNotificationFlags(deadListener=True)

        # define a topic, subscribe to it, and kill its listener:
        class TempListener:
            def __call__(self, **kwargs):
                pass
            def __del__(self):
                pass #print 'being deleted'
        tempListener = TempListener()
        expectLisrStr, _ = getListenerID(tempListener)
        self.pub.subscribe(tempListener, 'sadTopic')
        del tempListener

        # verify:
        assert DeathListener.listenerStr.startswith(expectLisrStr), \
            '"%s" !~ "%s"' % (DeathListener.listenerStr, expectLisrStr)

        self.pub.addNotificationHandler(None)
        self.pub.clearNotificationHandlers()


    def testSubscribe(self):
        topicName = 'testSubscribe'
        def proto(a, b, c=None):
            pass
        self.pub.getDefaultTopicMgr().getOrCreateTopic(topicName, proto)

        def listener(a, b, c=None): pass
        # verify that self.pub.isValid() works too
        self.pub.validate(listener, topicName)
        assert self.pub.isValid(listener, topicName)

        self.assertEqual(self.pub.getDefaultTopicMgr().getTopic(topicName).getNumListeners(), 0)
        self.assertEqual(self.pub.getDefaultTopicMgr().getTopicsSubscribed(listener), [])
        assert not self.pub.isSubscribed(listener, topicName)
        assert self.pub.subscribe(listener, topicName)
        assert self.pub.isSubscribed(listener, topicName)
        def topicNames(listener):
            return [t.getName() for t in self.pub.getDefaultTopicMgr().getTopicsSubscribed(listener)]
        self.assertEqual(topicNames(listener), [topicName])
        # should do nothing if already subscribed:
        assert not self.pub.subscribe(listener, topicName)[1]
        self.assertEqual(self.pub.getDefaultTopicMgr().getTopic(topicName).getNumListeners(), 1)

        # test self.pub.getDefaultTopicMgr().getTopics()
        self.pub.subscribe(listener, 'lt2', )
        self.assertEqual(set(topicNames(listener)),
                         set([topicName,'lt2']))
        self.pub.subscribe(listener, 'lt1.lst1')
        self.assertEqual(set(topicNames(listener)),
                      set([topicName,'lt2','lt1.lst1']))

        # test ALL_TOPICS
        def listenToAll():
            pass
        self.pub.subscribe(listenToAll, self.pub.ALL_TOPICS)
        self.assertEqual(topicNames(listenToAll), [self.pub.ALL_TOPICS])


    def testMissingReqdArgs(self):
        def proto(a, b, c=None):
            pass
        self.pub.getDefaultTopicMgr().getOrCreateTopic('missingReqdArgs', proto)
        self.assertRaises(self.pub.SenderMissingReqdMsgDataError, self.pub.sendMessage,
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
            def listen2(self, msgTopic=self.pub.AUTO_TOPIC, **kwarg):
                self.listen2Topics.append(msgTopic.getName())

        my = MyListener()
        self.pub.subscribe(my.listen0, 'testSendTopic')
        self.pub.subscribe(my.listen1, 'testSendTopic')
        self.pub.subscribe(my.listen2, 'testSendTopic')

        self.pub.sendMessage('testSendTopic')
        self.assertEqual(my.count, 1)
        self.assertEqual(my.heardTopic, True)

        self.pub.subscribe(my.listen0, 'testSendTopic.subtopic')
        self.pub.subscribe(my.listen1, 'testSendTopic.subtopic')
        self.pub.subscribe(my.listen2, 'testSendTopic.subtopic')

        self.pub.sendMessage('testSendTopic.subtopic')
        self.assertEqual(my.count, 3)
        self.assertEqual([], [topic for topic in my.listen2Topics
            if topic not in ('testSendTopic', 'testSendTopic.subtopic')] )


    def testAcceptAllArgs(self):
        def listen(arg1=None):
            pass
        def listenAllArgs(arg1=None, **kwargs):
            pass
        def listenAllArgs2(arg1=None, msgTopic=self.pub.AUTO_TOPIC, **kwargs):
            pass

        self.pub.subscribe(listen,  'testAcceptAllArgs')

        self.pub.subscribe(listenAllArgs,  'testAcceptAllArgs')
        self.pub.subscribe(listenAllArgs2, 'testAcceptAllArgs')

        self.pub.subscribe(listenAllArgs2, 'testAcceptAllArgs.subtopic')
        self.pub.subscribe(listenAllArgs,  'testAcceptAllArgs.subtopic')


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
        self.pub.subscribe(lisnrSub, 'pubsub.subscribe')
        self.assertEqual(self.pub.getDefaultTopicMgr().getTopic('pubsub.subscribe').getNumListeners(), 1)

        def subAll():
            self.pub.subscribe(lisnr1, 'testUnsubAll')
            self.pub.subscribe(lisnr2, 'testUnsubAll')
            self.pub.subscribe(lisnr3, 'testUnsubAll')
            self.pub.subscribe(lisnr4, 'testUnsubAll')
            self.assertEqual(self.pub.getDefaultTopicMgr().getTopic('testUnsubAll').getNumListeners(), 4)

        def filter(lisnr):
            passes = str(lisnr).endswith('meth')
            return passes

        # test unsub many non-pubsub topic listeners
        subAll()
        self.pub.unsubAll('testUnsubAll')
        self.assertEqual(self.pub.getDefaultTopicMgr().getTopic('testUnsubAll').getNumListeners(), 0)
        self.assertEqual(self.pub.getDefaultTopicMgr().getTopic('pubsub.subscribe').getNumListeners(), 1)
        # now same but with filter:
        subAll()
        unsubed = self.pub.unsubAll('testUnsubAll', listenerFilter=filter)
        self.assertEqual(self.pub.getDefaultTopicMgr().getTopic('testUnsubAll').getNumListeners(), 3)
        self.assertEqual(self.pub.getDefaultTopicMgr().getTopic('pubsub.subscribe').getNumListeners(), 1)

        # test unsub all listeners of all topics
        subAll()
        self.assertEqual(self.pub.getDefaultTopicMgr().getTopic('testUnsubAll').getNumListeners(), 4)
        unsubed = self.pub.unsubAll(listenerFilter=filter)
        self.assertEqual(unsubed, [lisnr4])
        self.assertEqual(self.pub.getDefaultTopicMgr().getTopic('testUnsubAll').getNumListeners(), 3)
        self.assertEqual(self.pub.getDefaultTopicMgr().getTopic('pubsub.subscribe').getNumListeners(), 1)
        unsubed = set( self.pub.unsubAll() )
        expect = set([lisnr1, lisnrSub, lisnr3, lisnr2])
        # at least all the 'expected' ones were unsub'd; will be others if this
        # test is run after other unit tests in same nosetests run
        assert unsubed >= expect


    def testSendForUndefinedTopic(self):
        self.pub.sendMessage('testSendForUndefinedTopic')
        assert self.pub.getDefaultTopicMgr().getTopic('testSendForUndefinedTopic')
        self.assertEqual(self.pub.getDefaultTopicMgr().getTopic('testSendForUndefinedTopic').getArgs(),
                         (None, None))

        # must also check for subtopics if parents have listeners since
        # filtering of args is affected
        def listener():
            pass
        self.pub.subscribe(listener, 'testSendForUndefinedTopic')
        self.pub.sendMessage('testSendForUndefinedTopic.subtopic', msg='something')

    def testTopicUnspecifiedError(self):
        #pub.TopicDefnError, pub.setTopicUnspecifiedFatal
        self.pub.getDefaultTopicMgr().getOrCreateTopic('a.b')
        self.assertRaises(self.pub.TopicDefnError, self.pub.setTopicUnspecifiedFatal)
        self.pub.setTopicUnspecifiedFatal(checkExisting=False)
        def fn():
            pass
        LSI = self.pub.TopicDefnError
        self.assertRaises(LSI, self.pub.sendMessage, 'testTopicUnspecifiedError')
        self.assertRaises(LSI, self.pub.subscribe, fn, 'testTopicUnspecifiedError')
        self.pub.setTopicUnspecifiedFatal(False)
        self.pub.sendMessage('testTopicUnspecifiedError')
        self.pub.subscribe(fn, 'testTopicUnspecifiedError')


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
        # is guaranteed to be a subset of 'all args'
        self.pub.getDefaultTopicMgr().getOrCreateTopic('tasd',          ok_0)
        self.pub.getDefaultTopicMgr().getOrCreateTopic('tasd.t_1',      ok_1)
        self.assertRaises(self.pub.MessageDataSpecError, self.pub.getDefaultTopicMgr().getOrCreateTopic,
                          'tasd.t_1.t_11',  err_11)
        self.assertRaises(self.pub.MessageDataSpecError, self.pub.getDefaultTopicMgr().getOrCreateTopic,
                          'tasd.t_1.t_12',  err_12)
        self.pub.getDefaultTopicMgr().getOrCreateTopic('tasd.t_2',      ok_2)
        self.pub.getDefaultTopicMgr().getOrCreateTopic('tasd.t_2.t_21', ok_21)
        self.assertRaises(self.pub.MessageDataSpecError, self.pub.getDefaultTopicMgr().getOrCreateTopic,
                          'tasd.t_2.t_22', err_22)

        # with newTopic(), 'required args' specified separately so
        # verify that errors caught
        def check(subName, required=(), **args):
            tName = 'tasd.'+subName
            try:
                self.pub.getDefaultTopicMgr().newTopic(tName, 'desc', required, **args)
                msg = 'Should have raised self.pub.MessageDataSpecError for %s, %s, %s'
                assert False, msg % (tName, required, args)
            except self.pub.MessageDataSpecError as exc:
                #import traceback
                #traceback.print_exc()
                pass

        self.pub.getDefaultTopicMgr().newTopic('tasd.t_1.t_13', 'desc', ('arg1',), arg1='docs for arg1') # ok_1
        check('t_1.t_14', arg1='docs for arg1')                                # err_11
        check('t_1.t_15', ('arg2',), arg2='docs for arg2')                     # err_12

        self.pub.getDefaultTopicMgr().newTopic('tasd.t_2.t_23', 'desc', ('arg1',), arg1='docs for arg1') # ok_21
        check('t_2.t_24', ('arg2',), arg2='docs for arg2')                     # err_22

        # check when no inheritance involved
        # reqd args wrong
        check('t_1.t_16', ('arg1',), arg2='docs for arg2')
        check('t_1.t_17', ('arg2',), arg1='docs for arg1')
        check('t_3',      ('arg1',), arg2='docs for arg2')


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()

