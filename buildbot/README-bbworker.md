How to set up a buildbot worker
================================

* Create a Python venv for the buildbot worker, and populate it with the
  buildbot-worker and dependent packages:

      cd ~/.myPyEnv
      python3.8 -m venv Py38-bb2
      source Py38-bb2/bin/activate
      pip install buildbot-worker


* Add a project folder, like bb2, that will be the base folder for the buildbot
  worker and the venvs used for the builds.

* Set up venvs for each Python to be supported on this platform. They should be
  located in the bb2 folder, and named like "venv-3.8"

* Add configuration for the new worker in master.cfg, and update the server.

* Create the worker config using:

      buildbot-worker create-worker . buildbot.wxpython.org:9988 <name> <passwd>

* Add start and stop scripts, like these:

      #!/bin/bash
      source ~/bin/wrangler.sh Py38-bb2
      echo "(Re)starting the buildbot-worker"
      buildbot-worker restart .


      #!/bin/bash
      source ~/bin/wrangler.sh Py38-bb2
      echo "Stopping the buildbot-worker"
      buildbot-worker stop .
