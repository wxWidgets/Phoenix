FROM wxpython4/build:fedora-30

RUN sudo dnf -y install tigervnc-server xterm
RUN mkdir ~/.vnc

# RUN sudo dnf -y install fluxbox
# RUN echo "fluxbox &"> ~/.vnc/xstartup

# RUN sudo dnf -y install @xfce-desktop-environment
# RUN echo "startxfce4 &"> ~/.vnc/xstartup

RUN sudo dnf -y install --allowerasing @mate-desktop-environment
RUN echo "mate-session &"> ~/.vnc/xstartup

# RUN sudo dnf -y install @lxde-desktop-environment
# RUN echo "startlxde &"> ~/.vnc/xstartup

RUN sudo dnf -y remove *screensaver*
RUN sudo dnf clean all 

RUN chmod u+x ~/.vnc/xstartup
RUN echo "password" | vncpasswd -f >> ~/.vnc/passwd
RUN chmod 600 ~/.vnc/passwd
RUN touch ~/.Xauthority

CMD ["start-vncserver.sh"]
