#!/bin/bash
#
# This script is used by CI jobs to update the git submodules in wxWidgets to
# newer versions than are currently in the wx 3.2 branch (mostly for security
# reasons.

set -e

pushd ext/wxWidgets/src/tiff && git checkout 4ab5e7a6aeacf09699e91300da9310874641053f && popd
pushd ext/wxWidgets/3rdparty/pcre && git checkout b4b4098743aaa80ec78ea18da2f175c1b26dda18 && popd
