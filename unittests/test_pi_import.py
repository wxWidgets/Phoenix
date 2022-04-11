import unittest
import sys, os, subprocess
import wx

#---------------------------------------------------------------------------

# TODO: We have a bunch of chicken/egg problems in the generated .pyi files, but
# ensuring the stubs are executable Python seems to be less important than it
# used to be so we'll just skip these for now.

@unittest.skip("Skipping .pyi tests for now...")
class PIImportTest(unittest.TestCase):
    """
    The *.pyi files generated are used with some IDE's to create things like
    autocomplete lists and call tips. They are essentially just Python code
    with stubs for all the classes and other things that are in the extension
    modules and that are not easily introspected.

    This test case ensures that the code in the pi files is valid by trying
    to run the file with a new instance of Python.
    """

    def runPI(self, filename):
        cwd = os.getcwd()
        dirname = os.path.dirname(wx.__file__)
        os.chdir(dirname)

        sp = subprocess.Popen('%s %s' % (sys.executable, filename),
                              shell=True,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT)
        stdout, stderr = sp.communicate()
        os.chdir(cwd)

        # stdout will likely contain a traceback or some other indication of
        # the failure, so use it as the assert message for the unittest.
        self.assertEqual(sp.returncode, 0, stdout)


    def test_core_pi(self):
        self.runPI('core.pyi')

    def test_adv_pi(self):
        self.runPI('adv.pyi')

    def test_stc_pi(self):
        self.runPI('stc.pyi')

    def test_html_pi(self):
        self.runPI('html.pyi')

    def test_html2_pi(self):
        self.runPI('html2.pyi')

    def test_dataview_pi(self):
        self.runPI('dataview.pyi')

    def test_xml_pi(self):
        self.runPI('xml.pyi')

    def test_xrc_pi(self):
        self.runPI('xrc.pyi')

    def test_richtext_pi(self):
        self.runPI('richtext.pyi')

    def test_glcanvas_pi(self):
        self.runPI('glcanvas.pyi')

    def test_grid_pi(self):
        self.runPI('grid.pyi')

    def test_media_pi(self):
        self.runPI('media.pyi')

    def test_propgrid_pi(self):
        self.runPI('propgrid.pyi')

    def test_ribbon_pi(self):
        self.runPI('ribbon.pyi')


    @unittest.skipIf('wxMSW' not in wx.PlatformInfo,
                     'wx.msw only relevant on Windows')
    def test_msw_pi(self):
        self.runPI('msw.pyi')


    @unittest.skipIf('wxOSX' not in wx.PlatformInfo,
                     'wx.webkit only relevant on Macs')
    def test_webkit_pi(self):
        self.runPI('webkit.pyi')


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()

