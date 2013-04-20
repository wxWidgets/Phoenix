"""

:copyright: Copyright 2006-2009 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE.txt for details.


"""

import imp_unittest, unittest
import wtc

from textwrap import dedent

from wx.lib.pubsub import pub


class my_topics:
    class rootTopic1:
        '''Root topic 1'''

        class subtopic_1:
            '''
            Sub topic 1 of root topic. Docs rely on one blank line for
            topic doc, and indentation for each argument doc.
            '''

            def msgDataSpec(arg1, arg2=None):
                '''
                - arg1: some multiline doc
                    for arg1
                - arg2: some multiline doc
                    for arg2
                '''
                pass

            class subsubtopic_12:
                '''Sub sub topic 2 of sub topic 1.'''

                def msgDataSpec(arg1, argA, arg2=None, argB=None):
                    '''
                    - argA: doc for argA
                    - argB: doc for argB
                    '''
                    pass

    class rootTopic2:
        '''Root topic 2'''

#---------------------------------------------------------------------------


class lib_pubsub_Except(wtc.WidgetTestCase):

    def test1(self):

        pub.importTopicTree(my_topics)
    
    
        provString = """
            class rootTopic1:
                class subtopic_1:
                    class subsubtopic_11:
                        '''
                        Sub sub topic 1 of sub topic 1. Only need to doc the
                        extra args.
                        '''
                        def msgDataSpec(arg1, arg3, arg2=None, arg4=None):
                            '''
                            - arg3: doc for arg3
                            - arg4: doc for arg4
                            '''
                            pass
    
                """
    
        pub.importTopicTree(provString, format=pub.TOPIC_TREE_FROM_STRING)
    
    
        provFile = """
            class rootTopic1:
                class subtopic_2:
                    class subsubtopic_21:
                        '''Sub sub topic 1 of sub topic 2.'''
                        def msgDataSpec(arg1, arg2=None, someArg=456, arg4=None):
                            '''
                            - arg1: doc for arg1
                            - arg2: doc for arg2
                            - arg4: doc for arg4
                            '''
                            pass
            """
    
        myTopicTree = file('myTopicTree.py', 'w')
        myTopicTree.write(dedent(provFile))
        myTopicTree.close()
        pub.importTopicTree('myTopicTree', format=pub.TOPIC_TREE_FROM_MODULE, lazy=True)
        import os
        os.remove('myTopicTree.py')
        if os.path.exists('myTopicTree.pyc'):
            os.remove('myTopicTree.pyc')
            
        assert not pub.getTopic('rootTopic1.subtopic_2', okIfNone=True)
        # the following should create all topic tree since parent
        # topics are automatically created
        assert pub.getOrCreateTopic('rootTopic1.subtopic_1.subsubtopic_11')
        assert pub.getOrCreateTopic('rootTopic1.subtopic_1.subsubtopic_12')
        assert pub.getOrCreateTopic('rootTopic1.subtopic_2.subsubtopic_21')
    
        # validate that topic specs were properly parsed
        def isValid(topicName, listener):
            topic = pub.getTopic(topicName)
            assert topic.getDescription()
            assert topic.isSendable()
            return topic.isValid(listener)
    
        def sub():
            pass
        def sub_1(arg1, arg2=123):
            pass
        def sub_11(arg1, arg3, arg2=None, arg4=None):
            pass
        assert isValid('rootTopic1', sub)
        assert isValid('rootTopic1.subtopic_1', sub_1)
        assert isValid('rootTopic1.subtopic_1.subsubtopic_11', sub_11)
        # no providers have spec for subtopic_2
        assert not pub.getTopic('rootTopic1.subtopic_2').isSendable()
    
        #printTreeSpec()
    
        pub.exportTopicTree('newTopicTree')
        root2Defn = pub.exportTopicTree(rootTopicName='rootTopic1')
    
        import os
        os.remove('newTopicTree.py')
        if os.path.exists('newTopicTree.pyc'):
            os.remove('newTopicTree.pyc')


    def test2_import_export_no_change(self):
        #
        # Test that import/export/import does not change the import
        #
        
        importStr = """
            '''Tree docs, can be anything you want.'''
    
            class test_import_export_no_change:
                '''Root topic 1.'''
    
                class subtopic_1:
                    '''
                    Sub topic 1 of root topic. Docs rely on one
                    blank line for topic doc, and indentation for
                    each argument doc.
                    '''
    
                    def msgDataSpec(arg1, arg2=None):
                        '''
                        - arg1: some multiline doc
                            for arg1
                        - arg2: some multiline doc
                            for arg2
                        '''
                        pass
            """
        pub.clearTopicDefnProviders()
        treeDoc = pub.importTopicTree(importStr, lazy = True,
            format = pub.TOPIC_TREE_FROM_STRING)
        assert treeDoc == '''Tree docs, can be anything you want.'''
        root = pub.getOrCreateTopic('test_import_export_no_change.subtopic_1')
        # few sanity checks
        def sub_1(arg1, arg2=None):
            pass
        assert root.isSendable()
        assert pub.isValid(sub_1, 'test_import_export_no_change.subtopic_1')
    
        # export tree
        exported = pub.exportTopicTree(rootTopicName='test_import_export_no_change', moduleDoc=treeDoc)
        #print exported
    
        expectExport = """\
            # Automatically generated by TopicTreeAsSpec(**kwargs).
            # The kwargs were:
            # - fileObj: StringIO
            # - width: 70
            # - treeDoc: 'Tree docs, can be anything you want....'
            # - indentStep: 4
            # - footer: '# End of topic tree definition. Note that application may l...'
    
    
            '''
            Tree docs, can be anything you want.
            '''
    
    
            class test_import_export_no_change:
                '''
                Root topic 1.
                '''
    
                class subtopic_1:
                    '''
                    Sub topic 1 of root topic. Docs rely on one
                    blank line for topic doc, and indentation for
                    each argument doc.
                    '''
    
                    def msgDataSpec(arg1, arg2=None):
                        '''
                        - arg1: some multiline doc
                            for arg1
                        - arg2: some multiline doc
                            for arg2
                        '''
    
    
            # End of topic tree definition. Note that application may load
            # more than one definitions provider.
            """
    
        # check there are no differences
        from difflib import context_diff, ndiff
        diffs = ndiff( dedent(expectExport).splitlines(), exported.splitlines())
        diffs = [d for d in diffs if not d.startswith(' ')]
        #print '\n'.join(diffs)
        assert diffs == ['- ', '+         ']
    
        # now for module:
        modDoc = pub.importTopicTree('lib_pubsub_provider_expect',
                                     format=pub.TOPIC_TREE_FROM_MODULE,
                                     lazy=False)
        assert modDoc.startswith('\nTree docs, can be anything you')
        pub.exportTopicTree('lib_pubsub_provider_actual',
            rootTopicName='test_import_export_no_change2',
            moduleDoc=treeDoc)
        lines1 = file('lib_pubsub_provider_actual.py', 'r').readlines()
        lines2 = file('lib_pubsub_provider_expect.py', 'r').readlines()
        diffs = context_diff( lines1, lines2 )
        assert not list(diffs)
    
    def test_module_as_class(self):
        assert pub.getTopic('root_topic1', True) is None
        assert pub.getTopic('root_topic2.sub_topic21', True) is None
    
        import lib_pubsub_provider_my_import_topics
        pub.importTopicTree(lib_pubsub_provider_my_import_topics)
    
        assert pub.getTopic('root_topic1') is not None
        assert pub.getTopic('root_topic2.sub_topic21') is not None
    
        pub.sendMessage(lib_pubsub_provider_my_import_topics.root_topic1)


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()

            