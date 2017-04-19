"""

:copyright: Copyright 2006-2009 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE.txt for details.


"""

import unittest
from unittests import wtc

from difflib import ndiff, unified_diff, context_diff


#---------------------------------------------------------------------------


class lib_pubsub_NotifyFlagChanges(wtc.PubsubTestCase):

    def testFlagChanges(self):
        savedFlags = self.pub.getNotificationFlags()

        self.pub.setNotificationFlags(all=True, sendMessage=False, deadListener=False)
        flags = self.pub.getNotificationFlags()
        assert not flags['sendMessage']
        assert not flags['deadListener']
        assert flags['newTopic']
        assert flags['delTopic']
        assert flags['subscribe']
        assert flags['unsubscribe']

        self.pub.setNotificationFlags(subscribe=False, deadListener=True)
        flags = self.pub.getNotificationFlags()
        assert not flags['sendMessage']
        assert not flags['subscribe']
        assert flags['newTopic']
        assert flags['delTopic']
        assert flags['deadListener']
        assert flags['unsubscribe']

        self.pub.setNotificationFlags(all=False, subscribe=True, unsubscribe=True)
        flags = self.pub.getNotificationFlags()
        assert not flags['sendMessage']
        assert not flags['deadListener']
        assert not flags['newTopic']
        assert not flags['delTopic']
        assert flags['subscribe']
        assert flags['unsubscribe']

        self.pub.setNotificationFlags(** savedFlags)


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
