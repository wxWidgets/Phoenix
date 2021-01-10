Buildbot Master Config
----------------------

The master.cfg file in this folder is the configuration file for Project
Phoenix's buildbot, running at http://buildbot.wxpython.org:8011/ This file
is the master copy and is kept here in order to keep it under revision
control. It is *NOT* automatically copied to the build master when it is
updated and committed and must be copied manually. This is to help avoid
security issues or problems resulting from DSM's by somebody who has commit
access to the source repository but does not know what they are doing with
Buildbot.

Developers with the proper SSH keys can copy the file and reconfigure the
server with these commands:

scp buildbot/master.cfg  wxpybb@buildbot.wxpython.org:/home/wxpybb/bb2
ssh wxpybb@buildbot.wxpython.org "cd /home/wxpybb/bb2 && ./reconfig"

