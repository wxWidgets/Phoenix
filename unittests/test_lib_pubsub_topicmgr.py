"""

:copyright: Copyright 2006-2009 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE.txt for details.


"""

import unittest
from unittests import wtc

from wx.lib.pubsub.pub import (
     ALL_TOPICS,
     MessageDataSpecError,
     TopicTreeTraverser,
     TopicNameError,
     TopicDefnError
     )

from wx.lib.pubsub.core import ITopicDefnProvider

from wx.lib.pubsub.core.topicmgr import \
     ArgSpecGiven

from wx.lib.pubsub.core.topicutils import validateName

from wx.lib.pubsub.utils.topictreeprinter import \
     printTreeDocs, ITopicTreeVisitor

class lib_pubsub_TopicMgr0_Basic(wtc.PubsubTestCase):
    """
    Only tests TopicMgr methods. This must use some query methods on
    topic objects to validate that TopicMgr did it's job properly.
    """
    def failTopicName(self, name):
        self.assertRaises(TopicNameError, validateName, name)

    def test10_GoodTopicNames(self):
        #
        # Test that valid topic names are accepted by pubsub'
        #

        validateName('test.asdf')
        validateName('test.a')
        validateName('test.a.b')

    def test10_BadTopicNames(self):
        #
        # Test that invalid topic names are rejected by pubsub
        #

        # parts of topic name are 'empty'
        self.failTopicName( '' )
        self.failTopicName( ('',) )
        self.failTopicName( ('test','asdf','') )
        self.failTopicName( ('test','a', None) )

        # parts of topic name have invalid char
        self.failTopicName( ('test','a','b','_') )
        self.failTopicName( ('(aa',) )

        self.failTopicName( (ALL_TOPICS,) )


