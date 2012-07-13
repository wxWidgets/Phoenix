
"""
This is a way to save the startup time when running img2py on lots of
files...
"""
import sys, os
if os.path.abspath('..') not in sys.path:
    sys.path.append(os.path.abspath('..'))

vspdir =  'f:/Python%s-sp.v%s' % ( '25', '660')  # version-specific site-packages
if os.path.exists(vspdir) and vspdir not in sys.path:
    sys.path.append(vspdir)

from wx.tools import img2py


command_lines = [
    "   -u -n First PlayerFirst.png ../images.py",
    "-a -u -n Prev PlayerPrev.png ../images.py",
    "-a -u -n Next PlayerNext.png ../images.py",
    "-a -u -n Last PlayerLast.png ../images.py",
    "-a -u -n PrintIt Printer.png ../images.py",
    "-a -u -n SaveIt Save.png ../images.py",
    "-a -u -n Left ArrowLeft.png ../images.py",
    "-a -u -n Right ArrowRight.png ../images.py",
    "-a -u -n Width DirectionH.png ../images.py",
    "-a -u -n Height DirectionV.png ../images.py",
    "-a -u -n ZoomIn ZoomIn.png ../images.py",
    "-a -u -n ZoomOut ZoomOut.png ../images.py",
    ]


if __name__ == "__main__":
    for line in command_lines:
        args = line.split()
        img2py.main(args)

