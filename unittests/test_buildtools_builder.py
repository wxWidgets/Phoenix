import os
import unittest
from unittest import mock


class buildtools_builder_Tests(unittest.TestCase):

    def test_msvc_builder_reads_environ(self):
        from buildtools.builder import MSVCProjectBuilder
        env = {'VS90COMNTOOLS': os.path.join('tools', 'vs90')}
        with mock.patch.dict(os.environ, env, clear=True):
            builder = MSVCProjectBuilder()
        self.assertEqual(builder.programDir,
                         os.path.join('tools', 'vs90', '..', 'IDE'))


if __name__ == '__main__':
    unittest.main()