class lib_pubsub_TopicMgr1_GetOrCreate_NoDefnProv(wtc.PubsubTestCase):
    """
    Only tests TopicMgr methods. This must use some query methods on
    topic objects to validate that TopicMgr did it's job properly.
    """

    def test10_NoProtoListener(self):
        #
        # Test the getOrCreateTopic without proto listener
        #
        topicMgr = self.pub.getDefaultTopicMgr()

        def verifyNonSendable(topicObj, nameTuple, parent):
            """Any non-sendable topic will satisfy these conditions:"""
            self.assertEqual(0, topicMgr.hasTopicDefinition(nameTuple))
            assert not topicObj.hasMDS()
            assert topicObj.getListeners() == []
            assert topicObj.getNameTuple() == nameTuple
            assert topicObj.getNumListeners() == 0
            assert topicObj.getParent() is parent
            assert topicObj.getNodeName() == topicObj.getNameTuple()[-1]
            def foobar():
                pass
            assert not topicObj.hasListener(foobar)
            assert not topicObj.hasListeners()
            assert not topicObj.hasSubtopic('asdfafs')
            assert not topicObj.isAll()
            self.assertRaises(TopicDefnError, topicObj.isValid, foobar)
            self.assertRaises(TopicDefnError, topicObj.validate, foobar)
            # check that getTopic and getOrCreateTopic won't create again:
            assert topicMgr.getOrCreateTopic(nameTuple) is topicObj
            assert topicMgr.getTopic(nameTuple) is topicObj

        # test with a root topic
        rootName = 'GetOrCreate_NoProtoListener'
        tName = rootName
        # verify doesn't exist yet
        assert topicMgr.getTopic(tName, True) is None
        # ok create it, unsendable
        rootTopic = topicMgr.getOrCreateTopic(tName)
        verifyNonSendable(rootTopic, (rootName,), topicMgr.getRootAllTopics())
        DESC_NO_SPEC = 'UNDOCUMENTED: created without spec'
        assert rootTopic.getDescription() == DESC_NO_SPEC
        assert rootTopic.isRoot()
        assert rootTopic.getSubtopics() == []
        assert not rootTopic.isAll()
        assert not rootTopic.hasSubtopic()

        # test with a subtopic
        tName1 = (rootName, 'stB')
        tName2 = tName1 + ('sstC',)
        assert topicMgr.getTopic(tName1, True) is None
        assert topicMgr.getTopic(tName2, True) is None
        subsubTopic = topicMgr.getOrCreateTopic(tName2)
        # verify that parent was created implicitly
        subTopic = topicMgr.getTopic(tName1)
        verifyNonSendable(subTopic, tName1, rootTopic)
        verifyNonSendable(subsubTopic, tName2, subTopic)
        assert subsubTopic.getDescription() == DESC_NO_SPEC
        DESC_PARENT_NO_SPEC = 'UNDOCUMENTED: created as parent without specification'
        assert subTopic.getDescription() == DESC_PARENT_NO_SPEC
        assert rootTopic.getSubtopics() == [subTopic]
        assert rootTopic.hasSubtopic()
        assert subTopic.getSubtopics() == [subsubTopic]
        assert subTopic.hasSubtopic()
        assert subsubTopic.getSubtopics() == []
        assert not subsubTopic.hasSubtopic()

        # check that getTopic raises expected exception when undefined topic:
        tName = 'Undefined'
        self.assertRaises(TopicNameError, topicMgr.getTopic, tName)
        tName = rootName + '.Undefined'
        self.assertRaises(TopicNameError, topicMgr.getTopic, tName)

    def test20_WithProtoListener(self):
        #
        # Test the getOrCreateTopic with proto listener
        #
        topicMgr = self.pub.getDefaultTopicMgr()

        rootName = 'GetOrCreate_WithProtoListener'
        tName = rootName
        # verify doesn't exist yet
        assert topicMgr.getTopic(tName, True) is None
        def protoListener(arg1, arg2=None):
            pass
        # ok create it, sendable
        rootTopic = topicMgr.getOrCreateTopic(tName, protoListener)
        # check that getTopic and getOrCreateTopic won't create again:
        assert topicMgr.getOrCreateTopic(tName) is rootTopic
        assert topicMgr.getTopic(tName) is rootTopic
        assert rootTopic.hasMDS()
        assert topicMgr.hasTopicDefinition(tName)
        expectDesc = 'UNDOCUMENTED: created from protoListener "protoListener" in module'
        assert rootTopic.getDescription().startswith(expectDesc)

        # check that topic created can discern between good and bad listener
        assert rootTopic.isValid(protoListener)
        def badListener1():
            pass # missing required arg
        def badListener2(arg2):
            pass # opt arg is required
        def badListener3(arg1, arg3):
            pass # extra required arg
        assert not rootTopic.isValid(badListener1)
        assert not rootTopic.isValid(badListener2)
        assert not rootTopic.isValid(badListener3)

        # verify that missing parent created is not sendable, child is
        def protoListener2(arg1, arg2=None):
            pass
        tName = (tName, 'stA', 'sstB')
        subsubTopic = topicMgr.getOrCreateTopic(tName, protoListener2)
        subTopic = topicMgr.getTopic( tName[:-1] )
        assert not topicMgr.hasTopicDefinition( tName[:-1] )
        assert topicMgr.hasTopicDefinition( tName )
        assert subsubTopic.isValid(protoListener2)


