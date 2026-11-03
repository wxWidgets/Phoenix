import sys
import tempfile
import threading
import unittest
from unittest import mock
from unittests import wtc
import wx

import wx.lib.infoframe as infoframe

#---------------------------------------------------------------------------

class lib_infoframe_Tests(wtc.WidgetTestCase):

    def makeOutput(self):
        tempDir = tempfile.TemporaryDirectory()
        self.addCleanup(tempDir.cleanup)
        # write() sets the global tempfile.tempdir to the output directory
        self.addCleanup(setattr, tempfile, 'tempdir', tempfile.tempdir)
        output = infoframe.PyInformationalMessagesFrame(dir=tempDir.name)
        output.SetParent(self.frame)
        self.addCleanup(lambda: output.f and output.f.close())
        return output

    def test_lib_infoframeWrite(self):
        output = self.makeOutput()
        output.write('from the main thread\n')
        self.assertIn('from the main thread', output.text.GetValue())

    def test_lib_infoframeWriteFromThread(self):
        output = self.makeOutput()
        errors = []

        def write():
            try:
                output.write('from another thread\n')
            except Exception as exc:
                errors.append(exc)

        thread = threading.Thread(target=write)
        thread.start()
        while thread.is_alive():
            thread.join(0.01)
        self.myYield()
        self.assertEqual(errors, [])
        self.assertIn('from another thread', output.text.GetValue())

    def test_lib_infoframeClassInSysModules(self):
        # Like typing.io and typing.re on Python < 3.13
        class FakeModule:
            pass

        output = self.makeOutput()
        with mock.patch.dict(sys.modules, {'fake_class_module': FakeModule}):
            output.write('with a class in sys.modules\n')
            output.DisableOutput()
        self.assertIsNone(output.frame)

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
