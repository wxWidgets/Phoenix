#!/usr/bin/env python
#---------------------------------------------------------------------------
# Name:        bin/make-new-unittest-file.py
# Author:      Robin Dunn
#
# Created:     12-July-2012
# Copyright:   (c) 2013-2020 by Robin Dunn
# License:     wxWindows License
#---------------------------------------------------------------------------

import os
import sys

script_dir = os.path.dirname(__file__)
root_dir = os.path.abspath(os.path.join(script_dir, ".."))

usage = "usage: %prog [options] name module"
unitteststub = """\
import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class %(name)s_Tests(wtc.WidgetTestCase):

    # TODO: Remove this test and add real ones.
    def test_%(name)s1(self):
        self.fail("Unit tests for %(name)s not implemented yet.")

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
"""




def main(args):
    if not args:
        print("usage: %s names" % __file__)
        return

    for name in args:
        writeFile(
            os.path.join(root_dir, "unittests", "test_%s.py" % name),
            unitteststub, dict(name=name))


def writeFile(filename, stub, values):
    if os.path.exists(filename):
        print("'%s' already exists. Exiting." % filename)
        sys.exit(1)
    with open(filename, 'w') as output:
        output.write(stub % values)

    print("Wrote %s" % filename)




if __name__ == '__main__':
    main(sys.argv[1:])
