"""

:copyright: Copyright 2006-2009 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE.txt for details.


"""

import imp_unittest, unittest
import wtc

from wx.lib.pubsub import pub


def throws():
    raise RuntimeError('test')

#---------------------------------------------------------------------------


class lib_pubsub_Except(wtc.WidgetTestCase):

    
    def testHandleExcept1a(self):
        from wx.lib.pubsub.utils.exchandling import ExcPublisher
        excPublisher = ExcPublisher( pub.getDefaultTopicMgr() )
        pub.setListenerExcHandler(excPublisher)
    
        # create a listener that raises an exception:
        from lib_pubsub_except_raisinglistener import getRaisingListener
        raisingListener = getRaisingListener()
    
        pub.setNotificationFlags(all=False)
        pub.subscribe(raisingListener, 'testHandleExcept1a')
    
        # first test when a listener raises an exception and exception listener also raises!
        class BadUncaughtExcListener:
            def __call__(self, listenerStr=None, excTraceback=None):
                raise RuntimeError('bad exception listener!')
        handler = BadUncaughtExcListener()
        pub.subscribe(handler, ExcPublisher.topicUncaughtExc)
        self.assertRaises(pub.ExcHandlerError, pub.sendMessage,
                          'testHandleExcept1a')
    
    def testHandleExcept1b(self):
        # create a listener that raises an exception:
        from lib_pubsub_except_raisinglistener import getRaisingListener
        raisingListener = getRaisingListener()
        pub.subscribe(raisingListener, 'testHandleExcept1b')
    
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
                #print 'Msg "%s"' % msg
                assert msg.startswith('  File')
                assert msg.endswith("global name 'RuntimeError2' is not defined\n")
    
        from wx.lib.pubsub.utils.exchandling import ExcPublisher
        topic = pub.getTopic(ExcPublisher.topicUncaughtExc)
        assert not topic.hasListeners()
        handler = UncaughtExcListener()
        handler.assertEqual = self.assertEqual
        pub.subscribe(handler, ExcPublisher.topicUncaughtExc)
        pub.sendMessage('testHandleExcept1b')
    
        # verify that listener isn't stuck in a cyclic reference by sys.exc_info()
        del raisingListener
        assert not pub.getTopic('testHandleExcept1b').hasListeners()
    
    
    def testHandleExcept2(self):
        #Test sendMessage when one handler, then change handler and verify changed
        testTopic = 'testTopics.testHandleExcept2'
        pub.subscribe(throws, testTopic)
        pub.setListenerExcHandler(None)
        #pubsub.utils.notification.useNotifyByWriteFile()
        #assert_equal( pub.getTopic(testTopic).getNumListeners(), 1 )
    
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
            pub.setListenerExcHandler(excHandler)
            pub.sendMessage(testTopic)
            assert expect is None
    
        doHandling(MyExcHandler)
        doHandling(MyExcHandler2)
    
        # restore to no handling and verify:
        pub.setListenerExcHandler(None)
        self.assertRaises(RuntimeError, pub.sendMessage, testTopic)
    
    
    def testNoExceptionHandling1(self):
        pub.setListenerExcHandler(None)
    
        def raises():
            raise RuntimeError('test')
        pub.getOrCreateTopic('testNoExceptionTrapping')
        pub.subscribe(raises, 'testNoExceptionTrapping')
        self.assertRaises(RuntimeError, pub.sendMessage, 'testNoExceptionTrapping')
    
    
    def testNoExceptionHandling2(self):
        testTopic = 'testTopics.testNoExceptionHandling'
        pub.subscribe(throws, testTopic)
        assert pub.getListenerExcHandler() is None
        self.assertRaises(RuntimeError, pub.sendMessage, testTopic)
    
    
#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()