class lib_pubsub_TopicMgr2_GetOrCreate_DefnProv(wtc.PubsubTestCase):
    """
    Test TopicManager when one or more definition providers
    can provide for some topic definitions.
    """

    def test10_DefnProvider(self):
        #
        # Test the addition and clearing of definition providers
        #
        topicMgr = self.pub.getDefaultTopicMgr()

        class DefnProvider(ITopicDefnProvider):
            pass
        dp1 = DefnProvider()
        dp2 = DefnProvider()
        topicMgr.addDefnProvider(dp1)
        assert 1 == topicMgr.getNumDefnProviders()
        topicMgr.addDefnProvider(dp1)
        assert 1 == topicMgr.getNumDefnProviders()
        topicMgr.addDefnProvider(dp2)
        assert 2 == topicMgr.getNumDefnProviders()
        topicMgr.addDefnProvider(dp2)
        assert 2 == topicMgr.getNumDefnProviders()
        topicMgr.addDefnProvider(dp1)
        assert 2 == topicMgr.getNumDefnProviders()

        topicMgr.clearDefnProviders()
        topicMgr.getNumDefnProviders()
        assert 0 == topicMgr.getNumDefnProviders()
        topicMgr.addDefnProvider(dp1)
        assert 1 == topicMgr.getNumDefnProviders()
        topicMgr.clearDefnProviders()

    def test20_UseProvider(self):
        #
        # Test the use of definition providers for topics. We create
        # two so we can check that more than one can work together.
        # One provides good definitions, one provides some with errors.
        #
        topicMgr = self.pub.getDefaultTopicMgr()

        class DefnProvider(ITopicDefnProvider):
            """
            Provide definitions for a root topic, subtopic, and
            one subtopic whose parent is not defined here. It is easier
            to use sub-only definitions.
            """
            def __init__(self):
                self.defns = {
                    ('a',) : (dict(arg1='arg1 desc', arg2='arg2 desc'),
                              ('arg1',) ),
                    ('a', 'b') : (dict(arg1='arg1 desc', arg2='arg2 desc',
                                       arg3='arg3 desc', arg4='arg2 desc'),
                                 ('arg1', 'arg3',) ),
                    # parent doesn't have defn
                    ('a', 'c', 'd') : (
                              dict(arg1='arg1 desc', arg2='arg2 desc',
                                   arg3='arg3 desc', arg4='arg4 desc',
                                   arg5='arg5 desc', arg6='arg6 desc'),
                              ('arg1', 'arg3', 'arg5',)),
                }

            def getDefn(self, topicNameTuple):
                if topicNameTuple not in self.defns:
                    return None, None
                defn = ArgSpecGiven()
                defn.setAll( * self.defns[topicNameTuple] )
                desc = '%s desc' % '.'.join(topicNameTuple)
                return desc, defn

        class DefnProviderErr(ITopicDefnProvider):
            """
            Provide some definitions that have wrong arg spec. It is
            easier to use the 'all-spec' for definitions, which provides
            an opportunity for a different method of ArgSpecGiven.
            """
            def __init__(self):
                self.defns = {
                    ('a', 'err1') : (# missing arg2
                                     dict(arg1=''),
                                     ('arg1',) ),
                    ('a', 'err2') : (# missing arg1
                                     dict(arg2=''), ),
                    ('a', 'err3') : (# arg1 is no longer required
                                     dict(arg1='', arg2=''), ),
                }

            def getDefn(self, topicNameTuple):
                if topicNameTuple not in self.defns:
                    return None, None
                defn = ArgSpecGiven()
                defn.setAll( * self.defns[topicNameTuple] )
                desc = '%s desc' % '.'.join(topicNameTuple)
                return desc, defn

        topicMgr.addDefnProvider( DefnProvider() )
        topicMgr.addDefnProvider( DefnProviderErr() )

        # create some topics that will use defn provider
        topic = topicMgr.getOrCreateTopic('a')
        assert topic.getDescription() == 'a desc'
        assert topic.hasMDS()
        topic = topicMgr.getOrCreateTopic('a.b')
        assert topic.getDescription() == 'a.b desc'
        assert topic.hasMDS()
        topic = topicMgr.getOrCreateTopic('a.c.d')
        assert topic.getDescription() == 'a.c.d desc'
        assert topic.hasMDS()
        assert not topicMgr.hasTopicDefinition('a.c')
        # check
        parent = topicMgr.getTopic('a.c')
        assert not parent.hasMDS()
        def protoListener(arg1, arg3, arg2=None, arg4=None): pass
        parent = topicMgr.getOrCreateTopic('a.c', protoListener)
        assert parent.hasMDS()
        assert topic.hasMDS()

        # now the erroneous ones:
        def testRaises(topicName, expectMsg):
            self.assertRaises(MessageDataSpecError, topicMgr.getOrCreateTopic,
                              topicName)
            try:
                assert topicMgr.getOrCreateTopic(topicName) is None
            except MessageDataSpecError as exc:
                # ok, did raise but is it correct message?
                try:
                    str(exc).index(expectMsg)
                except ValueError:
                    msg = 'Wrong message, expected \n  "%s", got \n  "%s"'
                    raise RuntimeError(msg % (expectMsg, str(exc)) )

        testRaises('a.err1', 'Params [arg1] missing inherited [arg2] for topic "a.err1"')
        testRaises('a.err2', 'Params [arg2] missing inherited [arg1] for topic "a.err2"')
        testRaises('a.err3', 'Params [] missing inherited [arg1] for topic "a.err3" required args')


    def test30_DelTopic(self):
        #
        # Test topic deletion
        #
        topicMgr = self.pub.getDefaultTopicMgr()

        topicMgr.getOrCreateTopic('delTopic.b.c.d.e')
        assert topicMgr.getTopic('delTopic.b.c.d.e') is not None
        assert topicMgr.getTopic('delTopic.b.c.d').hasSubtopic('e')

        assert topicMgr.getTopic('delTopic.b').hasSubtopic('c')
        topicMgr.delTopic('delTopic.b.c')
        assert not topicMgr.getTopic('delTopic.b').hasSubtopic('c')
        assert topicMgr.getTopic('delTopic.b.c.d.e', okIfNone=True) is None
        assert topicMgr.getTopic('delTopic.b.c.d', okIfNone=True) is None
        assert topicMgr.getTopic('delTopic.b.c', okIfNone=True) is None


