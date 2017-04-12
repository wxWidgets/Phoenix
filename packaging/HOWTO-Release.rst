HOWTO Release wxPython Phoenix
==============================

:note: This is just a note to myself, no need to publish this in the main
       documentation or anything silly like that...


1. Ensure the buildbot master and slaves are running, and that
   ~/release-builds on Havok is empty

2. Ensure that the branch to be built has been pushed to github.com/RobinD42/Phoenix

3. Log in to buildbot master

4. On the "Builders" page check the dist-* and the bdist-* builders

5. Set a name/value pair to buildargs/--release

6. If a branch other than master should be used (for testing, etc.) then enter
   that branch name in the Branch field

7. Click the Force Build button

8. Go do something else for a couple hours...

9. ...it's still not done, come back later...



10. When the build is done and successful then the release version of the docs
    src and wheel files should be on Havok in ~/release-builds. Do whatever
    testing should be done.

11. Digitally sign the files with this command::

        cd ~/release-builds
        for f in *.whl *.tar.gz; do gpg --detach-sign -a $f; done

12. Upload to PyPI with::

        cd ~/release-builds
        twine upload *

13.