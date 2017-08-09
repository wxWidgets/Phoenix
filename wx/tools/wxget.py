#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------
# Name:        wx.tools.wxget
# Purpose:     wx Based alternative to wget
#
# Author:      Steve Barnes
#
# Created:     06-Aug-2017
# Copyright:   (c) 2017 by Steve Barnes
# Licence:     wxWindows license
# Tags:        phoenix-port, py3-port
#
# Module to allow cross platform downloads originally from answers to:
# https://stackoverflow.com/questions/22676/how-do-i-download-a-file-over-http-using-python
# by Stan and PabloG then converted to wx.
#----------------------------------------------------------------------

"""
wxget.py -- wx Version of wget utility for platform that don't have it already.

Usage:
    wxget URL [DEST_DIR]

Where URL is a file URL and the optional DEST_DIR is a destination directory to
download to, (default is to prompt the user).
"""
from __future__ import (division, absolute_import, print_function, unicode_literals)

import sys
import os
import wx

if sys.version_info >= (3,):
    from urllib.error import (HTTPError, URLError)
    import urllib.request as urllib2
    import urllib.parse as urlparse
else:
    import urllib2
    from urllib2 import (HTTPError, URLError)
    import urlparse

def get_docs_demo_url(demo=False):
    """ Get the URL for the docs or demo."""
    if demo:
        pkg = 'demo'
    else:
        pkg = 'docs'
    base_url = "https://extras.wxpython.org/wxPython4/extras/%s/wxPython-%s-%s.tar.gz"
    ver = wx.version().split(' ')[0]
    major = ver.split('.')[0]
    if major != '4':
        raise ValueError("wx Versions before 4 not supported!")
    return base_url % (ver, pkg, ver)

def get_save_path(url, dest_dir, force=False):
    """ Get the file save location."""
    old_dir = os.getcwd()
    if not dest_dir:
        dest_dir = os.getcwd()
    else:
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        os.chdir(dest_dir)
    filename = os.path.basename(urlparse.urlsplit(url)[2])
    if not filename:
        filename = 'downloaded.file'

    if not force:
        with wx.FileDialog(
            None, message="Save As ...", defaultDir=dest_dir,
            defaultFile=filename, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        ) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                dest_dir, filename = os.path.split(dlg.GetPath())
            else:
                url = None
    else:
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        elif not os.path.isdir(dest_dir):
            url = None

    if dest_dir:
        filename = os.path.join(dest_dir, filename)
    os.chdir(old_dir)

    return (url, filename)

def download_file(url, dest=None, force=False):
    """
    Download and save a file specified by url to dest directory, with force will
    operate silently and overwrite any existing file.
    """
    url, filename = get_save_path(url, dest, force)
    if url is None:
        return 'Aborted!'

    if url:
        try:
            url_res = urllib2.urlopen(url)
            keep_going = True
        except (HTTPError, URLError) as err:
            msg = '\n'.join([
            "\n\nERROR in Web Access! - you may be behind a firewall",
            "You may be able to bybass this by using a browser to download:",
            "\n\t%s\n\nand copying to:\n\n\t%s" % (url, filename),
            ])
            print(msg, '\n')
            wx.MessageBox(msg, caption='WDOWNLOAD ERROR!',
                          style=wx.OK|wx.CENTRE|wx.ICON_ERROR)
            return "Error: %s" % err

    with open(filename, 'wb') as outfile:
        block_sz = 8192
        meta = url_res.info()
        meta_func = meta.getheaders if hasattr(meta, 'getheaders') else meta.get_all
        meta_length = meta_func("Content-Length")
        file_size = None
        if meta_length:
            file_size = int(meta_length[0])
        message = "Downloading: {0}\nBytes: {1}\n".format(url, file_size)
        dstyle = wx.PD_APP_MODAL | wx.PD_CAN_ABORT | wx.PD_AUTO_HIDE
        if file_size:
            progress = wx.ProgressDialog('Downloading', message,
                                         maximum=1+file_size/block_sz, style=dstyle)
        else:
            progress = wx.ProgressDialog('Downloading', message, style=dstyle)

        file_size_dl = 0
        while keep_going:
            read_buffer = url_res.read(block_sz)
            if not read_buffer:
                progress.Update(file_size_dl / block_sz, "message+\nDONE!")
                wx.Sleep(0.2)
                break

            file_size_dl += len(read_buffer)
            outfile.write(read_buffer)

            status = "{0:16}".format(file_size_dl)
            if file_size:
                status += "   [{0:6.2f}%]".format(file_size_dl * 100 / file_size)
            (keep_going, dummy_skip) = progress.Update(file_size_dl / block_sz,
                                                       message+status)
            wx.Sleep(0.08)  # Give the GUI some update time
        progress.Destroy()

    return filename

def main(args=sys.argv):
    """ Entry point for wxget."""
    APP = wx.App()

    if len(args) > 2:
        dest_dir = args[2]
    else:
        dest_dir = None
    if len(args) > 1:
        url = args[1]
    else:
        print(__doc__)
        yes_no = wx.MessageBox(__doc__+"\n\nRUN TEST?", "wxget",
                               wx.YES_NO|wx.CENTER)
        if yes_no == wx.YES:
            print("Testing with wxDemo")
            url = get_docs_demo_url()
        else:
            url = None
    if url:
        FILENAME = download_file(url)
        print(FILENAME)

if __name__ == "__main__":  # Only run if this file is called directly
    main()
