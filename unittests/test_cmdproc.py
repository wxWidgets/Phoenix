import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class cmdproc_Tests(wtc.WidgetTestCase):

    def test_cmdproc1(self):
        with self.assertRaises(TypeError):
            cmd = wx.Command()

    def test_cmdproc2(self):
        class MyCommand(wx.Command):
            def Do(self):
                return True
            def Undo(self):
                return True

        cmd = MyCommand(name='TestCommand')


    def test_cmdproc3(self):
        class MyCommand(wx.Command):
            def __init__(self, *args, **kw):
                wx.Command.__init__(self, *args, **kw)
                self.value = False
            def Do(self):
                self.value = True
                return True
            def Undo(self):
                self.value = False
                return True
            def CanUndo(self):
                return True

        cmdproc = wx.CommandProcessor()
        for name in 'one two three four five'.split():
            cmd = MyCommand(name=name)
            cmdproc.Submit(cmd)

        cmds = cmdproc.GetCommands()
        self.assertEqual(len(cmds), 5)
        self.assertEqual([x.value for x in cmds], [True]*5)

        self.assertTrue(cmdproc.CanUndo())
        self.assertFalse(cmdproc.CanRedo())

        cmdproc.Undo()
        cmdproc.Undo()
        self.assertEqual([x.value for x in cmds], [True]*3 + [False]*2)

        self.assertTrue(cmdproc.CanRedo())
        cmdproc.Redo()
        cmdproc.Redo()
        self.assertEqual([x.value for x in cmds], [True]*5)

        cmdproc.Undo()
        cmdproc.Undo()
        cmdproc.Submit(MyCommand(name='NewCmd'))
        self.assertEqual(len(cmds), 4)


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
