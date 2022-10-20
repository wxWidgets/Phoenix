#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------
# Name:        wx.tools.wxget_docs_demo
# Purpose:     wx fetch and launch demo or docs
#
# Author:      Steve Barnes
#
# Created:     06-Aug-2017
# Copyright:   (c) 2017-2020 by Steve Barnes
# Licence:     wxWindows license
# Tags:        phoenix-port, py3-port
#
# Module to allow the correct version of the documents and/or demos to be
# launched after, if necessarily being fetched.
#----------------------------------------------------------------------

"""
wxget_docs_demo.py -- Launch the appropriate wx Docs or Demo.

Usage:
    wxget_docs_demo [docs|demo]

Will install if missing, the requested item for the current version and then
launch it.

Use: doc|demo --force to force a fresh download.
"""
from __future__ import (division, absolute_import, print_function, unicode_literals)

import sys
import os
import subprocess
import webbrowser
import tarfile
if sys.version_info >= (3,):
    from urllib.error import HTTPError
    import urllib.request as urllib2
    import urllib.parse as urlparse
    from urllib.request import pathname2url
else:
    import urllib2
    from urllib2 import HTTPError
    import urlparse
    from urllib import pathname2url

import wx
from wx.tools import wxget

print(sys.version_info, sys.version, sys.argv)
APP = None
if wx.VERSION[0] != 4:
    raise ValueError("wx Versions other than 4 not currently supported!")

def ensure_wx_app():
    """ Ensure that there is a wx.App instance."""
    global APP
    if APP is None and not wx.GetApp():
        APP = wx.App()
        APP.SetAppName("wxPython")
    return (APP is not None)

def get_paths_dict():
    """ Get a dictionary of the required paths."""
    global APP
    ensure_wx_app()
    sp = wx.StandardPaths.Get()
    pathdict = {}
    pathdict['TempDir'] = sp.GetTempDir()
    pathdict['Cache'] = os.path.join(sp.GetUserLocalDataDir(), 'wxDocsDemoCache',
                                     wx.VERSION_STRING)
    pathdict['Docs_URL'] = wxget.get_docs_demo_url(False)
    #pathdict['wxDocs'] = os.path.join(sp.GetAppDocumentsDir(), 'wxDocs', wx.VERSION_STRING)
    pathdict['wxDocs'] = sp.GetAppDocumentsDir()
    pathdict['Docs_Name'] = "wxPython-docs-%s" % wx.VERSION_STRING
    pathdict['Demo_URL'] = wxget.get_docs_demo_url(True)
    #pathdict['wxDemo'] = os.path.join(sp.GetUserLocalDataDir(), 'wxDemo', wx.VERSION_STRING)
    pathdict['wxDemo'] = sp.GetUserLocalDataDir()
    pathdict['Demo_Name'] = "wxPython-demo-%s" % wx.VERSION_STRING
    pathdict['Ext'] = 'tar.gz'
    return pathdict

def unpack_cached(cached, dest_dir):
    """ Unpack from the cache."""
    print('Unpack', cached, 'to', dest_dir)
    with tarfile.open(cached, "r:*") as tf:
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(tf, dest_dir)
    dest_dir = os.listdir(dest_dir)[0]
    return dest_dir

def get_item(final, url, cache, name, ext, forced=False):
    """ Get the item """
    print('Looking for', name, 'at', final)
    fullpath = os.path.join(final, name)
    if os.path.exists(fullpath) and not forced:  # Already exists
        return fullpath

    cached = os.path.join(cache, name)
    cached = os.path.extsep.join([cached, ext])
    print('Looking for cached', cached)
    if not os.path.exists(cached) or forced:  # No cached copy
        yes_no = wx.MessageBox(
            "\n".join(
                ["%s is not yet installed." % name,
                 "Go on-line to get it?",
                 "(Select No on charged or slow connections)"]),
            "Download Prompt", wx.YES_NO|wx.CENTER|wx.ICON_INFORMATION)
        if yes_no == wx.YES:
            cached = wxget.download_file(url, cache, force=forced, trusted=True)
        else:
            report_error("Download Cancelled!")

    if os.path.exists(cached):  # We now have a cached copy
        unpack_cached(cached, final)
    else:
        fullpath = None
    return fullpath

def report_error(err_text):
    """ Report a problem."""
    ensure_wx_app()
    wx.MessageBox(err_text, caption='ERROR!',
                  style=wx.OK|wx.CENTRE|wx.ICON_ERROR)

def done(result=0):
    """ Tidy up and exit."""
    global APP
    if APP:
        print("Closing Launcher App!")  # Debug
        if result:
            print(result)
        wx.Exit()
    print("Done!")
    sys.exit(result)

def docs_main(args=sys.argv):
    """ Get/Launch Docs."""
    ensure_wx_app()
    result = 0
    print("Launch Docs for wxPython V%s" % wx.VERSION_STRING)
    pd = get_paths_dict()
    location = get_item(pd['wxDocs'], pd['Docs_URL'], pd['Cache'],
                        pd['Docs_Name'], pd['Ext'], forced="--force" in args)
    if location:
        location = os.path.join(location, 'docs', 'html', 'index.html')
        location_url = urlparse.urljoin('file:', pathname2url(location))
        print("Show Docs at:", location)
        webbrowser.open(location_url)
    else:
        result = 'Unable to find and show the wxPython Documentation!'
        report_error(result)
    done(result)

def demo_main(args=sys.argv):
    """ Get/Launch Demo."""
    result = 0
    ensure_wx_app()
    print("Launch Demo for wxPython V%s" % wx.VERSION_STRING)
    pd = get_paths_dict()
    location = get_item(pd['wxDemo'], pd['Demo_URL'], pd['Cache'],
                        pd['Demo_Name'], pd['Ext'], forced="--force" in args)
    if location:
        cmds = [sys.executable, os.path.join(location, "demo", "demo.py")]
        print("Launching", cmds[1])
        pid = subprocess.Popen(cmds).pid
        #subprocess.check_call(cmds) # Use instead for debug
        print("Demo starting as PID %s - may take a few seconds!" % pid)
    else:
        result = 'Unable to find and start the wxPython Demo!'
        report_error(result)
    done(result)

def main(args=sys.argv):
    """ Command line main."""
    if len(args) > 1:
        if "demo" in args[1].lower():
            return demo_main()
        elif "docs" in args[1].lower():
            return docs_main()
        #else:
    print(__doc__)
    #else:
        #APP = wx.App()

if __name__ == "__main__":
    main()
