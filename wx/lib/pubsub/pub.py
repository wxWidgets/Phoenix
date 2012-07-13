'''
This is the top-level API to pubsub, API version 3. It provides
functions for sending messages, subscribing listeners to receive
messages, and various auxiliary functions. It also exposes several
classes such as Topic, Listener, Publisher, and many more that could
be used in advanced pub-sub applications.

Note that many functions in this module actually make use of a
Publisher and TopicManager instance created upon import. 

Some usage details for some functions: 

- importTopicTree():

    Using pub.sendMessage('your.topic.name', **kwargs) is nice but in bigger
    apps you soon realize that typos are too easy and will create new topics. 
    Also, by default the first sendMessage or subscribe creates the message 
    data specification, which all other sendMessage and subscribe must adhere 
    to. It is better for this to be done in one place and validated every time
    sendMessage and subscribe are called. 
    
    To help with this, it is possible to create a hierarchy of topic definitions, 
    which contain the topic names and a signature that all listeners of the 
    topic will have to satisfy. The format of this tree can be seen by calling
    exportTopicTree(moduleName='yourModule'); then look at the contents of the 
    yourModule.py. If setTopicUnspecfiedFatal() has been called, then
    only topics that have a definition are allowed. 
      
    If lazy is True, the topics will be
    put in topic tree only upon first use by the application, otherwise,
    all topics that don't already exist are incorporated (this may result
    in a smaller topic tree if an application has evolved significantly).
    
    Some sources can accept extra arguments in **providerKwargs; these 
    get passed on to the TopicDefinitionProvider as is. 
    
    The doc string for the source is returned (for a module source, this
    is the module doc string; etc). 
    
    A typical workflow would be: 
    
    - use exportTopicTree() once in a while and inspect the generated 
      file for topics that differ only by a typo, fix issues
    - once the topic tree has started to gel, save the topic tree file
      created by exportTopicTree() and complete it with documentation
    - use importTopicTree() and setTopicUnspecifiedFatal()
    - to add new topics, manually add them to the topic tree file, OR
      comment out the call to setTopicUnspecifiedFatal() and recall 
      exportTopicTree (your docs should *not* be affected but YMMV)
    - by importing the topic tree file, you can use code completion
    
    Example::
    
        from pubsub import pub
        import your_topic_tree_module
        pub.importTopicTree(your_topic_tree_module)
        pub.setTopicUnspecifiedFatal()
        
        pub.subscribe(listener, your_topic_tree_module.topic1)
        pub.sendMessage(your_topic_tree_module.topic1.subtopic1, kwarg1=..., ...)

    Notes: 
    
    - This function can be called several times, but should be called
      only once per source. The topics get merged; existing topics get
      overwritten. 
    - More source formats can be defined via
      pub.registerTopicDefnProviderType(), which must be given a class
      that adheres to the pub.ITopicDefnProvider interface.
    - If lazy=True, then a later call to exportTopicTree() will only
      export those topics that have been used by the application 

TODO: add isMsgReceivable(listener, topicName) to find out if listener is
      subscribed to topicName or any of its subtopics. 

:copyright: Copyright 2006-2009 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE.txt for details.

'''

PUBSUB_VERSION = 3                     # DO NOT CHANGE
SVN_VERSION = "$Rev: 243 $".split()[1] # DO NOT CHANGE
VERSION_STR = "3.1.2.201112.r" + SVN_VERSION # update at each new release


from core.listener import \
    Listener, \
    getID as getListenerID, \
    ListenerInadequate
    
from core.topicobj import \
    Topic, \
    SenderMissingReqdArgs, \
    SenderUnknownOptArgs, \
    ListenerSpecInvalid, \
    ListenerNotValidatable, \
    ExcHandlerError

from core.topicmgr import \
    TopicManager as _TopicManager, \
    ListenerSpecIncomplete, \
    UndefinedTopic, \
    UndefinedSubtopic, \
    ALL_TOPICS

from core.topicdefnprovider import \
    ITopicDefnProvider, TopicDefnProvider, \
    registerTypeForImport as registerTopicDefnProviderType, \
    IMPORT_MODULE as TOPIC_TREE_FROM_MODULE, \
    IMPORT_STRING as TOPIC_TREE_FROM_STRING, \
    IMPORT_CLASS as TOPIC_TREE_FROM_CLASS, \
    exportTreeAsSpec, TopicTreeTraverser

from core.publisher import Publisher



__all__ = [
    # listener stuff:
    'Listener', 'ListenerInadequate', 
    'isValid', 'validate',
    
    # topic stuff:
    'ALL_TOPICS', 'Topic', 
    'topics', 'topicsMap', 'AUTO_TOPIC',
    'getOrCreateTopic', 'getTopic', 'newTopic', 'delTopic',
    'ListenerSpecIncomplete', 'ListenerNotValidatable',
    'UndefinedTopic', 'UndefinedSubtopic', 'ExcHandlerError',
    'getAssociatedTopics',
    'getDefaultTopicMgr', 'getDefaultRootAllTopics',

    # topioc defn provider stuff
    'addTopicDefnProvider', 'clearTopicDefnProviders',
    'registerTopicDefnProviderType', 'TOPIC_TREE_FROM_MODULE',
    'TOPIC_TREE_FROM_CLASS', 'TOPIC_TREE_FROM_STRING',
    'importTopicTree', 'exportTopicTree', 'TopicTreeTraverser',
    
    # publisher stuff:
    'Publisher', 
    'subscribe', 'unsubscribe', 'isSubscribed', 'unsubAll', 
    'sendMessage', 'SenderMissingReqdArgs', 'SenderUnknownOptArgs',
    'getListenerExcHandler', 'setListenerExcHandler',
    'addNotificationHandler', 'setNotificationFlags', 'clearNotificationHandlers',
    'setTopicUnspecifiedFatal',
    
    # misc:
    'PUBSUB_VERSION',
    ]


