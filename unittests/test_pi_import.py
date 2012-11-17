import imp_unittest, unittest
import sys, os, subprocess

#---------------------------------------------------------------------------

class PIImportTest(unittest.TestCase):
    """
    The *.pi files generated are used with IDE's like WingIDE to create
    things like autocomplete lists and call tips. They are essentially just
    Python code with stubs for all the classes and other things that are in
    the extension modules and that are not easily introspected.
    
    This test case ensures that the code in the pi files is valid by trying
    to run the file with a new instance of Python.
    """

    def runPI(self, filename):
        cwd = os.getcwd()
        dirname = os.path.join(os.path.dirname(__file__), '../wx')
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
        self.runPI('core.pi')
        
    #def test_adv_pi(self):
    #    self.runPI('adv.pi')

    def test_stc_pi(self):
        self.runPI('stc.pi')

    def test_html_pi(self):
        self.runPI('html.pi')
        
    def test_dataview_pi(self):
        self.runPI('dataview.pi')
        
#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
        