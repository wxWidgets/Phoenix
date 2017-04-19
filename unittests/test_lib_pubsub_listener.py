"""

:copyright: Copyright 2006-2009 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE.txt for details.

"""

import six
import unittest
from unittests import wtc

from wx.lib.pubsub.core.weakmethod import WeakMethod
from wx.lib.pubsub.core import listener
from wx.lib.pubsub.core.listener import (
     Listener, ListenerValidator,
     ListenerMismatchError,
     CallArgsInfo,
     getArgs)

#---------------------------------------------------------------------------

class ArgsInfoMock:
    def __init__(self, autoTopicArgName=None):
        self.autoTopicArgName = autoTopicArgName
        self.acceptsAllKwargs = False

#---------------------------------------------------------------------------


class lib_pubsub_ArgsInfo(wtc.PubsubTestCase):

    def test0_ArgsInfo(self):
        def listener0(msgTopic = Listener.AUTO_TOPIC):
            pass
        CallArgsInfo(listener0, 0)

        def listener1(arg1, msgTopic = Listener.AUTO_TOPIC):
            pass
        CallArgsInfo(listener1, 1)


    def test2_Validation0(self):
        # Test when ValidatorSameKwargsOnly used, ie when args in
        # listener and topic must be exact match (unless *arg).
        AA = Listener.AUTO_TOPIC

        # test for topic that has no arg/kwargs in topic message spec (TMS)
        def same():
            pass
        def varargs(*args, **kwargs):
            pass
        def autoArg(msgTopic=AA):
            pass
        def extraArg(a):
            pass
        def extraKwarg(a=1):
            pass

        # no arg/kwarg in topic message spec (TMS)
        validator = ListenerValidator([], [])
        validate = validator.validate

        validate(same)      # ok: same
        validate(varargs)   # ok: *args/**kwargs
        validate(autoArg)   # ok: extra but AUTO_TOPIC
        self.assertRaises(ListenerMismatchError, validate, extraArg)   # E: extra arg
        self.assertRaises(ListenerMismatchError, validate, extraKwarg) # E: extra kwarg

    def test2_Validation1(self):
        # one arg/kwarg in topic
        validator = ListenerValidator(['a'], ['b'])
        validate = validator.validate

        def same(a, b=1):
            pass
        def same2(a=2, b=1):
            pass
        def varkwargs(**kwargs):
            pass
        def varkwargs_a(a, **kwargs):
            pass

        def opt_reqd(b, **kwargs):
            pass
        def missing_arg(b=1):
            pass
        def missing_kwarg(a):
            pass
        def extra_kwarg1(a,b=1,c=2):
            pass
        def extra_kwarg2(c=1, *args, **kwargs):
            pass
        def extra_arg1(a,c,b=1):
            pass
        def extra_arg2(a,b,c=2):
            pass

        validate(same)           # ok: same
        validate(same2)          # ok: same even if a now has default value
        validate(varkwargs_a)    # ok: has **kwargs
        validate(varkwargs)    # ok: has **kwargs

        self.assertRaises(ListenerMismatchError, validate, opt_reqd)      # E: b now required
        self.assertRaises(ListenerMismatchError, validate, missing_arg)   # E: missing arg
        self.assertRaises(ListenerMismatchError, validate, missing_kwarg) # E: missing kwarg
        self.assertRaises(ListenerMismatchError, validate, extra_kwarg1)  # E: extra kwarg
        self.assertRaises( ListenerMismatchError, validate, extra_kwarg2)  # E: extra kwarg
        self.assertRaises( ListenerMismatchError, validate, extra_arg1)    # E: extra arg
        self.assertRaises( ListenerMismatchError, validate, extra_arg2)    # E: extra arg


    def test3_IsCallable(self):
        # Test the proper trapping of non-callable and certain types of
        # callable objects.

        # validate different types of callables
        validator = ListenerValidator([], [])
        # not a function:
        notAFunc = 1 # just pick something that is not a function
        self.assertRaises(ListenerMismatchError, validator.validate, notAFunc)
        # a regular function:
        def aFunc():
            pass
        validator.validate(aFunc)

        # a functor and a method
        class Foo(object):
            def __call__(self):
                pass
            def meth(self):
                pass
        foo = Foo()
        validator.validate(foo)
        validator.validate(foo.meth)


    def test4_WantTopic(self):
        # Test the correct determination of whether want topic
        # auto-passed during sendMessage() calls.

        # first check proper breakdown of listener args:
        def listener(a, b=1):
            pass
        argsInfo = CallArgsInfo(listener, 0)
        self.assertEqual(None, argsInfo.autoTopicArgName )

        msgTopic = 'auto'
        class MyListener:
            def method(self, a, b=1, auto=Listener.AUTO_TOPIC):
                pass
        listener = MyListener()
        argsInfo = getArgs(listener.method)
        self.assertEqual(msgTopic, argsInfo.autoTopicArgName )
        self.assertEqual(['a','b'], argsInfo.allParams )

        # now some white box testing of validator that makes use of args info:
        def checkWantTopic(validate, listener, wantTopicAsArg=None):
            argsInfo = getArgs(listener)
            self.assertEqual(argsInfo.autoTopicArgName, wantTopicAsArg)
            validate(listener)

        validator = ListenerValidator([], ['a'])
        validate = validator.validate
        def noWant(a=1):
            pass
        def want1(a=1, auto=Listener.AUTO_TOPIC):
            pass
        checkWantTopic(validate, noWant)
        checkWantTopic(validate, want1, msgTopic)

        validator = ListenerValidator(['a'], ['b'])
        validate = validator.validate

        def noWant2(a, b=1):
            pass
        def want2(a, auto=Listener.AUTO_TOPIC, b=1):
            pass
        checkWantTopic(validate, noWant2)
        checkWantTopic(validate, want2, msgTopic)

        # topic that has Listener.AUTO_TOPIC as an arg rather than kwarg
        validator = ListenerValidator([msgTopic], ['b'])
        validate = validator.validate
        def noWant3(auto, b=1):
            pass
        checkWantTopic(validate, noWant3)


    def test5_DOAListeners(self):
        # Test "dead on arrival"

        # test DOA of unbound method
        def getListener1():
            class DOA:
                def tmpFn(self):
                    pass
            Listener( DOA.tmpFn, ArgsInfoMock() )
        # Py3 doesn't have unbound methods so this won't throw a ValueError
        if not six.PY3:
            self.assertRaises(ValueError, getListener1)

        # test DOA of tmp callable:
        def getListener2():
            def fn():
                pass
            class Wrapper:
                def __init__(self, func):
                    self.func = func
                def __call__(self):
                    pass
            def onDead(listenerObj):
                pass

            # check dead-on-arrival when no death callback specified:
            doa1 = Listener( Wrapper(fn), ArgsInfoMock() )
            assert doa1.getCallable() is None
            assert doa1.isDead()
            self.assertRaises(RuntimeError, doa1, None, {})

            # check dead-on-arrival when a death callback specified:
            doa2 = Listener( Wrapper(fn), ArgsInfoMock(), onDead )
            assert doa2.getCallable() is None
            assert doa2.isDead()
            self.assertRaises(RuntimeError, doa2, None, {})

        getListener2()


    def test6_ListenerEq(self):
        # Test equality tests of two listeners

        def listener1():
            pass
        def listener2():
            pass
        l1 = Listener(listener1, ArgsInfoMock())
        l2 = Listener(listener2, ArgsInfoMock())
        # verify that Listener can be compared for equality to another Listener, weakref, or callable
        self.assertEqual    (l1, l1)
        self.assertNotEqual (l1, l2)
        self.assertEqual    (l1, listener1)
        self.assertNotEqual (l1, listener2)
        ll = [l1]
        assert listener1 in ll
        assert listener2 not in ll
        self.assertEqual(ll.index(listener1), 0)

        # now for class method listener:
        class MyListener:
            def __call__(self):
                pass
            def meth(self):
                pass
        listener3 = MyListener()
        l3 = Listener(listener3, ArgsInfoMock() )
        self.assertNotEqual (l3, l1)
        self.assertNotEqual (l3, l2)
        self.assertNotEqual (l3, listener2)
        self.assertEqual    (l3, l3)
        self.assertEqual    (l3, listener3)
        self.assertNotEqual (l3, listener3.__call__)

        l4 = Listener(listener3.meth, ArgsInfoMock())
        self.assertEqual    (l4, l4)
        self.assertNotEqual (l4, l3)
        self.assertNotEqual (l4, l2)
        self.assertNotEqual (l4, listener3.__call__)
        self.assertEqual    (l4, listener3.meth)


    def test7_DyingListenersClass(self):
        # Test notification callbacks when listener dies

        # test dead listener notification
        def onDead(weakListener):
            lsrs.remove(weakListener)

        def listener1():
            pass
        def listener2():
            pass
        def listener3():
            pass
        lsrs = []
        lsrs.append(Listener(listener1, ArgsInfoMock(False), onDead=onDead))
        lsrs.append(Listener(listener2, ArgsInfoMock(False), onDead=onDead))
        lsrs.append(Listener(listener3, ArgsInfoMock(False), onDead=onDead))

        # now force some listeners to die, verify lsrs list
        self.assertEqual(len(lsrs), 3)
        del listener1
        self.assertEqual(len(lsrs), 2)
        self.assertEqual(lsrs[0], listener2)
        self.assertEqual(lsrs[1], listener3)
        del listener2
        self.assertEqual(len(lsrs), 1)
        self.assertEqual(lsrs[0], listener3)
        del listener3
        self.assertEqual(len(lsrs), 0)


    def test8_getArgsBadListener(self):
        self.assertRaises(ListenerMismatchError, getArgs, 1)
        try:
            getArgs(1)
        except ListenerMismatchError as exc:
            msg = 'Listener "int" (from module "__main__") inadequate: type "int" not supported'
            self.assertEqual(str(exc), msg)


    def test10_weakMethod(self):
        class Foo:
            def meth(self):
                pass
        foo = Foo()
        wm = WeakMethod(foo.meth)
        str(wm)


    def test11_testNaming(self):
        aiMock = ArgsInfoMock()

        # define various type of listeners
        def fn():
            pass
        class Foo:
            def __call__(self):
                pass
            def meth(self):
                pass

        ll = Listener(fn, aiMock)
        self.assertEqual(ll.typeName(), "fn")
        self.assertEqual(ll.module(), __name__)
        assert not ll.wantsTopicObjOnCall()

        foo = Foo()
        ll = Listener(foo, aiMock)
        self.assertEqual(ll.typeName(), "Foo")
        self.assertEqual(ll.module(), __name__)
        assert not ll.wantsTopicObjOnCall()

        ll = Listener(foo.meth, ArgsInfoMock('argName'))
        self.assertEqual(ll.typeName(), "Foo.meth")
        self.assertEqual(ll.module(), __name__)
        assert ll.wantsTopicObjOnCall()

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
