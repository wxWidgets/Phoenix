
# The base image
FROM ubuntu:18.04

# Set environment variables
ENV HOME /root

# Define working directory
WORKDIR $HOME


# Install packages and setup environments
RUN \
## add-apt-repository ppa:deadsnakes/ppa  ## Not yet available for bionic
        apt update && \
        apt install -y build-essential dpkg-dev && \
        apt install -y libgtk2.0-dev libgtk-3-dev && \
        apt install -y libjpeg-dev libtiff-dev \
                libsdl1.2-dev libgstreamer-plugins-base1.0-dev \
                libnotify-dev freeglut3 freeglut3-dev libsm-dev \
                libwebkitgtk-dev libwebkitgtk-3.0-dev && \
        \
# Install all available Python packages and their dev packages, and create some virtualenvs
        apt install -y python2.7 python2.7-dev libpython2.7-dev python-virtualenv && \
        apt install -y python3.6 python3.6-dev libpython3.6-dev python3.6-venv && \
        apt install -y python3.7 python3.7-dev libpython3.7-dev python3.7-venv && \
        \
        mkdir $HOME/venvs && \
        cd $HOME && \
        virtualenv --python=python2.7 venvs/Py27 && \
        python3.6 -m venv venvs/Py36 && \
        python3.7 -m venv venvs/Py37 && \
        echo "Done with setup"


# Add files from host into the container
# ... ??? 


# Define moiunt-points for shared folders
VOLUME $HOME/dist

# Define default command
CMD ["bash"]

