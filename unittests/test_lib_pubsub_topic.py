"""

:copyright: Copyright 2006-2009 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE.txt for details.


"""

import unittest
from unittests import wtc

from wx.lib.pubsub.core.topicobj     import Topic
from wx.lib.pubsub.core.treeconfig   import TreeConfig
from wx.lib.pubsub.core.topicutils   import ALL_TOPICS
from wx.lib.pubsub.core.topicargspec import ArgsInfo, ArgSpecGiven
from wx.lib.pubsub.core.listener     import ListenerMismatchError
from wx.lib.pubsub.core.topicexc     import MessageDataSpecError



#---------------------------------------------------------------------------


class lib_pubsub_Topic(wtc.PubsubTestCase):

    rootTopic = None
    treeConfig = TreeConfig()

    def test0_CreateRoot(self):
        #
        # Test create and then modify state of a topic object
        #

        nameTuple = ('root',)
        description = 'root description'
        msgArgsInfo = None

        # when parent is None, only nameTuple=ALL_TOPICS is allowed, thereby
        # guaranteeing that only one tree root can be created
        self.assertRaises(ValueError, Topic, self.treeConfig, nameTuple, description, msgArgsInfo)

        # create the ALL TOPICS topic; it has no message args
        nameTuple = (ALL_TOPICS,)
        argSpec = ArgSpecGiven(dict() )
        msgArgsInfo = ArgsInfo(nameTuple, argSpec, None)
        obj = Topic(self.treeConfig, nameTuple, description, msgArgsInfo)

        # verify its state is as expected after creation:
        assert obj.getListeners() == []
        assert obj.getNumListeners() == 0
        assert obj.hasListeners() == False

        def listener1():
            pass
        def listener2():
            pass
        def badListener1(arg1):
            pass # extra required arg
        def badListener2(arg1=None):
            pass # extra is optional
        assert obj.isValid(listener1)
        assert not obj.isValid(badListener1)
        assert not obj.isValid(badListener2)

        self.rootTopic = obj


    def test1_SubUnsub(self):
        #
        # Test subscription and unsubscription of listeners
        #

        def listener1():
            pass
        def listener2():
            pass
        # need to run this here again to get rootTopic setup for this test
        self.test0_CreateRoot()
        obj = self.rootTopic

        # now modify its state by subscribing listeners
        obj.subscribe(listener1)
        obj.subscribe(listener2)

        obj.hasListener(listener1)
        obj.hasListener(listener2)
        assert obj.hasListeners() == True
        assert set(obj.getListeners()) == set([listener1, listener2])
        assert obj.getNumListeners() == 2

        # try to subscribe an invalid listener
        def badListener(arg1):
            pass # extra required arg
        self.assertRaises(ListenerMismatchError, obj.subscribe, badListener)

        # try unsubscribe
        obj.unsubscribe(listener1)
        assert obj.hasListeners() == True
        assert obj.getListeners() == [listener2]
        assert obj.getNumListeners() == 1

        # try unsubscribe all, with filtering
        obj.subscribe(listener1)
        def listener3(): pass
        obj.subscribe(listener3)
        assert obj.getNumListeners() == 3
        def ff(listener):
            # use != since it is defined in terms of ==; also, put listener
            # on RHS to verify works even when Listener used on RHS
            return listener2 != listener
        obj.unsubscribeAllListeners(filter=ff)
        assert obj.getNumListeners() == 1
        assert obj.getListeners() == [listener2]
        obj.subscribe(listener1)
        obj.subscribe(listener3)
        assert obj.getNumListeners() == 3
        obj.unsubscribeAllListeners()
        assert obj.getNumListeners() == 0


    def test2_CreateChild(self):
        #
        # Test creation of a child topic, subscription of listeners
        #

        # need to run this here again to get rootTopic setup for this test
        self.test0_CreateRoot()

        nameTuple = ('childOfAll',)
        description = 'child description'
        argsDocs = dict(arg1='arg1 desc', arg2='arg2 desc')
        reqdArgs = ('arg2',)
        argSpec = ArgSpecGiven(argsDocs=argsDocs, reqdArgs = reqdArgs)
        msgArgsInfo = ArgsInfo(nameTuple, argSpec, self.rootTopic._getListenerSpec())
        parent = Topic(self.treeConfig, nameTuple, description, msgArgsInfo,
                       parent=self.rootTopic)
        assert parent.getParent() is self.rootTopic

        # now create a child of child with wrong arguments so we can test exceptions
        nameTuple = ('childOfAll', 'grandChild')
        description = 'grandchild description'

        def tryCreate(ad, r):
            argSpec = ArgSpecGiven(argsDocs=ad, reqdArgs = r)
            msgArgsInfo = ArgsInfo(nameTuple, argSpec, parent._getListenerSpec())
            obj = Topic(self.treeConfig, nameTuple, description, msgArgsInfo,
                        parent=parent)

        # test when all OK
        argsDocs = dict(arg1='arg1 desc', arg2='arg2 desc')
        reqdArgs = ('arg2',)
        tryCreate(argsDocs, reqdArgs)
        # test when requiredArg wrong
        reqdArgs = ('arg3',)
        self.assertRaises(MessageDataSpecError, tryCreate, argsDocs, reqdArgs)
        reqdArgs = ()
        self.assertRaises(MessageDataSpecError, tryCreate, argsDocs, reqdArgs)
        # test when missing opt arg
        argsDocs = dict(arg1='arg1 desc', arg2='arg2 desc')
        reqdArgs = ('arg2',)


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()

