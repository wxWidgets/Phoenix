"""

:copyright: Copyright 2006-2009 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE.txt for details.


"""

import unittest
from io import StringIO
from unittests import wtc

from wx.lib.pubsub.utils import notification

#---------------------------------------------------------------------------


class lib_pubsub_DefaultLog(wtc.PubsubTestCase):

    def testNotifications(self):
        capture = StringIO()
        logger = notification.useNotifyByWriteFile(capture)
        def block():
            def listener(): pass
            self.pub.subscribe(listener, 'testNotifications')
        block()


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()