# ---------------------------------------------

_publisher = Publisher()

subscribe   = _publisher.subscribe    
unsubscribe = _publisher.unsubscribe
unsubAll    = _publisher.unsubAll
sendMessage = _publisher.sendMessage

getListenerExcHandler     = _publisher.getListenerExcHandler
setListenerExcHandler     = _publisher.setListenerExcHandler
addNotificationHandler    = _publisher.addNotificationHandler
clearNotificationHandlers = _publisher.clearNotificationHandlers
setNotificationFlags      = _publisher.setNotificationFlags
getNotificationFlags      = _publisher.getNotificationFlags

setTopicUnspecifiedFatal = _publisher.setTopicUnspecifiedFatal
getMsgProtocol = _publisher.getMsgProtocol

def getDefaultPublisher():
    '''Get the Publisher that is created by default when you 
    import package.'''
    return _publisher


# ---------------------------------------------
_topicMgr = _publisher.getTopicMgr()

topics    = _topicMgr.getRootTopic()
topicsMap = _topicMgr._topicsMap
AUTO_TOPIC  = Listener.AUTO_TOPIC


def isValid(listener, topicName):
    '''Return true only if listener can subscribe to messages of 
    type topicName.'''
    return _topicMgr.getTopic(topicName).isValid(listener)


def validate(listener, topicName):
    '''Checks if listener can subscribe to topicName. If not, raises
    ListenerInadequate, otherwise just returns.'''
    _topicMgr.getTopic(topicName).validate(listener)

    
def isSubscribed(listener, topicName):
    '''Returns true if listener has subscribed to topicName, false otherwise.
    WARNING: a false return is not a guarantee that listener won't get
    messages of topicName: it could receive messages of a subtopic of
    topicName. '''
    return _topicMgr.getTopic(topicName).hasListener(listener)
    

def getDefaultTopicMgr():
    '''Get the topic manager that is created by default when you 
    import package.'''
    return _topicMgr

def getDefaultRootAllTopics():
    '''Get the topic that is parent of all root (ie top-level) topics. Useful
    characteristics:
    
    - "root of all topics" topic satisfies isAll()==True, isRoot()==False,
      getParent() is None;
    - all top-level topics satisfy isAll()==False, isRoot()==True, and
      getParent() is getDefaultRootAllTopics();
    - all other topics satisfy neither. '''
    return _topicMgr.getRootTopic()

getOrCreateTopic     = _topicMgr.getOrCreateTopic
newTopic             = _topicMgr.newTopic
delTopic             = _topicMgr.delTopic
getTopic             = _topicMgr.getTopic
getAssociatedTopics  = _topicMgr.getTopics


addTopicDefnProvider = _topicMgr.addDefnProvider
clearTopicDefnProviders = _topicMgr.clearDefnProviders


def importTopicTree(source, format = TOPIC_TREE_FROM_CLASS, lazy=False, **providerKwargs):
    '''Import topic definitions. The source contains the definitions and can be one of 
    several types (module, class, string), indicated by the "format" parameter. If lazy 
    is True, all topics defined in source get instantiated even if not used by the 
    application. The providerKwargs are given vertabim to the TopicDefnProvider that 
    is used by this function. 
    '''
    provider = TopicDefnProvider(source, format, **providerKwargs)
    addTopicDefnProvider(provider)
    if not lazy:
        for topicName in provider:
            _topicMgr.getOrCreateTopic(topicName)

    return provider.getTreeDoc()


def _backupIfExists(filename, bak):
    import os, shutil
    if os.path.exists(filename):
        backupName = '%s.%s' % (filename, bak)
        shutil.copy(filename, backupName)


def exportTopicTree(moduleName = None, rootTopicName=None, rootTopic=None, 
    bak='bak', moduleDoc=None):
    '''Export the topic tree to a string and return the string. Parameters:

        - If moduleName is given, the string is also written to moduleName.py in
          os.getcwd() (the file is overwritten). If bak is None, the module file
          is not backed up. 
        - If rootTopicName or rootTopic are specified, the export only traverses 
          tree from corresponding topic. Otherwise, pub.ALL_TOPICS is starting point. 
        - The moduleDoc is the doc string for the module.
    '''

    if rootTopicName:
        rootTopic = _topicMgr.getTopic(rootTopicName)
    if rootTopic is None:
        rootTopic = getDefaultRootAllTopics()
        
    # create exporter
    if moduleName is None:
        from StringIO import StringIO
        capture = StringIO()
        exportTreeAsSpec(rootTopic, fileObj=capture, treeDoc=moduleDoc)
        return capture.getvalue()
        
    else:
        filename = '%s.py' % moduleName
        if bak:
            _backupIfExists(filename, bak)
        moduleFile = file(filename, 'w')
        try:
            exportTreeAsSpec(rootTopic, fileObj=moduleFile, treeDoc=moduleDoc)
        finally:
            moduleFile.close()


#---------------------------------------------------------------------------

# save the fact that we have been loaded, to pubsubconf
import pubsubconf
pubsubconf.pubModuleLoaded()
del pubsubconf
