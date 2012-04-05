# -*- coding: utf-8 -*-#
#!/usr/bin/env python
"""
This will generate the .pot and .mo files for the application domain and languages defined below.

The .po and .mo files are placed as per convention in

"appfolder/locale/lang/LC_MESSAGES"

The .pot file is placed in the current folder.

This script or something similar should be added to your build process.

The actual translation work is normally done using a tool like poEdit or
similar, it allows you to generate a particular language catalog from the .pot
file or to use the .pot to merge new translations into an existing language
catalog.

"""

domainName = 'i18nwxapp'
# define the languages you are supporting and need translation, so if texts
# in your source are English then you don't need 'en' here
supLang = ['fr', 'de']

import os
import sys
import subprocess

appFolder, loc = os.path.split(os.getcwd())

# setup some stuff to get at Python I18N tools/utilities

pyExe = sys.executable
pyFolder = os.path.split(pyExe)[0]
pyToolsFolder = os.path.join(pyFolder, 'Tools')
pyI18nFolder = os.path.join(pyToolsFolder, 'i18n')
pyGettext = os.path.join(pyI18nFolder, 'pygettext.py')
pyMsgfmt = os.path.join(pyI18nFolder, 'msgfmt.py')
outFolder = os.getcwd()

# build command for pygettext
gtOptions = '-a -d %s -o %s.pot -p %s %s'
tCmd = pyExe + ' ' + pyGettext + ' ' + (gtOptions % (domainName,
                                                     domainName,
                                                     outFolder,
                                                     appFolder))
print "Generating the .pot file"
print "cmd: %s" % tCmd
rCode = subprocess.call(tCmd)
print "return code: %s\n\n" % rCode

for tLang in supLang:
    # build command for msgfmt
    langDir = os.path.join(appFolder, ('locale\%s\LC_MESSAGES' % tLang))
    poFile = os.path.join(langDir, domainName + '.po')
    tCmd = pyExe + ' ' + pyMsgfmt + ' ' + poFile
    
    print "Generating the .mo file"
    print "cmd: %s" % tCmd
    rCode = subprocess.call(tCmd)
    print "return code: %s\n\n" % rCode
