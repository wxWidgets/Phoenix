'''
If this module is named autosetuppubsubv1, and it is in the pubsub
package's folder, it will cause pubsub to default to "version 1" (v1)
of the API when pub is imported. The v1 API was the version originally
developed as part of wxPython's wx.lib library.

If this module is named anything else (such as prefixed with an
underscore) it will not be found by pubsub: the most recent pubsub
API will be loaded upon import of the *pub* module.
'''

def testWxPython():
    if not __file__: 
        # we don't know where we are imported from, assume all is good
        return
        
    from fnmatch import fnmatch
    if not fnmatch(__file__, '*/wx/lib/pubsub/*'):
        # this is not the pubsub in wxPython
        return

    # print 'PubSub from wx.lib.pubsub'
        
    # if wx >= 2.9, use latest pubsub API ie kwargs
    # this is done by raising ImportError which will make
    # pubsub.__init__ think this autosetup module does not
    # exist
    import wx
    if wx.MAJOR_VERSION >= 3:
        raise ImportError
    if wx.MAJOR_VERSION == 2 and wx.MINOR_VERSION >= 9: 
        raise ImportError
    # print '   Found wx version < 2.9'
    
testWxPython()
# print 'Using pubsub API v1'
    