class lib_pubsub_TopicMgr3_TreeTraverser(wtc.PubsubTestCase):
    expectedOutput = \
r'''\-- Topic "a2"
    \-- Topic "a"
        \-- Topic "a"
        \-- Topic "b"
    \-- Topic "b"
        \-- Topic "a"
        \-- Topic "b"'''


    def test1(self):
        #
        # Test printing of topic tree
        #
        topicMgr = self.pub.getDefaultTopicMgr()

        root = topicMgr.getOrCreateTopic('a2')
        topicMgr.getOrCreateTopic('a2.a.a')
        topicMgr.getOrCreateTopic('a2.a.b')
        topicMgr.getOrCreateTopic('a2.b.a')
        topicMgr.getOrCreateTopic('a2.b.b')

        from six import StringIO
        buffer = StringIO()
        printTreeDocs(rootTopic=root, width=70, fileObj=buffer)
        self.assertEqual( buffer.getvalue(), self.expectedOutput )

    def test2(self):
        #
        # Test traversing with and without filtering, breadth and depth
        #
        topicMgr = self.pub.getDefaultTopicMgr()

        class MyTraverser(ITopicTreeVisitor):
            def __init__(self, pub):
                self.traverser = pub.TopicTreeTraverser(self)
                self.calls = ''
                self.topics = []

            def traverse(self, rootTopic, **kwargs):
                self.traverser.traverse(rootTopic, **kwargs)

            def __append(self, val):
                self.calls = self.calls + str(val)

            def _startTraversal(self):
                self.__append(1)

            def _accept(self, topicObj):
                self.__append(2)
                # only accept topics at root or second level tree, or if tailName() is 'A'
                return len(topicObj.getNameTuple()) <= 2 or topicObj.getNodeName() == 'A'

            def _onTopic(self, topicObj):
                self.__append(3)
                self.topics.append(topicObj.getNodeName())

            def _startChildren(self):
                self.__append(4)

            def _endChildren(self):
                self.__append(5)

            def _doneTraversal(self):
                self.__append(6)

        root = topicMgr.getOrCreateTopic('traversal')
        topicMgr.getOrCreateTopic('traversal.a.A')
        topicMgr.getOrCreateTopic('traversal.a.B.foo')
        topicMgr.getOrCreateTopic('traversal.b.C')
        topicMgr.getOrCreateTopic('traversal.b.D.bar')

        def exe(expectCalls, expectTopics, **kwargs):
            traverser = MyTraverser(self.pub)
            traverser.traverse(root, **kwargs)
            self.assertEqual(traverser.topics, expectTopics)
            self.assertEqual(traverser.calls,  expectCalls)

        exe(expectCalls  = '13434345343455534345343455556',
            expectTopics = ['traversal', 'a', 'A', 'B', 'foo', 'b', 'C', 'D', 'bar'],
            onlyFiltered = False)
        exe(expectCalls  = '13433543354335454354543545456',
            expectTopics = ['traversal', 'a', 'b', 'A', 'B', 'C', 'D', 'foo', 'bar'],
            how = TopicTreeTraverser.BREADTH, onlyFiltered = False)
        exe(expectCalls  = '123423423452523422556',
            expectTopics = ['traversal','a','A','b'])
        exe(expectCalls  = '123423235423254225456',
            expectTopics = ['traversal','a','b','A'],
            how = TopicTreeTraverser.BREADTH)


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
