#!/bin/bash
echo "starting VNC server ..."
vncserver :1 -geometry 1600x1050 -depth 24 && tail -F ~/.vnc/*.log
