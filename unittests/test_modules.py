import os
import subprocess
import sys
import unittest
import wx

#---------------------------------------------------------------------------

# Run in a new interpreter, since the extension modules have already been
# imported in this one before any wx.App was created.
LATE_IMPORT_SCRIPT = """\
import wx

class RecordingLog(wx.Log):
    def __init__(self):
        wx.Log.__init__(self)
        self.messages = []

    def DoLogTextAtLevel(self, level, msg):
        self.messages.append(msg)

app = wx.App()
log = RecordingLog()
wx.Log.SetActiveTarget(log)
wx.Log.SetLogLevel(wx.LOG_Max)

# wx.propgrid first, since it used to drop the already initialized modules
# from the module list, making the later imports initialize all of them again.
import wx.propgrid
import wx.html
import wx.adv
import wx.richtext
import wx.xrc

frame = wx.Frame(None)
htmlwin = wx.html.HtmlWindow(frame)
htmlwin.SetPage('<html><body><a href="target">link</a></body></html>')

def findLink(cell):
    while cell:
        if cell.GetLink():
            return cell.GetLink().GetHref()
        href = findLink(cell.GetFirstChild())
        if href:
            return href
        cell = cell.GetNext()

# The links tag handler is added by one of wx.html's wxModules
print('link:', findLink(htmlwin.GetInternalRepresentation()))
for msg in log.messages:
    print('log:', msg)

frame.Destroy()
"""

class modules_Tests(unittest.TestCase):

    def test_modulesLateImport(self):
        env = dict(os.environ)
        paths = [os.path.dirname(os.path.dirname(wx.__file__)),
                 env.get('PYTHONPATH')]
        env['PYTHONPATH'] = os.pathsep.join(p for p in paths if p)
        result = subprocess.run([sys.executable, '-c', LATE_IMPORT_SCRIPT],
                                env=env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

        lines = result.stdout.splitlines()
        self.assertIn('link: target', lines)
        problems = [line for line in lines if line.startswith('log:') and
                    ('duplicate' in line or 'Error' in line or
                     "doesn't exist" in line)]
        self.assertEqual(problems, [])

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
