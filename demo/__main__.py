#!/usr/bin/env python

import sys
import os
import Main

demoDir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, demoDir)
os.chdir(demoDir)
Main.main()
