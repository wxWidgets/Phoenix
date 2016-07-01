"""

:copyright: Copyright 2006-2009 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE.txt for details.

"""

import unittest
from unittests import wtc


from wx.lib.pubsub.core.topicargspec import (
     ArgsInfo,
     ArgSpecGiven,
     SenderMissingReqdMsgDataError ,
     SenderUnknownMsgDataError
     )

#---------------------------------------------------------------------------


class lib_pubsub_Specs(wtc.PubsubTestCase):


    def test1_create(self):
        # root
        td1 = ArgSpecGiven(dict())
        ai1 = ArgsInfo(('t1',), td1, None)
        assert ai1.isComplete()
        assert ai1.numArgs() == 0
        assert ai1.getArgs() == ()
        assert ai1.getCompleteAI() is ai1

        # sub, complete
        td2 = ArgSpecGiven(
            argsDocs = dict(arg1='doc for arg1', arg2='doc for arg2'),
            reqdArgs = ('arg2',))
        ai2 = ArgsInfo(('t1','st1'), td2, ai1)
        assert ai2.isComplete()
        assert ai2.numArgs() == 2
        assert ai2.getArgs() == ('arg1', 'arg2')
        assert ai2.getCompleteAI() is ai2

        # sub, missing
        td2.argsSpecType = ArgSpecGiven.SPEC_GIVEN_NONE
        ai4 = ArgsInfo(('t1','st3'), td2, ai1)
        assert not ai4.isComplete()
        assert ai4.numArgs() == 0
        assert ai4.getArgs() == ()
        assert ai4.getCompleteAI() is ai1

        # sub, of incomplete spec, given ALL args
        td3 = ArgSpecGiven(
            argsDocs = dict(arg1='doc for arg1', arg2='doc for arg2'),
            reqdArgs = ('arg2',))
        ai5 = ArgsInfo(('t1','st3','sst1'), td3, ai4)
        assert ai5.isComplete()
        assert ai5.numArgs() == 2
        assert ai5.hasSameArgs('arg1', 'arg2')
        assert ai5.getCompleteAI() is ai5

    def test2_update(self):
        td1 = ArgSpecGiven(dict())
        td2 = ArgSpecGiven()
        td4 = ArgSpecGiven()
        td5 = ArgSpecGiven(
            argsDocs = dict(
                arg1='doc for arg1', arg2='doc for arg2',
                arg3='doc for arg3', arg4='doc for arg4'),
            reqdArgs = ('arg4','arg2'))

        ai1 = ArgsInfo(('t1',), td1, None)             # root, complete
        ai2 = ArgsInfo(('t1','st1'), td2, ai1)         # sub 1, empty
        ai4 = ArgsInfo(('t1','st1','sst2'), td4, ai2)  # empty sub of sub 1
        ai5 = ArgsInfo(('t1','st1','sst3'), td5, ai2)  # completed sub of sub 1

        # check assumptions before we start:
        assert not ai2.isComplete()
        assert not ai4.isComplete()
        assert     ai5.isComplete()
        assert ai2.numArgs() == 0
        assert ai4.numArgs() == 0
        assert ai5.numArgs() == 4

        # pretend we have an update for ai2: all args now available
        ai2.updateAllArgsFinal( ArgSpecGiven(
                dict(arg1='doc for arg1', arg2='doc for arg2'),
                ('arg2',)) )
        assert ai2.isComplete()
        assert ai2.numArgs() == 2
        assert ai2.hasSameArgs('arg1', 'arg2')
        assert ai2.getCompleteAI() is ai2

        assert not ai4.isComplete()

        assert ai2.numArgs() == 2
        assert ai4.numArgs() == 0
        assert ai5.numArgs() == 4

        assert ai4.getCompleteAI() is ai2

        assert ai2.hasSameArgs('arg1', 'arg2')
        assert ai5.hasSameArgs('arg1', 'arg2', 'arg3', 'arg4')

    def test3_filter(self):
        td = ArgSpecGiven(
            argsDocs = dict(arg1='doc for arg1', arg2='doc for arg2'),
            reqdArgs = ('arg2',))
        ai = ArgsInfo(('t1',), td, None)

        # check:
        argsMissingReqd = {}
        self.assertRaises(SenderMissingReqdMsgDataError , ai.check, argsMissingReqd)

        argsExtraOpt = dict(arg2=2, arg5=5)
        self.assertRaises(SenderUnknownMsgDataError  , ai.check, argsExtraOpt)

        args = dict(arg1=1, arg2=2)
        ai.check(args)

        # filter:
        msgArgs = dict(arg1=1, arg2=2)
        argsOK = msgArgs.copy()
        assert ai.filterArgs( msgArgs ) == argsOK
        msgArgs.update(arg3=3, arg4=4)
        assert ai.filterArgs( msgArgs ) == argsOK

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
