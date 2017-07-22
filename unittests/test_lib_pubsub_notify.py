"""

:copyright: Copyright 2006-2009 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE.txt for details.


"""

import unittest
from unittests import wtc

from difflib import ndiff, unified_diff, context_diff


#---------------------------------------------------------------------------


class lib_pubsub_Notify(wtc.PubsubTestCase):


    def testNotifyByPrint(self):
        from wx.lib.pubsub.utils.notification import useNotifyByWriteFile

        def captureStdout():
            from six import StringIO
            capture = StringIO()
            useNotifyByWriteFile( fileObj = capture )
            return capture
        capture = captureStdout()


        def listener1(arg1):
            pass
        self.pub.subscribe(listener1, 'baz')
        self.pub.sendMessage('baz', arg1=123)
        self.pub.unsubscribe(listener1, 'baz')

        def doa():
            def listener2():
                pass
            self.pub.subscribe(listener2, 'bar')
        doa()

        self.pub.getDefaultTopicMgr().delTopic('baz')

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
    '''.strip()
        captured = capture.getvalue().strip()
        # strip as other wise one has \n, at least on windows
        assert captured == expect, \
            '\n'.join( unified_diff(expect.splitlines(), captured.splitlines(), n=0) )



#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
