"""

:copyright: Copyright 2006-2009 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE.txt for details.


"""

import unittest
from unittests import wtc


def throws():
    raise RuntimeError('test')

#---------------------------------------------------------------------------


class lib_pubsub_Except(wtc.PubsubTestCase):


    def testHandleExcept1a(self):
        from wx.lib.pubsub.utils.exchandling import ExcPublisher
        excPublisher = ExcPublisher(self.pub.getDefaultTopicMgr() )
        self.pub.setListenerExcHandler(excPublisher)

        # create a listener that raises an exception:
        from .lib_pubsub_except_raisinglistener import getRaisingListener
        raisingListener = getRaisingListener()

        self.pub.setNotificationFlags(all=False)
        self.pub.subscribe(raisingListener, 'testHandleExcept1a')

        # first test when a listener raises an exception and exception listener also raises!
        class BadUncaughtExcListener:
            def __call__(self, listenerStr=None, excTraceback=None):
                raise RuntimeError('bad exception listener!')
        handler = BadUncaughtExcListener()
        self.pub.subscribe(handler, ExcPublisher.topicUncaughtExc)
        self.assertRaises(self.pub.ExcHandlerError, self.pub.sendMessage,
                          'testHandleExcept1a')

    def testHandleExcept1b(self):
        # create a listener that raises an exception:
        from .lib_pubsub_except_raisinglistener import getRaisingListener
        raisingListener = getRaisingListener()
        self.pub.subscribe(raisingListener, 'testHandleExcept1b')

        # subscribe a good exception listener and validate
        # create the listener for uncaught exceptions in listeners:
        class UncaughtExcListener:
            def __call__(self, listenerStr=None, excTraceback=None):
                # verify that information received; first the listenerStr
                assert listenerStr.startswith('raisingListener')
                # next the traceback:
                tb = excTraceback.traceback
                self.assertEqual(len(tb), 2)
                def validateTB(tbItem, eFN, eLine, eFnN, assertE=self.assertEqual):
                    assert tbItem[0].endswith(eFN), '%s !~ %s' % (tbItem[0], eFN)
                    assertE(tbItem[1], eLine)
                    assertE(tbItem[2], eFnN)
                validateTB(tb[0], 'lib_pubsub_except_raisinglistener.py', 5, 'raisingListener')
                validateTB(tb[1], 'lib_pubsub_except_raisinglistener.py', 4, 'nested')
                # next the formatted traceback:
                self.assertEqual(len(excTraceback.getFormattedList() ), len(tb)+1)
                # finally the string for formatted traceback:
                msg = excTraceback.getFormattedString()
                assert msg.startswith('  File')
                assert msg.endswith("name 'RuntimeError2' is not defined\n")

        from wx.lib.pubsub.utils.exchandling import ExcPublisher
        if not self.pub.getDefaultTopicMgr().hasTopicDefinition(ExcPublisher.topicUncaughtExc):
            excPublisher = ExcPublisher(self.pub.getDefaultTopicMgr() )
            self.pub.setListenerExcHandler(excPublisher)
        topic = self.pub.getDefaultTopicMgr().getTopic(ExcPublisher.topicUncaughtExc)
        assert not topic.hasListeners()
        handler = UncaughtExcListener()
        handler.assertEqual = self.assertEqual
        self.pub.subscribe(handler, ExcPublisher.topicUncaughtExc)
        self.pub.sendMessage('testHandleExcept1b')

        # verify that listener isn't stuck in a cyclic reference by sys.exc_info()
        del raisingListener
        assert not self.pub.getDefaultTopicMgr().getTopic('testHandleExcept1b').hasListeners()


    def testHandleExcept2(self):
        #Test sendMessage when one handler, then change handler and verify changed
        testTopic = 'testTopics.testHandleExcept2'
        self.pub.subscribe(throws, testTopic)
        self.pub.setListenerExcHandler(None)
        #pubsub.utils.notification.useNotifyByWriteFile()
        #assert_equal( self.pub.getDefaultTopicMgr().getTopic(testTopic).getNumListeners(), 1 )

        expect = None

        def validate(className):
            global expect
            assert expect == className
            expect = None

        class MyExcHandler:
            def __call__(self, listener, topicObj):
                validate(self.__class__.__name__)

        class MyExcHandler2:
            def __call__(self, listener, topicObj):
                validate(self.__class__.__name__)

        def doHandling(HandlerClass):
            global expect
            expect = HandlerClass.__name__  #'MyExcHandler'
            excHandler = HandlerClass()
            self.pub.setListenerExcHandler(excHandler)
            self.pub.sendMessage(testTopic)
            assert expect is None

        doHandling(MyExcHandler)
        doHandling(MyExcHandler2)

        # restore to no handling and verify:
        self.pub.setListenerExcHandler(None)
        self.assertRaises(RuntimeError, self.pub.sendMessage, testTopic)


    def testNoExceptionHandling1(self):
        self.pub.setListenerExcHandler(None)

        def raises():
            raise RuntimeError('test')
        self.pub.getDefaultTopicMgr().getOrCreateTopic('testNoExceptionTrapping')
        self.pub.subscribe(raises, 'testNoExceptionTrapping')
        self.assertRaises(RuntimeError, self.pub.sendMessage, 'testNoExceptionTrapping')


    def testNoExceptionHandling2(self):
        testTopic = 'testTopics.testNoExceptionHandling'
        self.pub.subscribe(throws, testTopic)
        assert self.pub.getListenerExcHandler() is None
        self.assertRaises(RuntimeError, self.pub.sendMessage, testTopic)


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()

